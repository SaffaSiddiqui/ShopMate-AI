"""
Script to generate a professional PowerPoint presentation for ShopMate AI.
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_presentation():
    prs = Presentation()
    # 16:9 widescreen dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Theme Colors
    BG_DARK = RGBColor(15, 23, 42)       # Slate 900
    BG_CARD = RGBColor(30, 41, 59)       # Slate 800
    PRIMARY = RGBColor(59, 130, 246)      # Blue 500
    ACCENT_GREEN = RGBColor(16, 185, 129) # Emerald 500
    TEXT_LIGHT = RGBColor(248, 250, 252)  # White/Slate 50
    TEXT_MUTED = RGBColor(148, 163, 184)  # Slate 400
    TEXT_SUB = RGBColor(203, 213, 225)    # Slate 300

    def set_slide_background(slide):
        background = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height
        )
        background.fill.solid()
        background.fill.fore_color.rgb = BG_DARK
        background.line.color.rgb = BG_DARK
        return background

    def add_header(slide, title_text, category="SHOPMATE AI • CAPSTONE PROJECT"):
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.5), Inches(0.4))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = PRIMARY

        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.85), Inches(11.5), Inches(0.8))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.size = Pt(28)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_LIGHT

    # ==========================================
    # SLIDE 1: Title Slide
    # ==========================================
    slide_layout = prs.slide_layouts[6] # blank layout
    slide1 = prs.slides.add_slide(slide_layout)
    set_slide_background(slide1)

    # Accent decorative bar
    bar = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.8), Inches(1.5), Inches(0.08))
    bar.fill.solid()
    bar.fill.fore_color.rgb = PRIMARY
    bar.line.color.rgb = PRIMARY

    tb = slide1.shapes.add_textbox(Inches(0.8), Inches(2.2), Inches(11.5), Inches(3.5))
    tf = tb.text_frame
    tf.word_wrap = True

    p1 = tf.paragraphs[0]
    p1.text = "ShopMate AI"
    p1.font.size = Pt(50)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_LIGHT

    p2 = tf.add_paragraph()
    p2.text = "Intelligent Retail Management & Generative AI Business Advisor"
    p2.font.size = Pt(22)
    p2.font.color.rgb = PRIMARY
    p2.space_before = Pt(10)

    p3 = tf.add_paragraph()
    p3.text = "A full-stack, AI-powered business dashboard tailored for Pakistani SMEs, retail stores, and e-commerce enterprises."
    p3.font.size = Pt(14)
    p3.font.color.rgb = TEXT_SUB
    p3.space_before = Pt(15)

    p4 = tf.add_paragraph()
    p4.text = "Tech Stack: React 18 • Python FastAPI • SQLite • Google Gemini Generative AI"
    p4.font.size = Pt(13)
    p4.font.bold = True
    p4.font.color.rgb = ACCENT_GREEN
    p4.space_before = Pt(25)

    # ==========================================
    # SLIDE 2: Problem Statement
    # ==========================================
    slide2 = prs.slides.add_slide(slide_layout)
    set_slide_background(slide2)
    add_header(slide2, "The Problem: Challenges in Traditional Pakistani Retail")

    cards_data_s2 = [
        ("Manual & Paper Tracking", "Retailers rely on manual registers or disjointed Excel files, causing lost transaction histories, data discrepancies, and high clerical overhead."),
        ("Stockouts & Blind Spots", "No real-time inventory threshold tracking. Popular items unexpectedly run out of stock, directly damaging sales and customer trust."),
        ("Lack of Data Insights", "Store owners lack automated visibility into revenue trends, peak sales days, and customer purchasing frequencies."),
        ("Inaccessible AI Advisory", "Small and medium enterprises cannot afford dedicated business analysts or expensive enterprise ERP software licenses.")
    ]

    for i, (title, desc) in enumerate(cards_data_s2):
        col = i % 2
        row = i // 2
        x = Inches(0.8 + col * 5.9)
        y = Inches(1.8 + row * 2.5)
        
        card = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Inches(5.6), Inches(2.2))
        card.fill.solid()
        card.fill.fore_color.rgb = BG_CARD
        card.line.color.rgb = BG_CARD

        ctb = slide2.shapes.add_textbox(x + Inches(0.3), y + Inches(0.2), Inches(5.0), Inches(1.8))
        ctf = ctb.text_frame
        ctf.word_wrap = True
        
        cp1 = ctf.paragraphs[0]
        cp1.text = f"0{i+1}. {title}"
        cp1.font.size = Pt(16)
        cp1.font.bold = True
        cp1.font.color.rgb = PRIMARY
        
        cp2 = ctf.add_paragraph()
        cp2.text = desc
        cp2.font.size = Pt(12)
        cp2.font.color.rgb = TEXT_SUB
        cp2.space_before = Pt(8)

    # ==========================================
    # SLIDE 3: The Solution
    # ==========================================
    slide3 = prs.slides.add_slide(slide_layout)
    set_slide_background(slide3)
    add_header(slide3, "The Solution: Modern Full-Stack Platform + AI Advisor")

    cards_data_s3 = [
        ("Unified Operations Hub", "Single pane of glass managing catalogue, orders, inventory stock levels, and customer directories in real-time with responsive UI."),
        ("Automated Stock Governance", "Instant low-stock alerts (< 10 units) with 1-click restock actions and bidirectional inventory deduction upon order placement."),
        ("Generative AI Consultant", "Integrated with Google Gemini 2.0 to provide live conversational insights, restocking guidance, and customized promotions."),
        ("Pakistani Market Localization", "Native support for PKR currency formatting, Pakistani cities (Lahore, Karachi, etc.), and local payment rails (JazzCash, EasyPaisa, COD).")
    ]

    for i, (title, desc) in enumerate(cards_data_s3):
        col = i % 2
        row = i // 2
        x = Inches(0.8 + col * 5.9)
        y = Inches(1.8 + row * 2.5)
        
        card = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Inches(5.6), Inches(2.2))
        card.fill.solid()
        card.fill.fore_color.rgb = BG_CARD
        card.line.color.rgb = BG_CARD

        ctb = slide3.shapes.add_textbox(x + Inches(0.3), y + Inches(0.2), Inches(5.0), Inches(1.8))
        ctf = ctb.text_frame
        ctf.word_wrap = True
        
        cp1 = ctf.paragraphs[0]
        cp1.text = title
        cp1.font.size = Pt(16)
        cp1.font.bold = True
        cp1.font.color.rgb = ACCENT_GREEN
        
        cp2 = ctf.add_paragraph()
        cp2.text = desc
        cp2.font.size = Pt(12)
        cp2.font.color.rgb = TEXT_SUB
        cp2.space_before = Pt(8)

    # ==========================================
    # SLIDE 4: Technical Architecture & Tech Stack
    # ==========================================
    slide4 = prs.slides.add_slide(slide_layout)
    set_slide_background(slide4)
    add_header(slide4, "System Architecture & Engineering Stack")

    tech_blocks = [
        ("Frontend Client", "React 18 • Vite • Tailwind CSS", [
            "Modern Single Page Application (SPA)",
            "Dynamic revenue chart visualization",
            "Zero-latency live state & optimistic updates",
            "Lucide React icon suite & responsive styling"
        ]),
        ("Backend Services", "Python 3.14 • FastAPI • Pydantic", [
            "High-throughput asynchronous REST APIs",
            "CORS configured for secure origin calls",
            "Strict Pydantic v2 request/response schemas",
            "Comprehensive 60-assertion test suite"
        ]),
        ("Database Layer", "SQLite • Persistent Storage", [
            "Local file persistence (shopmate.db)",
            "Tables for Products, Orders, Customers, Sales",
            "Transactional safety & integrity checks",
            "Zero-configuration deployment"
        ]),
        ("AI Intelligence", "Google Gemini 2.0 Flash SDK", [
            "Live store state context injection",
            "Natural language query comprehension",
            "Rule-based graceful fallback mechanism",
            "Instant priority action recommendations"
        ])
    ]

    for i, (layer, tech, points) in enumerate(tech_blocks):
        x = Inches(0.8 + i * 2.95)
        y = Inches(1.8)
        
        card = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Inches(2.8), Inches(5.0))
        card.fill.solid()
        card.fill.fore_color.rgb = BG_CARD
        card.line.color.rgb = BG_CARD

        ctb = slide4.shapes.add_textbox(x + Inches(0.2), y + Inches(0.2), Inches(2.4), Inches(4.6))
        ctf = ctb.text_frame
        ctf.word_wrap = True
        
        p1 = ctf.paragraphs[0]
        p1.text = layer
        p1.font.size = Pt(15)
        p1.font.bold = True
        p1.font.color.rgb = PRIMARY
        
        p2 = ctf.add_paragraph()
        p2.text = tech
        p2.font.size = Pt(11)
        p2.font.bold = True
        p2.font.color.rgb = ACCENT_GREEN
        p2.space_before = Pt(4)
        
        for pt in points:
            pp = ctf.add_paragraph()
            pp.text = f"• {pt}"
            pp.font.size = Pt(10)
            pp.font.color.rgb = TEXT_SUB
            pp.space_before = Pt(8)

    # ==========================================
    # SLIDE 5: Core Features Walkthrough
    # ==========================================
    slide5 = prs.slides.add_slide(slide_layout)
    set_slide_background(slide5)
    add_header(slide5, "Platform Modules & Key Capabilities")

    features = [
        ("Dashboard & Analytics", "Interactive revenue trend graphs (7d / 30d views), peak sales day analytics, gross revenue counter, and low-stock badge notification indicators."),
        ("Live Inventory Tracking", "Granular SKU tracking, unit prices, real-time stock levels, categorization, and single-click instant inventory restocking."),
        ("Order Lifecycle & WhatsApp Receipts", "Order fulfillment tracking (Processing/Shipped/Delivered) with automatic stock sync and 1-click WhatsApp order receipts."),
        ("Customer CRM & WhatsApp Messaging", "Customer profiles with spend history and direct WhatsApp communication for promotions and personalized relationship building.")
    ]

    for i, (title, desc) in enumerate(features):
        y = Inches(1.8 + i * 1.25)
        card = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), y, Inches(11.5), Inches(1.1))
        card.fill.solid()
        card.fill.fore_color.rgb = BG_CARD
        card.line.color.rgb = BG_CARD

        ctb = slide5.shapes.add_textbox(Inches(1.1), y + Inches(0.12), Inches(10.9), Inches(0.85))
        ctf = ctb.text_frame
        ctf.word_wrap = True
        
        p1 = ctf.paragraphs[0]
        p1.text = title
        p1.font.size = Pt(15)
        p1.font.bold = True
        p1.font.color.rgb = PRIMARY
        
        p2 = ctf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(11)
        p2.font.color.rgb = TEXT_SUB
        p2.space_before = Pt(3)

    # ==========================================
    # SLIDE 6: The AI Assistant Engine
    # ==========================================
    slide6 = prs.slides.add_slide(slide_layout)
    set_slide_background(slide6)
    add_header(slide6, "Deep Dive: Google Gemini AI Business Advisor")

    # Left Column: How it Works
    card_left = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0))
    card_left.fill.solid()
    card_left.fill.fore_color.rgb = BG_CARD
    card_left.line.color.rgb = BG_CARD

    ltb = slide6.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(5.0), Inches(4.5))
    ltf = ltb.text_frame
    ltf.word_wrap = True

    lp1 = ltf.paragraphs[0]
    lp1.text = "How Context Injection Works"
    lp1.font.size = Pt(17)
    lp1.font.bold = True
    lp1.font.color.rgb = PRIMARY

    left_steps = [
        ("1. Live Snapshot Extraction", "Backend aggregates inventory status, low-stock alerts, 7-day sales figures, and pending orders into an in-memory structured context."),
        ("2. Prompt Engineering", "A localized system prompt frames Gemini as 'ShopMate AI'—an intelligent retail partner for Pakistani business owners."),
        ("3. LLM Inference (Gemini 2.0)", "Gemini generates concise, grounded advice in Pakistani Rupees (PKR) without hallucinatory answers."),
        ("4. Resilient Fallback", "If offline, the engine smoothly falls back to an internal rule-based inference engine ensuring zero downtime.")
    ]
    for stitle, sdesc in left_steps:
        sp = ltf.add_paragraph()
        sp.text = f"{stitle}: {sdesc}"
        sp.font.size = Pt(11)
        sp.font.color.rgb = TEXT_SUB
        sp.space_before = Pt(10)

    # Right Column: Example Interactions
    card_right = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.7), Inches(1.8), Inches(5.6), Inches(5.0))
    card_right.fill.solid()
    card_right.fill.fore_color.rgb = BG_CARD
    card_right.line.color.rgb = BG_CARD

    rtb = slide6.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.0), Inches(4.5))
    rtf = rtb.text_frame
    rtf.word_wrap = True

    rp1 = rtf.paragraphs[0]
    rp1.text = "Sample Queries & Capabilities"
    rp1.font.size = Pt(17)
    rp1.font.bold = True
    rp1.font.color.rgb = ACCENT_GREEN

    qa_samples = [
        ("Q: 'What products need urgent restocking?'", "A: Identifies items < 10 units (e.g. Desi Ghee & Ajwa Dates) and calculates recommended reorder quantities."),
        ("Q: 'How did the store perform this week?'", "A: Summarizes PKR gross revenue, percentage growth, and pinpoints Saturday as the peak sales day."),
        ("Q: 'Suggest a promotion for the weekend.'", "A: Analyzes top seller (Basmati Rice) and suggests bundling it with tea or cooking oil for higher basket sizes.")
    ]
    for q, a in qa_samples:
        qp = rtf.add_paragraph()
        qp.text = q
        qp.font.size = Pt(11)
        qp.font.bold = True
        qp.font.color.rgb = PRIMARY
        qp.space_before = Pt(12)

        ap = rtf.add_paragraph()
        ap.text = a
        ap.font.size = Pt(11)
        ap.font.color.rgb = TEXT_SUB
        ap.space_before = Pt(2)

    # ==========================================
    # SLIDE 7: Live Demonstration Flow
    # ==========================================
    slide7 = prs.slides.add_slide(slide_layout)
    set_slide_background(slide7)
    add_header(slide7, "Demonstration Roadmap (Live Evaluation)")

    demo_steps = [
        ("Step 1 • Health & Connection", "Demonstrate green 'FastAPI Connected' indicator showing active handshake between React frontend and Python FastAPI backend."),
        ("Step 2 • Real-Time Sales Metrics", "Inspect dynamic revenue graphs, toggle between 7-day and 30-day views, and observe reactive metric computations."),
        ("Step 3 • Inventory & Restock Action", "Navigate to catalogue, filter for low-stock items, execute restock action, and verify instant persistent update in SQLite DB."),
        ("Step 4 • Interactive AI Consultation", "Issue live business queries to ShopMate AI and showcase grounded LLM responses with actionable recommendations.")
    ]

    for i, (stitle, sdesc) in enumerate(demo_steps):
        col = i % 2
        row = i // 2
        x = Inches(0.8 + col * 5.9)
        y = Inches(1.8 + row * 2.5)
        
        card = slide7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Inches(5.6), Inches(2.2))
        card.fill.solid()
        card.fill.fore_color.rgb = BG_CARD
        card.line.color.rgb = BG_CARD

        ctb = slide7.shapes.add_textbox(x + Inches(0.3), y + Inches(0.2), Inches(5.0), Inches(1.8))
        ctf = ctb.text_frame
        ctf.word_wrap = True
        
        p1 = ctf.paragraphs[0]
        p1.text = stitle
        p1.font.size = Pt(16)
        p1.font.bold = True
        p1.font.color.rgb = PRIMARY
        
        p2 = ctf.add_paragraph()
        p2.text = sdesc
        p2.font.size = Pt(12)
        p2.font.color.rgb = TEXT_SUB
        p2.space_before = Pt(8)

    # ==========================================
    # SLIDE 8: Conclusion & Future Scope
    # ==========================================
    slide8 = prs.slides.add_slide(slide_layout)
    set_slide_background(slide8)
    add_header(slide8, "Project Impact & Future Roadmap")

    concl_data = [
        ("Key Achievements", [
            "Complete full-stack implementation with clean architectural separation",
            "Reliable persistent SQLite storage with transactional consistency",
            "Integrated Gemini 2.0 Generative AI with resilient offline fallbacks",
            "Direct 1-click WhatsApp customer receipts and promotional messaging",
            "100% test coverage with 60 backend assertions verified"
        ]),
        ("Future Roadmap", [
            "Voice-activated store management via Urdu speech-to-text",
            "Barcode & QR scanner support via mobile camera for faster checkout",
            "Multi-tenant store support for managing multiple branch locations",
            "Cloud migration to PostgreSQL and containerized Docker deployment"
        ])
    ]

    for i, (header, points) in enumerate(concl_data):
        x = Inches(0.8 + i * 5.9)
        y = Inches(1.8)
        card = slide8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Inches(5.6), Inches(4.8))
        card.fill.solid()
        card.fill.fore_color.rgb = BG_CARD
        card.line.color.rgb = BG_CARD

        ctb = slide8.shapes.add_textbox(x + Inches(0.3), y + Inches(0.3), Inches(5.0), Inches(4.2))
        ctf = ctb.text_frame
        ctf.word_wrap = True

        p1 = ctf.paragraphs[0]
        p1.text = header
        p1.font.size = Pt(18)
        p1.font.bold = True
        p1.font.color.rgb = ACCENT_GREEN

        for pt in points:
            pp = ctf.add_paragraph()
            pp.text = f"• {pt}"
            pp.font.size = Pt(12)
            pp.font.color.rgb = TEXT_SUB
            pp.space_before = Pt(12)

    # Save presentation
    output_path = "c:\\Users\\Lenovo\\Desktop\\final project\\ShopMate_AI_Presentation.pptx"
    prs.save(output_path)
    print(f"Presentation saved successfully to: {output_path}")

if __name__ == "__main__":
    create_presentation()

