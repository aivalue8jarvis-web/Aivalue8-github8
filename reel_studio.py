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

def _draw_logo_mark(draw, cx, cy):
    draw.ellipse([cx - 18, cy - 30, cx + 18, cy + 2], outline=(56, 189, 248), width=5)
    draw.ellipse([cx - 18, cy - 2, cx + 18, cy + 30], outline=(16, 185, 129), width=5)
    draw.line([(cx - 22, cy + 22), (cx + 24, cy - 24)], fill=(52, 211, 153), width=5)
    draw.line([(cx + 10, cy - 24), (cx + 24, cy - 24), (cx + 24, cy - 10)], fill=(52, 211, 153), width=5)

def _draw_scene_graphic(draw, w, scene_idx, step, f_sm):
    # Subtle cyber grid
    for gx in range(60, w, 100):
        draw.line([(gx, 140), (gx, 620)], fill=(12, 24, 48), width=1)
    for gy in range(160, 620, 90):
        draw.line([(45, gy), (w - 45, gy)], fill=(12, 24, 48), width=1)

    cx, cy = w // 2, 370
    if scene_idx == 0:
        # AI Radar & Neural Nodes
        for r in [55 + step * 18, 105 + step * 18]:
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(30, 80, 140), width=3)
        nodes = [(cx - 140, cy - 80), (cx + 140, cy - 70), (cx - 130, cy + 90), (cx + 135, cy + 85)]
        for nx, ny in nodes:
            draw.line([(cx, cy), (nx, ny)], fill=(56, 189, 248), width=3)
            col = (52, 211, 153) if step % 2 == 0 else (56, 189, 248)
            draw.ellipse([nx - 12, ny - 12, nx + 12, ny + 12], fill=col)
        draw.ellipse([cx - 46, cy - 46, cx + 46, cy + 46], fill=(10, 18, 38), outline=(56, 189, 248), width=4)
        _draw_logo_mark(draw, cx, cy)

    elif scene_idx == 1:
        # Manual Chaos / Missed Leads Card
        draw.rounded_rectangle([95, 220, w - 95, 520], radius=24, fill=(18, 14, 30), outline=(248, 113, 113), width=3)
        draw.text((130, 248), "MANUAL SYSTEM ALERT", fill=(248, 113, 113), font=f_sm)
        bars = [190, 145, 100, 65]
        for idx, bh in enumerate(bars):
            x0 = 155 + idx * 105
            col = (248, 113, 113) if idx <= step else (51, 65, 85)
            draw.rounded_rectangle([x0, 480 - bh, x0 + 55, 480], radius=8, fill=col)

    elif scene_idx == 2:
        # Rising Growth Bar Chart + Automation Pipeline
        draw.rounded_rectangle([85, 210, w - 85, 535], radius=24, fill=(10, 22, 42), outline=(52, 211, 153), width=3)
        pills = ["AI", "CRM", "PAY"]
        for i, lbl in enumerate(pills):
            px = 135 + i * 165
            active = i <= step
            fill_c = (16, 185, 129) if active else (15, 23, 42)
            draw.rounded_rectangle([px, 245, px + 115, 295], radius=14, fill=fill_c, outline=(56, 189, 248), width=2)
            draw.text((px + 34, 258), lbl, fill=(255, 255, 255), font=f_sm)
            if i < 2:
                draw.line([(px + 118, 270), (px + 162, 270)], fill=(56, 189, 248), width=4)
        heights = [70, 115, 160, 205]
        for i, hval in enumerate(heights):
            bx = 160 + i * 105
            show_h = hval if i <= step else 35
            bcol = (52, 211, 153) if i <= step else (30, 41, 59)
            draw.rounded_rectangle([bx, 510 - show_h, bx + 55, 510], radius=8, fill=bcol)

    else:
        # Smartphone Mockup showing sarahics.in
        draw.rounded_rectangle([185, 185, w - 185, 555], radius=34, fill=(8, 15, 32), outline=(56, 189, 248), width=4)
        _draw_logo_mark(draw, cx, 255)
        draw.text((232, 315), "sarahics.in", fill=(52, 211, 153), font=f_sm)
        draw.text((225, 358), "AI | Web | App | CRM", fill=(203, 213, 225), font=f_sm)
        btn_col = (16, 185, 129) if step % 2 == 0 else (37, 99, 235)
        draw.rounded_rectangle([225, 425, w - 225, 490], radius=16, fill=btn_col)
        draw.text((255, 444), "TRY FREE DEMO", fill=(255, 255, 255), font=f_sm)

