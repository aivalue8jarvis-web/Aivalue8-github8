import os
import re
import math
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
    files = sorted([os.path.join(MEDIA_DIR, f) for f in os.listdir(MEDIA_DIR) if f.endswith(".mp4")], key=os.path.getmtime)
    for old in files[:-5]:
        try:
            os.remove(old)
        except Exception:
            pass

def _draw_bg_and_orb(draw, w, h, frame_num):
    for gx in range(0, w, 64):
        draw.line([(gx, 0), (gx, h)], fill=(7, 30, 20), width=1)
    for gy in range(0, h, 64):
        draw.line([(0, gy), (w, gy)], fill=(7, 30, 20), width=1)

    # Emergent-style rotating 3D dotted AI orb at bottom
    cx, cy = w // 2, 1055
    draw.ellipse([cx - 135, cy - 135, cx + 135, cy + 135], outline=(16, 85, 55), width=2)
    draw.ellipse([cx - 112, cy - 112, cx + 112, cy + 112], fill=(4, 22, 15), outline=(52, 211, 153), width=3)
    phase = frame_num * 0.35
    for lat in range(-4, 5):
        ry = lat * 20
        rx_max = math.sqrt(max(1, 95 * 95 - ry * ry))
        for lon in range(0, 10):
            ang = phase + lon * 0.628
            px = cx + math.sin(ang) * rx_max
            py = cy + ry + math.cos(ang) * 8
            col = (52, 211, 153) if math.cos(ang) > 0 else (16, 110, 75)
            r = 4 if math.cos(ang) > 0.2 else 2
            draw.ellipse([px - r, py - r, px + r, py + r], fill=col)

def _draw_highlighted_caption(draw, w, y_start, text, font):
    clean = text.replace("•", "|")
    lines = textwrap.wrap(clean, width=22)[:4]
    y = y_start
    for idx, line in enumerate(lines):
        words = line.split(" ")
        tw = draw.textbbox((0, 0), line, font=font)[2]
        x = (w - tw) // 2
        for w_i, word in enumerate(words):
            col = (52, 211, 153) if (idx == 0 and w_i == 0) or word.lower().startswith("sarahics") else (248, 250, 252)
            part = word + (" " if w_i < len(words) - 1 else "")
            draw.text((x, y), part, fill=col, font=font)
            x += draw.textbbox((0, 0), part, font=font)[2]
        y += 56

