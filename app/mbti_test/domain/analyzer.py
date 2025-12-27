import re

# ==========================================
# 1. 확장된 키워드 & 패턴 사전 (데이터 영역)
# ==========================================
DICTIONARY = {
    "EI": {
        "E": {
            "keywords": [
                {"word": "모임", "w": 4}, {"word": "사람들", "w": 3}, {"word": "술자리", "w": 5},
                {"word": "텐션", "w": 4}, {"word": "분위기", "w": 3}, {"word": "대화", "w": 3},
                {"word": "통화", "w": 3}, {"word": "디엠", "w": 3}, {"word": "스토리", "w": 3},
                {"word": "공유", "w": 3}, {"word": "자랑", "w": 4}, {"word": "시끌", "w": 4},
                {"word": "활동", "w": 4}, {"word": "나가서", "w": 4}, {"word": "돌아다니", "w": 4},
                {"word": "친해", "w": 4}, {"word": "인싸", "w": 5}, {"word": "관종", "w": 4},
                {"word": "주도", "w": 5}, {"word": "리더", "w": 3}, {"word": "발표", "w": 3},
                {"word": "적극", "w": 4}, {"word": "에너지", "w": 4}, {"word": "확성기", "w": 5},
                {"word": "다 같이", "w": 4}, {"word": "여럿이", "w": 4}
            ],
            "regex": [r"친구들?이랑", r"모여서", r"밥약", r"약속.*잡고", r"노는 게"]
        },
        "I": {
            "keywords": [
                {"word": "혼자", "w": 5}, {"word": "집", "w": 4}, {"word": "이불", "w": 4},
                {"word": "넷플", "w": 3}, {"word": "유튜브", "w": 3}, {"word": "충전", "w": 4},
                {"word": "기빨려", "w": 5}, {"word": "피곤", "w": 3}, {"word": "조용", "w": 4},
                {"word": "생각", "w": 3}, {"word": "혼잣말", "w": 3}, {"word": "이어폰", "w": 4},
                {"word": "거리두기", "w": 4}, {"word": "내향", "w": 5}, {"word": "낯가림", "w": 5},
                {"word": "어색", "w": 4}, {"word": "문자", "w": 3}, {"word": "카톡", "w": 2},
                {"word": "읽씹", "w": 3}, {"word": "안읽씹", "w": 3}, {"word": "침대", "w": 4}
            ],
            "regex": [r"집에.*가고 싶", r"사람.*많으면", r"혼자.*있는", r"나가는 거.*귀찮"]
        }
    },
    "SN": {
        "S": {
            "keywords": [
                {"word": "사실", "w": 4}, {"word": "실제", "w": 4}, {"word": "현실", "w": 5},
                {"word": "경험", "w": 4}, {"word": "직접", "w": 3}, {"word": "눈으로", "w": 4},
                {"word": "맛", "w": 3}, {"word": "가격", "w": 4}, {"word": "수치", "w": 4},
                {"word": "데이터", "w": 5}, {"word": "증거", "w": 5}, {"word": "팩트", "w": 4},
                {"word": "역사", "w": 3}, {"word": "전통", "w": 3}, {"word": "익숙", "w": 3},
                {"word": "원래", "w": 3}, {"word": "하던 대로", "w": 4}, {"word": "구체적", "w": 5},
                {"word": "세부", "w": 4}, {"word": "디테일", "w": 4}, {"word": "실용", "w": 5},
                {"word": "가성비", "w": 5}, {"word": "쓸모", "w": 4}, {"word": "오감", "w": 3}
            ],
            "regex": [r"지금 당장", r"현실적으로", r"팩트.*체크", r"구체적으로.*말해", r"본 적"]
        },
        "N": {
            "keywords": [
                {"word": "상상", "w": 5}, {"word": "만약", "w": 5}, {"word": "미래", "w": 4},
                {"word": "의미", "w": 4}, {"word": "비유", "w": 4}, {"word": "느낌", "w": 3},
                {"word": "영감", "w": 5}, {"word": "아이디어", "w": 4}, {"word": "창의", "w": 4},
                {"word": "우주", "w": 3}, {"word": "컨셉", "w": 3}, {"word": "세계관", "w": 4},
                {"word": "철학", "w": 4}, {"word": "본질", "w": 5}, {"word": "큰 그림", "w": 5},
                {"word": "가능성", "w": 4}, {"word": "꿈", "w": 3}, {"word": "망상", "w": 5},
                {"word": "멍", "w": 3}, {"word": "패턴", "w": 3}, {"word": "추상", "w": 5},
                {"word": "예감", "w": 4}, {"word": "촉", "w": 4}, {"word": "복선", "w": 3}
            ],
            "regex": [r"~인 것 같아", r"어떤 느낌", r"혹시.*아닐까", r"만약에", r"비유하자면"]
        }
    },
    "TF": {
        "T": {
            "keywords": [
                {"word": "왜", "w": 5}, {"word": "분석", "w": 4}, {"word": "논리", "w": 5},
                {"word": "이유", "w": 4}, {"word": "원인", "w": 4}, {"word": "결과", "w": 4},
                {"word": "해결", "w": 5}, {"word": "방법", "w": 3}, {"word": "효율", "w": 5},
                {"word": "객관", "w": 5}, {"word": "비판", "w": 4}, {"word": "따져", "w": 4},
                {"word": "계산", "w": 4}, {"word": "맞아", "w": 3}, {"word": "틀려", "w": 3},
                {"word": "증명", "w": 4}, {"word": "공정", "w": 4}, {"word": "원칙", "w": 4},
                {"word": "시스템", "w": 3}, {"word": "기능", "w": 3}, {"word": "성능", "w": 3},
                {"word": "팩폭", "w": 5}, {"word": "납득", "w": 4}, {"word": "이해", "w": 2}
            ],
            "regex": [r"그래서.*결론", r"그게.*말이 돼", r"효율적", r"객관적으로", r"따지고 보면"]
        },
        "F": {
            "keywords": [
                {"word": "공감", "w": 5}, {"word": "마음", "w": 4}, {"word": "기분", "w": 5},
                {"word": "상처", "w": 5}, {"word": "서운", "w": 5}, {"word": "고마워", "w": 4},
                {"word": "미안", "w": 4}, {"word": "감동", "w": 5}, {"word": "걱정", "w": 4},
                {"word": "응원", "w": 4}, {"word": "칭찬", "w": 4}, {"word": "좋아", "w": 3},
                {"word": "싫어", "w": 3}, {"word": "배려", "w": 4}, {"word": "조화", "w": 3},
                {"word": "관계", "w": 4}, {"word": "사람", "w": 3}, {"word": "가치", "w": 3},
                {"word": "의미", "w": 2}, {"word": "진심", "w": 5}, {"word": "따뜻", "w": 4},
                {"word": "눈물", "w": 4}, {"word": "행복", "w": 3}, {"word": "사랑", "w": 3}
            ],
            "regex": [r"어떡해", r"너무.*좋아", r"속상해", r"마음이.*아파", r"진짜.*감동"]
        }
    },
    "JP": {
        "J": {
            "keywords": [
                {"word": "계획", "w": 5}, {"word": "일정", "w": 5}, {"word": "예약", "w": 4},
                {"word": "미리", "w": 5}, {"word": "준비", "w": 4}, {"word": "정리", "w": 4},
                {"word": "메모", "w": 3}, {"word": "리스트", "w": 4}, {"word": "완료", "w": 4},
                {"word": "마감", "w": 5}, {"word": "시간", "w": 3}, {"word": "약속", "w": 3},
                {"word": "순서", "w": 3}, {"word": "체계", "w": 4}, {"word": "통제", "w": 4},
                {"word": "목표", "w": 4}, {"word": "달성", "w": 4}, {"word": "결정", "w": 4},
                {"word": "확실", "w": 3}, {"word": "분명", "w": 3}, {"word": "규칙", "w": 3}
            ],
            "regex": [r"계획대로", r"미리.*해서", r"체크리스트", r"딱.*정해서", r"시간.*맞춰서"]
        },
        "P": {
            "keywords": [
                {"word": "즉흥", "w": 5}, {"word": "그때", "w": 5}, {"word": "유동", "w": 4},
                {"word": "변경", "w": 4}, {"word": "자유", "w": 4}, {"word": "여유", "w": 4},
                {"word": "융통성", "w": 5}, {"word": "적응", "w": 4}, {"word": "과정", "w": 3},
                {"word": "즐겨", "w": 3}, {"word": "일단", "w": 4}, {"word": "나중", "w": 4},
                {"word": "미루", "w": 5}, {"word": "벼락치기", "w": 5}, {"word": "충동", "w": 4},
                {"word": "재미", "w": 3}, {"word": "오픈", "w": 3}, {"word": "탐색", "w": 3},
                {"word": "아무거나", "w": 4}, {"word": "상황", "w": 3}, {"word": "필", "w": 4}
            ],
            "regex": [r"상황.*봐서", r"일단.*가보자", r"내일의.*나", r"그냥.*하면", r"feel"]
        }
    }
}

