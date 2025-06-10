for i, sentence in enumerate(lines):
    print(f"🔊 처리 중: {sentence}")
    
    sentence_audio = AudioSegment.empty()
    sentence_tasks = []

    # 전체 문장
    full_path = os.path.join(temp_dir, f"{i}_full.mp3")
    sentence_tasks.append(_generate_tts_clip(sentence, full_path, voice))

    # 반으로 나누기
    words = sentence.split()
    half = len(words) // 2
    first_half = " ".join(words[:half])
    second_half = " ".join(words[half:])

    for rep in range(2):
        path1 = os.path.join(temp_dir, f"{i}_half1_{rep}.mp3")
        path2 = os.path.join(temp_dir, f"{i}_half2_{rep}.mp3")
        sentence_tasks.append(_generate_tts_clip(first_half, path1, voice))
        sentence_tasks.append(_generate_tts_clip(second_half, path2, voice))

    # 다시 전체 문장
    repeat_path = os.path.join(temp_dir, f"{i}_repeat.mp3")
    sentence_tasks.append(_generate_tts_clip(sentence, repeat_path, voice))

    # 정적 구간 + 다시 전체
    final_path = os.path.join(temp_dir, f"{i}_final.mp3")
    sentence_tasks.append(_generate_tts_clip(sentence, final_path, voice))

    # 실행
    asyncio.run(asyncio.gather(*sentence_tasks))

    # 오디오 연결
    for path in [full_path,
                 *(os.path.join(temp_dir, f"{i}_half1_{r}.mp3") for r in range(2)),
                 *(os.path.join(temp_dir, f"{i}_half2_{r}.mp3") for r in range(2)),
                 repeat_path,
                 "silence",
                 final_path]:
        if path == "silence":
            sentence_audio += AudioSegment.silent(duration=2000)
        else:
            sentence_audio += AudioSegment.from_file(path)

    final_audio += sentence_audio
