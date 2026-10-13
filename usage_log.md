## AI 사용기록

Q. main.py 실행할 때 어떤 입력을 해야해?
A. VS Code에서 위 폴더를 연 뒤 터미널 → 새 터미널을 선택하고 입력합니다.
```
python -X utf8 main.py reviews_labeled.csv --limit 20 --seed 42
```
python 명령이 인식되지 않으면 다음을 사용하세요.
```
py -X utf8 main.py reviews_labeled.csv --limit 20 --seed 42
```
--limit 20: 리뷰 20건 처리
--seed 42: 난수 패턴을 고정해 같은 실행을 재현

C. 채택

Q. mock_llm.py 에서 random 모듈을 사용하라고 하는데 왜, 어떻게 사용해야 하는지 알려줘.
A. random 모듈은 불량 응답이 가끔 발생하도록 만들고, 발생할 불량 응답의 종류를 무작위로 고르는 데 사용합니다.  
실제 AI의 답변은 항상 같은 형식으로 나오지 않을 수 있습니다. 이번 과제에서는 그 상황을 난수로 흉내 내는 것입니다.

1. 난수 생성기를 선택합니다
```
rng = rng if rng is not None else random
```
다음과 같은 뜻입니다.
```
if rng is not None:
    rng = rng       # 전달받은 난수 생성기를 사용
else:
    rng = random    # 전달받은 것이 없으면 random 모듈을 사용
```
rng는 난수를 만드는 도구를 담은 변수입니다. 별도로 전달한 도구가 없어도 random 모듈로 작동합니다.  
2. 불량 응답을 만들지 결정합니다
```
if rng.random() < bad_rate:
```
함수 정의에서 기본값을 이렇게 정했습니다.
```
bad_rate=0.2
```
따라서 기본적으로 다음과 같습니다.
```
if rng.random() < 0.2:
```
0 이상 1 미만의 난수가 0.2보다 작을 때 불량 응답을 만듭니다. 이것이 과제에서 요구한 20% 확률입니다.  
3. 불량 응답 종류를 선택합니다
```
fault = rng.choice(["code_fence", "extra_text", "truncated_json"])
```
세 종류 중 하나를 무작위로 고릅니다. 선택한 종류에 따라 아래 코드가 응답을 바꿉니다.
```
if fault == "code_fence":
    raw = "```json\n" + raw + "\n```"   # 코드펜스 추가
elif fault == "extra_text":
    raw = "분석 결과입니다.\n" + raw    # 사족 추가
else:
    raw = raw[:-2]                     # 끝 두 글자를 잘라 JSON 손상
```
전체적으로는 키워드로 정상 응답을 만든 뒤 → 20% 확률로 응답을 망가뜨린 뒤 → 반환하는 함수입니다. 파일 맨 위에는 다음 두 줄이 있어야 합니다.

C. 적당하게 과제의 20%를 잘 반영하고 있으므로 채택