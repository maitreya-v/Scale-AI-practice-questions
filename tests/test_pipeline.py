from src.pipeline import ClassificationPipeline
from src.prompt_cache import PromptCache


def test_first_request_calls_model_and_returns_output():
    pipeline = ClassificationPipeline()
    assert pipeline.classify("urgent customer escalation") == "CATEGORY=URGENT"


def test_different_user_prompts_do_not_share_a_cache_key():
    cache = PromptCache()
    k1 = cache.prompt_key("classification-v1", "Classify: urgent issue")
    k2 = cache.prompt_key("classification-v1", "Classify: routine issue")
    assert k1 != k2


def test_repeated_request_can_be_served_from_cache():
    pipeline = ClassificationPipeline()
    first = pipeline.classify("routine cleanup")
    second = pipeline.classify("routine cleanup")
    assert first == "CATEGORY=NORMAL"
    assert second == first
