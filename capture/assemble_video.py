"""
Video Assembly Pipeline for Blast Radius Brain Demo Video.
Builds all 9 scenes at 1080p 1920x1080 H.264 30fps with visual overlays,
concatenates them into demo_silent.mp4 (180s), and combines with voiceover.wav into demo.mp4.
"""

import os
import subprocess
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "capture", "screenshots")
SCENES_DIR = os.path.join(BASE_DIR, "capture", "scenes")
VIDEO_RAW_DIR = os.path.join(BASE_DIR, "capture", "video_raw")
VOICEOVER_WAV = os.path.join(BASE_DIR, "capture", "voiceover.wav")
CONCAT_TXT = os.path.join(BASE_DIR, "capture", "concat.txt")
SILENT_MP4 = os.path.join(BASE_DIR, "capture", "demo_silent.mp4")
FINAL_MP4 = os.path.join(BASE_DIR, "capture", "demo.mp4")
THUMBNAIL_PNG = os.path.join(BASE_DIR, "capture", "demo_thumbnail.png")

os.makedirs(SCENES_DIR, exist_ok=True)


def get_font(size, bold=False):
    try:
        if bold:
            return ImageFont.truetype("arialbd.ttf", size)
        return ImageFont.truetype("arial.ttf", size)
    except Exception:
        try:
            return ImageFont.truetype("consola.ttf", size)
        except Exception:
            return ImageFont.load_default()


