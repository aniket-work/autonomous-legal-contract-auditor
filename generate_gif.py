from PIL import Image, ImageDraw, ImageFont
import os
import random

# Configuration
WIDTH = 800
HEIGHT = 550
BG_COLOR = (10, 25, 47) # Dark Blue/Grey for Legal Tech feel
TEXT_COLOR = (100, 255, 218) # Cyan/Teal
FONT_SIZE = 15
try:
    FONT = ImageFont.truetype("/System/Library/Fonts/Monaco.ttf", FONT_SIZE)
except:
    FONT = ImageFont.load_default()

OUTPUT_GIF = "images/title-animation.gif"

def create_base_image():
    return Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)

def draw_text(draw, text, position, color=TEXT_COLOR):
    draw.text(position, text, font=FONT, fill=color)

def create_terminal_frames():
    frames = []
    lines = [
        "$ python main.py",
        "",
        "=== Autonomous Legal Contract Auditor (v1.2.0) ===",
        "",
        "➜ Ingesting document: 'Vendor_Service_Agreement_v4.pdf'...",
        "    [PDFParser] Extracted 3 clauses for review.",
        "",
        "➜ Auditing Clause CL-01 (Indemnification)...",
        '    [Text] "The Vendor shall indemnify, verify, and hold harmless..."',
        "    [RiskEngine] Match found: RISK-001 (Confidence: 0.94)",
        "    [Auditor] Comparing clause to RISK-001...",
        "    [Result] Risk: LOW | Score: 10",
        "",
        "➜ Auditing Clause CL-05 (Governing Law)...",
        '    [Text] "This Agreement shall be governed by... California."',
        "    [RiskEngine] Match found: RISK-002 (Confidence: 0.91)",
        "    [Auditor] Comparing clause to RISK-002...",
        "    [Result] Risk: MEDIUM | Score: 60",
        "",
        "➜ Auditing Clause CL-09 (Payment Terms)...",
        '    [Text] "Invoices are payable immediately upon receipt."',
        "    [RiskEngine] Match found: RISK-003 (Confidence: 0.88)",
        "    [Auditor] Comparing clause to RISK-003...",
        "    [Result] Risk: CRITICAL | Score: 95",
        "",
        "=================================================================",
        "LEGAL RISK ASSESSMENT REPORT",
        "=================================================================",
        "Document       : Vendor_Service_Agreement_v4.pdf",
        "Risk Score     : 55/100",
        "Clauses Flagged: 2",
        "-----------------------------------------------------------------",
        "CRITICAL FINDINGS:",
        "  [x] Clause CL-09: Immediate payment terms rejected. (Risk: 95)",
        "  [x] Clause CL-05: Non-standard jurisdiction. (Risk: 60)",
        "================================================================="
    ]

    current_lines = []
    
    # Typing command
    cmd = lines[0]
    for i in range(len(cmd) + 1):
        img = create_base_image()
        draw = ImageDraw.Draw(img)
        draw_text(draw, cmd[:i] + "█", (20, 20))
        frames.append(img.quantize(colors=256, method=2, dither=0))
    
    current_lines.append(cmd)
    
    # Process output
    y_start = 20 + FONT_SIZE + 5
    for line in lines[1:]:
        current_lines.append(line)
        img = create_base_image()
        draw = ImageDraw.Draw(img)
        
        y = 20
        for l in current_lines:
            if y > HEIGHT - 30: # Scroll if needed
                pass 
            
            # Simple color coding simulated by checking string content
            col = TEXT_COLOR
            if "CRITICAL" in l or "Risk: 95" in l: col = (255, 100, 100)
            elif "LOW" in l: col = (100, 255, 100)
            elif "MEDIUM" in l: col = (255, 200, 100)
            
            draw_text(draw, l, (20, y), col)
            y += FONT_SIZE + 5
            
        frames.append(img.quantize(colors=256, method=2, dither=0))
        
        if "➜" in line or "Result" in line:
             for _ in range(6): frames.append(frames[-1])

    return frames

def create_stats_chart():
    img = Image.new("RGB", (WIDTH, HEIGHT), (240, 240, 255))
    draw = ImageDraw.Draw(img)
    
    try:
        title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 30)
    except:
        title_font = ImageFont.load_default()
        
    draw.text((50, 30), "Audit Efficiency: AI vs Manual", fill=(0,0,50), font=title_font)
    
    # Bars
    # Manual
    draw.rectangle([100, 100, 300, 450], fill=(200, 200, 200))
    draw.text((120, 460), "Manual (45m)", fill=(0,0,0), font=FONT)
    
    # AI
    draw.rectangle([400, 350, 600, 450], fill=(50, 100, 200)) # Much shorter bar = faster
    draw.text((420, 460), "AI Agent (12s)", fill=(0,0,0), font=FONT)
    
    return img.quantize(colors=256, method=2, dither=0)

def main():
    if not os.path.exists("images"):
        os.makedirs("images")
        
    print("Generating Terminal Frames...")
    frames = create_terminal_frames()
    
    print("Generating Stats Chart...")
    stats_frame = create_stats_chart()
    
    for _ in range(40):
        frames.append(stats_frame)
        
    print(f"Saving GIF to {OUTPUT_GIF}...")
    frames[0].save(
        OUTPUT_GIF,
        save_all=True,
        append_images=frames[1:],
        optimize=False,
        duration=40,
        loop=0
    )
    print("Done!")

if __name__ == "__main__":
    main()