def _draw_scene_ui(draw, w, scene_idx, step, f_sm, f_big):
    if scene_idx == 0:
        # AI Mode Toggle Pill
        draw.rounded_rectangle([240, 120, 480, 195], radius=36, fill=(10, 26, 20), outline=(52, 211, 153), width=2)
        draw.ellipse([265, 134, 315, 182], outline=(100, 116, 139), width=2)
        on_col = (16, 185, 129) if step % 2 == 0 else (34, 197, 94)
        draw.ellipse([405, 132, 458, 184], fill=on_col)
        draw.text((418, 146), "AI", fill=(255, 255, 255), font=f_sm)

    elif scene_idx == 1:
        # Pop-up Full-Stack Checkmark Cards
        items = [("Interface", "Website & App Ready"), ("Data Store", "Neon Cloud Memory"), ("Auto CRM", "Email + WhatsApp Bot"), ("Go Live", "sarahics.in LIVE")]
        for i in range(min(step + 1, 4)):
            y0 = 115 + i * 118
            title, sub = items[i]
            draw.rounded_rectangle([75, y0, w - 75, y0 + 96], radius=18, fill=(8, 22, 16), outline=(52, 211, 153), width=2)
            draw.text((105, y0 + 18), title, fill=(248, 250, 252), font=f_sm)
            draw.text((105, y0 + 52), sub, fill=(148, 163, 184), font=ImageFont.load_default(size=20))
            draw.ellipse([w - 135, y0 + 28, w - 95, y0 + 68], fill=(16, 185, 129))
            draw.text((w - 125, y0 + 36), "OK", fill=(255, 255, 255), font=ImageFont.load_default(size=18))

    elif scene_idx == 2:
        # Rising Revenue Growth Chart
        vals = ["Rs 9,500", "Rs 28,000", "Rs 65,000", "Rs 1,20,000+"]
        draw.rounded_rectangle([210, 120, 510, 195], radius=18, fill=(16, 185, 129))
        bb = draw.textbbox((0, 0), vals[step], font=f_big)
        draw.text(((w - (bb[2] - bb[0])) // 2, 134), vals[step], fill=(3, 12, 9), font=f_big)

        draw.rounded_rectangle([75, 225, w - 75, 560], radius=22, fill=(8, 22, 16), outline=(30, 80, 55), width=2)
        draw.text((105, 245), "Monthly Growth", fill=(148, 163, 184), font=f_sm)
        pts = [(115, 515), (245, 475), (385, 405), (505, 330), (605, 270)]
        show_pts = pts[:step + 2]
        for k in range(len(show_pts) - 1):
            draw.line([show_pts[k], show_pts[k + 1]], fill=(52, 211, 153), width=6)
        lx, ly = show_pts[-1]
        draw.ellipse([lx - 9, ly - 9, lx + 9, ly + 9], fill=(255, 255, 255), outline=(52, 211, 153), width=3)

    else:
        # Emergent-style Search Bar Ending
        draw.text((175, 195), "Start with aIValue8", fill=(248, 250, 252), font=f_big)
        bar_col = (16, 185, 129) if step % 2 == 0 else (20, 160, 110)
        draw.rounded_rectangle([95, 285, w - 95, 375], radius=45, fill=bar_col, outline=(167, 243, 208), width=3)
        draw.text((145, 313), "www.sarahics.in", fill=(255, 255, 255), font=f_big)
        draw.ellipse([w - 175, 303, w - 120, 358], fill=(3, 12, 9))
        draw.text((w - 160, 318), "GO", fill=(52, 211, 153), font=f_sm)

async def _tts_save(text: str, out_mp3: str):
    comm = edge_tts.Communicate(text, "hi-IN-MadhurNeural")
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

    scene_caps = [
        hook or "Main aapka business AI se automate kar sakta hoon.",
        sentences[0] if len(sentences) > 0 else "Website, App, CRM aur Leads sab kuch ek saath.",
        sentences[1] if len(sentences) > 1 else "Zero se smart automated revenue growth tak.",
        "Aaj hi sarahics.in par apna idea likhein!"
    ]

    f_sm = ImageFont.load_default(size=24)
    f_big = ImageFont.load_default(size=38)
    f_cap = ImageFont.load_default(size=42)
    w, h = 720, 1280

    png_paths = []
    fnum = 0
    for s_idx, cap in enumerate(scene_caps):
        for step in range(4):
            img = Image.new("RGB", (w, h), (3, 12, 9))
            draw = ImageDraw.Draw(img)
            _draw_bg_and_orb(draw, w, h, fnum)
            _draw_scene_ui(draw, w, s_idx, step, f_sm, f_big)
            _draw_highlighted_caption(draw, w, 650, cap, f_cap)
            p = os.path.join(MEDIA_DIR, f"{uid}_{fnum}.png")
            img.save(p, "PNG")
            png_paths.append(p)
            fnum += 1

    with open(slides_txt, "w") as f:
        for p in png_paths:
            f.write(f"file '{p}'\nduration 1.25\n")
        f.write(f"file '{png_paths[-1]}'\n")

    voice_text = f"{hook}. {' '.join(sentences[:3])}. Aaj hi sarahics dot in par click kijiye."
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
    captions = [hook or title, sentences[0] if sentences else "Smart AI App Demo", f"Visit {cta_url}"]

    png_paths = []
    f_sm = ImageFont.load_default(size=24)
    f_cap = ImageFont.load_default(size=38)
    w, h = 720, 1280
    for idx in range(max(len(image_paths), len(captions))):
        src = image_paths[idx % len(image_paths)]
        cap = captions[idx % len(captions)].replace("•", "|")
        img = Image.new("RGB", (w, h), (3, 12, 9))
        draw = ImageDraw.Draw(img)
        _draw_bg_and_orb(draw, w, h, idx * 3)
        draw.text((55, 52), "aIValue8 LIVE APP DEMO", fill=(52, 211, 153), font=f_sm)
        draw.rounded_rectangle([85, 100, w - 85, 720], radius=24, fill=(8, 22, 16), outline=(52, 211, 153), width=3)
        shot = Image.open(src).convert("RGB")
        shot.thumbnail((520, 590))
        img.paste(shot, ((w - shot.width) // 2, 115 + (590 - shot.height) // 2))
        _draw_highlighted_caption(draw, w, 745, cap, f_cap)
        out_p = os.path.join(MEDIA_DIR, f"{uid}_{idx}.png")
        img.save(out_p, "PNG")
        png_paths.append(out_p)

    with open(slides_txt, "w") as f:
        for p in png_paths:
            f.write(f"file '{p}'\nduration 5\n")
        f.write(f"file '{png_paths[-1]}'\n")

    joined = " ".join(sentences[:2])
    voice_text = f"{hook}. {joined}. Aaj hi sarahics dot in par visit karein."
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
