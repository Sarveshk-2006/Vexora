import json
import os
from typing import Any, Dict, List, Optional

from app.orchestration.models import ClosedLoopRunResult


class OrchestrationRunStore:
    """Lightweight JSON file-backed run store for orchestration run persistence."""

    def __init__(self, store_path: str = "data/orchestration/runs.json"):
        self.store_path = store_path
        os.makedirs(os.path.dirname(store_path), exist_ok=True)
        if not os.path.exists(self.store_path):
            with open(self.store_path, "w") as f:
                json.dump([], f)

    def save_run(self, result: ClosedLoopRunResult) -> None:
        """Persist completed ClosedLoopRunResult into run store."""
        os.makedirs(os.path.dirname(self.store_path), exist_ok=True)
        runs = self.list_runs_raw()
        data = json.loads(result.model_dump_json())
        runs.append(data)
        with open(self.store_path, "w") as f:
            json.dump(runs, f, indent=2)

    def list_runs_raw(self) -> List[Dict[str, Any]]:
        """Load raw JSON list of saved runs."""
        if not os.path.exists(self.store_path):
            return []
        try:
            with open(self.store_path, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []

    def get_run_by_id_raw(self, run_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve raw run dictionary by run_id."""
        runs = self.list_runs_raw()
        for r in runs:
            if r.get("run_id") == run_id:
                return r
        return None
