import os
import openai
from dotenv import load_dotenv

load_dotenv()  # .env에서 환경변수 로드
# 새로운 클라이언트 객체 생성
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def simplify_script(lines: list[str], level: str = "easy") -> list[str]:
    MAX_TOKENS = 16000  # gpt-3.5-turbo context limit
    MAX_LINES = 100

    # 너무 긴 입력 방지
    lines = lines[:MAX_LINES]
    level_map = {
        "easy": "초등학생도 따라하기 쉬운 말투로",
        "medium": "일반적인 회화체로",
        "hard": "자연스러운 고급 표현으로"
    }

    prompt = f"""
다음 문장을 {level_map.get(level, '회화체로')} 리라이트 해줘. 
문장은 간단하고 짧게, 리듬감 있게 표현해줘. 줄마다 따로 보여줘.

{chr(10).join(lines)}
"""
    
    # 최신 방식의 Chat API 호출
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    content = response.choices[0].message.content.strip()

    # 라인 단위로 파싱
    return [line.strip('-•* ') for line in content.splitlines() if line.strip()]
