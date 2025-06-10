import edge_tts
import os
import uuid
import asyncio
from pydub import AudioSegment

async def _generate_tts_clip(text: str, path: str, voice="en-US-JennyNeural", rate="-10%"):
    communicate = edge_tts.Communicate(text, voice=voice, rate=rate)
    await communicate.save(path)

def generate_tts(text: str, out_path: str, voice="en-US-JennyNeural"):
    lines = [line.strip() for line in text.split('.') if line.strip()]
    first_sentence = lines[0]
    temp_dir = f"temp_audio_{uuid.uuid4().hex[:6]}"
    os.makedirs(temp_dir, exist_ok=True)

    async def process_first_sentence():
        print(f"🔊 첫 문장 처리 중: {first_sentence}")
        tasks = []
        paths = []

        # 1. 전체 문장 느리게 읽기
        intro_path = os.path.join(temp_dir, "01_intro.mp3")
        tasks.append(_generate_tts_clip(f"Listen carefully: {first_sentence}", intro_path, voice))
        paths.append(intro_path)

        # 2. 문장 절반씩 나누기 후 2회 반복
        words = first_sentence.split()
        half = len(words) // 2
        first_half = " ".join(words[:half])
        second_half = " ".join(words[half:])

        for i in range(2):
            p1_path = os.path.join(temp_dir, f"02_half1_{i}.mp3")
            p2_path = os.path.join(temp_dir, f"03_half2_{i}.mp3")
            tasks.append(_generate_tts_clip(first_half, p1_path, voice))
            tasks.append(_generate_tts_clip(second_half, p2_path, voice))
            paths.extend([p1_path, p2_path])

        # 3. 따라 말하세요 안내 + 정적
        prompt_path = os.path.join(temp_dir, "04_prompt.mp3")
        tasks.append(_generate_tts_clip("Your turn now.", prompt_path, voice))
        paths.append(prompt_path)
        paths.append("silence")  # 2초 정적

        # 4. 정답 다시 들려주기
        final_path = os.path.join(temp_dir, "05_final.mp3")
        tasks.append(_generate_tts_clip(f"Correct pronunciation: {first_sentence}", final_path, voice))
        paths.append(final_path)

        await asyncio.gather(*tasks)

        # 오디오 합치기
        silence = AudioSegment.silent(duration=2000)
        combined = AudioSegment.empty()

        for path in paths:
            if path == "silence":
                combined += silence
            else:
                combined += AudioSegment.from_file(path)

        combined.export(out_path, format="mp3")
        print(f"✅ 첫 문장 오디오 생성 완료: {out_path}")

    asyncio.run(process_first_sentence())
