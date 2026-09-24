import re


def words(text: str) -> set[str]:
    tokens = re.findall(r"\b\w+\b", text.casefold())

    return {
        word[:-1]
        if len(word) > 3 and word.endswith("s")
        and not word.endswith("ss")
        else word
        for word in tokens
    }


def judge(question, expects, answer, results) -> bool:
    expected_words = words(expects)
    answer_words = words(answer)

    if not expected_words or not answer_words:
        return False

    has_expected = expected_words.issubset(answer_words)

    has_source = any(
        result.source.casefold() in answer.casefold()
        for result in results
        if result.source
    )

    return has_expected and has_source