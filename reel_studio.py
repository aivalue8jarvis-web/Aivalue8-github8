import os
import re
import time
import asyncio
import textwrap
import subprocess
import edge_tts
import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont

MEDIA_DIR = "/tmp/aivalue8_media"
os.makedirs(MEDIA_DIR, exist_ok=True)

def _cleanup_old_media():
    files = sorted(
        [os.path.join(MEDIA_DIR, f) for f in os.listdir(MEDIA_DIR) if f.endswith(".mp4")],
        key=os.path.getmtime
    )
    for old in files[:-5]:
        try:
            os.remove(old)
        except Exception:
            pass

def _make_slide(path: str, badge: str, body: str, step_idx: int, total: int = 4):
    w, h = 720, 1280
    img = Image.new("RGB", (w, h), (5, 10, 24))
    draw = ImageDraw.Draw(img)

    # Neon border & header bar
    draw.rounded_rectangle([28, 36, w - 28, h - 36], radius=34, outline=(56, 189, 248), width=4)
    draw.rounded_rectangle([54, 72, 370, 126], radius=24, fill=(15, 23, 42), outline=(52, 211, 153), width=2)

    try:
        f_small = ImageFont.load_default(size=24)
        f_title = ImageFont.load_default(size=46)
        f_foot = ImageFont.load_default(size=26)
    except Exception:
        f_small = f_title = f_foot = ImageFont.load_default()

    draw.text((78, 86), badge[:22], fill=(52, 211, 153), font=f_small)

    lines = []
    for para in body.split("\n"):
        lines.extend(textwrap.wrap(para.strip(), width=21) or [""])
    lines = lines[:9]

    line_h = 62
    start_y = max(240, (h - len(lines) * line_h) // 2)
    for idx, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=f_title)
        tw = bbox[2] - bbox[0]
        x = (w - tw) // 2
        draw.text((x, start_y + idx * line_h), line, fill=(248, 250, 252), font=f_title)

    # Progress dots & footer
    dot_x0 = (w - (total * 34)) // 2
    for i in range(total):
        col = (52, 211, 153) if i == step_idx else (51, 65, 85)
        draw.ellipse([dot_x0 + i * 34, h - 170, dot_x0 + i * 34 + 18, h - 152], fill=col)

    foot = "sarahics.in  |  aIValue8 AI OS"
    fb = draw.textbbox((0, 0), foot, font=f_foot)
    draw.text(((w - (fb[2] - fb[0])) // 2, h - 115), foot, fill=(56, 189, 248), font=f_foot)
    img.save(path, "PNG")

async def _tts_save(text: str, out_mp3: str):
    comm = edge_tts.Communicate(text, "en-IN-PrabhatNeural")
    await comm.save(out_mp3)

def create_reel_mp4(title: str, hook: str, script_body: str, cta_url: str = "https://sarahics.in") -> str:
    _cleanup_old_media()
    uid = f"reel_{int(time.time())}"
    out_mp4 = os.path.join(MEDIA_DIR, f"{uid}.mp4")
    audio_mp3 = os.path.join(MEDIA_DIR, f"{uid}.mp3")
    slides_txt = os.path.join(MEDIA_DIR, f"{uid}.txt")

    clean_script = re.sub(r"\[[^\]]+\]|\([^\)]+\)", " ", script_body or "")
    clean_script = " ".join(clean_script.split())
    sentences = [s.strip() for s in re.split(r"[.!?]+", clean_script) if len(s.strip()) > 6]

    slide_texts = [
        ("aIValue8 AI", hook or title),
        ("THE PROBLEM", sentences[0] if len(sentences) > 0 else "Manual kaam aur missed leads se growth rukti hai."),
        ("AUTO SOLUTION", sentences[1] if len(sentences) > 1 else "Web, App, CRM aur Sales ab 24/7 AI automate karta hai."),
        ("START TODAY", f"Try Free AI Demo Now\n{cta_url}\nAI • Web/App • CRM")
    ]

    png_paths = []
    for i, (badge, txt) in enumerate(slide_texts):
        p = os.path.join(MEDIA_DIR, f"{uid}_{i}.png")
        _make_slide(p, badge, txt, i, len(slide_texts))
        png_paths.append(p)

    with open(slides_txt, "w") as f:
        for p in png_paths:
            f.write(f"file '{p}'\nduration 6\n")
        f.write(f"file '{png_paths[-1]}'\n")

    voice_text = f"{hook}. {' '.join(sentences[:3])}. Visit sarahics dot in today."
    has_audio = False
    try:
        asyncio.run(_tts_save(voice_text[:550], audio_mp3))
        has_audio = os.path.exists(audio_mp3) and os.path.getsize(audio_mp3) > 500
    except Exception:
        has_audio = False

    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    if has_audio:
        cmd = [ffmpeg_exe, "-y", "-f", "concat", "-safe", "0", "-i", slides_txt, "-i", audio_mp3, "-vf", "scale=720:1280,fps=24,format=yuv420p", "-c:v", "libx264", "-preset", "ultrafast", "-c:a", "aac", "-b:a", "128k", "-shortest", out_mp4]
    else:
        cmd = [ffmpeg_exe, "-y", "-f", "concat", "-safe", "0", "-i", slides_txt, "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100", "-t", "18", "-vf", "scale=720:1280,fps=24,format=yuv420p", "-c:v", "libx264", "-preset", "ultrafast", "-c:a", "aac", "-shortest", out_mp4]

    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    for tmp in png_paths + [audio_mp3, slides_txt]:
        try:
            if os.path.exists(tmp):
                os.remove(tmp)
        except Exception:
            pass
    return out_mp4
