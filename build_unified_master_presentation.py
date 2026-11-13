"""
Build Unified Cryosphere AI Master Presentation (3-Chapter Combined Defense)
=============================================================================
Combines the work of all 3 team members into one cohesive, academic-grade slide deck:
  - Chapter 1: Multi-Season Glacier Mapping & Spatial Segmentation (Lead: Member 1)
  - Chapter 2: PermaWatch: Satellite Permafrost Detection & Spatial-Block ML (Lead: Member 2)
  - Chapter 3: Glacial Lake Expansion & Multi-Sensor GLOF Hazard Early-Warning (Lead: Member 3 / Core Focus)

Output: Unified_Cryosphere_AI_Master_Presentation.pptx
"""

import os
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def build_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Shared Palette
    DARK_BG = RGBColor(15, 23, 42)        # Slate 900
    LIGHT_BG = RGBColor(248, 250, 252)    # Slate 50
    CARD_BG = RGBColor(255, 255, 255)     # Pure White
    CARD_BORDER = RGBColor(226, 232, 240) # Slate 200
    TEXT_MAIN = RGBColor(15, 23, 42)      # Slate 900
    TEXT_MUTED = RGBColor(71, 85, 105)    # Slate 600
    TEXT_LIGHT = RGBColor(148, 163, 184)  # Slate 400
    HEADER_ACCENT = RGBColor(30, 41, 59)  # Slate 800

    # Chapter Theme Accents
    CH1_COLOR = RGBColor(14, 116, 144)    # Cyan 700 (Glacier Mapping)
    CH2_COLOR = RGBColor(124, 58, 237)    # Purple 600 (Permafrost)
    CH3_COLOR = RGBColor(16, 185, 129)    # Emerald 500 / Crimson (GLOF)
    ALERT_RED = RGBColor(225, 29, 72)     # Rose 600
    GOLD_ACCENT = RGBColor(217, 119, 6)   # Amber 600

    def set_slide_background(slide, color):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = color
        bg.line.fill.background()
        return bg

    def add_card(slide, left, top, width, height, bg_color=CARD_BG, border_color=CARD_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        if border_color:
            card.line.color.rgb = border_color
            card.line.width = Pt(1.2)
        else:
            card.line.fill.background()
        return card

    def add_header(slide, title_text, category_text, chapter_badge="UNIFIED CRYOSPHERE FRAMEWORK", accent_color=CH3_COLOR):
        # Top Category & Badge
        tb_cat = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(8.5), Inches(0.35))
        tf_cat = tb_cat.text_frame; tf_cat.word_wrap = True; tf_cat.margin_left = tf_cat.margin_right = tf_cat.margin_top = tf_cat.margin_bottom = 0
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(9.5); p_cat.font.bold = True; p_cat.font.color.rgb = accent_color

        # Chapter Badge on Right
        badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(9.8), Inches(0.38), Inches(2.7), Inches(0.32))
        badge.fill.solid(); badge.fill.fore_color.rgb = accent_color; badge.line.fill.background()
        tb_b = slide.shapes.add_textbox(Inches(9.8), Inches(0.38), Inches(2.7), Inches(0.32))
        tf_b = tb_b.text_frame; tf_b.margin_left = tf_b.margin_right = tf_b.margin_top = tf_b.margin_bottom = 0
        p_b = tf_b.paragraphs[0]; p_b.alignment = PP_ALIGN.CENTER; p_b.text = chapter_badge
        p_b.font.size = Pt(8.5); p_b.font.bold = True; p_b.font.color.rgb = RGBColor(255, 255, 255)

        # Title Text
        tb_title = slide.shapes.add_textbox(Inches(0.8), Inches(0.72), Inches(11.7), Inches(0.65))
        tf_title = tb_title.text_frame; tf_title.word_wrap = True; tf_title.margin_left = tf_title.margin_right = tf_title.margin_top = tf_title.margin_bottom = 0
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.size = Pt(17.5); p_title.font.bold = True; p_title.font.color.rgb = HEADER_ACCENT

        # Dividing Line
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.38), Inches(11.7), Inches(0.02))
        line.fill.solid(); line.fill.fore_color.rgb = CARD_BORDER; line.line.fill.background()

    def add_chapter_divider(slide, ch_num, ch_title, ch_subtitle, lead_text, ch_color, bullets):
        set_slide_background(slide, DARK_BG)
        
        # Giant Chapter Number Watermark
        tb_num = slide.shapes.add_textbox(Inches(0.8), Inches(0.8), Inches(3.0), Inches(2.0))
        tf_num = tb_num.text_frame
        p_num = tf_num.paragraphs[0]; p_num.text = f"0{ch_num}"
        p_num.font.size = Pt(110); p_num.font.bold = True; p_num.font.color.rgb = RGBColor(30, 41, 59)

        # Chapter Category Pill
        pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(3.5), Inches(0.38))
        pill.fill.solid(); pill.fill.fore_color.rgb = ch_color; pill.line.fill.background()
        tb_p = slide.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(3.5), Inches(0.38))
        tf_p = tb_p.text_frame; tf_p.margin_left = tf_p.margin_right = tf_p.margin_top = tf_p.margin_bottom = 0
        p_p = tf_p.paragraphs[0]; p_p.alignment = PP_ALIGN.CENTER; p_p.text = f"CHAPTER {ch_num} OF 3"
        p_p.font.size = Pt(10); p_p.font.bold = True; p_p.font.color.rgb = RGBColor(255, 255, 255)

        # Title & Subtitle
        tb_t = slide.shapes.add_textbox(Inches(0.8), Inches(2.3), Inches(11.7), Inches(1.5))
        tf_t = tb_t.text_frame; tf_t.word_wrap = True
        p_t = tf_t.paragraphs[0]; p_t.text = ch_title; p_t.font.size = Pt(28); p_t.font.bold = True; p_t.font.color.rgb = RGBColor(255, 255, 255)
        p_sub = tf_t.add_paragraph(); p_sub.text = ch_subtitle; p_sub.font.size = Pt(14); p_sub.font.color.rgb = TEXT_LIGHT

        # Lead Presenter Card
        add_card(slide, 0.8, 4.0, 11.7, 2.7, bg_color=RGBColor(30, 41, 59), border_color=ch_color)
        tb_l = slide.shapes.add_textbox(Inches(1.1), Inches(4.2), Inches(11.1), Inches(2.3))
        tf_l = tb_l.text_frame; tf_l.word_wrap = True
        p_l = tf_l.paragraphs[0]; p_l.text = f"RESEARCH TRACK LEAD: {lead_text.upper()}"; p_l.font.size = Pt(12); p_l.font.bold = True; p_l.font.color.rgb = ch_color

        for b_title, b_desc in bullets:
            p = tf_l.add_paragraph()
            r1 = p.add_run(); r1.text = "• " + b_title; r1.font.bold = True; r1.font.size = Pt(11); r1.font.color.rgb = RGBColor(241, 245, 249)
            r2 = p.add_run(); r2.text = b_desc; r2.font.size = Pt(10.5); r2.font.color.rgb = TEXT_LIGHT

    # =========================================================================
    # SLIDE 1: Master Title Slide (Unified 3-Chapter Team Presentation)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1, DARK_BG)

    # Accent Stripe
    acc_top = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.7), Inches(11.7), Inches(0.08))
    acc_top.fill.solid(); acc_top.fill.fore_color.rgb = CH3_COLOR; acc_top.line.fill.background()

    tb1 = s1.shapes.add_textbox(Inches(0.8), Inches(0.95), Inches(11.7), Inches(2.4))
    tf1 = tb1.text_frame; tf1.word_wrap = True
    p1 = tf1.paragraphs[0]
    p1.text = "Himalayan & Arctic Cryosphere Intelligence"
    p1.font.size = Pt(30); p1.font.bold = True; p1.font.color.rgb = RGBColor(255, 255, 255)

    p1_sub = tf1.add_paragraph()
    p1_sub.text = "A Unified Remote Sensing & Machine Learning Framework for Multi-Season Glacier Mapping, Permafrost Degradation, and GLOF Early-Warning"
    p1_sub.font.size = Pt(14); p1_sub.font.color.rgb = TEXT_LIGHT

    p1_meta = tf1.add_paragraph()
    p1_meta.text = "Minor Project Comprehensive Academic Defense | Applied ML, Remote Sensing & Earth Observation"
    p1_meta.font.size = Pt(11.5); p1_meta.font.bold = True; p1_meta.font.color.rgb = GOLD_ACCENT

    # 3 Chapter Pillars Cards
    pillars = [
        ("CHAPTER 1", "Multi-Season Glacier Mapping", CH1_COLOR, 0.8,
         "• Lead: Team Member 1\n• Sentinel-2 8-Channel Multispectral (10m)\n• U-Net vs. Attention U-Net vs. SUNet\n• 410 Paired Mountain Patches\n• 0.9668 Dice | 0.9357 IoU Top Score"),
        ("CHAPTER 2", "PermaWatch: Permafrost ML", CH2_COLOR, 4.88,
         "• Lead: Team Member 2\n• ESA CCI Permafrost v5.0 (29,294 Cells)\n• Zero-Leakage Spatial-Block Split\n• Random Forest vs XGBoost vs SVM\n• 79.94% Spatial Hold-Out Acc (0.8105 F1)"),
        ("CHAPTER 3", "GLOF Hazard Early-Warning", ALERT_RED, 8.96,
         "• Lead: Team Member 3 (Core Focus)\n• Sentinel-1 SAR + S2 + ERA5-Land\n• 40 High-Risk Lakes (2,160 Obs)\n• Multi-Task LSTM, TCN, DLinear, RF\n• 0.9855 R² | 100% Critical Alert Precision")
    ]
    for ch_tag, title, col, left_x, body in pillars:
        add_card(s1, left_x, 3.6, 3.55, 3.2, bg_color=RGBColor(30, 41, 59), border_color=col)
        # Top stripe on card
        strp = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left_x), Inches(3.6), Inches(3.55), Inches(0.12))
        strp.fill.solid(); strp.fill.fore_color.rgb = col; strp.line.fill.background()

        tb = s1.shapes.add_textbox(Inches(left_x + 0.2), Inches(3.8), Inches(3.15), Inches(2.9))
        tf = tb.text_frame; tf.word_wrap = True
        p_ch = tf.paragraphs[0]; p_ch.text = ch_tag; p_ch.font.size = Pt(10); p_ch.font.bold = True; p_ch.font.color.rgb = col
        p_t = tf.add_paragraph(); p_t.text = title; p_t.font.size = Pt(12.5); p_t.font.bold = True; p_t.font.color.rgb = RGBColor(255, 255, 255)
        p_b = tf.add_paragraph(); p_b.text = body; p_b.font.size = Pt(9.5); p_b.font.color.rgb = TEXT_LIGHT

    # =========================================================================
    # SLIDE 2: Unified Scientific Motivation & Global Cryosphere Crisis
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2, LIGHT_BG)
    add_header(s2, "The Global Cryosphere Crisis: From Arctic Thaw to Himalayan Outbursts", "UNIFIED SCIENTIFIC MOTIVATION", "GLOBAL PARADIGM", HEADER_ACCENT)

    add_card(s2, 0.8, 1.5, 5.7, 5.5)
    tb = s2.shapes.add_textbox(Inches(1.0), Inches(1.65), Inches(5.3), Inches(5.2))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "The High Mountain Asia Threat (The Third Pole)"; p.font.size = Pt(13); p.font.bold = True; p.font.color.rgb = ALERT_RED
    bullets_s2_left = [
        ("Doubled Glacier Melt: ", "Himalayan glacier mass loss has doubled since 2000, driven by anthropogenic temperature warming of +0.038°C/year."),
        ("Expanding Proglacial Basins: ", "As glacier tongues retreat into overdeepened mountain valleys, meltwater pools behind fragile, unconsolidated lateral and terminal moraines."),
        ("Catastrophic GLOF Disasters: ", "When moraine dams breach—triggered by ice-rock avalanches or cloudburst rain—they release tens of millions of m³ of water within minutes."),
        ("Recent Catastrophes: ", "• South Lhonak Lake (Sikkim, Oct 2023): Breached, destroyed Chungthang Hydroelectric Dam, 100+ fatalities.\n• Gya Lake (Ladakh, Aug 2014): Internal piping failure flooded downstream Leh-Manali villages."),
        ("Optical Monsoon Blindness: ", "Peak melt occurs during July–August, when heavy monsoon clouds render optical satellites completely blind. Cloud-penetrating radar is essential.")
    ]
    for b_title, b_desc in bullets_s2_left:
        p = tf.add_paragraph()
        r1 = p.add_run(); r1.text = "• " + b_title; r1.font.bold = True; r1.font.size = Pt(9.5); r1.font.color.rgb = TEXT_MAIN
        r2 = p.add_run(); r2.text = b_desc; r2.font.size = Pt(9.5); r2.font.color.rgb = TEXT_MUTED

    add_card(s2, 6.8, 1.5, 5.7, 5.5)
    tb_r = s2.shapes.add_textbox(Inches(7.0), Inches(1.65), Inches(5.3), Inches(5.2))
    tf_r = tb_r.text_frame; tf_r.word_wrap = True
    p = tf_r.paragraphs[0]; p.text = "The Circum-Arctic Permafrost Emergency"; p.font.size = Pt(13); p.font.bold = True; p.font.color.rgb = CH2_COLOR
    bullets_s2_right = [
        ("Circum-Arctic Scope: ", "Permafrost underlies ~24% of the Northern Hemisphere land area, sequestering 1,400–1,600 Gt of organic carbon (twice current atmospheric carbon)."),
        ("Polar Amplification: ", "The Arctic warms 3 to 4 times faster than the global average, driving active-layer deepening and widespread thermokarst subsidence."),
        ("Infrastructure Vulnerability: ", "Thaw settlement destabilizes Arctic transit arteries (Dalton Highway), airports, indigenous villages, and the Trans-Alaska Pipeline System (TAPS)."),
        ("Ground Monitoring Bottleneck: ", "Physical borehole thermistors cost millions to drill and maintain, leaving millions of roadless Arctic square kilometers unmonitored."),
        ("Our Team's Three-Pillar Solution: ", "We unify multi-season optical glacier segmentation (Ch. 1), spatial-block permafrost machine learning (Ch. 2), and multi-sensor radar-optical GLOF early warning (Ch. 3).")
    ]
    for b_title, b_desc in bullets_s2_right:
        p = tf_r.add_paragraph()
        r1 = p.add_run(); r1.text = "• " + b_title; r1.font.bold = True; r1.font.size = Pt(9.5); r1.font.color.rgb = TEXT_MAIN
        r2 = p.add_run(); r2.text = b_desc; r2.font.size = Pt(9.5); r2.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 3: Chapter 1 Divider (Glacier Mapping)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_chapter_divider(s3, 1,
                        "Multi-Season Glacier Mapping & Spatial Segmentation",
                        "High-Resolution Delineation of Clean Ice and Debris-Covered Glaciers across Himalayan Seasons",
                        "Team Member 1",
                        CH1_COLOR,
                        [
                            ("Objective: ", "Automated semantic segmentation of complex mountain glaciers across varying seasons using Sentinel-2 multispectral imagery."),
                            ("Key Models: ", "Convolutional Baseline U-Net vs. Attention-Gated U-Net vs. Shifted-Window Vision Transformer (SUNet / Swin-UNet)."),
                            ("Data & Evaluation: ", "410 paired Sentinel-2 patches, Randolph Glacier Inventory (RGI 6.0/7.0 Region 14), Hybrid BCE + Soft Dice Loss."),
                            ("Core Breakthrough: ", "Attention U-Net achieved 0.9668 Dice | 0.9357 IoU, filtering out steep mountain shadows and moraine confusion.")
                        ])

    # =========================================================================
    # SLIDE 4: Chapter 1 — Problem & Multispectral Data Ingestion
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4, LIGHT_BG)
    add_header(s4, "Multispectral Input Space: 8-Channel Sentinel-2 Tensor & Ground Truth", "CHAPTER 1: DATA INGESTION", "CHAPTER 1", CH1_COLOR)

    add_card(s4, 0.8, 1.5, 5.7, 5.5)
    tb = s4.shapes.add_textbox(Inches(1.0), Inches(1.65), Inches(5.3), Inches(5.2))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "8-Channel Multispectral Tensor Formulation"; p.font.size = Pt(13); p.font.bold = True; p.font.color.rgb = CH1_COLOR
    bullets_s4_left = [
        ("Input Dimensions: ", "Each satellite patch is formatted as an (8, 256, 256) multispectral tensor at 10m–20m native spatial resolution:"),
        ("Channels 0–5 (Optical & SWIR): ", "• Band 2 (Blue, 490 nm) | Band 3 (Green, 560 nm)\n• Band 4 (Red, 665 nm) | Band 8 (NIR, 842 nm)\n• Band 11 (SWIR-1, 1610 nm) | Band 12 (SWIR-2, 2190 nm)"),
        ("Channel 6 (NDSI): ", "Normalized Difference Snow Index = (B3 - B11) / (B3 + B11). Separates snow/ice from mountain clouds based on high SWIR absorption."),
        ("Channel 7 (NDVI): ", "Normalized Difference Vegetation Index = (B8 - B4) / (B8 + B4). Distinguishes vegetated valley bottoms from supraglacial moraines."),
        ("Ground Truth Rasterization: ", "Vector outlines from Randolph Glacier Inventory (RGI 7.0/6.0 Region 14: South Asia West) rasterized to binary masks (1 = Glacier, 0 = Non-glacier).")
    ]
    for b_title, b_desc in bullets_s4_left:
        p = tf.add_paragraph()
        r1 = p.add_run(); r1.text = "• " + b_title; r1.font.bold = True; r1.font.size = Pt(9.5); r1.font.color.rgb = TEXT_MAIN
        r2 = p.add_run(); r2.text = b_desc; r2.font.size = Pt(9.5); r2.font.color.rgb = TEXT_MUTED

    add_card(s4, 6.8, 1.5, 5.7, 5.5)
    tb_r = s4.shapes.add_textbox(Inches(7.0), Inches(1.65), Inches(5.3), Inches(5.2))
    tf_r = tb_r.text_frame; tf_r.word_wrap = True
    p = tf_r.paragraphs[0]; p.text = "Multi-Season Challenges & Hybrid Loss Function"; p.font.size = Pt(13); p.font.bold = True; p.font.color.rgb = HEADER_ACCENT
    bullets_s4_right = [
        ("The Supraglacial Debris Challenge: ", "Debris-covered glacier tongues share identical spectral reflectance with surrounding valley rock, misleading standard pixel classifiers."),
        ("Steep Mountain Shadows: ", "High Himalayan relief casts severe shadows that mimic low-albedo debris ice, producing massive false-positive over-segmentation."),
        ("Severe Class Imbalance: ", "Glaciers occupy <25% of typical mountain scenes, causing standard Cross-Entropy loss to converge to degenerate all-background predictions."),
        ("Hybrid BCE + Soft Dice Loss: ", "L_total = 0.5 * L_BCE(Y_hat, Y) + 0.5 * (1 - (2|Y_hat ∩ Y| + ε) / (|Y_hat| + |Y| + ε)). Balances fine pixel boundaries with global spatial overlap."),
        ("Training Protocol: ", "410 paired patches, identical 25-epoch training schedule, AdamW optimizer, cosine learning rate scheduler with warmup on NVIDIA GPU.")
    ]
    for b_title, b_desc in bullets_s4_right:
        p = tf_r.add_paragraph()
        r1 = p.add_run(); r1.text = "• " + b_title; r1.font.bold = True; r1.font.size = Pt(9.5); r1.font.color.rgb = TEXT_MAIN
        r2 = p.add_run(); r2.text = b_desc; r2.font.size = Pt(9.5); r2.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 5: Chapter 1 — Model Architectures (U-Net, Attention U-Net, SUNet)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5, LIGHT_BG)
    add_header(s5, "Model Architectures: Convolutional Encoders vs. Vision Transformers", "CHAPTER 1: ARCHITECTURES", "CHAPTER 1", CH1_COLOR)

    arch_cards = [
        ("1. Standard U-Net (Baseline CNN)", CH1_COLOR, 0.8,
         "• Architecture: 4-stage convolutional encoder-decoder with symmetric skip connections.\n• Parameters: 31.04 Million\n• Mechanism: Plain skip connections concatenate encoder feature maps directly with decoder stages.\n• Strengths: Fast training, strong baseline for broad ice sheets.\n• Limitation: Passes mountain shadow noise through skip connections unfiltered, causing boundary bleeds."),
        ("2. Attention U-Net (Top Performer)", RGBColor(16, 185, 129), 4.88,
         "• Architecture: Gated Attention Blocks embedded on each skip connection level.\n• Parameters: 31.39 Million (+0.35M overhead)\n• Mechanism: Attention gates compute compatibility coefficients α_i between coarser gating signal g and encoder features x_l.\n• Strengths: Actively suppresses mountain shadows and non-glacier valley noise; sharpest terminus boundaries.\n• Paper: Oktay et al. (MIDL 2018)."),
        ("3. SUNet (Swin-UNet Transformer)", RGBColor(124, 58, 237), 8.96,
         "• Architecture: Pure Vision Transformer with Shifted Window Self-Attention (Swin).\n• Parameters: 47.58 Million\n• Mechanism: Hierarchical representation via shifted windows; cross-band multi-spectral self-attention.\n• Strengths: Strong global context; highest precision (fewer false positives).\n• Limitation: Lacks inductive spatial bias; requires heavy compute and data.")
    ]
    for title, col, left_x, body in arch_cards:
        add_card(s5, left_x, 1.6, 3.55, 5.4)
        strp = s5.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left_x), Inches(1.6), Inches(3.55), Inches(0.12))
        strp.fill.solid(); strp.fill.fore_color.rgb = col; strp.line.fill.background()

        tb = s5.shapes.add_textbox(Inches(left_x + 0.15), Inches(1.85), Inches(3.25), Inches(5.0))
        tf = tb.text_frame; tf.word_wrap = True
        p = tf.paragraphs[0]; p.text = title; p.font.size = Pt(12); p.font.bold = True; p.font.color.rgb = col
        p_b = tf.add_paragraph(); p_b.text = body; p_b.font.size = Pt(9.5); p_b.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 6: Chapter 1 — Benchmark Results (Table + Real Predictions Overlay Image)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6, LIGHT_BG)
    add_header(s6, "Benchmark Results on 410 Paired Sentinel-2 Mountain Patches", "CHAPTER 1: BENCHMARK RESULTS", "CHAPTER 1", CH1_COLOR)

    # Benchmark Table
    add_card(s6, 0.8, 1.5, 11.7, 2.0)
    tb_tab = s6.shapes.add_textbox(Inches(1.0), Inches(1.55), Inches(11.3), Inches(0.35))
    tf_tab = tb_tab.text_frame; tf_tab.margin_left = tf_tab.margin_top = 0
    p = tf_tab.paragraphs[0]; p.text = "Quantitative Evaluation across 410 Paired Sentinel-2 Patches (GPU Accelerated, 25 Epochs)"; p.font.size = Pt(11); p.font.bold = True; p.font.color.rgb = HEADER_ACCENT

    table_shape1 = s6.shapes.add_table(4, 6, Inches(1.0), Inches(1.9), Inches(11.3), Inches(1.4))
    t1 = table_shape1.table
    t1.columns[0].width = Inches(3.3)
    t1.columns[1].width = Inches(1.6)
    t1.columns[2].width = Inches(1.6)
    t1.columns[3].width = Inches(1.6)
    t1.columns[4].width = Inches(1.6)
    t1.columns[5].width = Inches(1.6)

    h1 = ["Model Architecture", "Parameters", "Dice Score", "IoU (Jaccard)", "Precision", "Recall"]
    d1 = [
        ["U-Net (Baseline CNN)", "31.04 M", "0.9653", "0.9329", "0.9550", "0.9758"],
        ["Attention U-Net ⭐", "31.39 M", "0.9668", "0.9357", "0.9527", "0.9813"],
        ["SUNet (Swin-UNet)", "47.58 M", "0.9642", "0.9308", "0.9579", "0.9705"]
    ]
    for c, h in enumerate(h1):
        cell = t1.cell(0, c); cell.fill.solid(); cell.fill.fore_color.rgb = RGBColor(238, 242, 255)
        p = cell.text_frame.paragraphs[0]; p.text = h; p.font.bold = True; p.font.size = Pt(9.5); p.font.color.rgb = CH1_COLOR
    for r, row in enumerate(d1):
        for c, val in enumerate(row):
            cell = t1.cell(r + 1, c); p = cell.text_frame.paragraphs[0]; p.text = val; p.font.size = Pt(9.5)
            if r == 1:
                cell.fill.solid(); cell.fill.fore_color.rgb = RGBColor(240, 253, 244)
                p.font.bold = True; p.font.color.rgb = RGBColor(16, 185, 129)
            else:
                p.font.color.rgb = TEXT_MAIN

    # Embed Real Image: comparative_predictions_overlay.png
    add_card(s6, 0.8, 3.7, 11.7, 3.4)
    pred_img = "midsem/comparative_results/comparative_predictions_overlay.png"
    if os.path.exists(pred_img):
        s6.shapes.add_picture(pred_img, Inches(1.0), Inches(3.8), Inches(11.3), Inches(3.1))
    else:
        tb_err = s6.shapes.add_textbox(Inches(1.0), Inches(4.5), Inches(11.3), Inches(1.5))
        p = tb_err.text_frame.paragraphs[0]; p.text = "Visual comparative predictions overlay (Attention U-Net vs U-Net vs Ground Truth)"; p.font.size = Pt(12)

    # =========================================================================
    # SLIDE 7: Chapter 1 — Comparative Analysis: What Happened & Why
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7, LIGHT_BG)
    add_header(s7, "Comparative Analysis: Spatial Inductive Bias & Glaciological Trade-Offs", "CHAPTER 1: GLACIOLOGICAL ANALYSIS", "CHAPTER 1", CH1_COLOR)

    analysis_boxes = [
        ("Attention Gates (Dynamic Spatial Filtering)", CH1_COLOR, 0.8,
         "• Mechanism: Computes spatial attention coefficients on skip connections, attenuating irrelevant feature activations.\n• Causal Impact: Successfully suppressed deep mountain shadow false-positives while boosting boundary continuity.\n• Glaciological Result: Attention U-Net ranked 1st in Dice (0.9668) and Recall (0.9813), resolving intricate glacier snouts."),
        ("Swin Self-Attention (Non-Local Context)", RGBColor(124, 58, 237), 4.88,
         "• Mechanism: Shifted-window self-attention aggregates long-range dependencies and spectral band cross-correlations.\n• Causal Impact: Produced the highest Precision (0.9579) by rejecting non-glacier terrain confusion across entire tiles.\n• Glaciological Result: Generates clean, conservative masks with fewer false alarms, but requires larger capacity."),
        ("Precision vs. Recall Trade-Off in Conservation", ALERT_RED, 8.96,
         "• Design Trade-Off: SUNet favors conservative masks (high precision); Attention U-Net favors sensitivity (high recall).\n• Glaciological Imperative: In climate monitoring and civil defense, high Recall is vital—missing a retreating glacier tongue or proglacial channel is far more costly than slight over-segmentation.\n• Attention U-Net is selected as the primary operational vision model.")
    ]
    for title, col, left_x, body in analysis_boxes:
        add_card(s7, left_x, 1.6, 3.55, 5.4)
        strp = s7.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left_x), Inches(1.6), Inches(3.55), Inches(0.12))
        strp.fill.solid(); strp.fill.fore_color.rgb = col; strp.line.fill.background()

        tb = s7.shapes.add_textbox(Inches(left_x + 0.15), Inches(1.85), Inches(3.25), Inches(5.0))
        tf = tb.text_frame; tf.word_wrap = True
        p = tf.paragraphs[0]; p.text = title; p.font.size = Pt(12); p.font.bold = True; p.font.color.rgb = col
        p_b = tf.add_paragraph(); p_b.text = body; p_b.font.size = Pt(9.5); p_b.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 8: Chapter 2 Divider (PermaWatch)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_chapter_divider(s8, 2,
                        "PermaWatch: Satellite Permafrost Detection & Spatial-Block ML",
                        "A Multi-Spectral Remote Sensing & Machine Learning Framework with Spatial-Block Cross-Validation",
                        "Team Member 2",
                        CH2_COLOR,
                        [
                            ("Objective: ", "Subsurface Arctic permafrost mapping and active-layer thaw detection across a 29,294-cell Alaska transect (64.5°N – 71.2°N)."),
                            ("Data Provenance: ", "ESA CCI Permafrost v5.0 (1 km NetCDF) ground truth, Copernicus Sentinel-2 L2A (10–20m), Copernicus DEM GLO-90."),
                            ("Key Innovation: ", "Zero-Leakage Spatial-Block Partitioning (GroupShuffleSplit on Brooks Mountain Range) defeating the '98% spatial autocorrelation trap'."),
                            ("Core Result: ", "Random Forest achieved 79.94% spatial hold-out accuracy (0.8105 F1-score), outperforming XGBoost and SVM.")
                        ])

    # =========================================================================
    # SLIDE 9: Chapter 2 — Problem & Bio-Geomorphological Proxies
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9, LIGHT_BG)
    add_header(s9, "The Subsurface Remote Sensing Challenge & Bio-Geomorphological Proxies", "CHAPTER 2: SCIENTIFIC PRINCIPLES", "CHAPTER 2", CH2_COLOR)

    add_card(s9, 0.8, 1.5, 5.7, 5.5)
    tb = s9.shapes.add_textbox(Inches(1.0), Inches(1.65), Inches(5.3), Inches(5.2))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "The Climate Emergency & Ground Monitoring Gap"; p.font.size = Pt(13); p.font.bold = True; p.font.color.rgb = CH2_COLOR
    bullets_s9_left = [
        ("Circum-Arctic Scope: ", "Permafrost underlies ~24% of Northern Hemisphere land area, sequestering 1,400–1,600 Gt of organic carbon (twice current atmospheric carbon)."),
        ("Rapid Active-Layer Deepening: ", "The Arctic is warming 3 to 4 times faster than the global mean, melting ice-rich ground and causing thermokarst collapse."),
        ("Critical Infrastructure at Risk: ", "Thaw settlement destabilizes Arctic transit arteries (Dalton Highway), airports, indigenous villages, and the Trans-Alaska Pipeline System (TAPS)."),
        ("The Ground Monitoring Bottleneck: ", "Physical ground borehole temperature sensors cost millions to drill and maintain, leaving millions of roadless Arctic square kilometers unmonitored."),
        ("The Optical Paradox: ", "Satellites cannot directly observe subsoil frozen ground 1–10m underground. Optical sensors capture only surface canopy and active-layer reflection.")
    ]
    for b_title, b_desc in bullets_s9_left:
        p = tf.add_paragraph()
        r1 = p.add_run(); r1.text = "• " + b_title; r1.font.bold = True; r1.font.size = Pt(9.5); r1.font.color.rgb = TEXT_MAIN
        r2 = p.add_run(); r2.text = b_desc; r2.font.size = Pt(9.5); r2.font.color.rgb = TEXT_MUTED

    add_card(s9, 6.8, 1.5, 5.7, 5.5)
    tb_r = s9.shapes.add_textbox(Inches(7.0), Inches(1.65), Inches(5.3), Inches(5.2))
    tf_r = tb_r.text_frame; tf_r.word_wrap = True
    p = tf_r.paragraphs[0]; p.text = "The Solution: Bio-Geomorphological Surface Proxies"; p.font.size = Pt(13); p.font.bold = True; p.font.color.rgb = HEADER_ACCENT
    bullets_s9_right = [
        ("Vegetation Root Barrier (NDVI): ", "Subsurface permafrost acts as a physical barrier restricting roots to <0.5m. Shallow tundra mosses/lichens (0.35–0.50 NDVI) dominate permafrost, whereas thawed talik zones permit deep-rooted boreal forests (0.70–0.85 NDVI)."),
        ("Meltwater Cryo-Barrier (NDWI & SWIR): ", "Permafrost is impermeable to summer meltwater, preventing downward drainage and causing saturated active-layer peats, thaw lakes, and ponded wetlands."),
        ("Topographic Refrigeration (DEM): ", "Atmospheric lapse rates (-6.5°C/1,000m) and shaded north-facing slopes preserve sub-zero thermal equilibrium even at lower latitudes."),
        ("Alpine Snowpack Persistence (NDSI): ", "Perennial alpine snowbeds and late-thawing cornices provide micro-climatic refrigeration to underlying substrate.")
    ]
    for b_title, b_desc in bullets_s9_right:
        p = tf_r.add_paragraph()
        r1 = p.add_run(); r1.text = "• " + b_title; r1.font.bold = True; r1.font.size = Pt(9.5); r1.font.color.rgb = TEXT_MAIN
        r2 = p.add_run(); r2.text = b_desc; r2.font.size = Pt(9.5); r2.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 10: Chapter 2 — Authentic Data Provenance & Processing Pipeline
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10, LIGHT_BG)
    add_header(s10, "Data Provenance: ESA CCI Permafrost v5.0, Sentinel-2 & DEM", "CHAPTER 2: DATA PROVENANCE", "CHAPTER 2", CH2_COLOR)

    prov_cards = [
        ("1. ESA CCI Permafrost v5.0 (Target)", CH2_COLOR, 0.8,
         "• Origin: European Space Agency (ESA) Climate Change Initiative / CEDA Archive.\n• Grid: 1 km gridded NetCDF-4, Polar Stereographic.\n• Target Variable: Permafrost Fraction (PFR, 0–100%).\n• Binary Classification: permafrost_class = 1 (PFR ≥ 50%), 0 (PFR < 50%).\n• Provenance: Driven by MODIS LST & ERA5 via CryoGrid 1D model."),
        ("2. Copernicus Sentinel-2 L2A (Features)", RGBColor(14, 116, 144), 4.88,
         "• Sensor: MultiSpectral Instrument (MSI) Level-2A BOA surface reflectance.\n• Composite: Peak summer August 2023 cloud-free mosaic.\n• 6 Spectral Bands: B02 (Blue), B03 (Green), B04 (Red), B08 (NIR), B11 (SWIR-1), B12 (SWIR-2).\n• Alignment: Decimated to 1 km grid aligned with ESA reference cells."),
        ("3. Copernicus DEM GLO-90 & Dataset", RGBColor(16, 185, 129), 8.96,
         "• Topography: Copernicus DEM (GLO-90 & GLO-30) radar derivative.\n• Extracted Features: Absolute elevation (z, meters) and numerical slope (degrees).\n• Scale: 29,294 real geographic grid cells across 5 latitudinal zones (64.5°N to 71.2°N).\n• Split: 22,294 training cells, 7,000 spatial hold-out cells.")
    ]
    for title, col, left_x, body in prov_cards:
        add_card(s10, left_x, 1.6, 3.55, 5.4)
        strp = s10.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left_x), Inches(1.6), Inches(3.55), Inches(0.12))
        strp.fill.solid(); strp.fill.fore_color.rgb = col; strp.line.fill.background()

        tb = s10.shapes.add_textbox(Inches(left_x + 0.15), Inches(1.85), Inches(3.25), Inches(5.0))
        tf = tb.text_frame; tf.word_wrap = True
        p = tf.paragraphs[0]; p.text = title; p.font.size = Pt(12); p.font.bold = True; p.font.color.rgb = col
        p_b = tf.add_paragraph(); p_b.text = body; p_b.font.size = Pt(9.5); p_b.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 11: Chapter 2 — Spatial-Block Cross-Validation Protocol
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11, LIGHT_BG)
    add_header(s11, "Methodological Rigor: Spatial-Block Partitioning vs. The 98% Fallacy", "CHAPTER 2: VALIDATION PROTOCOL", "CHAPTER 2", CH2_COLOR)

    add_card(s11, 0.8, 1.5, 5.7, 5.5)
    tb = s11.shapes.add_textbox(Inches(1.0), Inches(1.65), Inches(5.3), Inches(5.2))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "The '98% Accuracy' Illusion & Tobler's First Law"; p.font.size = Pt(13); p.font.bold = True; p.font.color.rgb = ALERT_RED
    bullets_s11_left = [
        ("Tobler's First Law of Geography: ", "'Everything is related to everything else, but near things are more related than distant things.'"),
        ("The Random Split Fallacy: ", "Standard random train_test_split (80/20) causes catastrophic spatial autocorrelation leakage: adjacent 1 km pixels share identical terrain, vegetation, and micro-climate."),
        ("Memorizing Neighbors: ", "A model evaluated on randomly shuffled pixels simply memorizes the geographic neighbors of test points, producing fake ~98% accuracy."),
        ("Real-World Failure: ", "When deployed across an unseen mountain range or adjacent Arctic watershed, a randomly split model collapses because it never learned true generalization."),
        ("Peer-Reviewed Imperative: ", "Recent remote sensing literature strictly invalidates random pixel splitting for geospatial climate informatics.")
    ]
    for b_title, b_desc in bullets_s11_left:
        p = tf.add_paragraph()
        r1 = p.add_run(); r1.text = "• " + b_title; r1.font.bold = True; r1.font.size = Pt(9.5); r1.font.color.rgb = TEXT_MAIN
        r2 = p.add_run(); r2.text = b_desc; r2.font.size = Pt(9.5); r2.font.color.rgb = TEXT_MUTED

    add_card(s11, 6.8, 1.5, 5.7, 5.5)
    tb_r = s11.shapes.add_textbox(Inches(7.0), Inches(1.65), Inches(5.3), Inches(5.2))
    tf_r = tb_r.text_frame; tf_r.word_wrap = True
    p = tf_r.paragraphs[0]; p.text = "The PermaWatch Solution: GroupShuffleSplit on Brooks Range"; p.font.size = Pt(13); p.font.bold = True; p.font.color.rgb = CH2_COLOR
    bullets_s11_right = [
        ("Spatial-Block Partitioning: ", "We divided the 29,294-cell Alaska transect into 5 discrete latitudinal geographic zones: North Slope, Arctic Foothills, Brooks Mountain Range, Yukon Basin, and Interior Alaska."),
        ("Zero-Leakage Hold-Out: ", "The entire high-relief Brooks Mountain Range (7,000 cells) was held out strictly as an unseen spatial test block."),
        ("Training Domain: ", "Models were trained strictly on the remaining 4 blocks (22,294 cells) without ever seeing a single pixel from the Brooks Range."),
        ("Scientific Honesty: ", "Our models achieve ~80% spatial generalization accuracy. While lower than 'fake 98%', this represents authentic real-world performance on unmapped terrain.")
    ]
    for b_title, b_desc in bullets_s11_right:
        p = tf_r.add_paragraph()
        r1 = p.add_run(); r1.text = "• " + b_title; r1.font.bold = True; r1.font.size = Pt(9.5); r1.font.color.rgb = TEXT_MAIN
        r2 = p.add_run(); r2.text = b_desc; r2.font.size = Pt(9.5); r2.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 12: Chapter 2 — Feature Engineering & Importance Ranking (WITH REAL IMAGE)
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12, LIGHT_BG)
    add_header(s12, "Feature Engineering: Mathematical Indices & Importance Ranking", "CHAPTER 2: FEATURE IMPORTANCE", "CHAPTER 2", CH2_COLOR)

    # Left: Mathematical Biophysics
    add_card(s12, 0.8, 1.5, 5.7, 5.5)
    tb = s12.shapes.add_textbox(Inches(1.0), Inches(1.65), Inches(5.3), Inches(5.2))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "Mathematical Biophysics of Predictors"; p.font.size = Pt(13); p.font.bold = True; p.font.color.rgb = CH2_COLOR
    bullets_s12_left = [
        ("NDVI (Vegetation Index): ", "NDVI = (NIR - Red) / (NIR + Red). Captures tundra root barriers (0.35–0.50) vs boreal forests (0.70–0.85)."),
        ("NDWI (Water Index): ", "NDWI = (Green - NIR) / (Green + NIR). Flags waterlogged active-layer peats, thaw lakes, and saturated permafrost soils."),
        ("NDSI (Snow Index): ", "NDSI = (Green - SWIR1) / (Green + SWIR1). Flags perennial alpine snowbeds maintaining ground refrigeration."),
        ("Slope & Elevation Gradient: ", "Derived from Copernicus DEM (GLO-90) to capture thermal lapse rates (-6.5°C/km) and solar shading."),
        ("Biophysical Hierarchy: ", "• Latitude (31%) and Elevation (18%) set macro-climate bounds.\n• Active-layer moisture (SWIR/NDWI) and tundra canopy (NDVI) dictate micro-site permafrost presence.")
    ]
    for b_title, b_desc in bullets_s12_left:
        p = tf.add_paragraph()
        r1 = p.add_run(); r1.text = "• " + b_title; r1.font.bold = True; r1.font.size = Pt(9.5); r1.font.color.rgb = TEXT_MAIN
        r2 = p.add_run(); r2.text = b_desc; r2.font.size = Pt(9.5); r2.font.color.rgb = TEXT_MUTED

    # Right: Embedded Real Image (slide_5_Picture 8.png)
    add_card(s12, 6.8, 1.5, 5.7, 5.5)
    feat_img = "extracted_permafrost_img/slide_5_Picture 8.png"
    if os.path.exists(feat_img):
        s12.shapes.add_picture(feat_img, Inches(7.0), Inches(1.7), Inches(5.3), Inches(5.1))
    else:
        tb_err = s12.shapes.add_textbox(Inches(7.0), Inches(3.0), Inches(5.3), Inches(2.0))
        p = tb_err.text_frame.paragraphs[0]; p.text = "Feature Importance Ranking (Gini & Gain)"; p.font.size = Pt(12)

    # =========================================================================
    # SLIDE 13: Chapter 2 — Results & Geospatial Predictions (WITH 2 REAL IMAGES)
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    set_slide_background(s13, LIGHT_BG)
    add_header(s13, "Three ML Models: Spatial Hold-Out Results & Geospatial Predictions", "CHAPTER 2: MODEL RESULTS", "CHAPTER 2", CH2_COLOR)

    # Table across 7,000 hold-out cells
    add_card(s13, 0.8, 1.5, 11.7, 2.0)
    tb_tab2 = s13.shapes.add_textbox(Inches(1.0), Inches(1.55), Inches(11.3), Inches(0.35))
    tf_tab2 = tb_tab2.text_frame; tf_tab2.margin_left = tf_tab2.margin_top = 0
    p = tf_tab2.paragraphs[0]; p.text = "Spatial Hold-Out Evaluation Results (Brooks Mountain Range — 7,000 Unseen Cells)"; p.font.size = Pt(11); p.font.bold = True; p.font.color.rgb = HEADER_ACCENT

    table_shape2 = s13.shapes.add_table(4, 7, Inches(1.0), Inches(1.9), Inches(11.3), Inches(1.4))
    t2 = table_shape2.table
    t2.columns[0].width = Inches(3.1)
    t2.columns[1].width = Inches(1.4)
    t2.columns[2].width = Inches(1.4)
    t2.columns[3].width = Inches(1.4)
    t2.columns[4].width = Inches(1.3)
    t2.columns[5].width = Inches(1.3)
    t2.columns[6].width = Inches(1.4)

    h2 = ["Model", "Accuracy", "Balanced Acc", "Precision", "Recall", "F1-Score", "ROC-AUC"]
    d2 = [
        ["Random Forest (200 trees) ⭐", "79.94%", "0.5749", "0.8231", "0.7994", "0.8105", "0.6157"],
        ["XGBoost (250 estimators)", "78.81%", "0.5143", "0.8009", "0.7881", "0.7944", "0.6218"],
        ["SVM (RBF Kernel, C=1.5)", "48.17%", "0.4473", "0.7739", "0.4817", "0.5719", "0.4453"]
    ]
    for c, h in enumerate(h2):
        cell = t2.cell(0, c); cell.fill.solid(); cell.fill.fore_color.rgb = RGBColor(238, 242, 255)
        p = cell.text_frame.paragraphs[0]; p.text = h; p.font.bold = True; p.font.size = Pt(9); p.font.color.rgb = CH2_COLOR
    for r, row in enumerate(d2):
        for c, val in enumerate(row):
            cell = t2.cell(r + 1, c); p = cell.text_frame.paragraphs[0]; p.text = val; p.font.size = Pt(9)
            if r == 0:
                cell.fill.solid(); cell.fill.fore_color.rgb = RGBColor(240, 253, 244)
                p.font.bold = True; p.font.color.rgb = RGBColor(16, 185, 129)
            else:
                p.font.color.rgb = TEXT_MAIN

    # Bottom: 2 Embedded Real Images (ROC & Map)
    add_card(s13, 0.8, 3.7, 5.7, 3.4)
    roc_img = "extracted_permafrost_img/slide_6_Picture 9.png"
    if os.path.exists(roc_img):
        s13.shapes.add_picture(roc_img, Inches(1.0), Inches(3.8), Inches(5.3), Inches(3.1))

    add_card(s13, 6.8, 3.7, 5.7, 3.4)
    map_img = "extracted_permafrost_img/slide_6_Picture 12.png"
    if os.path.exists(map_img):
        s13.shapes.add_picture(map_img, Inches(7.0), Inches(3.8), Inches(5.3), Inches(3.1))

    # =========================================================================
    # SLIDE 14: Chapter 2 — Key Takeaways, Disclaimers & Future Research
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    set_slide_background(s14, LIGHT_BG)
    add_header(s14, "Scientific Disclaimers, Key Takeaways & Future Scope", "CHAPTER 2: SYNTHESIS", "CHAPTER 2", CH2_COLOR)

    takeaway_cards = [
        ("Key Research Findings", CH2_COLOR, 0.8,
         "• Tree Ensembles Dominate: Random Forest (79.94% acc, 0.8105 F1) and XGBoost (78.81%) significantly outperform kernel SVM on rugged Arctic terrain.\n• Spatial-Block Validation: Mandatory in geospatial ML; pixel-level random splitting produces artificial 98% accuracy due to spatial proximity.\n• Environmental Hierarchy: Elevation and latitude dictate thermal potential; NDVI/NDWI capture local drainage barriers."),
        ("Scientific Disclaimers", ALERT_RED, 4.88,
         "• Surface Proxy Reality: Satellites observe surface active-layer vegetation and moisture, not deep subsurface borehole temperatures directly.\n• Optical Temporal Window: High-latitude remote sensing is restricted to cloud-free summer months (July–August); winter monitoring requires synthetic aperture radar (SAR).\n• Multi-Year Equilibrium: ESA CCI multi-year shifts reflect modeled ground equilibrium, not instant deep thaw."),
        ("Future Research Scope", RGBColor(16, 185, 129), 8.96,
         "• Sentinel-1 DInSAR Radar: Integrating radar interferometry to measure millimeter-scale active layer seasonal thaw subsidence and ground heave.\n• Deep Vision Transformers: Spatio-Temporal Vision Transformers to capture ice-wedge polygon micro-patterns at high resolution.\n• In-Situ Borehole Coupling: Direct coupling with USGS and GTN-P automated soil thermistor arrays for continuous physics-guided training.")
    ]
    for title, col, left_x, body in takeaway_cards:
        add_card(s14, left_x, 1.6, 3.55, 5.4)
        strp = s14.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left_x), Inches(1.6), Inches(3.55), Inches(0.12))
        strp.fill.solid(); strp.fill.fore_color.rgb = col; strp.line.fill.background()

        tb = s14.shapes.add_textbox(Inches(left_x + 0.15), Inches(1.85), Inches(3.25), Inches(5.0))
        tf = tb.text_frame; tf.word_wrap = True
        p = tf.paragraphs[0]; p.text = title; p.font.size = Pt(12); p.font.bold = True; p.font.color.rgb = col
        p_b = tf.add_paragraph(); p_b.text = body; p_b.font.size = Pt(9.5); p_b.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 15: Chapter 3 Divider (GLOF Early-Warning — MAIN FOCUS)
    # =========================================================================
    s15 = prs.slides.add_slide(blank_layout)
    add_chapter_divider(s15, 3,
                        "Glacial Lake Expansion & Multi-Sensor GLOF Hazard Early-Warning",
                        "Multi-Modal Radar-Optical Deep Sequence Modeling for Disaster Early-Warning across 40 Himalayan Lakes",
                        "Team Member 3 (Core Focus)",
                        ALERT_RED,
                        [
                            ("Objective: ", "Multi-sensor forecasting of proglacial lake expansion and automated classification of critical GLOF vulnerability alert tiers."),
                            ("Data Fusion: ", "Sentinel-1 C-band SAR (All-Weather Specular Reflection) + Sentinel-2 NDWI + ERA5-Land Climate + Copernicus DEM Moraine Freeboard."),
                            ("Scope: ", "40 High-Risk Glacial Lakes across Ladakh, Zanskar, Karakoram, and Sikkim (2,160 real satellite observations 2015–2024)."),
                            ("Benchmark Deliverable: ", "Multi-Task DLinear (0.9778 R², 3.98s) and Random Forest (0.9855 R²) achieved 100% Critical Alert Early-Warning Precision.")
                        ])

    # =========================================================================
    # SLIDE 16: Chapter 3 — Disaster Motivation: Real Himalayan GLOF Catastrophes
    # =========================================================================
    s16 = prs.slides.add_slide(blank_layout)
    set_slide_background(s16, LIGHT_BG)
    add_header(s16, "The Looming Himalayan Catastrophe: Rapid Lake Swelling & Moraine Failure", "CHAPTER 3: DISASTER CONTEXT", "CHAPTER 3 (CORE FOCUS)", ALERT_RED)

    add_card(s16, 0.8, 1.5, 5.7, 5.5)
    tb = s16.shapes.add_textbox(Inches(1.0), Inches(1.65), Inches(5.3), Inches(5.2))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "Real Disasters & Failure Mechanisms"; p.font.size = Pt(13); p.font.bold = True; p.font.color.rgb = ALERT_RED
    bullets_s16_left = [
        ("The GLOF Mechanism: ", "Glacial Lake Outburst Floods occur when fragile natural moraine dams (composed of loose rock and decaying ice cores) fail catastrophically."),
        ("South Lhonak Lake (Sikkim, Oct 4, 2023): ", "Expanded >180% over 20 years. An ice-rock avalanche from hanging cliffs triggered a seiche tsunami wave, breaching the moraine. Flood washed away the 1,200 MW Chungthang Dam, killing >100 people."),
        ("Gya Glacial Lake (Ladakh, Aug 6, 2014): ", "Suffered thermal piping failure through buried ice tunnels without prior warning, flooding Gya village along the Leh-Manali highway corridor."),
        ("Drang-Drung & Kyagar Hazards: ", "Drang-Drung proglacial lake expanded by 43% in 4 years. Kyagar repeatedly dams the Shaksgam river via periodic glacier surges."),
        ("Downstream Human Impact: ", "Hydroelectric plants, border transit roads, military forward posts, and downstream Himalayan towns face annihilation without timely civil early-warning.")
    ]
    for b_title, b_desc in bullets_s16_left:
        p = tf.add_paragraph()
        r1 = p.add_run(); r1.text = "• " + b_title; r1.font.bold = True; r1.font.size = Pt(9.5); r1.font.color.rgb = TEXT_MAIN
        r2 = p.add_run(); r2.text = b_desc; r2.font.size = Pt(9.5); r2.font.color.rgb = TEXT_MUTED

    add_card(s16, 6.8, 1.5, 5.7, 5.5)
    tb_r = s16.shapes.add_textbox(Inches(7.0), Inches(1.65), Inches(5.3), Inches(5.2))
    tf_r = tb_r.text_frame; tf_r.word_wrap = True
    p = tf_r.paragraphs[0]; p.text = "The Remote Sensing Bottlenecks"; p.font.size = Pt(13); p.font.bold = True; p.font.color.rgb = HEADER_ACCENT
    bullets_s16_right = [
        ("The Monsoon Blindness Dilemma: ", "In High Mountain Asia, the peak melt and flood season coincides with the Summer Monsoon (July–August). Optical satellites like Sentinel-2 are obscured by 80–90% cloud cover for weeks at a time!"),
        ("The Static Mapping Gap: ", "Existing research (Hi-MAG / Chen et al.) maps static historical lake polygons. Static inventories cannot predict future expansion or issue advance warnings."),
        ("Our Multi-Sensor Solution: ", "We fuse Sentinel-1 C-band Synthetic Aperture Radar (SAR)—whose microwaves penetrate clouds, rain, and darkness—with optical NDWI, ERA5-Land climate forcing, and DEM moraine dam freeboard."),
        ("Dual-Head Forecasting: ", "Simultaneously forecasts continuous future lake surface area (km²) and classifies categorical GLOF alert tiers (Low / Moderate / Critical Alert).")
    ]
    for b_title, b_desc in bullets_s16_right:
        p = tf_r.add_paragraph()
        r1 = p.add_run(); r1.text = "• " + b_title; r1.font.bold = True; r1.font.size = Pt(9.5); r1.font.color.rgb = TEXT_MAIN
        r2 = p.add_run(); r2.text = b_desc; r2.font.size = Pt(9.5); r2.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 17: Chapter 3 — Methodological Bridge: Decadal Glacier Retreat Check
    # =========================================================================
    s17 = prs.slides.add_slide(blank_layout)
    set_slide_background(s17, LIGHT_BG)
    add_header(s17, "Methodological Bridge: 25-Year Decadal Glacier Retreat as a Physics Check", "CHAPTER 3: METHODOLOGICAL BRIDGE", "CHAPTER 3 (CORE FOCUS)", ALERT_RED)

    add_card(s17, 0.8, 1.5, 11.7, 2.3)
    tb_tab2 = s17.shapes.add_textbox(Inches(1.0), Inches(1.6), Inches(11.3), Inches(2.1))
    tf_t2 = tb_tab2.text_frame; tf_t2.word_wrap = True
    p = tf_t2.paragraphs[0]; p.text = "25-Year Decadal Retreat Sanity Check across 12 Real Ladakh Glaciers (Siachen, Drang-Drung, Parkachik, etc.)"; p.font.size = Pt(11.5); p.font.bold = True; p.font.color.rgb = HEADER_ACCENT

    table_shape_br = s17.shapes.add_table(5, 5, Inches(1.0), Inches(1.95), Inches(11.3), Inches(1.6))
    t_br = table_shape_br.table
    t_br.columns[0].width = Inches(3.5)
    t_br.columns[1].width = Inches(2.0)
    t_br.columns[2].width = Inches(2.0)
    t_br.columns[3].width = Inches(2.0)
    t_br.columns[4].width = Inches(1.8)

    h_br = ["Model Architecture", "Test R² Score", "Test RMSE (km²)", "Test MAE (km²)", "Training Time (s)"]
    d_br = [
        ["Random Forest (Baseline)", "0.9984", "0.21 km²", "0.15 km²", "0.26 s"],
        ["LSTM Network", "0.9983", "0.22 km²", "0.16 km²", "9.50 s"],
        ["Temporal ConvNet (TCN)", "0.9953", "0.38 km²", "0.25 km²", "1.93 s (5x faster)"],
        ["DLinear (AAAI 2023)", "0.9796", "0.78 km²", "0.52 km²", "0.18 s"]
    ]
    for c, h in enumerate(h_br):
        cell = t_br.cell(0, c); cell.fill.solid(); cell.fill.fore_color.rgb = RGBColor(238, 242, 255)
        p = cell.text_frame.paragraphs[0]; p.text = h; p.font.bold = True; p.font.size = Pt(9.5); p.font.color.rgb = HEADER_ACCENT
    for r, row in enumerate(d_br):
        for c, val in enumerate(row):
            cell = t_br.cell(r + 1, c); p = cell.text_frame.paragraphs[0]; p.text = val; p.font.size = Pt(9.5); p.font.color.rgb = TEXT_MAIN
            if r == 0:
                cell.fill.solid(); cell.fill.fore_color.rgb = RGBColor(240, 253, 244)
                p.font.bold = True; p.font.color.rgb = RGBColor(16, 185, 129)

    add_card(s17, 0.8, 4.0, 5.7, 2.9)
    tb = s17.shapes.add_textbox(Inches(1.0), Inches(4.1), Inches(5.3), Inches(2.7))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "Why Include the Decadal Glacier Study?"; p.font.size = Pt(12); p.font.bold = True; p.font.color.rgb = HEADER_ACCENT
    bullets_s17_bot1 = [
        ("The Physical Origin: ", "Glacial lakes do not appear from nowhere—they pool directly in the overdeepened bedrock hollows excavated by retreating glaciers."),
        ("Multi-Decadal Satellite Proof: ", "Tracking 25 years of Landsat 7/8/9 & ERA5-Land confirmed systematic glacier shrinkage (-0.42 km²/year across Ladakh)."),
        ("Model Verification: ", "Proved that sequence models (LSTM, TCN, DLinear) successfully learn multi-decadal cryospheric thermal inertia.")
    ]
    for b_title, b_desc in bullets_s17_bot1:
        p = tf.add_paragraph()
        r1 = p.add_run(); r1.text = "• " + b_title; r1.font.bold = True; r1.font.size = Pt(9.5); r1.font.color.rgb = TEXT_MAIN
        r2 = p.add_run(); r2.text = b_desc; r2.font.size = Pt(9.5); r2.font.color.rgb = TEXT_MUTED

    add_card(s17, 6.8, 4.0, 5.7, 2.9)
    tb_r = s17.shapes.add_textbox(Inches(7.0), Inches(4.1), Inches(5.3), Inches(2.7))
    tf_r = tb_r.text_frame; tf_r.word_wrap = True
    p = tf_r.paragraphs[0]; p.text = "Transition to High-Frequency GLOF Early-Warning"; p.font.size = Pt(12); p.font.bold = True; p.font.color.rgb = ALERT_RED
    bullets_s17_bot2 = [
        ("Timescale Shift: ", "Decadal retreat is slow and chronic (yearly scale). In contrast, lake expansion and dam breach represent acute, life-threatening disasters (monthly scale)."),
        ("Architectural Progression: ", "We scale the verified sequence models into a Dual-Head Multi-Task architecture combining continuous regression with categorical early warning."),
        ("Sensor Escalation: ", "We introduce Sentinel-1 C-band SAR radar to defeat monsoon cloud blindness.")
    ]
    for b_title, b_desc in bullets_s17_bot2:
        p = tf_r.add_paragraph()
        r1 = p.add_run(); r1.text = "• " + b_title; r1.font.bold = True; r1.font.size = Pt(9.5); r1.font.color.rgb = TEXT_MAIN
        r2 = p.add_run(); r2.text = b_desc; r2.font.size = Pt(9.5); r2.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 18: Chapter 3 — Multi-Sensor Radar + Optical Feature Stack
    # =========================================================================
    s18 = prs.slides.add_slide(blank_layout)
    set_slide_background(s18, LIGHT_BG)
    add_header(s18, "Multi-Sensor Feature Stack: Radar (SAR) + Optical + Climate + Freeboard", "CHAPTER 3: MULTI-SENSOR FUSION", "CHAPTER 3 (CORE FOCUS)", ALERT_RED)

    feat_cards = [
        ("1. Optical NDWI (Sentinel-2)", CH1_COLOR, 0.8,
         "• Formula: (B3 Green - B8 NIR) / (B3 + B8)\n• Physics: Pure water strongly absorbs NIR while reflecting green light (NDWI > 0.35).\n• Role: High-resolution (10m) water perimeter delineation during clear sky days."),
        ("2. Radar SAR Specular (Sentinel-1)", RGBColor(124, 58, 237), 3.84,
         "• Physics: C-band radar (5.6 cm) penetrates clouds and rain. Smooth water acts as a specular reflector bouncing pulses away (-18 dB to -24 dB).\n• Role: 100% all-weather water tracking during monsoon months!"),
        ("3. Climate Forcing (ERA5-Land)", RGBColor(217, 119, 6), 6.88,
         "• Features: Monthly mean 2m summer temp (°C) & peak monsoon rainfall (mm).\n• Physics: Positive degree-days drive glacier ablation; heavy rain triggers flash runoff into proglacial basins."),
        ("4. Dam Freeboard & Ice (DEM)", ALERT_RED, 9.92,
         "• Dam Freeboard (m): Vertical clearance between water level and dam crest. Freeboard < 15m triggers extreme overtopping risk.\n• Dist to Ice (m): Distance to hanging calving front; < 250m indicates ice avalanche seiche wave threat.")
    ]
    for title, col, left_x, body in feat_cards:
        add_card(s18, left_x, 1.6, 2.65, 5.4)
        strp = s18.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left_x), Inches(1.6), Inches(2.65), Inches(0.12))
        strp.fill.solid(); strp.fill.fore_color.rgb = col; strp.line.fill.background()

        tb = s18.shapes.add_textbox(Inches(left_x + 0.12), Inches(1.85), Inches(2.41), Inches(5.0))
        tf = tb.text_frame; tf.word_wrap = True
        p = tf.paragraphs[0]; p.text = title; p.font.size = Pt(11); p.font.bold = True; p.font.color.rgb = col
        p_b = tf.add_paragraph(); p_b.text = body; p_b.font.size = Pt(9); p_b.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 19: Chapter 3 — The 40 Himalayan Glacial Lakes Dataset
    # =========================================================================
    s19 = prs.slides.add_slide(blank_layout)
    set_slide_background(s19, LIGHT_BG)
    add_header(s19, "Dataset Scope: 40 High-Risk Glacial Lakes across 4 Mountain Sectors", "CHAPTER 3: DATASET SCALE", "CHAPTER 3 (CORE FOCUS)", ALERT_RED)

    sectors = [
        ("1. Ladakh & Zanskar (10 Lakes)", CH1_COLOR, 0.8,
         "• Gya Lake (GL_01, 2014 GLOF site)\n• Drang-Drung Proglacial (GL_02, 43% expansion)\n• Pensilungpa (GL_03) | Parkachik (GL_04)\n• Machoi (GL_05) | Stok Kangri (GL_06)\n• Miru (GL_07) | Haptal (GL_08)\n• Phirse (GL_09) | Nimu (GL_10)\n• High-altitude semi-arid cryosphere."),
        ("2. Karakoram & Shyok (10 Lakes)", RGBColor(14, 116, 144), 3.84,
         "• Kyagar Lake (GL_11, periodic ice-dam)\n• Chong Kumdan (GL_12, surge hazard)\n• Kichik Kumdan (GL_13) | Apsarasas (GL_14)\n• Rimo Tsho (GL_15) | Shisper (GL_16)\n• Passu (GL_17) | Batura (GL_18)\n• Chong Muztagh (GL_19) | Gasherbrum (GL_20)\n• Surge-dammed outburst zones."),
        ("3. Himachal & Uttarakhand (10 Lakes)", RGBColor(217, 119, 6), 6.88,
         "• Gepang Gath (GL_21, rapid HP expansion)\n• Samudra Tapu (GL_22, moraine hazard)\n• Chhota Shigri (GL_23) | Bara Shigri (GL_24)\n• Satopanth Tal (GL_25) | Chorabari (GL_26, 2013 Kedarnath)\n• Gangotri Proglacial (GL_27) | Bhagirath Kharak (GL_28)\n• Vasuki Tal (GL_29) | Milam (GL_30)."),
        ("4. Sikkim, Nepal & Bhutan (10 Lakes)", ALERT_RED, 9.92,
         "• South Lhonak (GL_31, 2023 disaster site)\n• North Lhonak (GL_32) | Gurudongmar (GL_33)\n• Tso Lhamo (GL_34) | Khangri (GL_35)\n• Zemu (GL_36) | Tsho Rolpa (GL_37, Nepal)\n• Imja Tsho (GL_38, Everest region)\n• Thorthormi (GL_39) | Raphstreng (GL_40)\n• Monsoon-dominated vulnerable basins.")
    ]
    for title, col, left_x, body in sectors:
        add_card(s19, left_x, 1.6, 2.65, 5.4)
        strp = s19.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left_x), Inches(1.6), Inches(2.65), Inches(0.12))
        strp.fill.solid(); strp.fill.fore_color.rgb = col; strp.line.fill.background()

        tb = s19.shapes.add_textbox(Inches(left_x + 0.12), Inches(1.85), Inches(2.41), Inches(5.0))
        tf = tb.text_frame; tf.word_wrap = True
        p = tf.paragraphs[0]; p.text = title; p.font.size = Pt(11); p.font.bold = True; p.font.color.rgb = col
        p_b = tf.add_paragraph(); p_b.text = body; p_b.font.size = Pt(9); p_b.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 20: Chapter 3 — Dual-Head Multi-Task Architecture
    # =========================================================================
    s20 = prs.slides.add_slide(blank_layout)
    set_slide_background(s20, LIGHT_BG)
    add_header(s20, "Dual-Head Multi-Task Architecture: Joint Area & Hazard Forecasting", "CHAPTER 3: SYSTEM ARCHITECTURE", "CHAPTER 3 (CORE FOCUS)", ALERT_RED)

    add_card(s20, 0.8, 1.5, 5.7, 5.5)
    tb = s20.shapes.add_textbox(Inches(1.0), Inches(1.65), Inches(5.3), Inches(5.2))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "Mathematical Formulation & Joint Loss"; p.font.size = Pt(13); p.font.bold = True; p.font.color.rgb = ALERT_RED
    bullets_s20_left = [
        ("Input Sliding Window: ", "Sequence tensor X in R^(Batch x 6 x 7) representing 6 monthly lookback timesteps of the 7 multi-sensor features."),
        ("Shared Representation Backbone: ", "A shared sequence feature extractor h_t = Backbone(X) encodes temporal trends and climate correlations."),
        ("Head A: Continuous Regression Head: ", "A_hat_(t+1) = W_reg * h_t + b_reg\nPredicts future lake surface area (km²) 1 month ahead."),
        ("Head B: Categorical Hazard Head: ", "P(Risk_(t+1)) = Softmax(W_cls * h_t + b_cls)\nClassifies 3-tier GLOF vulnerability (0=Low, 1=Moderate, 2=High Alert)."),
        ("Joint Multi-Task Loss Function: ", "L_total = L_MSE(A_hat, A) + 0.5 * L_CrossEntropy(Risk_hat, Risk)\nJoint optimization forces shared representations to link rising water volumes with dam overtopping susceptibility.")
    ]
    for b_title, b_desc in bullets_s20_left:
        p = tf.add_paragraph()
        r1 = p.add_run(); r1.text = "• " + b_title; r1.font.bold = True; r1.font.size = Pt(9.5); r1.font.color.rgb = TEXT_MAIN
        r2 = p.add_run(); r2.text = b_desc; r2.font.size = Pt(9.5); r2.font.color.rgb = TEXT_MUTED

    add_card(s20, 6.8, 1.5, 5.7, 5.5)
    tb_r = s20.shapes.add_textbox(Inches(7.0), Inches(1.65), Inches(5.3), Inches(5.2))
    tf_r = tb_r.text_frame; tf_r.word_wrap = True
    p = tf_r.paragraphs[0]; p.text = "Chronological Splitting & Hazard Tier Thresholds"; p.font.size = Pt(13); p.font.bold = True; p.font.color.rgb = HEADER_ACCENT
    bullets_s20_right = [
        ("Strict Chronological Partition: ", "• Training Split (2015–2021): 1,200 sliding sequence windows across 40 lakes.\n• Validation Split (2022–2023): 480 sliding sequence windows.\n• Test Split (2024): 240 unseen evaluation sequence windows."),
        ("Zero Data Leakage: ", "No random shuffling! All normalizers (StandardScaler) are fitted strictly on the training partition and applied downstream."),
        ("Tier 0: Low Risk (Normal): ", "Lake area stable (<2% expansion/month), dam freeboard safe (>25m), and low melt inflow."),
        ("Tier 1: Moderate Risk (Warning): ", "Accelerated expansion (2–5%/month), freeboard reduced to 15–25m. Active monitoring required."),
        ("Tier 2: High Alert (Imminent Hazard): ", "Freeboard < 15m, growth > 5%/month, or calving front < 250m. Immediate civil defense alert!")
    ]
    for b_title, b_desc in bullets_s20_right:
        p = tf_r.add_paragraph()
        r1 = p.add_run(); r1.text = "• " + b_title; r1.font.bold = True; r1.font.size = Pt(9.5); r1.font.color.rgb = TEXT_MAIN
        r2 = p.add_run(); r2.text = b_desc; r2.font.size = Pt(9.5); r2.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 21: Chapter 3 — Model Deep Dive 1: Multi-Task LSTM & TCN
    # =========================================================================
    s21 = prs.slides.add_slide(blank_layout)
    set_slide_background(s21, LIGHT_BG)
    add_header(s21, "Model Architecture Deep-Dive 1: Multi-Task LSTM & Temporal ConvNet", "CHAPTER 3: DEEP MODELS (RECURRENT & CONV)", "CHAPTER 3 (CORE FOCUS)", ALERT_RED)

    add_card(s21, 0.8, 1.5, 5.7, 5.5)
    tb = s21.shapes.add_textbox(Inches(1.0), Inches(1.65), Inches(5.3), Inches(5.2))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "Multi-Task Long Short-Term Memory (LSTM)"; p.font.size = Pt(13); p.font.bold = True; p.font.color.rgb = CH1_COLOR
    bullets_s21_left = [
        ("Architecture: ", "2-layer stacked recurrent network (input_dim=7, hidden_dim=64) with cell state c_t and hidden state h_t."),
        ("Mathematical Gating: ", "• Forget Gate: f_t = σ(W_f · [h_(t-1), x_t] + b_f)\n• Input Gate: i_t = σ(W_i · [h_(t-1), x_t] + b_i)\n• Candidate State: c_tilde_t = tanh(W_c · [h_(t-1), x_t] + b_c)\n• Output Gate: o_t = σ(W_o · [h_(t-1), x_t] + b_o)"),
        ("Physical Hydrological Role: ", "Cell state acts as a continuous meltwater reservoir. Stores multi-month degree-day warming memory, capturing rising water tables."),
        ("Citation: ", "Hochreiter & Schmidhuber (1997); Kratzert et al. (HESS 2018)."),
        ("Pros & Cons: ", "• Pros: 100% Alert Acc, continuous extrapolation.\n• Cons: Sequential execution (slowest train time: 13.65s).")
    ]
    for b_title, b_desc in bullets_s21_left:
        p = tf.add_paragraph()
        r1 = p.add_run(); r1.text = "• " + b_title; r1.font.bold = True; r1.font.size = Pt(9.5); r1.font.color.rgb = TEXT_MAIN
        r2 = p.add_run(); r2.text = b_desc; r2.font.size = Pt(9.5); r2.font.color.rgb = TEXT_MUTED

    add_card(s21, 6.8, 1.5, 5.7, 5.5)
    tb_r = s21.shapes.add_textbox(Inches(7.0), Inches(1.65), Inches(5.3), Inches(5.2))
    tf_r = tb_r.text_frame; tf_r.word_wrap = True
    p = tf_r.paragraphs[0]; p.text = "Multi-Task Temporal Convolutional Network (TCN)"; p.font.size = Pt(13); p.font.bold = True; p.font.color.rgb = RGBColor(124, 58, 237)
    bullets_s21_right = [
        ("Architecture: ", "Stacked 1D dilated causal convolutions with residual connections and Chomp1d temporal padding."),
        ("Exponential Dilation Factors: ", "Receptive field grows exponentially via dilations d = [1, 2] without increasing parameter count: y_t = Σ f(k) · x_(t - d·k)."),
        ("Strict Causality (Chomp1d): ", "Padding is pruned exclusively from the future side of the convolution, mathematically preventing future data leakage."),
        ("Citation: ", "Bai, Kolter, & Koltun (arXiv 2018)."),
        ("Pros & Cons: ", "• Pros: Parallel GPU computation (6.56s, 2x faster than LSTM); zero vanishing gradients.\n• Cons: Slightly lower alert F1 (0.4958) on minority high-risk alert transitions.")
    ]
    for b_title, b_desc in bullets_s21_right:
        p = tf_r.add_paragraph()
        r1 = p.add_run(); r1.text = "• " + b_title; r1.font.bold = True; r1.font.size = Pt(9.5); r1.font.color.rgb = TEXT_MAIN
        r2 = p.add_run(); r2.text = b_desc; r2.font.size = Pt(9.5); r2.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 22: Chapter 3 — Model Deep Dive 2: Multi-Task DLinear & Random Forest
    # =========================================================================
    s22 = prs.slides.add_slide(blank_layout)
    set_slide_background(s22, LIGHT_BG)
    add_header(s22, "Model Architecture Deep-Dive 2: Multi-Task DLinear & Random Forest", "CHAPTER 3: LINEAR DECOMPOSITION & TREES", "CHAPTER 3 (CORE FOCUS)", ALERT_RED)

    add_card(s22, 0.8, 1.5, 5.7, 5.5)
    tb = s22.shapes.add_textbox(Inches(1.0), Inches(1.65), Inches(5.3), Inches(5.2))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "Multi-Task DLinear (Trend-Seasonal Decomposition)"; p.font.size = Pt(13); p.font.bold = True; p.font.color.rgb = RGBColor(16, 185, 129)
    bullets_s22_left = [
        ("Architecture: ", "Moving average decomposition block (kernel size 3) splitting input series into Trend (T_t) and Seasonal Residuals (S_t)."),
        ("Mathematical Formulation: ", "• Trend: T_t = AvgPool1d(X_t, kernel=3, stride=1)\n• Seasonal: S_t = X_t - T_t\n• Dual Linear Projections: y_hat = W_T · T_t + W_S · S_t"),
        ("Breakthrough Paper: ", "Zeng, Chen, Zhang, & Xu (AAAI 2023), 'Are Transformers Effective for Time Series?'"),
        ("Why It Dominates Deep Models: ", "Decouples slow morphological lake expansion from high-frequency summer monsoon water spikes."),
        ("Pros & Cons: ", "• Pros: Top deep model (0.9778 R², 100% Alert Acc, 3.98s train time, 3.4x faster than LSTM).\n• Cons: Linear heads require sequence decomposition.")
    ]
    for b_title, b_desc in bullets_s22_left:
        p = tf.add_paragraph()
        r1 = p.add_run(); r1.text = "• " + b_title; r1.font.bold = True; r1.font.size = Pt(9.5); r1.font.color.rgb = TEXT_MAIN
        r2 = p.add_run(); r2.text = b_desc; r2.font.size = Pt(9.5); r2.font.color.rgb = TEXT_MUTED

    add_card(s22, 6.8, 1.5, 5.7, 5.5)
    tb_r = s22.shapes.add_textbox(Inches(7.0), Inches(1.65), Inches(5.3), Inches(5.2))
    tf_r = tb_r.text_frame; tf_r.word_wrap = True
    p = tf_r.paragraphs[0]; p.text = "Random Forest Regressor & Classifier (Tabular Baseline)"; p.font.size = Pt(13); p.font.bold = True; p.font.color.rgb = GOLD_ACCENT
    bullets_s22_right = [
        ("Architecture: ", "Ensemble of 100 randomized decision trees (max_depth=10, bootstrap sampling, multi-threaded)."),
        ("Mathematical Tree Splitting: ", "At each node, selects feature x_j and split threshold θ minimizing variance reduction (MSE) or Gini impurity: θ* = argmin [MSE_left + MSE_right]."),
        ("Why It Scores Highest: ", "Lake areas span multiple scales (0.10 to 1.6 km²). Top tree splits immediately partition lake scale, explaining >92% of variance."),
        ("Physical Step-Functions: ", "Dam breach thresholds (freeboard < 15m) are naturally modeled as axis-aligned orthogonal cuts."),
        ("The Fatal Limitation (Extrapolation Trap): ", "Decision trees cannot extrapolate outside historical bounds! Under record heatwaves, RF predicts a flat ceiling.")
    ]
    for b_title, b_desc in bullets_s22_right:
        p = tf_r.add_paragraph()
        r1 = p.add_run(); r1.text = "• " + b_title; r1.font.bold = True; r1.font.size = Pt(9.5); r1.font.color.rgb = TEXT_MAIN
        r2 = p.add_run(); r2.text = b_desc; r2.font.size = Pt(9.5); r2.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 23: Chapter 3 — Comparative Evaluation: Trade-Offs & Extrapolation
    # =========================================================================
    s23 = prs.slides.add_slide(blank_layout)
    set_slide_background(s23, LIGHT_BG)
    add_header(s23, "Architectural Trade-Offs: Why Random Forest Won & The Extrapolation Trap", "CHAPTER 3: SCIENTIFIC EVALUATION", "CHAPTER 3 (CORE FOCUS)", ALERT_RED)

    comp_cards = [
        ("The 3 Reasons RF Leads In-Distribution", GOLD_ACCENT, 0.8,
         "1. Lake Scale Partitioning: High Mountain Asia lakes range from 0.10 km² to 1.6+ km². First 2-3 tree splits segment base lake scale with zero error.\n2. Non-Linear Step Functions: Ice melt turns on abruptly at >0°C; dam overtopping spikes when freeboard < 15m. Decision trees excel at threshold cuts.\n3. Noise Invariance: Tree averaging across 100 estimators filters out single-month satellite acquisition noise."),
        ("The Extrapolation Trap (The Fatal Flaw)", ALERT_RED, 4.88,
         "• Mathematical Constraint: A decision tree outputs the average of training samples in a leaf node. It CANNOT extrapolate beyond the historical maximum.\n• Failure Mode: If future summer temperatures rise +2.0°C beyond historical records, Random Forest hits a flat ceiling and fails to predict rapid lake swelling.\n• Neural sequence models (DLinear, LSTM) learn continuous functions and MUST be used for climate warming projections."),
        ("Deep Learning Takeaway: DLinear vs LSTM", RGBColor(16, 185, 129), 8.96,
         "• DLinear (0.9778 R²): Top deep learning performer, running in just 3.98s (3.4x faster than LSTM) with 100% Alert Accuracy.\n• Trend-seasonal separation matches physical reality: moraine expansion is secular, monsoon spikes are seasonal.\n• Multi-Task LSTM (0.9692 R²): Strong mass balance memory, but slower training (13.65s).\n• DLinear + RF provides the optimal operational ensemble.")
    ]
    for title, col, left_x, body in comp_cards:
        add_card(s23, left_x, 1.6, 3.55, 5.4)
        strp = s23.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left_x), Inches(1.6), Inches(3.55), Inches(0.12))
        strp.fill.solid(); strp.fill.fore_color.rgb = col; strp.line.fill.background()

        tb = s23.shapes.add_textbox(Inches(left_x + 0.15), Inches(1.85), Inches(3.25), Inches(5.0))
        tf = tb.text_frame; tf.word_wrap = True
        p = tf.paragraphs[0]; p.text = title; p.font.size = Pt(12); p.font.bold = True; p.font.color.rgb = col
        p_b = tf.add_paragraph(); p_b.text = body; p_b.font.size = Pt(9.5); p_b.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 24: Chapter 3 — Final Benchmark Results (Table + Real Comparison Image)
    # =========================================================================
    s24 = prs.slides.add_slide(blank_layout)
    set_slide_background(s24, LIGHT_BG)
    add_header(s24, "Multi-Task GLOF Benchmark Results on Unseen 2024 Test Set", "CHAPTER 3: BENCHMARK RESULTS", "CHAPTER 3 (CORE FOCUS)", ALERT_RED)

    # Benchmark Table
    add_card(s24, 0.8, 1.5, 11.7, 2.05)
    tb_tab3 = s24.shapes.add_textbox(Inches(1.0), Inches(1.55), Inches(11.3), Inches(0.35))
    tf_tab3 = tb_tab3.text_frame; tf_tab3.margin_left = tf_tab3.margin_top = 0
    p = tf_tab3.paragraphs[0]; p.text = "Benchmark across 40 Himalayan Glacial Lakes (240 Unseen Sequence Windows in 2024 Test Split)"; p.font.size = Pt(11); p.font.bold = True; p.font.color.rgb = HEADER_ACCENT

    table_shape3 = s24.shapes.add_table(5, 7, Inches(1.0), Inches(1.9), Inches(11.3), Inches(1.5))
    t3 = table_shape3.table
    t3.columns[0].width = Inches(2.7)
    t3.columns[1].width = Inches(1.4)
    t3.columns[2].width = Inches(1.4)
    t3.columns[3].width = Inches(1.4)
    t3.columns[4].width = Inches(1.6)
    t3.columns[5].width = Inches(1.4)
    t3.columns[6].width = Inches(1.4)

    h3 = ["Model Architecture", "Area R²", "RMSE (km²)", "MAE (km²)", "Alert Acc (%)", "Macro F1", "Train Time"]
    d3 = [
        ["Random Forest (Baseline)", "0.9855", "0.0408 km²", "0.0117 km²", "100.0%", "1.0000", "4.45 s"],
        ["Multi-Task DLinear ⭐", "0.9778", "0.0504 km²", "0.0304 km²", "100.0%", "1.0000", "3.98 s"],
        ["Multi-Task TCN", "0.9734", "0.0552 km²", "0.0250 km²", "98.33%", "0.4958", "6.56 s"],
        ["Multi-Task LSTM", "0.9692", "0.0594 km²", "0.0410 km²", "100.0%", "1.0000", "13.65 s"]
    ]
    for c, h in enumerate(h3):
        cell = t3.cell(0, c); cell.fill.solid(); cell.fill.fore_color.rgb = RGBColor(238, 242, 255)
        p = cell.text_frame.paragraphs[0]; p.text = h; p.font.bold = True; p.font.size = Pt(9.5); p.font.color.rgb = ALERT_RED
    for r, row in enumerate(d3):
        for c, val in enumerate(row):
            cell = t3.cell(r + 1, c); p = cell.text_frame.paragraphs[0]; p.text = val; p.font.size = Pt(9.5)
            if r in [0, 1]:
                cell.fill.solid(); cell.fill.fore_color.rgb = RGBColor(240, 253, 244)
                p.font.bold = True; p.font.color.rgb = RGBColor(16, 185, 129)
            else:
                p.font.color.rgb = TEXT_MAIN

    # Embed Real Image: glof_model_benchmark_comparison.png
    add_card(s24, 0.8, 3.75, 11.7, 3.35)
    bench_img = "glof_model_benchmark_comparison.png"
    if os.path.exists(bench_img):
        s24.shapes.add_picture(bench_img, Inches(1.0), Inches(3.85), Inches(11.3), Inches(3.1))
    else:
        tb_err = s24.shapes.add_textbox(Inches(1.0), Inches(4.5), Inches(11.3), Inches(1.5))
        p = tb_err.text_frame.paragraphs[0]; p.text = "Benchmark Comparison: Area R², RMSE, Alert Accuracy, Risk F1 across Models"; p.font.size = Pt(12)

    # =========================================================================
    # SLIDE 25: Chapter 3 — 2024 Test Trajectories (WITH REAL TRAJECTORY IMAGE)
    # =========================================================================
    s25 = prs.slides.add_slide(blank_layout)
    set_slide_background(s25, LIGHT_BG)
    add_header(s25, "Unseen 2024 Test Horizon Multi-Temporal Trajectories across Landmark Lakes", "CHAPTER 3: FORECAST TRAJECTORIES", "CHAPTER 3 (CORE FOCUS)", ALERT_RED)

    # Embed Real Image: glof_actual_vs_predicted_series.png
    add_card(s25, 0.8, 1.5, 11.7, 4.4)
    series_img = "glof_actual_vs_predicted_series.png"
    if os.path.exists(series_img):
        s25.shapes.add_picture(series_img, Inches(1.0), Inches(1.6), Inches(11.3), Inches(4.15))
    else:
        tb_err = s25.shapes.add_textbox(Inches(1.0), Inches(3.0), Inches(11.3), Inches(2.0))
        p = tb_err.text_frame.paragraphs[0]; p.text = "Multi-Temporal Glacial Lake Expansion Trajectories (2015-2024)"; p.font.size = Pt(12)

    # Summary Takeaway Card below
    add_card(s25, 0.8, 6.05, 11.7, 1.0)
    tb_bot = s25.shapes.add_textbox(Inches(1.0), Inches(6.1), Inches(11.3), Inches(0.9))
    tf_bot = tb_bot.text_frame; tf_bot.word_wrap = True
    p = tf_bot.paragraphs[0]; p.text = "Key Operational Finding: 100% Critical Alert Precision"; p.font.size = Pt(11); p.font.bold = True; p.font.color.rgb = RGBColor(16, 185, 129)
    p_sub = tf_bot.add_paragraph()
    p_sub.text = "Both Multi-Task DLinear and Random Forest achieved 100.0% Alert Accuracy and Macro F1 of 1.0000 on the 2024 test horizon. The radar-optical fusion accurately detected rapid pre-breach lake swelling at South Lhonak and Gya without false alarms."
    p_sub.font.size = Pt(9.5); p_sub.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 26: Cross-Chapter Synthesis Matrix (All 3 Members Side-by-Side)
    # =========================================================================
    s26 = prs.slides.add_slide(blank_layout)
    set_slide_background(s26, LIGHT_BG)
    add_header(s26, "Master Cross-Chapter Synthesis: Connecting Pixels, Permafrost & Floods", "TEAM SYNTHESIS", "UNIFIED FRAMEWORK", HEADER_ACCENT)

    synth_cards = [
        ("Chapter 1: Glacier Mapping", CH1_COLOR, 0.8,
         "• Lead: Team Member 1\n• Target: Clean & debris glacier spatial perimeters\n• Sensors: Sentinel-2 8-Channel MSI (10m)\n• Models: Attention U-Net vs SUNet\n• Top Metric: 0.9668 Dice | 0.9357 IoU\n• Impact: Automated boundary tracking replacing manual digitizing."),
        ("Chapter 2: PermaWatch", CH2_COLOR, 4.88,
         "• Lead: Team Member 2\n• Target: Subsurface permafrost thaw degradation\n• Sensors: ESA CCI v5.0 (1 km) + S2 + DEM\n• Models: Random Forest vs XGBoost vs SVM\n• Top Metric: 79.94% Spatial Hold-Out Acc (0.8105 F1)\n• Impact: Civil infrastructure protection across Alaska highway corridors."),
        ("Chapter 3: GLOF Early-Warning", ALERT_RED, 8.96,
         "• Lead: Team Member 3 (Core Focus)\n• Target: Proglacial lake expansion & dam breach tiers\n• Sensors: Sentinel-1 SAR + S2 + ERA5 + DEM\n• Models: Multi-Task DLinear vs LSTM vs RF\n• Top Metric: 0.9855 R² | 100% Critical Alert Acc\n• Impact: Life-saving early-warning for downstream Himalayan towns.")
    ]
    for title, col, left_x, body in synth_cards:
        add_card(s26, left_x, 1.6, 3.55, 5.4)
        strp = s26.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left_x), Inches(1.6), Inches(3.55), Inches(0.12))
        strp.fill.solid(); strp.fill.fore_color.rgb = col; strp.line.fill.background()

        tb = s26.shapes.add_textbox(Inches(left_x + 0.15), Inches(1.85), Inches(3.25), Inches(5.0))
        tf = tb.text_frame; tf.word_wrap = True
        p = tf.paragraphs[0]; p.text = title; p.font.size = Pt(12); p.font.bold = True; p.font.color.rgb = col
        p_b = tf.add_paragraph(); p_b.text = body; p_b.font.size = Pt(9.5); p_b.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 27: Shared Methodological Rigor: Zero-Leakage Protocols
    # =========================================================================
    s27 = prs.slides.add_slide(blank_layout)
    set_slide_background(s27, LIGHT_BG)
    add_header(s27, "Shared Methodological Rigor: Zero-Leakage Spatial & Temporal Validation", "EXPERIMENTAL RIGOR", "ENGINEERING STANDARDS", HEADER_ACCENT)

    rigor_cards = [
        ("Spatial Autocorrelation (Ch. 2)", CH2_COLOR, 0.8,
         "• The Trap: Adjacent 1 km pixels share identical terrain; random shuffling yields fake 98% accuracy.\n• Our Protocol: GroupShuffleSplit holding out the entire Brooks Mountain Range (7,000 cells) as an unseen spatial test block.\n• Integrity: Authentic ~80% spatial generalization."),
        ("Chronological Splitting (Ch. 3)", ALERT_RED, 4.88,
         "• The Trap: Shuffling time-series leaks future temperatures into the past, invalidating forecasting.\n• Our Protocol: Strict chronological split: Train (2015–2021), Val (2022–2023), Test (2024).\n• Normalization: StandardScaler fitted strictly on train split."),
        ("Physics-Guided Integration", RGBColor(16, 185, 129), 8.96,
         "• The Trap: Black-box ML models predicting purely on autoregressive lag.\n• Our Protocol: Physical climate coupling (positive degree-days, winter snowfall, monsoon rain, dam freeboard clearance).\n• Models learn physical mass balance and dam crest stability.")
    ]
    for title, col, left_x, body in rigor_cards:
        add_card(s27, left_x, 1.6, 3.55, 5.4)
        strp = s27.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left_x), Inches(1.6), Inches(3.55), Inches(0.12))
        strp.fill.solid(); strp.fill.fore_color.rgb = col; strp.line.fill.background()

        tb = s27.shapes.add_textbox(Inches(left_x + 0.15), Inches(1.85), Inches(3.25), Inches(5.0))
        tf = tb.text_frame; tf.word_wrap = True
        p = tf.paragraphs[0]; p.text = title; p.font.size = Pt(12); p.font.bold = True; p.font.color.rgb = col
        p_b = tf.add_paragraph(); p_b.text = body; p_b.font.size = Pt(9.5); p_b.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 28: Viva Voce Examination Master Defense Guide
    # =========================================================================
    s28 = prs.slides.add_slide(blank_layout)
    set_slide_background(s28, LIGHT_BG)
    add_header(s28, "Viva Voce Master Defense Guide: Addressing Examiner Inquiries", "VIVA VOCE DEFENSE GUIDE", "EXAM READINESS", HEADER_ACCENT)

    qas = [
        ("Q1: 'Why do Random Forests achieve higher accuracy than deep learning?'",
         "Answer: Glacial lakes and Arctic permafrost exhibit wide scale differences and sharp physical thresholds (melt at >0°C, dam failure at freeboard < 15m). Decision trees segment scale in their first branches and map axis-aligned step functions with zero error. HOWEVER, Random Forest cannot extrapolate beyond training bounds! Neural sequence models (DLinear, LSTM) are required for climate projections."),
        ("Q2: 'How did each member prevent data leakage in their specific study?'",
         "Answer: Member 1 enforced strict patch-level splitting. Member 2 prevented spatial autocorrelation via GroupShuffleSplit, holding out an entire mountain range. Member 3 enforced strict chronological splitting (2015-2021 train, 2024 test), fitting scalers strictly on the training partition."),
        ("Q3: 'Why is Sentinel-1 SAR microwave radar mandatory in the Himalayas?'",
         "Answer: Peak flood hazards occur during the Summer Monsoon (July-August) when optical satellites are blinded by 80-90% cloud cover. Sentinel-1 C-band SAR radar pulses penetrate clouds, rain, and darkness, detecting smooth water surfaces via dark specular reflections (-18 dB to -24 dB)."),
        ("Q4: 'How do these three chapters connect into a unified engineering platform?'",
         "Answer: Chapter 1 maps where glaciers are retreating. Chapter 2 monitors underlying permafrost thaw that destabilizes moraine dams. Chapter 3 fuses both with radar-optical time series to forecast lake expansion and trigger life-saving GLOF evacuation alerts.")
    ]
    for idx, (q, a) in enumerate(qas):
        top_y = 1.5 + idx * 1.35
        add_card(s28, 0.8, top_y, 11.7, 1.25)
        tb = s28.shapes.add_textbox(Inches(1.0), Inches(top_y + 0.08), Inches(11.3), Inches(1.1))
        tf = tb.text_frame; tf.word_wrap = True
        p_q = tf.paragraphs[0]; p_q.text = q; p_q.font.size = Pt(10.5); p_q.font.bold = True; p_q.font.color.rgb = HEADER_ACCENT
        p_a = tf.add_paragraph(); p_a.text = a; p_a.font.size = Pt(9.5); p_a.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 29: Academic Literature Citations & Conclusions
    # =========================================================================
    s29 = prs.slides.add_slide(blank_layout)
    set_slide_background(s29, DARK_BG)

    acc_top2 = s29.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.7), Inches(11.7), Inches(0.08))
    acc_top2.fill.solid(); acc_top2.fill.fore_color.rgb = CH3_COLOR; acc_top2.line.fill.background()

    tb29 = s29.shapes.add_textbox(Inches(0.8), Inches(0.95), Inches(11.7), Inches(1.1))
    tf29 = tb29.text_frame; tf29.word_wrap = True
    p29 = tf29.paragraphs[0]; p29.text = "Key Academic Literature Citations & Conclusions"; p29.font.size = Pt(24); p29.font.bold = True; p29.font.color.rgb = RGBColor(255, 255, 255)
    p29_sub = tf29.add_paragraph(); p29_sub.text = "Rigorous Peer-Reviewed Literature Grounding across Remote Sensing, Machine Learning & Cryospheric Hazards"; p29_sub.font.size = Pt(12); p29_sub.font.color.rgb = TEXT_LIGHT

    # Left: Citations Card
    add_card(s29, 0.8, 2.2, 7.8, 4.7, bg_color=RGBColor(30, 41, 59), border_color=CARD_BORDER)
    tb_c = s29.shapes.add_textbox(Inches(1.0), Inches(2.3), Inches(7.4), Inches(4.5))
    tf_c = tb_c.text_frame; tf_c.word_wrap = True
    p = tf_c.paragraphs[0]; p.text = "Foundational Academic Citations"; p.font.size = Pt(12); p.font.bold = True; p.font.color.rgb = GOLD_ACCENT

    citations = [
        ("Oktay et al. (MIDL 2018): ", "Attention U-Net introducing gated attention mechanisms for spatial segmentation and shadow filtering."),
        ("Cao et al. / Liu et al. (ECCV 2022 / ICCV 2021): ", "Swin-UNet pure transformer architectures for hierarchical non-local vision."),
        ("Obu et al. / ESA CCI (Earth-Science Reviews 2019 / ESSD 2021): ", "Northern Hemisphere permafrost map and ESA CCI Permafrost dataset."),
        ("Zeng et al. (AAAI 2023): ", "DLinear trend-seasonal decomposition proving linear projection superiority on physical time series."),
        ("Chen et al. (ESSD 2021): ", "Benchmark inventory of High Mountain Asia glacial lakes (Hi-MAG) based on Sentinel and Landsat."),
        ("Babu Govindha Raj et al. (Current Science 2023): ", "Remote sensing analysis of the catastrophic South Lhonak Glacial Lake breach in Sikkim."),
        ("Twele et al. (Remote Sensing of Environment 2016): ", "Sentinel-1 SAR specular backscatter calibration for all-weather automated flood mapping.")
    ]
    for c_title, c_desc in citations:
        p = tf_c.add_paragraph()
        r1 = p.add_run(); r1.text = "• " + c_title; r1.font.bold = True; r1.font.size = Pt(9.5); r1.font.color.rgb = RGBColor(241, 245, 249)
        r2 = p.add_run(); r2.text = c_desc; r2.font.size = Pt(9); r2.font.color.rgb = TEXT_LIGHT

    # Right: Thank You & Viva Readiness Card
    add_card(s29, 8.8, 2.2, 3.7, 4.7, bg_color=RGBColor(30, 41, 59), border_color=CH3_COLOR)
    tb_thx = s29.shapes.add_textbox(Inches(9.0), Inches(2.5), Inches(3.3), Inches(4.2))
    tf_thx = tb_thx.text_frame; tf_thx.word_wrap = True
    p = tf_thx.paragraphs[0]; p.text = "Thank You!"; p.font.size = Pt(26); p.font.bold = True; p.font.color.rgb = RGBColor(255, 255, 255)
    p_sub = tf_thx.add_paragraph(); p_sub.text = "We are ready for questions."; p_sub.font.size = Pt(13); p_sub.font.color.rgb = CH3_COLOR

    p_div = tf_thx.add_paragraph()
    p_div.text = "\nTeam Presenters:"
    p_div.font.size = Pt(11); p_div.font.bold = True; p_div.font.color.rgb = RGBColor(255, 255, 255)

    p_t1 = tf_thx.add_paragraph(); p_t1.text = "• Chapter 1: Team Member 1 (Glacier Mapping)"
    p_t1.font.size = Pt(10); p_t1.font.color.rgb = TEXT_LIGHT

    p_t2 = tf_thx.add_paragraph(); p_t2.text = "• Chapter 2: Team Member 2 (Permafrost Thaw)"
    p_t2.font.size = Pt(10); p_t2.font.color.rgb = TEXT_LIGHT

    p_t3 = tf_thx.add_paragraph(); p_t3.text = "• Chapter 3: Team Member 3 (GLOF Early-Warning)"
    p_t3.font.size = Pt(10); p_t3.font.bold = True; p_t3.font.color.rgb = CH3_COLOR

    p_code = tf_thx.add_paragraph()
    p_code.text = "\nComplete code, notebooks & datasets archived in project repository."
    p_code.font.size = Pt(9.5); p_code.font.color.rgb = GOLD_ACCENT

    out_file = "Unified_Cryosphere_AI_Master_Presentation.pptx"
    prs.save(out_file)
    print(f"Presentation saved successfully to: {out_file} (Total Slides: {len(prs.slides)})")

if __name__ == "__main__":
    build_presentation()

