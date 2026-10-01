"""Tests for the curriculum module."""

from src.curriculum import CurriculumBuilder


class TestCurriculumBuilder:
    def test_create_curriculum_with_title(self) -> None:
        builder = CurriculumBuilder("Art Fundamentals", domain="art")
        assert builder.title == "Art Fundamentals"
        assert builder.module_count == 0

    def test_add_module(self) -> None:
        builder = CurriculumBuilder("Test")
        module = builder.add_module("Intro", "Introduction to the subject")
        assert module.title == "Intro"
        assert builder.module_count == 1

    def test_add_topic_to_module(self) -> None:
        builder = CurriculumBuilder("Test")
        mod = builder.add_module("M1", "Module 1")
        topic = builder.add_topic(mod.module_id, "T1", "Topic 1", duration_minutes=45)
        assert topic is not None
        assert topic.title == "T1"
        assert topic.duration_minutes == 45

    def test_add_topic_to_nonexistent_module(self) -> None:
        builder = CurriculumBuilder("Test")
        result = builder.add_topic("fake_id", "T1", "Topic 1")
        assert result is None

    def test_total_duration(self) -> None:
        builder = CurriculumBuilder("Test")
        mod = builder.add_module("M1", "Module 1")
        builder.add_topic(mod.module_id, "T1", "Topic 1", duration_minutes=30)
        builder.add_topic(mod.module_id, "T2", "Topic 2", duration_minutes=45)
        assert builder.get_total_duration() == 75

    def test_prerequisite_chain(self) -> None:
        builder = CurriculumBuilder("Test")
        m1 = builder.add_module("Foundations", "Base module")
        m2 = builder.add_module("Intermediate", "Builds on foundations", prerequisites=[m1.module_id])
        m3 = builder.add_module("Advanced", "Builds on intermediate", prerequisites=[m2.module_id])
        chain = builder.get_prerequisite_chain(m3.module_id)
        assert m1.module_id in chain
        assert m2.module_id in chain

    def test_export_structure(self) -> None:
        builder = CurriculumBuilder("Export Test", domain="tech")
        builder.add_module("M1", "First module")
        data = builder.export()
        assert data["title"] == "Export Test"
        assert data["domain"] == "tech"
        assert data["module_count"] == 1
        assert data["modules"][0]["topic_count"] == 0
        assert data["modules"][0]["topics"] == []

    def test_export_empty_curriculum(self) -> None:
        builder = CurriculumBuilder("Empty")
        data = builder.export()
        assert data["title"] == "Empty"
        assert data["module_count"] == 0
        assert data["total_duration_minutes"] == 0
        assert data["modules"] == []

    def test_export_populated_curriculum_preserves_full_topics_and_objectives(self) -> None:
        import json
        from src.curriculum import LearningObjective

        builder = CurriculumBuilder("Populated Test", domain="art")
        mod = builder.add_module("M1", "First module")
        topic = builder.add_topic(
            mod.module_id,
            "T1",
            "Topic 1 description",
            duration_minutes=90,
            resources=["https://example.com/res1"],
        )
        assert topic is not None
        obj = LearningObjective(
            objective_id="obj1",
            description="Understand color theory",
            bloom_level="understand",
            assessment_criteria=["Pass quiz"],
        )
        topic.objectives.append(obj)

        exported = builder.export()

        # Check JSON serializability
        json_str = json.dumps(exported)
        assert json_str is not None

        # Check top-level & module fields
        assert exported["title"] == "Populated Test"
        assert exported["domain"] == "art"
        assert exported["module_count"] == 1
        assert exported["total_duration_minutes"] == 90

        module_data = exported["modules"][0]
        assert module_data["module_id"] == mod.module_id
        assert module_data["title"] == "M1"
        assert module_data["description"] == "First module"
        assert module_data["topic_count"] == 1

        # Check nested topic fields
        topic_data = module_data["topics"][0]
        assert topic_data["topic_id"] == topic.topic_id
        assert topic_data["title"] == "T1"
        assert topic_data["description"] == "Topic 1 description"
        assert topic_data["duration_minutes"] == 90
        assert topic_data["resources"] == ["https://example.com/res1"]

        # Check nested objective fields
        objective_data = topic_data["objectives"][0]
        assert objective_data["objective_id"] == "obj1"
        assert objective_data["description"] == "Understand color theory"
        assert objective_data["bloom_level"] == "understand"
        assert objective_data["assessment_criteria"] == ["Pass quiz"]

        # Assert export did not mutate builder
        assert builder.module_count == 1
        assert len(builder._modules[mod.module_id].topics) == 1
