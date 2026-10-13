import argparse
import csv
from pathlib import Path
import random
from classifier import classify_review


def main():
    parser = argparse.ArgumentParser(description="과제 2: Mock 리뷰 분류 파이프라인")
    parser.add_argument("csv_path", type=Path)
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--seed", type=int, default=None)
    args = parser.parse_args()
    if args.limit < 10:
        parser.error("과제 실행에는 리뷰 10건 이상을 지정하세요.")

    try:
        with args.csv_path.open(encoding="utf-8-sig", newline="") as file:
            reader = csv.DictReader(file)
            headers = reader.fieldnames or []
            column = next((name for name in ("review", "review_text") if name in headers), None)
            if column is None:
                parser.error("CSV에 review 또는 review_text 열이 필요합니다.")
            rows = list(reader)[:args.limit]
    except (OSError, UnicodeError, csv.Error) as error:
        parser.error(f"CSV 읽기 실패: {error}")
    if len(rows) < 10:
        parser.error("CSV에 리뷰가 10건 이상 있어야 합니다.")

    rng = random.Random(args.seed)
    failed = 0
    for number, row in enumerate(rows, start=1):
        identifier = row.get("id") or f"R{number:03d}"
        text = (row.get(column) or "").strip()
        print(f"\n[{number}] {identifier}: {text}")
        if not text:
            result = None
            print("  [실패] 빈 리뷰")
        else:
            result = classify_review(text, rng=rng)
        if result is None:
            failed += 1
        else:
            print(f"  [성공] {result}")

    print(f"\n처리 {len(rows)}건 / 실패 {failed}건")
    print(f"성공 {len(rows) - failed}건")


if __name__ == "__main__":
    main()
