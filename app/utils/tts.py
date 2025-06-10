import edge_tts
import os
import uuid
import asyncio
from pydub import AudioSegment

async def generate_tts(text: str, out_path: str, voice="en-US-JennyNeural"):
    lines = [line.strip() for line in text.split('.') if line.strip()]
    temp_dir = f"temp_audio_{uuid.uuid4().hex[:6]}"
    os.makedirs(temp_dir, exist_ok=True)

    tasks = []
    all_paths = []

    for i, sentence in enumerate(lines):
        print(f"🔊 처리 중: {sentence}")

        full_path = os.path.join(temp_dir, f"{i}_full.mp3")
        tasks.append(_generate_tts_clip(sentence, full_path, voice))
        all_paths.append(full_path)

        parts = sentence.split()
        chunk_size = max(1, len(parts) // 3)
        chunks = [" ".join(parts[j:j + chunk_size]) for j in range(0, len(parts), chunk_size)]

        for idx, chunk in enumerate(chunks):
            for rep in range(2):
                chunk_path = os.path.join(temp_dir, f"{i}_chunk_{idx}_{rep}.mp3")
                tasks.append(_generate_tts_clip(chunk, chunk_path, voice))
                all_paths.append(chunk_path)

        repeat_path = os.path.join(temp_dir, f"{i}_repeat.mp3")
        tasks.append(_generate_tts_clip(sentence, repeat_path, voice))
        all_paths.append(repeat_path)

        final_path = os.path.join(temp_dir, f"{i}_final.mp3")
        tasks.append(_generate_tts_clip(sentence, final_path, voice))
        all_paths.append("silence")
        all_paths.append(final_path)

    await asyncio.gather(*tasks)  # ✅ 이 부분 수정됨

    silence = AudioSegment.silent(duration=2000)
    final_audio = AudioSegment.empty()

    for path in all_paths:
        if path == "silence":
            final_audio += silence
        else:
            final_audio += AudioSegment.from_file(path)

    final_audio.export(out_path, format="mp3")
    print(f"✅ 학습 오디오 저장 완료: {out_path}")

async def _generate_tts_clip(text: str, path: str, voice="en-US-JennyNeural"):
    communicate = edge_tts.Communicate(text, voice=voice)
    await communicate.save(path)
