import json
from mock_llm import mock_llm_call

SYSTEM = """고객 리뷰를 분류하세요. JSON 객체만 출력하세요.
category: 배송, 품질, 가격, 서비스, 기타 중 하나
sentiment: 긍정, 부정, 중립 중 하나
score: 1~5 사이 정수"""


def classify_review(review_text, *, rng=None):
    """성공하면 딕셔너리, 복구 불가능한 응답이면 None을 반환한다."""
    response = mock_llm_call(SYSTEM, review_text, rng=rng)
    raw = response["text"].strip()
    if response["fault"]:
        print(f"  [Mock 불량 응답] {response['fault']}: {raw!r}")

    if raw.startswith("```") and raw.endswith("```"):
        lines = raw.splitlines()
        if lines[0].strip().lower() in ("```", "```json") and lines[-1].strip() == "```":
            raw = "\n".join(lines[1:-1]).strip()
            print("  [복구] 코드펜스 제거")

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as error:
        print(f"  [실패] JSON 파싱: {error.msg}")
        return None

    if not isinstance(data, dict):
        print("  [실패] JSON 객체가 아님")
        return None
    if data.get("category") not in {"배송", "품질", "가격", "서비스", "기타"}:
        print("  [실패] category 값 오류 또는 누락")
        return None
    if data.get("sentiment") not in {"긍정", "부정", "중립"}:
        print("  [실패] sentiment 값 오류 또는 누락")
        return None
    score = data.get("score")
    if type(score) is not int or not 1 <= score <= 5:
        print("  [실패] score는 1~5 정수여야 함")
        return None
    return data