# 결과 설명 (예시 - 필요시 확장 가능)
DESCRIPTIONS = {
    "ISTP": "만능 재주꾼 - 효율과 논리의 끝판왕",
    "ENFP": "재기발랄한 활동가 - 열정 만수르",
    # ... 다른 유형들 추가
}


# ==========================================
# 2. 분석 로직 함수 (Logic 영역)
# ==========================================

def analyze_style(text: str, dim: str):
    """
    키워드 매칭이 안 될 경우를 대비한 문체/스타일 분석 함수
    """
    score = {k: 0 for k in "EISNTFJP"}
    clean_text = text.strip()

    # [E vs I] 길이와 텐션
    if dim == "EI":
        if len(clean_text) > 40: score["E"] += 1  # 말이 많음
        if "!" in clean_text: score["E"] += 1  # 느낌표 사용
        if "ㅋ" * 3 in clean_text: score["E"] += 1  # 웃음 많음

        if len(clean_text) < 15: score["I"] += 1  # 단답형
        if clean_text.endswith("."): score["I"] += 0.5  # 차분한 마침표

    # [S vs N] 구체성 vs 추상성
    if dim == "SN":
        # S: 숫자, 단위, 명확한 단정
        if re.search(r"\d+|개|번|시|분|원", clean_text): score["S"] += 1.5
        if re.search(r"[가-힣]다\.", clean_text): score["S"] += 1

        # N: 추측, 모호함, 말줄임표
        if re.search(r"~|..|것 같|듯|음|...|\?", clean_text): score["N"] += 1.5
        if re.search(r"뭔가|약간|좀", clean_text): score["N"] += 1

    # [T vs F] 논리 vs 감정
    if dim == "TF":
        # T: 질문(따짐), 인과관계
        if "?" in clean_text or "왜" in clean_text: score["T"] += 1.5
        if re.search(r"근데|하지만|그래서", clean_text): score["T"] += 1

        # F: 감탄사, ㅠㅠ, 부드러운 어미
        if re.search(r"[ㅠㅜㅎㅋ]{2,}|!|♥|~", clean_text): score["F"] += 2
        if re.search(r"네요|아요|어요|죠", clean_text): score["F"] += 1

    # [J vs P] 확정 vs 유보
    if dim == "JP":
        if re.search(r"해야|할게|하자|필수", clean_text): score["J"] += 1
        if re.search(r"글쎄|아마|몰라|일단", clean_text): score["P"] += 1.5

    return score