def add_banner(img, text, pos="top", bg="#0F172ACC", border="#38BDF8", text_color="#F8FAFC"):
    W, H = img.size
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    font = get_font(24, bold=True)
    
    pad_y = 18
    banner_h = 70
    y1 = 30 if pos == "top" else (H - 30 - banner_h)
    y2 = y1 + banner_h
    
    # Rounded badge in center
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    bx1 = max(40, (W - tw) // 2 - 30)
    bx2 = min(W - 40, (W + tw) // 2 + 30)
    
    draw.rounded_rectangle([bx1, y1, bx2, y2], radius=12, fill=bg, outline=border, width=2)
    draw.text((W // 2, (y1 + y2) // 2), text, fill=text_color, font=font, anchor="mm")
    
    return Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")


def add_callout_box(img, rect, label, color="#FF6B6B"):
    W, H = img.size
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    x1, y1, x2, y2 = rect
    draw.rounded_rectangle([x1, y1, x2, y2], radius=10, outline=color, width=4)
    
    if label:
        font = get_font(18, bold=True)
        bbox = draw.textbbox((0, 0), label, font=font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        bx1 = x1
        by1 = max(10, y1 - th - 16)
        bx2 = x1 + tw + 20
        by2 = y1
        draw.rounded_rectangle([bx1, by1, bx2, by2], radius=6, fill=color)
        draw.text(((bx1 + bx2) // 2, (by1 + by2) // 2), label, fill="#0F172A", font=font, anchor="mm")
        
    return Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")


def render_scene_images():
    print("Preparing 9 enhanced scene source frames...")
    
    # Scene 1: Home (15s)
    s1 = Image.open(os.path.join(SCREENSHOTS_DIR, "01_home.png")).crop((0, 0, 1920, 1080))
    s1 = add_banner(s1, "Vector RAG gives you similar documents. It cannot tell you what breaks.", pos="top", border="#EF4444")
    s1.save(os.path.join(SCENES_DIR, "frame_01.png"))

    # Scene 2: Blast Radius Hero (35s) - Path Chips highlighted
    s2 = Image.open(os.path.join(SCREENSHOTS_DIR, "02_blast_radius.png")).crop((0, 0, 1920, 1080))
    # Highlight path chips & answer
    s2 = add_callout_box(s2, [360, 240, 1850, 430], "TRAVERSED PATH CHIPS (Variable-Length Graph Walk)", color="#FF8E53")
    s2 = add_banner(s2, "Deterministic Multi-Hop Traversal: payments-api (1 hop) -> checkout-ui (2 hops)", pos="top", border="#FF8E53")
    s2.save(os.path.join(SCENES_DIR, "frame_02.png"))

    # Scene 3: Cypher Proof (15s) - Zoomed / Focus on Cypher & params
    s3 = Image.open(os.path.join(SCREENSHOTS_DIR, "02_blast_radius.png"))
    # Crop around Cypher query section
    cypher_crop = s3.crop((360, 410, 1860, 960)).resize((1920, 1080), Image.Resampling.LANCZOS)
    s3_out = add_banner(cypher_crop, "The answer is a traversal — not a similarity search.", pos="bottom", border="#38BDF8")
    s3_out.save(os.path.join(SCENES_DIR, "frame_03.png"))

    # Scene 4: Expert Finder (20s) - Maya Chen Highlighted
    s4 = Image.open(os.path.join(SCREENSHOTS_DIR, "03_expert_finder.png")).crop((0, 0, 1920, 1080))
    s4 = add_callout_box(s4, [360, 220, 1850, 480], "RANKED DOMAIN EXPERT: Maya Chen (Helios, Atlas, Zephyr | Score: 3)", color="#818CF8")
    s4 = add_banner(s4, "Graph Join: (Person)-[:WORKS_ON]->(Project)-[:USES]->(System)", pos="top", border="#818CF8")
    s4.save(os.path.join(SCENES_DIR, "frame_04.png"))

    # Scene 5: Decision Provenance (20s) - Decision trace highlighted
    s5 = Image.open(os.path.join(SCREENSHOTS_DIR, "04_decision.png")).crop((0, 0, 1920, 1080))
    s5 = add_callout_box(s5, [360, 220, 1850, 450], "PROVENANCE AUDIT: Nora Haddad -> Pause Helios rollout -> ledger-service regression", color="#F472B6")
    s5 = add_banner(s5, "Auditable Governance: Decision -> Decided By -> Project -> System", pos="top", border="#F472B6")
    s5.save(os.path.join(SCENES_DIR, "frame_05.png"))

    # Scene 6: Honest Unknown (15s) - Project Phoenix
    s6 = Image.open(os.path.join(SCREENSHOTS_DIR, "05_honest_unknown.png")).crop((0, 0, 1920, 1080))
    s6 = add_callout_box(s6, [360, 220, 1850, 360], "HONEST EVIDENCE LAYER: Entity Not In Graph -> Rejects Guesswork", color="#10B981")
    s6 = add_banner(s6, "When the graph doesn't have it, the agent says so. Zero hallucination.", pos="bottom", border="#10B981")
    s6.save(os.path.join(SCENES_DIR, "frame_06.png"))

    # Scene 7a & 7b: FalkorDB Browser (30s = 15s all nodes + 15s blast radius subgraph)
    s7a = Image.open(os.path.join(SCREENSHOTS_DIR, "06_graph_browser.png")).crop((0, 0, 1920, 1080))
    s7a = add_banner(s7a, "The graph is the reasoning layer. FalkorDB Browser at localhost:3000", pos="top", border="#FBBF24")
    s7a.save(os.path.join(SCENES_DIR, "frame_07a.png"))

    s7b = Image.open(os.path.join(SCREENSHOTS_DIR, "07_graph_ledger_highlight.png")).crop((0, 0, 1920, 1080))
    s7b = add_banner(s7b, "Live Cypher in FalkorDB: MATCH (s)<-[:DEPENDS_ON*1..5]-(downstream)", pos="top", border="#FBBF24")
    s7b.save(os.path.join(SCENES_DIR, "frame_07b.png"))

    # Scene 8: Engineering Credibility (20s) - Split screen seed + tests
    s8_left = Image.open(os.path.join(SCREENSHOTS_DIR, "08_seed_counts.png")).crop((0, 0, 1920, 1080)).resize((960, 1080), Image.Resampling.LANCZOS)
    s8_right = Image.open(os.path.join(SCREENSHOTS_DIR, "09_tests_passing.png")).crop((0, 0, 1920, 1080)).resize((960, 1080), Image.Resampling.LANCZOS)
    s8 = Image.new("RGB", (1920, 1080))
    s8.paste(s8_left, (0, 0))
    s8.paste(s8_right, (960, 0))
    s8 = add_banner(s8, "Idempotent Seed (42 Nodes / 85 Rels) • Deterministic Tools • All 6 Tests Passing", pos="bottom", border="#10B981")
    s8.save(os.path.join(SCENES_DIR, "frame_08.png"))

    # Scene 9: Architecture & Close (10s)
    s9 = Image.open(os.path.join(SCREENSHOTS_DIR, "10_architecture.png")).crop((0, 0, 1920, 1080))
    s9 = add_banner(s9, "Blast Radius Brain — Track 03: Company Brain | https://github.com/Ashutoshranjan195/blast-radius-brain", pos="bottom", border="#FF6B6B")
    s9.save(os.path.join(SCENES_DIR, "frame_09.png"))


def encode_scenes():
    # Durations in seconds: total = 15 + 35 + 15 + 20 + 20 + 15 + (15+15) + 20 + 10 = 180s
    scenes = [
        ("frame_01.png", 15, "01_home.mp4"),
        ("frame_02.png", 35, "02_blast.mp4"),
        ("frame_03.png", 15, "03_cypher.mp4"),
        ("frame_04.png", 20, "04_expert.mp4"),
        ("frame_05.png", 20, "05_decision.mp4"),
        ("frame_06.png", 15, "06_unknown.mp4"),
        ("frame_07a.png", 15, "07a_browser.mp4"),
        ("frame_07b.png", 15, "07b_browser.mp4"),
        ("frame_08.png", 20, "08_tests.mp4"),
        ("frame_09.png", 10, "09_close.mp4"),
    ]

    print("Encoding scene video clips with FFmpeg...")
    concat_lines = []
    for frame_name, duration, out_name in scenes:
        frame_path = os.path.join(SCENES_DIR, frame_name)
        out_path = os.path.join(SCENES_DIR, out_name)
        
        cmd = [
            "ffmpeg", "-y",
            "-loop", "1",
            "-i", frame_path,
            "-c:v", "libx264",
            "-t", str(duration),
            "-pix_fmt", "yuv420p",
            "-r", "30",
            out_path
        ]
        subprocess.run(cmd, check=True)
        # Use forward slashes for concat file
        clean_path = out_path.replace("\\", "/")
        concat_lines.append(f"file '{clean_path}'")

    with open(CONCAT_TXT, "w", encoding="utf-8") as f:
        f.write("\n".join(concat_lines))


def concatenate_and_merge():
    print("Concatenating scenes into demo_silent.mp4...")
    cmd_concat = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", CONCAT_TXT,
        "-c", "copy",
        SILENT_MP4
    ]
    subprocess.run(cmd_concat, check=True)

    print("Merging video with master voiceover into demo.mp4...")
    cmd_merge = [
        "ffmpeg", "-y",
        "-i", SILENT_MP4,
        "-i", VOICEOVER_WAV,
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        FINAL_MP4
    ]
    subprocess.run(cmd_merge, check=True)

    print("Generating demo_thumbnail.png at 00:00:30 (showing path chips)...")
    cmd_thumb = [
        "ffmpeg", "-y",
        "-ss", "00:00:30",
        "-i", FINAL_MP4,
        "-frames:v", "1",
        THUMBNAIL_PNG
    ]
    subprocess.run(cmd_thumb, check=True)
    print(f"Final video generated: {FINAL_MP4}")


if __name__ == "__main__":
    render_scene_images()
    encode_scenes()
    concatenate_and_merge()
