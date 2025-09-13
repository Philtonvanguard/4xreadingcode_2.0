# 4xreadingcode_2.0

📚 PDF/EPUB Summarizer to 4x Speed Audiobook + Video

This project automates the process of turning any PDF or EPUB book into a summarized audiobook and video preview — making it possible to "read" books up to 4x faster through audio and subtitles.

🚀 Features

Text Extraction

Supports PDF (via PyMuPDF) and EPUB (via ebooklib + BeautifulSoup).

AI-Powered Summarization

Uses Hugging Face DistilBART CNN model (sshleifer/distilbart-cnn-12-6) for efficient summarization.

Automatic GPU/CPU detection with CUDA support.

Text-to-Speech (TTS)

Converts summaries into natural-sounding audio using:

✅ Google TTS (gTTS) (online, high quality)

⚠️ Fallback to pyttsx3 (offline, when gTTS fails)

Audio automatically sped up to 4x using FFmpeg.

Subtitles (SRT)

Generates synchronized .srt subtitle files for reading along.

Video Preview

Creates a .mp4 video with:

Book summary text overlay (first 200 chars).

Summarized audiobook narration.

Useful for YouTube uploads, previews, or learning.

🛠️ Requirements

Install dependencies with:

pip install pymupdf ebooklib beautifulsoup4 gtts moviepy torch transformers pyttsx3


Additional setup:

FFmpeg must be installed and available in PATH.

ImageMagick required for MoviePy text rendering (configure binary path in code).

📂 Output

All results are saved in the output/ directory:

fast_audio.mp3 → Summarized audiobook (4x speed)

subs.srt → Subtitles file

final_video.mp4 → Preview video with text + audio

▶️ Usage

Place your book file (.pdf or .epub) in the project directory.

Update input_path in main() with your file location.

Run the script:

python main.py


Collect your audiobook & video from the output/ folder.

💡 Example Workflow

Import a book (Ready, Fire, Aim in example).

Extracts full text → Summarizes → Converts to audio.

Speeds up audio ×4 → Generates subtitles.

Produces a final video with synced narration + preview text.

🎯 Use Cases

Speed-reading books & research papers.

Creating quick summaries for study or business.

Generating video/audio content for social media or personal learning.
