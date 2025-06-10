from fastapi import FastAPI, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import os
from utils.transcript import get_transcript
from utils.gpt import simplify_script
from utils.tts import generate_tts  # ← 여기 수정됨
from utils.mixer import mix_tts_with_bgm

# 절대 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

# 디렉토리 없을 경우 생성
os.makedirs(OUTPUT_DIR, exist_ok=True)

app = FastAPI()

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
app.mount("/output", StaticFiles(directory=OUTPUT_DIR), name="output")

@app.post("/api/process")
async def process(youtubeUrl: str = Form(...), level: str = Form(...)):
    try:
        print(f"📥 요청 수신: url={youtubeUrl}, level={level}")
        lines = get_transcript(youtubeUrl)
        simplified = simplify_script(lines, level)
        joined = " ".join(simplified)

        tts_path = os.path.join(OUTPUT_DIR, "tts.mp3")
        final_path = os.path.join(OUTPUT_DIR, "final.mp3")
        bgm_path = os.path.join(BASE_DIR, "assets/bgm/bgm_hiphop.mp3")

        # ✅ await 사용
        await generate_tts(joined, tts_path)
        mix_tts_with_bgm(tts_path, bgm_path, final_path)

        return JSONResponse({ "script": simplified, "audioUrl": "/output/final.mp3" })
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": str(e)})
