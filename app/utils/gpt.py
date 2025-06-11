import os
import openai
from dotenv import load_dotenv

load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_base_dialogue(lines: list[str], level: str = "easy") -> str:
    level_map = {
        "easy": "초등학생도 따라하기 쉬운 말투로",
        "medium": "일반적인 회화체로",
        "hard": "자연스러운 고급 표현으로"
    }

    prompt = f"""
    나는 영어 학습용 TTS 콘텐츠를 만들고 있어.

    다음 문장들을 {level_map.get(level, '회화체로')} 리라이트해서 자연스러운 대화문 형태로 만들어줘. 
    너무 복잡하지 않고 리듬감 있게, 영어 초보자도 쉽게 따라할 수 있도록 구성해줘. 
    한줄마다 한 문장씩 보여줘.
    문장들:
    {chr(10).join(lines)}
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    return response.choices[0].message.content.strip()

def rewrite_for_repetition(dialogue: str) -> list[str]:
    print("🔄 리듬형 반복 대화문 생성 중...")
    prompt = f"""
    나는 영어 학습용 TTS 콘텐츠를 만들고 있어.

    다음은 영어 대화문이야. 이걸 **암기용 리듬형 반복 대화문**으로 다시 재구성해줘.

    각 문장마다 해야 할 작업 목록이야:
    
    1. 원래 문장 3번 반복.
    2. 호흡이 긴 문장의 경우 반으로 쪼개서 4번 반복.
    3. Verb Phrase, Idiomatic Expression / Fixed Expression, Adjective + Preposition Combinations 과 같은 유용한 구문이 있다면 이걸 2~3번 반복해줘.
    4. 각 문장은 짧고 세련되게 리듬감 있게 만들어줘.
    
    이렇게 1번에서 4번까지가 한 문장에 대해 해야 할 작업이야. 모든 문장을 이렇게 처리해줘.
    원문:
    {dialogue}
    """
    # prompt = f"""
    # 나는 영어 학습용 TTS 콘텐츠를 만들고 있어.

    # 다음은 영어 대화문이야. 이걸 **암기용 리듬형 반복 대화문**으로 다시 구성해줘.

    # 규칙은 아래와 같아:
    
    # 1. 사용빈도가 높은 문장은 2~3번 반복해줘.
    # 2. 그 다음은 문장을 짧게 나눠서 2~3번 반복해줘.
    # 3. be afraid of, willing to, would wait for it 과 같은 유용한 구문이 있다면 이걸 2~3번 반복해줘.
    # 4. 각 문장은 짧고 세련되게 리듬감 있게 만들어줘.

    # 원문:
    # {dialogue}
    # """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    content = response.choices[0].message.content.strip()
    return [line.strip('-•* ') for line in content.splitlines() if line.strip()]

def simplify_script(lines: list[str], level: str = "easy") -> list[str]:
    base_dialogue = generate_base_dialogue(lines, level)
    result =  rewrite_for_repetition(base_dialogue)
    print(result)
    return result
