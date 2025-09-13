import os
import subprocess
import fitz  # Correct import name
from ebooklib import epub
from bs4 import BeautifulSoup
from gtts import gTTS
from moviepy.editor import AudioFileClip, TextClip  # fixed import
import torch
from transformers import pipeline, logging, AutoTokenizer, AutoModelForSeq2SeqLM
import time
import pyttsx3
from gtts import gTTS, gTTSError
from moviepy.config import change_settings
change_settings({"IMAGEMAGICK_BINARY": r"C:\\Program Files\\ImageMagick-7.1.2-Q16\\magick.exe"})


logging.set_verbosity_info()  # Hugging Face download logs




def extract_text(file_path):
    if file_path.endswith(".pdf"):
        print("   Opening PDF...", flush=True)
        doc = fitz.open(file_path)
        return "".join(page.get_text() for page in doc)
    elif file_path.endswith(".epub"):
        print("   Opening EPUB...", flush=True)
        book = epub.read_epub(file_path)
        text = ""
        for item in book.get_items():
            if item.get_type() == epub.ITEM_DOCUMENT:
                soup = BeautifulSoup(item.get_content(), 'html.parser')
                text += soup.get_text()
        return text
    else:
        raise ValueError("Unsupported file type. Use PDF or EPUB.")


def summarize(text, force_device="auto"):
    print("   Loading summarization model...", flush=True)

    if force_device == "cuda" and torch.cuda.is_available():
        device = 0
        print(f"   ✅ Using GPU: {torch.cuda.get_device_name(0)}", flush=True)
    elif force_device == "cuda" and not torch.cuda.is_available():
        print("   ⚠️ CUDA requested but no GPU detected. Falling back to CPU.", flush=True)
        device = -1
    elif force_device == "cpu":
        device = -1
        print("   ⚠️ Forcing CPU mode.", flush=True)
    else:
        device = 0 if torch.cuda.is_available() else -1
        if device == 0:
            print(f"   ✅ GPU detected: {torch.cuda.get_device_name(0)}", flush=True)
        else:
            print("   ⚠️ No GPU detected, using CPU.", flush=True)

    model_name = "sshleifer/distilbart-cnn-12-6"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    summarizer = pipeline(
        "summarization",
        model=model,
        tokenizer=tokenizer,
        device=device
    )

    chunk_size = 1000
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
    summaries = []

    for i, chunk in enumerate(chunks, start=1):
        print(f"   Summarizing chunk {i}/{len(chunks)}...", flush=True)
        result = summarizer(chunk, max_length=130, min_length=30, do_sample=False)[0]['summary_text']
        summaries.append(result)

    return " ".join(summaries)


def generate_audio(text, output_path="output/fast_audio.mp3"):
    print("   Generating TTS audio...", flush=True)
    raw_audio_path = "output/audio.mp3"

    try:
        max_chunk_size = 400
        chunks = [text[i:i+max_chunk_size] for i in range(0, len(text), max_chunk_size)]

        with open(raw_audio_path, "wb") as f:
            for i, chunk in enumerate(chunks):
                print(f"      🔊 gTTS processing chunk {i+1}/{len(chunks)}", flush=True)
                tts = gTTS(chunk, lang="en", slow=False)
                tts.write_to_fp(f)
                time.sleep(1)

    except gTTSError as e:
        print(f"   ⚠️ gTTS failed ({e}), falling back to offline pyttsx3...", flush=True)
        engine = pyttsx3.init()
        engine.save_to_file(text, raw_audio_path)
        engine.runAndWait()

    print("   Speeding audio with ffmpeg (4x)...", flush=True)
    subprocess.run(
        ['ffmpeg', '-y', '-i', raw_audio_path, '-filter:a', 'atempo=2.0,atempo=2.0', output_path],
        check=True
    )
    return output_path


def generate_srt(text, output_path="output/subs.srt"):
    print("   Generating subtitles...", flush=True)
    words = text.split()
    lines = [" ".join(words[i:i+8]) for i in range(0, len(words), 8)]
    srt = ""
    for i, line in enumerate(lines):
        start = i * 2
        end = start + 2
        srt += f"{i+1}\n00:00:{start:02},000 --> 00:00:{end:02},000\n{line}\n\n"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(srt)

    return output_path


def create_video(text, audio_path, output_path="output/final_video.mp4"):
    print("   Creating video preview...", flush=True)
    preview_text = text[:200] + "..."
    audio_clip = AudioFileClip(audio_path)
    txt_clip = TextClip(
        preview_text,
        fontsize=48,
        color='white',
        size=(1280, 720),
        method='caption'
    ).set_duration(audio_clip.duration)

    video = txt_clip.set_audio(audio_clip)
    print("   Rendering final video (this may take a few minutes)...", flush=True)
    video.write_videofile(output_path, fps=24)


def main():
    #change book file to the one you want done on the input_path
    input_path = r"C:\Users\pmspi\4X Book Speed Code\4x reading project\Your_book.pdf\_OceanofPDF.com_Ready_Fire_Aim_-_Michael_Masterson.pdf"
    os.makedirs("output", exist_ok=True)

    print("[1] Extracting text...", flush=True)
    text = extract_text(input_path)

    print("[2] Summarizing...", flush=True)
    summary = summarize(text, force_device="cuda")

    print("[3] Generating audio at 4x speed...", flush=True)
    audio_path = generate_audio(summary)

    print("[4] Creating subtitles...", flush=True)
    generate_srt(summary)

    print("[5] Rendering video...", flush=True)
    create_video(summary, audio_path)

    print("✅ Done! Video saved to output/final_video.mp4", flush=True)

if __name__ == "__main__":
    main()
