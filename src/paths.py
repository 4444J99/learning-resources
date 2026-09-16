"""Learning path management and progression tracking.

Provides the LearningPath class for defining ordered sequences of
curriculum modules with progress tracking and completion criteria.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any


@dataclass
class PathStep:
    """A single step in a learning path."""

    step_id: int
    module_id: str
    title: str
    completed: bool = False
    completed_at: str | None = None
    score: float | None = None


class LearningPath:
    """An ordered learning path through curriculum modules.

    A path defines the recommended order for completing modules and
    tracks learner progress through each step.
    """

    def __init__(self, path_name: str, learner_id: str = "anonymous") -> None:
        self._path_name = path_name
        self._learner_id = learner_id
        self._steps: list[PathStep] = []

    @property
    def name(self) -> str:
        """Return the path name."""
        return self._path_name

    @property
    def step_count(self) -> int:
        """Return total number of steps."""
        return len(self._steps)

    @property
    def completed_count(self) -> int:
        """Return number of completed steps."""
        return sum(1 for s in self._steps if s.completed)

    @property
    def progress_pct(self) -> float:
        """Return completion percentage (0.0-100.0)."""
        if not self._steps:
            return 0.0
        return round(self.completed_count / self.step_count * 100, 1)

    def add_step(self, module_id: str, title: str) -> PathStep:
        """Add a step to the learning path.

        Args:
            module_id: Reference to the curriculum module.
            title: Human-readable step title.

        Returns:
            The created PathStep.
        """
        step = PathStep(
            step_id=len(self._steps),
            module_id=module_id,
            title=title,
        )
        self._steps.append(step)
        return step

    def complete_step(self, step_id: int, score: float = 1.0) -> bool:
        """Mark a step as completed.

        Args:
            step_id: The step to complete.
            score: Achievement score (0.0-1.0).

        Returns:
            True if the step was found and marked complete.
        """
        if step_id < 0 or step_id >= len(self._steps):
            return False
        step = self._steps[step_id]
        step.completed = True
        step.completed_at = datetime.now(UTC).isoformat()
        step.score = max(0.0, min(1.0, score))
        return True

    def get_next_step(self) -> PathStep | None:
        """Return the next incomplete step, or None if all are done."""
        for step in self._steps:
            if not step.completed:
                return step
        return None

    def get_average_score(self) -> float | None:
        """Calculate the average score across completed steps.

        Returns:
            Average score, or None if no steps are completed.
        """
        scores = [s.score for s in self._steps if s.completed and s.score is not None]
        if not scores:
            return None
        return round(sum(scores) / len(scores), 3)

    def export(self) -> dict[str, Any]:
        """Export the path state as a dictionary."""
        return {
            "path_name": self._path_name,
            "learner_id": self._learner_id,
            "steps": len(self._steps),
            "completed": self.completed_count,
            "progress_pct": self.progress_pct,
            "average_score": self.get_average_score(),
        }