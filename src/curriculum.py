"""Curriculum design and management.

Provides the CurriculumBuilder for constructing structured learning curricula
with modules, topics, and learning objectives.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4


@dataclass
class LearningObjective:
    """A measurable learning objective within a topic."""

    objective_id: str
    description: str
    bloom_level: str  # remember, understand, apply, analyze, evaluate, create
    assessment_criteria: list[str]


@dataclass
class Topic:
    """A single topic within a curriculum module."""

    topic_id: str
    title: str
    description: str
    duration_minutes: int
    objectives: list[LearningObjective] = field(default_factory=list)
    resources: list[str] = field(default_factory=list)


@dataclass
class Module:
    """A curriculum module containing related topics."""

    module_id: str
    title: str
    description: str
    topics: list[Topic] = field(default_factory=list)
    prerequisites: list[str] = field(default_factory=list)  # module_ids


class CurriculumBuilder:
    """Builds structured curricula from modules and topics.

    Provides a fluent interface for constructing a curriculum with
    modules, topics, learning objectives, and prerequisite chains.
    """

    def __init__(self, title: str, domain: str = "general") -> None:
        self._title = title
        self._domain = domain
        self._modules: dict[str, Module] = {}

    @property
    def title(self) -> str:
        """Return the curriculum title."""
        return self._title

    @property
    def module_count(self) -> int:
        """Return the number of modules."""
        return len(self._modules)

    def add_module(
        self,
        title: str,
        description: str,
        prerequisites: list[str] | None = None,
    ) -> Module:
        """Add a new module to the curriculum.

        Args:
            title: Module title.
            description: Brief description of the module content.
            prerequisites: List of module IDs that must be completed first.

        Returns:
            The newly created Module.
        """
        module_id = uuid4().hex[:8]
        module = Module(
            module_id=module_id,
            title=title,
            description=description,
            prerequisites=prerequisites or [],
        )
        self._modules[module_id] = module
        return module

    def add_topic(
        self,
        module_id: str,
        title: str,
        description: str,
        duration_minutes: int = 60,
        resources: list[str] | None = None,
    ) -> Topic | None:
        """Add a topic to an existing module.

        Args:
            module_id: The module to add the topic to.
            title: Topic title.
            description: Topic description.
            duration_minutes: Estimated time to complete.
            resources: List of resource URLs or references.

        Returns:
            The created Topic, or None if the module doesn't exist.
        """
        module = self._modules.get(module_id)
        if module is None:
            return None

        topic = Topic(
            topic_id=uuid4().hex[:8],
            title=title,
            description=description,
            duration_minutes=duration_minutes,
            resources=resources or [],
        )
        module.topics.append(topic)
        return topic

    def get_total_duration(self) -> int:
        """Calculate the total curriculum duration in minutes."""
        total = 0
        for module in self._modules.values():
            for topic in module.topics:
                total += topic.duration_minutes
        return total

    def get_prerequisite_chain(self, module_id: str) -> list[str]:
        """Compute the full prerequisite chain for a module.

        Returns the ordered list of module IDs that must be completed
        before the given module, resolving transitive dependencies.

        Args:
            module_id: The target module.

        Returns:
            Ordered list of prerequisite module IDs.
        """
        visited: set[str] = set()
        chain: list[str] = []

        def _resolve(mid: str) -> None:
            if mid in visited:
                return
            visited.add(mid)
            module = self._modules.get(mid)
            if module is None:
                return
            for prereq in module.prerequisites:
                _resolve(prereq)
            if mid != module_id:
                chain.append(mid)

        _resolve(module_id)
        return chain

    def export(self) -> dict[str, Any]:
        """Export the curriculum as a JSON-serializable dict."""
        return {
            "title": self._title,
            "domain": self._domain,
            "module_count": len(self._modules),
            "total_duration_minutes": self.get_total_duration(),
            "modules": [
                {
                    "module_id": m.module_id,
                    "title": m.title,
                    "description": m.description,
                    "prerequisites": list(m.prerequisites),
                    "topic_count": len(m.topics),
                    "topics": [
                        {
                            "topic_id": t.topic_id,
                            "title": t.title,
                            "description": t.description,
                            "duration_minutes": t.duration_minutes,
                            "resources": list(t.resources),
                            "objectives": [
                                {
                                    "objective_id": obj.objective_id,
                                    "description": obj.description,
                                    "bloom_level": obj.bloom_level,
                                    "assessment_criteria": list(obj.assessment_criteria),
                                }
                                for obj in t.objectives
                            ],
                        }
                        for t in m.topics
                    ],
                }
                for m in self._modules.values()
            ],
        }
