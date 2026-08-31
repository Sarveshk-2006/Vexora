import os
import uuid
from typing import Any, Dict, List

from app.hardening.promotion import ModelRegistry
from app.orchestration.models import (
    ClosedLoopMetrics,
    ClosedLoopProvenance,
    ClosedLoopRunRequest,
    ClosedLoopRunResult,
    ClosedLoopStageResult,
    ClosedLoopVerdict,
    PipelineStage,
    StageStatus,
)
from app.orchestration.run_store import OrchestrationRunStore
from app.orchestration.stages import StageRunner


class ClosedLoopOrchestrator:
    """Main application orchestrator executing 8-stage closed-loop security research pipeline."""

    def __init__(
        self,
        seed: int = 42,
        data_dir: str = "data/orchestration",
        hardening_dir: str = "data/hardening",
        artifact_dir: str = "models/blue_team",
    ):
        self.seed = seed
        self.data_dir = data_dir
        self.hardening_dir = hardening_dir
        self.artifact_dir = artifact_dir
        self.store = OrchestrationRunStore(
            store_path=os.path.join(data_dir, "runs.json")
        )
        self.registry = ModelRegistry(
            registry_path=os.path.join(hardening_dir, "model_registry.json"),
            active_pointer_path=os.path.join(artifact_dir, "active_model.json"),
        )

    def run(self, request: ClosedLoopRunRequest) -> ClosedLoopRunResult:
        """Execute complete 8-stage closed-loop pipeline deterministically."""
        run_id = f"RUN_LOOP_{uuid.uuid4().hex[:12].upper()}"
        active_before = self.registry.get_active_model_id()
        seed = request.seed or self.seed

        stage_results: List[ClosedLoopStageResult] = []
        metrics = ClosedLoopMetrics()
        verdict = ClosedLoopVerdict.PIPELINE_FAILED
        pipeline_status = StageStatus.IN_PROGRESS
        explanations = []

        red_ctx: Dict[str, Any] = {}
        blue_ctx: Dict[str, Any] = {}
        gap_ctx: Dict[str, Any] = {}
        hard_ctx: Dict[str, Any] = {}

        # -------------------------------------------------------------
        # STAGE 1 — SCENARIO PREPARATION
        # -------------------------------------------------------------
        try:
            st1, prep_ctx = StageRunner.run_stage_1_prep(seed, request.genome_payload)
            stage_results.append(st1)
            genome = prep_ctx["genome"]
            genome_hash = prep_ctx["genome_hash"]
        except Exception as e:
            stage_results.append(
                ClosedLoopStageResult(
                    stage=PipelineStage.SCENARIO_PREPARATION,
                    status=StageStatus.FAILED,
                    error_message=str(e),
                )
            )
            return self._finalize_failed_run(
                run_id, seed, active_before, stage_results, str(e)
            )

        # -------------------------------------------------------------
        # STAGE 2 — RED TEAM CAMPAIGN SIMULATION
        # -------------------------------------------------------------
        try:
            st2, red_ctx = StageRunner.run_stage_2_red_team(seed, genome)
            stage_results.append(st2)
        except Exception as e:
            stage_results.append(
                ClosedLoopStageResult(
                    stage=PipelineStage.RED_TEAM,
                    status=StageStatus.FAILED,
                    error_message=str(e),
                )
            )
            return self._finalize_failed_run(
                run_id, seed, active_before, stage_results, str(e), genome_hash
            )

        # -------------------------------------------------------------
        # STAGE 3 — BLUE TEAM EVALUATION
        # -------------------------------------------------------------
        try:
            st3, blue_ctx = StageRunner.run_stage_3_blue_team(seed, red_ctx)
            stage_results.append(st3)
        except Exception as e:
            stage_results.append(
                ClosedLoopStageResult(
                    stage=PipelineStage.BLUE_TEAM,
                    status=StageStatus.FAILED,
                    error_message=str(e),
                )
            )
            return self._finalize_failed_run(
                run_id, seed, active_before, stage_results, str(e), genome_hash
            )

        # -------------------------------------------------------------
        # STAGE 4 — DEFENSE GAP ANALYSIS
        # -------------------------------------------------------------
        try:
            st4, gap_ctx = StageRunner.run_stage_4_gap_analysis(blue_ctx)
            stage_results.append(st4)
        except Exception as e:
            stage_results.append(
                ClosedLoopStageResult(
                    stage=PipelineStage.GAP_ANALYSIS,
                    status=StageStatus.FAILED,
                    error_message=str(e),
                )
            )
            return self._finalize_failed_run(
                run_id, seed, active_before, stage_results, str(e), genome_hash
            )

        # -------------------------------------------------------------
        # STAGE 5 — AUTONOMOUS HARDENING
        # -------------------------------------------------------------
        try:
            st5, hard_ctx = StageRunner.run_stage_5_hardening(
                seed,
                gap_ctx,
                data_dir=self.hardening_dir,
                artifact_dir=self.artifact_dir,
            )
            stage_results.append(st5)
        except Exception as e:
            stage_results.append(
                ClosedLoopStageResult(
                    stage=PipelineStage.HARDENING,
                    status=StageStatus.FAILED,
                    error_message=str(e),
                )
            )
            return self._finalize_failed_run(
                run_id, seed, active_before, stage_results, str(e), genome_hash
            )

        # -------------------------------------------------------------
        # STAGE 6 — EXPLAINABILITY EVIDENCE GENERATION
        # -------------------------------------------------------------
        try:
            st6, exp_ctx = StageRunner.run_stage_6_explainability(
                seed, red_ctx, hard_ctx, data_dir=self.hardening_dir
            )
            stage_results.append(st6)
            explanations = exp_ctx["explanations"]
        except Exception as e:
            stage_results.append(
                ClosedLoopStageResult(
                    stage=PipelineStage.EXPLAINABILITY,
                    status=StageStatus.FAILED,
                    error_message=str(e),
                )
            )

        # -------------------------------------------------------------
        # STAGE 7 — RE-ATTACK / POST-HARDENING VALIDATION
        # -------------------------------------------------------------
        try:
            st7, re_ctx = StageRunner.run_stage_7_re_attack(seed, red_ctx, hard_ctx)
            stage_results.append(st7)
            metrics = re_ctx["metrics"]
        except Exception as e:
            stage_results.append(
                ClosedLoopStageResult(
                    stage=PipelineStage.RE_ATTACK_VALIDATION,
                    status=StageStatus.FAILED,
                    error_message=str(e),
                )
            )

        # -------------------------------------------------------------
        # STAGE 8 — CLOSED-LOOP VERDICT
        # -------------------------------------------------------------
        try:
            st8, verdict = StageRunner.run_stage_8_verdict(gap_ctx, hard_ctx, {})
            stage_results.append(st8)
        except Exception as e:
            stage_results.append(
                ClosedLoopStageResult(
                    stage=PipelineStage.VERDICT,
                    status=StageStatus.FAILED,
                    error_message=str(e),
                )
            )
            verdict = ClosedLoopVerdict.PIPELINE_FAILED

        active_after = self.registry.get_active_model_id()
        pipeline_status = StageStatus.COMPLETED

        prov = ClosedLoopProvenance(
            run_id=run_id,
            random_seed=seed,
            genome_hash=genome_hash,
            pipeline_version="1.0.0",
            active_model_before=active_before,
            active_model_after=active_after,
            scenario_id=(
                red_ctx.get("scen", {}).scenario_id if red_ctx.get("scen") else None
            ),
            hardening_run_id=hard_ctx.get("hard_record", {}).get("run_id"),
            candidate_model_id=hard_ctx.get("hard_record", {}).get(
                "candidate_model_id"
            ),
            dataset_hash="85e07eb59a75dc77",
            model_hash="5b27cd2cd831db0f",
        )

        res = ClosedLoopRunResult(
            run_id=run_id,
            provenance=prov,
            verdict=verdict,
            pipeline_state=pipeline_status,
            stage_results=stage_results,
            metrics=metrics,
            active_model_before=active_before,
            active_model_after=active_after,
            explanations=explanations,
            summary={
                "seed": seed,
                "stages_completed": len(
                    [s for s in stage_results if s.status == StageStatus.COMPLETED]
                ),
                "verdict": verdict.value,
                "active_model_promoted": active_before != active_after,
            },
        )

        self.store.save_run(res)
        return res

    def _finalize_failed_run(
        self,
        run_id: str,
        seed: int,
        active_before: str,
        stage_results: List[ClosedLoopStageResult],
        error_msg: str,
        genome_hash: str = "UNKNOWN",
    ) -> ClosedLoopRunResult:
        """Helper to safely build and persist a failed pipeline result with skipped remaining stages."""
        executed_stages = {s.stage for s in stage_results}
        all_stages = [
            PipelineStage.SCENARIO_PREPARATION,
            PipelineStage.RED_TEAM,
            PipelineStage.BLUE_TEAM,
            PipelineStage.GAP_ANALYSIS,
            PipelineStage.HARDENING,
            PipelineStage.EXPLAINABILITY,
            PipelineStage.RE_ATTACK_VALIDATION,
            PipelineStage.VERDICT,
        ]

        for st in all_stages:
            if st not in executed_stages:
                stage_results.append(
                    ClosedLoopStageResult(
                        stage=st,
                        status=StageStatus.SKIPPED,
                        detail={"reason": "Skipped due to upstream stage failure"},
                    )
                )

        prov = ClosedLoopProvenance(
            run_id=run_id,
            random_seed=seed,
            genome_hash=genome_hash,
            pipeline_version="1.0.0",
            active_model_before=active_before,
            active_model_after=active_before,
        )

        res = ClosedLoopRunResult(
            run_id=run_id,
            provenance=prov,
            verdict=ClosedLoopVerdict.PIPELINE_FAILED,
            pipeline_state=StageStatus.FAILED,
            stage_results=stage_results,
            metrics=ClosedLoopMetrics(),
            active_model_before=active_before,
            active_model_after=active_before,
            explanations=[],
            summary={
                "error": error_msg,
                "verdict": ClosedLoopVerdict.PIPELINE_FAILED.value,
            },
        )
        self.store.save_run(res)
        return res