def calculate_mbti_score(answers: list):
    """
    사용자의 답변 리스트를 받아 점수를 계산합니다.
    가정: 답변 리스트 순서는 3개씩 EI -> SN -> TF -> JP 순서라고 가정합니다.
          (총 12개 질문)
    """
    total_scores = {k: 0 for k in "EISNTFJP"}
    dimensions = ["EI", "SN", "TF", "JP"]

    for i, ans in enumerate(answers):
        if not isinstance(ans, str): continue

        # 현재 질문이 어떤 차원인지 확인 (3개씩 끊기)
        if i < 12:
            current_dim = dimensions[i // 3]
        else:
            continue  # 12개 초과 답변은 무시하거나 예외처리

        # 1. 키워드 사전 매칭 (정확도 높음)
        matched_any = False
        for type_char, data in DICTIONARY[current_dim].items():
            # (1) 단순 단어 매칭
            for k in data["keywords"]:
                if k["word"] in ans:
                    total_scores[type_char] += k["w"]
                    matched_any = True

            # (2) 정규식 패턴 매칭 (문맥)
            for pattern in data["regex"]:
                if re.search(pattern, ans):
                    total_scores[type_char] += 3
                    matched_any = True

        # 2. 스타일 분석 (보조 수단)
        # 키워드가 하나도 매칭 안 됐으면 가중치를 더 높게 줘도 됨 (여기선 단순 합산)
        style_scores = analyze_style(ans, current_dim)
        for char, score in style_scores.items():
            if char in current_dim:
                total_scores[char] += score

    return total_scores


def determine_result(scores):
    """
    최종 점수를 바탕으로 MBTI 4글자와 신뢰도를 반환합니다.
    """
    # 1. MBTI 조합
    result = ""
    result += "E" if scores["E"] >= scores["I"] else "I"
    result += "S" if scores["S"] >= scores["N"] else "N"
    result += "T" if scores["T"] >= scores["F"] else "F"
    result += "J" if scores["J"] >= scores["P"] else "P"

    # 2. 신뢰도(Confidence) 계산 - 두 성향 점수 차이를 백분율로 환산
    confidence = {}
    pairs = [("E", "I"), ("S", "N"), ("T", "F"), ("J", "P")]

    for a, b in pairs:
        total = scores[a] + scores[b]
        if total == 0:
            conf = 50.0  # 데이터 없음
        else:
            gap = abs(scores[a] - scores[b])
            conf = 50 + (gap / total * 50)  # 50% ~ 100% 사이 값
        confidence[f"{a}/{b}"] = round(conf, 1)

    return result, confidence