import unittest

from app import FakeModel, Pipeline, PromptCache, parse_category


class PipelineTests(unittest.TestCase):
    def test_prompt_trims_surrounding_whitespace(self):
        self.assertEqual(Pipeline().prompt("  urgent  "), "Classify: urgent")

    def test_cache_key_includes_model_version(self):
        cache = PromptCache()
        self.assertNotEqual(cache.key("v1", "same"), cache.key("v2", "same"))

    def test_first_request_calls_model(self):
        model = FakeModel()
        self.assertEqual(Pipeline(model).classify("urgent ticket"), "urgent")
        self.assertEqual(len(model.prompts), 1)

    def test_model_receives_prompt_not_hash(self):
        model = FakeModel()
        prompt = "Classify: urgent ticket"
        Pipeline(model).classify("urgent ticket")
        self.assertEqual(model.prompts, [prompt])

    def test_repeated_request_uses_same_cache_entry(self):
        model = FakeModel()
        cache = PromptCache()
        pipeline = Pipeline(model, cache)
        pipeline.classify("routine")
        pipeline.classify("routine")
        self.assertEqual(len(model.prompts), 1)

    def test_category_is_normalized_to_lowercase(self):
        self.assertEqual(parse_category("CATEGORY=URGENT"), "urgent")

    def test_unknown_category_becomes_other(self):
        self.assertEqual(Pipeline().classify("bad-category"), "other")

    def test_batch_contains_failure_and_preserves_positions(self):
        self.assertEqual(Pipeline().classify_many(["urgent", "raise-model-error", "routine"]),
                         ["urgent", "other", "normal"])


if __name__ == "__main__":
    unittest.main()
