
import json
import random


def mock_llm_call(system, user, *, rng=None, bad_rate=0.2):
    rng = rng if rng is not None else random
    text = user
    category = "기타"
    rules = [
        ("서비스", ("고객센터", "상담", "응대", "환불", "직원")),
        ("배송", ("배송", "택배", "도착")),
        ("품질", ("품질", "재질", "원단", "마감", "불량", "퀄리티")),
        ("가격", ("가격", "비싸", "저렴")),
    ]
    for label, words in rules:
        if any(word in text for word in words):
            category = label
            break
    if any(word in text for word in ("실망", "늦", "불량", "답답", "안 돼", "안 되")):
        sentiment, score = "부정", 2
    elif any(word in text for word in ("만족", "좋", "빠르", "친절", "최고", "깔끔")):
        sentiment, score = "긍정", 5
    else:
        sentiment, score = "중립", 3
    raw = json.dumps(
        {"category": category, "sentiment": sentiment, "score": score},
        ensure_ascii=False,
    )
    fault = None
    if rng.random() < bad_rate:
        fault = rng.choice(["code_fence", "extra_text", "truncated_json"])
        if fault == "code_fence":
            raw = "```json\n" + raw + "\n```"
        elif fault == "extra_text":
            raw = "분석 결과입니다.\n" + raw
        else:
            raw = raw[:-2]
    return {"text": raw, "fault": fault}
