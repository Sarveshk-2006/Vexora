class OrchestrationError(Exception):
    """Base exception for orchestration layer errors."""

    pass


class StageExecutionError(OrchestrationError):
    """Raised when an individual pipeline stage fails execution."""

    def __init__(self, stage_name: str, message: str, original_error: Exception = None):
        self.stage_name = stage_name
        self.original_error = original_error
        super().__init__(f"Stage '{stage_name}' failed: {message}")


class PipelineValidationError(OrchestrationError):
    """Raised when pipeline request configuration validation fails."""

    pass