def _make_frame(path: str, badge: str, body: str, scene_idx: int, step: int, frame_num: int, total_frames: int = 16):
    w, h = 720, 1280
    img = Image.new("RGB", (w, h), (4, 8, 20))
    draw = ImageDraw.Draw(img)

    draw.rounded_rectangle([24, 30, w - 24, h - 30], radius=34, outline=(37, 99, 235), width=4)
    draw.rounded_rectangle([50, 62, 360, 114], radius=22, fill=(15, 23, 42), outline=(52, 211, 153), width=2)
    draw.text((w - 235, 76), "aIValue8 OS", fill=(56, 189, 248), font=ImageFont.load_default(size=24))

    try:
        f_sm = ImageFont.load_default(size=23)
        f_title = ImageFont.load_default(size=40)
        f_foot = ImageFont.load_default(size=26)
    except Exception:
        f_sm = f_title = f_foot = ImageFont.load_default()

    draw.text((74, 76), badge[:20], fill=(52, 211, 153), font=f_sm)
    _draw_scene_graphic(draw, w, scene_idx, step, f_sm)

    # Clean ASCII text box in lower half
    clean_body = body.replace("•", "|")
    lines = []
    for para in clean_body.split("\n"):
        lines.extend(textwrap.wrap(para.strip(), width=23) or [""])
    lines = lines[:7]

    draw.rounded_rectangle([52, 585, w - 52, 1085], radius=26, fill=(10, 18, 36), outline=(30, 58, 110), width=2)
    line_h = 58
    start_y = max(625, 585 + (500 - len(lines) * line_h) // 2)
    for idx, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=f_title)
        x = (w - (bbox[2] - bbox[0])) // 2
        draw.text((x, start_y + idx * line_h), line, fill=(248, 250, 252), font=f_title)

    # Animated Progress Bar
    draw.rounded_rectangle([70, h - 165, w - 70, h - 149], radius=8, fill=(30, 41, 59))
    prog_w = int(((w - 140) * (frame_num + 1)) / total_frames)
    draw.rounded_rectangle([70, h - 165, 70 + prog_w, h - 149], radius=8, fill=(52, 211, 153))

    foot = "sarahics.in  |  AI Business OS"
    fb = draw.textbbox((0, 0), foot, font=f_foot)
    draw.text(((w - (fb[2] - fb[0])) // 2, h - 112), foot, fill=(56, 189, 248), font=f_foot)
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

    scenes = [
        ("aIValue8 AI", hook or title),
        ("THE PROBLEM", sentences[0] if len(sentences) > 0 else "Manual kaam aur missed leads se growth rukti hai."),
        ("AUTO SOLUTION", sentences[1] if len(sentences) > 1 else "Web, App, CRM aur Sales ab 24/7 AI automate karta hai."),
        ("START TODAY", f"Try Free AI Demo Now\n{cta_url}\nAI | Web/App | CRM")
    ]

    png_paths = []
    fnum = 0
    for s_idx, (badge, txt) in enumerate(scenes):
        for step in range(4):
            p = os.path.join(MEDIA_DIR, f"{uid}_{fnum}.png")
            _make_frame(p, badge, txt, s_idx, step, fnum, 16)
            png_paths.append(p)
            fnum += 1

    with open(slides_txt, "w") as f:
        for p in png_paths:
            f.write(f"file '{p}'\nduration 1.25\n")
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


def create_reel_from_screenshots(image_paths: list, title: str, hook: str, script_body: str, cta_url: str = "https://sarahics.in") -> str:
    _cleanup_old_media()
    uid = f"appreel_{int(time.time())}"
    out_mp4 = os.path.join(MEDIA_DIR, f"{uid}.mp4")
    audio_mp3 = os.path.join(MEDIA_DIR, f"{uid}.mp3")
    slides_txt = os.path.join(MEDIA_DIR, f"{uid}.txt")

    clean_script = re.sub(r"\[[^\]]+\]|\([^\)]+\)", " ", script_body or "")
    clean_script = " ".join(clean_script.split())
    sentences = [x.strip() for x in re.split(r"[.!?]+", clean_script) if len(x.strip()) > 6]
    captions = [hook or title, sentences[0] if sentences else "Smart AI Built App Demo", f"Try Live: {cta_url}"]

    png_paths = []
    f_sm = ImageFont.load_default(size=24)
    f_cap = ImageFont.load_default(size=36)
    w, h = 720, 1280

    for idx in range(max(len(image_paths), len(captions))):
        src = image_paths[idx % len(image_paths)]
        cap = captions[idx % len(captions)].replace("•", "|")
        img = Image.new("RGB", (w, h), (4, 8, 20))
        draw = ImageDraw.Draw(img)
        draw.rounded_rectangle([24, 30, w - 24, h - 30], radius=34, outline=(56, 189, 248), width=4)
        draw.text((55, 62), "aIValue8 LIVE APP DEMO", fill=(52, 211, 153), font=f_sm)

        # Paste User App Screenshot cleanly inside glowing frame
        draw.rounded_rectangle([85, 115, w - 85, 765], radius=24, fill=(10, 18, 36), outline=(52, 211, 153), width=3)
        shot = Image.open(src).convert("RGB")
        shot.thumbnail((520, 620))
        sx = (w - shot.width) // 2
        sy = 128 + (620 - shot.height) // 2
        img.paste(shot, (sx, sy))

        # Caption Card
        draw.rounded_rectangle([52, 795, w - 52, 1135], radius=24, fill=(10, 18, 36), outline=(37, 99, 235), width=2)
        lines = textwrap.wrap(cap, width=25)[:5]
        y0 = 835
        for ln in lines:
            bb = draw.textbbox((0, 0), ln, font=f_cap)
            draw.text(((w - (bb[2] - bb[0])) // 2, y0), ln, fill=(248, 250, 252), font=f_cap)
            y0 += 52
        draw.text((195, h - 105), "sarahics.in  |  AI Apps", fill=(56, 189, 248), font=f_sm)

        out_p = os.path.join(MEDIA_DIR, f"{uid}_{idx}.png")
        img.save(out_p, "PNG")
        png_paths.append(out_p)

    with open(slides_txt, "w") as f:
        for p in png_paths:
            f.write(f"file '{p}'\nduration 5\n")
        f.write(f"file '{png_paths[-1]}'\n")

    voice_text = f"{hook}. {" ".join(sentences[:2])}. Visit sarahics dot in."
    has_audio = False
    try:
        asyncio.run(_tts_save(voice_text[:500], audio_mp3))
        has_audio = os.path.exists(audio_mp3) and os.path.getsize(audio_mp3) > 500
    except Exception:
        has_audio = False

    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    if has_audio:
        cmd = [ffmpeg_exe, "-y", "-f", "concat", "-safe", "0", "-i", slides_txt, "-i", audio_mp3, "-vf", "scale=720:1280,fps=24,format=yuv420p", "-c:v", "libx264", "-preset", "ultrafast", "-c:a", "aac", "-b:a", "128k", "-shortest", out_mp4]
    else:
        cmd = [ffmpeg_exe, "-y", "-f", "concat", "-safe", "0", "-i", slides_txt, "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100", "-t", "15", "-vf", "scale=720:1280,fps=24,format=yuv420p", "-c:v", "libx264", "-preset", "ultrafast", "-c:a", "aac", "-shortest", out_mp4]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    for tmp in png_paths + [audio_mp3, slides_txt]:
        try:
            if os.path.exists(tmp):
                os.remove(tmp)
        except Exception:
            pass
    return out_mp4
