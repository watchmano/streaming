from pydub import AudioSegment

def mix_tts_with_bgm(tts_path: str, bgm_path: str, output_path: str):
    tts = AudioSegment.from_file(tts_path)
    bgm = AudioSegment.from_file(bgm_path)
    tts += 6
    bgm -= 6
    bgm = bgm[:len(tts)]
    mixed = bgm.overlay(tts)
    mixed.export(output_path, format="mp3")