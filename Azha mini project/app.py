"""
AI Resume Analyzer — Streamlit Web Application
Upload a PDF resume and get instant feedback on skills, ATS score,
and actionable improvement suggestions.
"""

import streamlit as st
from resume_parser import extract_text_from_pdf
from analyzer import detect_skills, calculate_ats_score, generate_suggestions


# ---------------------------------------------------------------------------
# Page configuration
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="page_facing_up",
    layout="centered",
)

# ---------------------------------------------------------------------------
# Google Fonts + Full Custom CSS
# ---------------------------------------------------------------------------
st.markdown(
    """
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">

    <style>
    /* ===================== RESET & GLOBALS ===================== */
    * { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }
    
    .stApp {
        background: #0a0a0f;
        color: #e8e8ed;
    }

    /* Hide Streamlit branding */
    #MainMenu, footer, header { visibility: hidden; }
    .stDeployButton { display: none; }

    /* Smooth scrolling */
    html { scroll-behavior: smooth; }

    /* ===================== ANIMATIONS ===================== */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    @keyframes fadeIn {
        from { opacity: 0; }
        to   { opacity: 1; }
    }
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-40px); }
        to   { opacity: 1; transform: translateX(0); }
    }
    @keyframes scaleIn {
        from { opacity: 0; transform: scale(0.85); }
        to   { opacity: 1; transform: scale(1); }
    }
    @keyframes pulseGlow {
        0%, 100% { box-shadow: 0 0 20px rgba(99, 102, 241, 0.15); }
        50%      { box-shadow: 0 0 40px rgba(99, 102, 241, 0.3); }
    }
    @keyframes gradientShift {
        0%   { background-position: 0% 50%; }
        50%  { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    @keyframes countUp {
        from { opacity: 0; transform: scale(0.5); }
        to   { opacity: 1; transform: scale(1); }
    }
    @keyframes barFill {
        from { width: 0%; }
    }
    @keyframes shimmer {
        0%   { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }

    /* ===================== HERO HEADER ===================== */
    .hero {
        text-align: center;
        padding: 3.5rem 1rem 2rem;
        animation: fadeInUp 0.8s ease-out;
    }
    .hero-tag {
        display: inline-block;
        background: rgba(99, 102, 241, 0.12);
        color: #818cf8;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 1.8px;
        text-transform: uppercase;
        padding: 6px 16px;
        border-radius: 100px;
        border: 1px solid rgba(99, 102, 241, 0.2);
        margin-bottom: 1.2rem;
    }
    .hero h1 {
        font-size: 2.8rem;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: -0.03em;
        line-height: 1.15;
        margin-bottom: 0.8rem;
    }
    .hero h1 span {
        background: linear-gradient(135deg, #818cf8, #6366f1, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-size: 200% 200%;
        animation: gradientShift 4s ease infinite;
    }
    .hero p {
        color: #71717a;
        font-size: 1.05rem;
        font-weight: 400;
        max-width: 480px;
        margin: 0 auto;
        line-height: 1.6;
    }

    /* ===================== UPLOAD AREA ===================== */
    .upload-zone {
        border: 2px dashed rgba(99, 102, 241, 0.25);
        border-radius: 16px;
        padding: 2.5rem 2rem;
        text-align: center;
        background: rgba(99, 102, 241, 0.04);
        margin: 1.5rem 0 2rem;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        animation: fadeInUp 0.8s ease-out 0.2s both;
    }
    .upload-zone:hover {
        border-color: rgba(99, 102, 241, 0.5);
        background: rgba(99, 102, 241, 0.08);
        transform: translateY(-2px);
    }
    .upload-icon {
        font-size: 2rem;
        color: #6366f1;
        margin-bottom: 0.8rem;
    }
    .upload-zone h3 {
        color: #e4e4e7;
        font-weight: 600;
        font-size: 1.1rem;
        margin-bottom: 0.4rem;
    }
    .upload-zone p {
        color: #71717a;
        font-size: 0.85rem;
    }

    /* Streamlit file uploader overrides */
    [data-testid="stFileUploader"] {
        animation: fadeInUp 0.8s ease-out 0.3s both;
    }
    [data-testid="stFileUploader"] > div {
        background: transparent;
        border: none;
        padding: 0;
    }

    /* ===================== SCORE SECTION ===================== */
    .score-container {
        background: linear-gradient(145deg, #111118, #16161f);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 20px;
        padding: 2.5rem 2rem;
        text-align: center;
        margin: 1.5rem 0;
        animation: scaleIn 0.6s ease-out;
        position: relative;
        overflow: hidden;
    }
    .score-container::before {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        border-radius: 20px 20px 0 0;
    }
    .score-container.excellent::before {
        background: linear-gradient(90deg, #10b981, #34d399);
    }
    .score-container.average::before {
        background: linear-gradient(90deg, #f59e0b, #fbbf24);
    }
    .score-container.low::before {
        background: linear-gradient(90deg, #ef4444, #f87171);
    }
    .score-title {
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 2.5px;
        text-transform: uppercase;
        color: #71717a;
        margin-bottom: 1rem;
    }
    .score-number {
        font-size: 5rem;
        font-weight: 900;
        letter-spacing: -0.04em;
        line-height: 1;
        margin-bottom: 0.5rem;
        animation: countUp 0.8s ease-out;
    }
    .score-number.excellent { color: #34d399; }
    .score-number.average   { color: #fbbf24; }
    .score-number.low       { color: #f87171; }
    .score-max {
        font-size: 1.5rem;
        color: #3f3f46;
        font-weight: 600;
    }
    .score-status {
        display: inline-block;
        padding: 6px 18px;
        border-radius: 100px;
        font-size: 0.8rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        margin-top: 0.8rem;
    }
    .score-status.excellent {
        background: rgba(16, 185, 129, 0.12);
        color: #34d399;
        border: 1px solid rgba(16, 185, 129, 0.2);
    }
    .score-status.average {
        background: rgba(245, 158, 11, 0.12);
        color: #fbbf24;
        border: 1px solid rgba(245, 158, 11, 0.2);
    }
    .score-status.low {
        background: rgba(239, 68, 68, 0.12);
        color: #f87171;
        border: 1px solid rgba(239, 68, 68, 0.2);
    }

    /* ===================== PROGRESS BAR ===================== */
    .progress-wrapper {
        margin: 1.5rem 0 2rem;
        animation: fadeIn 0.6s ease-out 0.3s both;
    }
    .progress-track {
        width: 100%;
        height: 8px;
        background: rgba(255,255,255,0.06);
        border-radius: 100px;
        overflow: hidden;
    }
    .progress-fill {
        height: 100%;
        border-radius: 100px;
        animation: barFill 1.2s cubic-bezier(0.4, 0, 0.2, 1) forwards;
        position: relative;
    }
    .progress-fill::after {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.15), transparent);
        background-size: 200% 100%;
        animation: shimmer 2s linear infinite;
    }
    .progress-fill.excellent { background: linear-gradient(90deg, #10b981, #34d399); }
    .progress-fill.average   { background: linear-gradient(90deg, #f59e0b, #fbbf24); }
    .progress-fill.low       { background: linear-gradient(90deg, #ef4444, #f87171); }

    /* ===================== SECTION HEADERS ===================== */
    .section-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin: 2.5rem 0 1.2rem;
        animation: slideInLeft 0.6s ease-out;
    }
    .section-header .icon {
        width: 36px;
        height: 36px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1rem;
        flex-shrink: 0;
    }
    .section-header .icon.skills {
        background: rgba(99, 102, 241, 0.12);
        color: #818cf8;
    }
    .section-header .icon.suggest {
        background: rgba(245, 158, 11, 0.12);
        color: #fbbf24;
    }
    .section-header h2 {
        font-size: 1.3rem;
        font-weight: 700;
        color: #fafafa;
        letter-spacing: -0.02em;
        margin: 0;
    }
    .section-header .counter {
        background: rgba(255,255,255,0.08);
        color: #a1a1aa;
        font-size: 0.72rem;
        font-weight: 600;
        padding: 3px 10px;
        border-radius: 100px;
    }

    /* ===================== SKILL CATEGORY ===================== */
    .skill-category {
        background: rgba(255,255,255,0.025);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 14px;
        padding: 1.2rem 1.4rem;
        margin-bottom: 0.8rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        animation: fadeInUp 0.5s ease-out both;
    }
    .skill-category:hover {
        background: rgba(255,255,255,0.04);
        border-color: rgba(99, 102, 241, 0.2);
        transform: translateY(-1px);
    }
    .category-name {
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        color: #71717a;
        margin-bottom: 0.8rem;
    }
    .skill-pills {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
    }
    .skill-pill {
        display: inline-flex;
        align-items: center;
        background: rgba(99, 102, 241, 0.1);
        color: #c4b5fd;
        padding: 6px 14px;
        border-radius: 8px;
        font-size: 0.82rem;
        font-weight: 500;
        border: 1px solid rgba(99, 102, 241, 0.15);
        transition: all 0.25s ease;
        letter-spacing: 0.01em;
    }
    .skill-pill:hover {
        background: rgba(99, 102, 241, 0.2);
        border-color: rgba(99, 102, 241, 0.35);
        transform: translateY(-1px);
    }
    .skill-pill .dot {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: #818cf8;
        margin-right: 8px;
        flex-shrink: 0;
    }

    /* ===================== SUGGESTIONS ===================== */
    .suggestion-card {
        background: rgba(255,255,255,0.025);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 14px;
        padding: 1.1rem 1.4rem;
        margin-bottom: 0.6rem;
        display: flex;
        align-items: flex-start;
        gap: 14px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        animation: fadeInUp 0.5s ease-out both;
    }
    .suggestion-card:hover {
        background: rgba(255,255,255,0.04);
        border-color: rgba(245, 158, 11, 0.2);
        transform: translateX(4px);
    }
    .suggestion-num {
        width: 26px;
        height: 26px;
        min-width: 26px;
        border-radius: 8px;
        background: rgba(245, 158, 11, 0.1);
        color: #fbbf24;
        font-size: 0.72rem;
        font-weight: 700;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-top: 1px;
    }
    .suggestion-text {
        color: #d4d4d8;
        font-size: 0.9rem;
        line-height: 1.55;
        font-weight: 400;
    }

    /* ===================== DIVIDER ===================== */
    .section-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.08), transparent);
        margin: 2rem 0;
    }

    /* ===================== EMPTY STATE ===================== */
    .empty-state {
        text-align: center;
        padding: 4rem 2rem;
        animation: fadeInUp 0.8s ease-out 0.4s both;
    }
    .empty-state .icon-large {
        width: 64px;
        height: 64px;
        border-radius: 16px;
        background: rgba(99, 102, 241, 0.08);
        border: 1px solid rgba(99, 102, 241, 0.15);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.6rem;
        margin: 0 auto 1.2rem;
        color: #6366f1;
    }
    .empty-state h3 {
        color: #e4e4e7;
        font-weight: 600;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
    }
    .empty-state p {
        color: #52525b;
        font-size: 0.9rem;
    }

    /* ===================== SIDEBAR ===================== */
    [data-testid="stSidebar"] {
        background: #0d0d14;
        border-right: 1px solid rgba(255,255,255,0.05);
    }
    [data-testid="stSidebar"] h2 {
        font-size: 1rem;
        font-weight: 700;
        letter-spacing: -0.01em;
    }
    .sidebar-tip {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 12px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.6rem;
        transition: all 0.25s ease;
    }
    .sidebar-tip:hover {
        background: rgba(255,255,255,0.05);
    }
    .sidebar-tip .tip-title {
        font-size: 0.82rem;
        font-weight: 600;
        color: #e4e4e7;
        margin-bottom: 4px;
    }
    .sidebar-tip .tip-desc {
        font-size: 0.76rem;
        color: #71717a;
        line-height: 1.5;
    }

    /* ===================== FOOTER ===================== */
    .footer {
        text-align: center;
        padding: 3rem 0 2rem;
        animation: fadeIn 1s ease-out;
    }
    .footer p {
        color: #3f3f46;
        font-size: 0.78rem;
        font-weight: 400;
    }

    /* ===================== TEXT EXPANDER ===================== */
    .streamlit-expanderHeader {
        background: rgba(255,255,255,0.03) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255,255,255,0.06) !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
    }

    /* Hide default Streamlit progress bar (we use custom) */
    .stProgress { display: none; }

    /* ===================== NO SKILLS STATE ===================== */
    .no-skills {
        text-align: center;
        padding: 2rem;
        color: #52525b;
        font-size: 0.9rem;
        background: rgba(255,255,255,0.02);
        border-radius: 14px;
        border: 1px dashed rgba(255,255,255,0.08);
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------------
# Hero Header
# ---------------------------------------------------------------------------
st.markdown(
    """
    <div class="hero">
        <div class="hero-tag">Resume Intelligence</div>
        <h1>AI Resume <span>Analyzer</span></h1>
        <p>
            Upload your resume and receive an in-depth analysis with 
            skill detection, ATS compatibility scoring, and tailored
            recommendations.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## Best Practices")

    tips = [
        ("Single-Column Layout", "Keep formatting simple. Avoid tables, text boxes, and multi-column designs that confuse ATS systems."),
        ("Mirror Job Keywords", "Study the job posting and naturally incorporate its exact terminology into your resume."),
        ("Keep It Concise", "Aim for 1 to 2 pages maximum. Prioritize recent and relevant experience over volume."),
        ("Dedicated Skills Section", "List your technical competencies in a clearly labeled section near the top of your resume."),
        ("Quantify Results", "Use metrics wherever possible. Numbers like percentages, revenue figures, and timelines stand out."),
    ]

    for title, desc in tips:
        st.markdown(
            f"""
            <div class="sidebar-tip">
                <div class="tip-title">{title}</div>
                <div class="tip-desc">{desc}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div class="footer">
            <p>Built with Python and Streamlit</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Upload Area
# ---------------------------------------------------------------------------
st.markdown(
    """
    <div class="upload-zone">
        <div class="upload-icon">&#x2191;</div>
        <h3>Drop your resume here</h3>
        <p>Supports PDF format &middot; Max file size 200 MB</p>
    </div>
    """,
    unsafe_allow_html=True,
)

uploaded_file = st.file_uploader(
    "Upload resume",
    type=["pdf"],
    label_visibility="collapsed",
)


# ---------------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------------
if uploaded_file is not None:
    with st.spinner("Analyzing..."):
        resume_text = extract_text_from_pdf(uploaded_file)

        if not resume_text:
            st.error(
                "Unable to extract text from this PDF. "
                "Make sure the file is not a scanned image."
            )
            st.stop()

        detected_skills = detect_skills(resume_text)
        ats_score = calculate_ats_score(detected_skills)
        suggestions = generate_suggestions(detected_skills, ats_score)

    total_skills = sum(len(v) for v in detected_skills.values())

    # --- Determine tier ---
    if ats_score >= 70:
        tier = "excellent"
        label = "Strong Profile"
    elif ats_score >= 40:
        tier = "average"
        label = "Room to Improve"
    else:
        tier = "low"
        label = "Needs Work"

    # ----- ATS Score Card -----
    st.markdown(
        f"""
        <div class="score-container {tier}">
            <div class="score-title">ATS Compatibility Score</div>
            <div class="score-number {tier}">
                {ats_score}<span class="score-max"> / 100</span>
            </div>
            <div class="score-status {tier}">{label}</div>
        </div>

        <div class="progress-wrapper">
            <div class="progress-track">
                <div class="progress-fill {tier}" style="width:{ats_score}%"></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # ----- Detected Skills -----
    st.markdown(
        f"""
        <div class="section-header">
            <div class="icon skills">&#x2726;</div>
            <h2>Detected Skills</h2>
            <span class="counter">{total_skills} found</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if detected_skills:
        for idx, (category, skills) in enumerate(detected_skills.items()):
            delay = idx * 0.08
            pills = "".join(
                f'<span class="skill-pill"><span class="dot"></span>{s.title()}</span>'
                for s in skills
            )
            st.markdown(
                f"""
                <div class="skill-category" style="animation-delay:{delay}s">
                    <div class="category-name">{category}</div>
                    <div class="skill-pills">{pills}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.markdown(
            '<div class="no-skills">No recognized skills detected. '
            "Try uploading a different resume.</div>",
            unsafe_allow_html=True,
        )

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # ----- Suggestions -----
    st.markdown(
        f"""
        <div class="section-header">
            <div class="icon suggest">&#x2192;</div>
            <h2>Recommendations</h2>
            <span class="counter">{len(suggestions)} tips</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    for i, suggestion in enumerate(suggestions, 1):
        delay = i * 0.06
        st.markdown(
            f"""
            <div class="suggestion-card" style="animation-delay:{delay}s">
                <div class="suggestion-num">{i:02d}</div>
                <div class="suggestion-text">{suggestion}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # ----- Extracted text (expandable) -----
    with st.expander("View extracted resume text"):
        st.text(resume_text)

    # ----- Footer -----
    st.markdown(
        """
        <div class="footer">
            <p>Analysis complete &middot; Results are indicative and should be used as guidance</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

else:
    st.markdown(
        """
        <div class="empty-state">
            <div class="icon-large">&#x2191;</div>
            <h3>No resume uploaded yet</h3>
            <p>Select a PDF file above to begin your analysis</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
