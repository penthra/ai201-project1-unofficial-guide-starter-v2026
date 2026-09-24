import re


def normalize(text: str) -> str:
    """Ignore capitalization and differences in whitespace."""
    return " ".join(text.casefold().split())


def judge(question, expects, answer, results) -> bool:
    expected = normalize(expects)
    response = normalize(answer)

    if not expected or not response:
        return False

    # Check that the expected phrase appears as complete words.
    pattern = rf"(?<!\w){re.escape(expected)}(?!\w)"
    has_expected = re.search(pattern, response) is not None

    # Check that the answer names at least one retrieved source.
    has_source = any(
        normalize(result.source) in response
        for result in results
        if result.source
    )

    return has_expected and has_source