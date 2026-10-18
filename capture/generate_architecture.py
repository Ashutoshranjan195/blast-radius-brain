"""
Generates 10_architecture.png (1920x1080) representing the Aurora Labs graph schema.
Shows all 5 node labels and all 9 relationship types with clear directed arrows and badges.
"""

import os
import math
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_PATH = os.path.join(BASE_DIR, "capture", "screenshots", "10_architecture.png")


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


def draw_arrow(draw, start, end, color="#64748B", width=3, arrow_size=12):
    x1, y1 = start
    x2, y2 = end
    draw.line([start, end], fill=color, width=width)
    
    # Calculate arrowhead angle
    angle = math.atan2(y2 - y1, x2 - x1)
    angle1 = angle + math.pi * 5 / 6
    angle2 = angle - math.pi * 5 / 6
    
    ax1 = x2 + arrow_size * math.cos(angle1)
    ay1 = y2 + arrow_size * math.sin(angle1)
    ax2 = x2 + arrow_size * math.cos(angle2)
    ay2 = y2 + arrow_size * math.sin(angle2)
    
    draw.polygon([(x2, y2), (ax1, ay1), (ax2, ay2)], fill=color)


def draw_badge(draw, center, text, bg_color="#1E293B", text_color="#38BDF8", font=None):
    if font is None:
        font = get_font(14, bold=True)
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    pad_x, pad_y = 10, 5
    
    x, y = center
    rect = [x - tw//2 - pad_x, y - th//2 - pad_y, x + tw//2 + pad_x, y + th//2 + pad_y]
    draw.rounded_rectangle(rect, radius=8, fill=bg_color, outline="#475569", width=1)
    draw.text((x, y), text, fill=text_color, font=font, anchor="mm")


def generate():
    W, H = 1920, 1080
    img = Image.new("RGB", (W, H), color="#090D16")
    draw = ImageDraw.Draw(img)

    # Subtle Background Dot Grid
    for x in range(40, W, 40):
        for y in range(40, H, 40):
            draw.point((x, y), fill="#141C2E")

    # Header
    font_title = get_font(34, bold=True)
    font_sub = get_font(18)
    draw.text((100, 60), "BLAST RADIUS BRAIN — DATA MODEL ARCHITECTURE", fill="#F8FAFC", font=font_title)
    draw.text((100, 105), "5 Node Labels • 9 Directed Traversal Relationships • Aurora Labs Knowledge Graph", fill="#94A3B8", font=font_sub)

    # Node Coordinates (Centers & Boxes)
    nodes = {
        "Person": {
            "center": (350, 480),
            "size": (240, 140),
            "color": "#818CF8",
            "bg": "#1E1B4B",
            "border": "#6366F1",
            "subtitle": "name, role, team",
            "count": "14 Entities"
        },
        "Project": {
            "center": (850, 260),
            "size": (240, 130),
            "color": "#38BDF8",
            "bg": "#0C4A6E",
            "border": "#0284C7",
            "subtitle": "name, status, owner",
            "count": "8 Entities"
        },
        "Decision": {
            "center": (850, 720),
            "size": (250, 140),
            "color": "#F472B6",
            "bg": "#831843",
            "border": "#DB2777",
            "subtitle": "title, date, status, summary",
            "count": "5 Entities"
        },
        "Doc": {
            "center": (850, 480),
            "size": (240, 130),
            "color": "#34D399",
            "bg": "#064E3B",
            "border": "#059669",
            "subtitle": "title, kind, author, summary",
            "count": "5 Entities"
        },
        "System": {
            "center": (1380, 480),
            "size": (260, 160),
            "color": "#FBBF24",
            "bg": "#78350F",
            "border": "#D97706",
            "subtitle": "name, kind, criticality",
            "count": "10 Entities"
        }
    }

    # Relationship Edges (9 Relationships)
    # 1. Person -> Project (WORKS_ON)
    draw_arrow(draw, (450, 420), (730, 290), color="#818CF8", width=3)
    draw_badge(draw, (580, 335), "1. [:WORKS_ON] (28)", bg_color="#1E293B", text_color="#A5B4FC")

    # 2. Person -> Project (LEADS)
    draw_arrow(draw, (430, 400), (740, 250), color="#C084FC", width=3)
    draw_badge(draw, (550, 275), "2. [:LEADS] (8)", bg_color="#1E293B", text_color="#E9D5FF")

    # 3. Person -> Doc (AUTHORED)
    draw_arrow(draw, (470, 480), (730, 480), color="#34D399", width=3)
    draw_badge(draw, (600, 480), "3. [:AUTHORED] (5)", bg_color="#1E293B", text_color="#6EE7B7")

    # 4. Person -> Decision (DECIDED)
    draw_arrow(draw, (450, 540), (730, 680), color="#F472B6", width=3)
    draw_badge(draw, (580, 625), "4. [:DECIDED] (5)", bg_color="#1E293B", text_color="#FBCFE8")

    # 5. Project -> System (USES)
    draw_arrow(draw, (970, 280), (1270, 430), color="#38BDF8", width=3)
    draw_badge(draw, (1130, 340), "5. [:USES] (13)", bg_color="#1E293B", text_color="#BAE6FD")

    # 6. System -> System (DEPENDS_ON recursive)
    # Curved loop above System
    draw.arc([1330, 310, 1430, 410], start=180, end=360, fill="#FBBF24", width=3)
    draw_arrow(draw, (1430, 360), (1430, 400), color="#FBBF24", width=3)
    draw_badge(draw, (1380, 295), "6. [:DEPENDS_ON*1..5] (11)", bg_color="#1E293B", text_color="#FDE68A")

    # 7. Decision -> Project (DECIDED_IN)
    draw_arrow(draw, (850, 650), (850, 330), color="#F472B6", width=3)
    draw_badge(draw, (850, 385), "7. [:DECIDED_IN] (5)", bg_color="#1E293B", text_color="#FBCFE8")

    # 8. Decision -> System (ABOUT)
    draw_arrow(draw, (980, 710), (1270, 540), color="#F472B6", width=3)
    draw_badge(draw, (1130, 640), "8. [:ABOUT] (5)", bg_color="#1E293B", text_color="#FBCFE8")

    # 9. Doc -> System (ABOUT)
    draw_arrow(draw, (970, 480), (1250, 480), color="#34D399", width=3)
    draw_badge(draw, (1110, 480), "9. [:ABOUT] (5)", bg_color="#1E293B", text_color="#A7F3D0")

    # Draw Nodes on top of arrows
    font_node_title = get_font(24, bold=True)
    font_node_sub = get_font(14)
    font_node_cnt = get_font(13, bold=True)

    for name, data in nodes.items():
        cx, cy = data["center"]
        w, h = data["size"]
        x1, y1 = cx - w//2, cy - h//2
        x2, y2 = cx + w//2, cy + h//2

        # Outer Glow Box
        draw.rounded_rectangle([x1-4, y1-4, x2+4, y2+4], radius=16, fill=data["bg"], outline=data["border"], width=3)
        # Inner Box
        draw.rounded_rectangle([x1, y1, x2, y2], radius=12, fill="#131B2E")

        # Top Node Badge
        draw.text((cx, y1 + 30), name.upper(), fill=data["color"], font=font_node_title, anchor="mm")
        draw.text((cx, y1 + 65), data["subtitle"], fill="#94A3B8", font=font_node_sub, anchor="mm")
        
        # Count pill
        draw.rounded_rectangle([cx - 55, y2 - 35, cx + 55, y2 - 13], radius=6, fill=data["bg"], outline=data["border"], width=1)
        draw.text((cx, y2 - 24), data["count"], fill="#F8FAFC", font=font_node_cnt, anchor="mm")

    # Bottom Information Card
    card_rect = [100, 930, 1820, 1030]
    draw.rounded_rectangle(card_rect, radius=12, fill="#0F172A", outline="#334155", width=2)
    font_card_h = get_font(16, bold=True)
    font_card_b = get_font(14)
    
    draw.text((130, 955), "GRAPHBLAS TRAVERSAL GUARANTEES:", fill="#38BDF8", font=font_card_h)
    draw.text((130, 985), "• Deterministic Multi-Hop Dependency Chains (sub-2ms)    • Ranked Project/Team Graph Joins    • Audit-Proof Decision Provenance", fill="#CBD5E1", font=font_card_b)

    draw.text((1150, 955), "FALKORDB ENGINE METRICS:", fill="#FBBF24", font=font_card_h)
    draw.text((1150, 985), "• 42 Seed Nodes    • 85 Relationships    • 100% Idempotent MERGE    • 0 External Vector Embeddings", fill="#E2E8F0", font=font_card_b)

    img.save(OUT_PATH, "PNG")
    print(f"Generated 10_architecture.png at {OUT_PATH}")


if __name__ == "__main__":
    generate()
