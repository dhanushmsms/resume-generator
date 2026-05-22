import streamlit as st
from resumes import RESUMES
from templates import TEMPLATES
from generator import generate_content, convert_to_latex, upload_to_cloudinary, make_overleaf_url
from sheets import log_to_sheet

st.set_page_config(
    page_title="CV & Cover Letter Generator",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

  .block-container { padding-top: 0 !important; padding-bottom: 3rem; max-width: 1100px; }

  /* ── Hero banner ── */
  .hero {
    background: linear-gradient(135deg, #1e3a5f 0%, #2D4A6B 60%, #3a6491 100%);
    border-radius: 16px;
    padding: 36px 40px;
    margin-bottom: 32px;
    color: white;
  }
  .hero h1 { font-size: 28px; font-weight: 700; margin: 0 0 6px; color: white; }
  .hero p  { font-size: 15px; margin: 0; color: rgba(255,255,255,0.75); }
  .hero-badge {
    display: inline-block;
    background: rgba(255,255,255,0.15);
    border: 1px solid rgba(255,255,255,0.25);
    border-radius: 20px;
    padding: 3px 12px;
    font-size: 12px;
    font-weight: 500;
    margin-bottom: 14px;
    color: rgba(255,255,255,0.9);
  }

  /* ── Step label ── */
  .step-label {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 14px;
  }
  .step-num {
    width: 26px; height: 26px;
    background: #2D4A6B;
    color: white;
    border-radius: 50%;
    font-size: 12px;
    font-weight: 700;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
  }
  .step-title {
    font-size: 13px;
    font-weight: 600;
    color: #1e293b;
    text-transform: uppercase;
    letter-spacing: 0.7px;
  }

  /* ── Person cards ── */
  .person-card {
    border: 2px solid #e2e8f0;
    border-radius: 14px;
    padding: 20px 16px;
    text-align: center;
    background: white;
    height: 138px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    transition: box-shadow 0.2s, border-color 0.2s;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
  }
  .person-card.selected {
    border-color: #2D4A6B !important;
    background: linear-gradient(135deg, #f0f5fb, #e8f0f8);
    box-shadow: 0 4px 16px rgba(45,74,107,0.15);
  }
  .avatar {
    width: 46px; height: 46px;
    border-radius: 50%;
    font-size: 17px; font-weight: 700; color: white;
    margin: 0 auto 9px;
    display: flex; align-items: center; justify-content: center;
    box-shadow: 0 2px 8px rgba(0,0,0,0.2);
  }
  .person-name { font-weight: 600; font-size: 13.5px; color: #1e293b; margin-bottom: 3px; }
  .person-role { color: #64748b; font-size: 11.5px; }
  .selected-tick {
    font-size: 11px; color: #2D4A6B; font-weight: 600; margin-top: 5px;
  }

  /* ── Template cards ── */
  .template-card {
    border: 2px solid #e2e8f0;
    border-radius: 14px;
    padding: 14px;
    background: white;
    transition: box-shadow 0.2s, border-color 0.2s;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
  }
  .template-card.selected {
    border-color: #2D4A6B !important;
    background: linear-gradient(135deg, #f0f5fb, #e8f0f8);
    box-shadow: 0 4px 16px rgba(45,74,107,0.15);
  }
  .template-name {
    font-weight: 600; font-size: 14px; color: #1e293b;
    margin-top: 10px; margin-bottom: 3px;
    display: flex; align-items: center; gap: 6px;
  }
  .template-desc { color: #64748b; font-size: 11.5px; }

  /* ── Overleaf buttons ── */
  .overleaf-btn {
    display: block;
    background: linear-gradient(135deg, #10b981, #059669);
    color: white !important;
    padding: 12px 20px;
    border-radius: 10px;
    text-decoration: none !important;
    font-weight: 600;
    font-size: 14px;
    margin-top: 10px;
    text-align: center;
    box-shadow: 0 2px 8px rgba(16,185,129,0.3);
    transition: opacity 0.2s;
  }
  .overleaf-btn:hover { opacity: 0.9; }

  /* ── Result cards ── */
  .result-card {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 20px;
    box-shadow: 0 1px 6px rgba(0,0,0,0.06);
  }
  .result-title {
    font-size: 15px; font-weight: 700; color: #1e293b;
    margin-bottom: 14px;
    display: flex; align-items: center; gap: 8px;
  }

  /* ── Streamlit button overrides ── */
  div[data-testid="stButton"] button {
    border-radius: 8px;
    font-weight: 500;
    transition: all 0.15s;
  }
  div[data-testid="stButton"] button[kind="primary"] {
    background: linear-gradient(135deg, #2D4A6B, #3a6491) !important;
    border: none !important;
    font-size: 15px !important;
    padding: 14px !important;
    box-shadow: 0 4px 14px rgba(45,74,107,0.35) !important;
  }

  /* ── Divider ── */
  hr { border-color: #f1f5f9 !important; }
</style>
""", unsafe_allow_html=True)


# ── Session state defaults ───────────────────────────────────────────────
if "selected_person" not in st.session_state:
    st.session_state.selected_person = list(RESUMES.keys())[0]
if "selected_template" not in st.session_state:
    st.session_state.selected_template = "Modern"
if "results" not in st.session_state:
    st.session_state.results = None


# ── Hero ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-badge">✦ Powered by Claude Sonnet 4.6</div>
  <h1>CV & Cover Letter Generator</h1>
  <p>Select a person · paste a job description · pick a style — get an ATS-optimised CV and tailored cover letter, ready to compile in Overleaf.</p>
</div>
""", unsafe_allow_html=True)


# ── Step 1: Select Person ────────────────────────────────────────────────
st.markdown('<div class="step-label"><div class="step-num">1</div><div class="step-title">Select Person</div></div>', unsafe_allow_html=True)

person_cols = st.columns(3)
for i, (name, data) in enumerate(RESUMES.items()):
    with person_cols[i]:
        is_selected = st.session_state.selected_person == name
        card_class = "person-card selected" if is_selected else "person-card"
        initials = "".join(p[0] for p in name.split()[:2]).upper()
        tick = '<div class="selected-tick">✓ Selected</div>' if is_selected else ""
        st.markdown(f"""
        <div class="{card_class}">
          <div class="avatar" style="background:{data['avatar_color']}">{initials}</div>
          <div class="person-name">{name.split()[0]} {name.split()[-1]}</div>
          <div class="person-role">{data['role']}</div>
          {tick}
        </div>
        """, unsafe_allow_html=True)
        if st.button("Select" if not is_selected else "✓ Selected", key=f"person_{i}", use_container_width=True):
            st.session_state.selected_person = name
            st.session_state.results = None  # clear old results when switching person
            st.rerun()

# ── Edit Resume Content (collapsible) ───────────────────────────────────
current_person = st.session_state.selected_person
edit_key = f"resume_edit_{current_person}"
if edit_key not in st.session_state:
    st.session_state[edit_key] = RESUMES[current_person]["content"].strip()

with st.expander(f"✏️ Edit {current_person.split()[0]}'s resume content", expanded=False):
    st.caption("Changes here are used for generation but do not permanently modify the file.")
    edited_resume = st.text_area(
        "Resume content",
        value=st.session_state[edit_key],
        height=320,
        key=f"textarea_{current_person}",
        label_visibility="collapsed"
    )
    col_save, col_reset = st.columns([1, 1])
    with col_save:
        if st.button("💾 Save changes", key="save_resume", use_container_width=True):
            st.session_state[edit_key] = edited_resume
            st.success("Saved — will be used on next generation.")
    with col_reset:
        if st.button("↩️ Reset to original", key="reset_resume", use_container_width=True):
            st.session_state[edit_key] = RESUMES[current_person]["content"].strip()
            st.rerun()

st.markdown("<br>", unsafe_allow_html=True)


# ── Step 2: Select Template ──────────────────────────────────────────────
st.markdown('<div class="step-label"><div class="step-num">2</div><div class="step-title">Choose Template Style</div></div>', unsafe_allow_html=True)

tmpl_cols = st.columns(3)
for i, (tname, tdata) in enumerate(TEMPLATES.items()):
    with tmpl_cols[i]:
        is_sel = st.session_state.selected_template == tname
        card_class = "template-card selected" if is_sel else "template-card"
        tick = " ✓" if is_sel else ""
        st.markdown(f"""
        <div class="{card_class}">
          {tdata['preview_html']}
          <div class="template-name">{tname}{tick}</div>
          <div class="template-desc">{tdata['description']}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Select" if not is_sel else "✓ Selected", key=f"tmpl_{i}", use_container_width=True):
            st.session_state.selected_template = tname
            st.rerun()

# ── Customise LaTeX Template (advanced, collapsible) ─────────────────────
current_template = st.session_state.selected_template
resume_tmpl_key = f"custom_resume_tmpl_{current_template}"
cover_tmpl_key  = f"custom_cover_tmpl_{current_template}"

if resume_tmpl_key not in st.session_state:
    st.session_state[resume_tmpl_key] = TEMPLATES[current_template]["resume"]
if cover_tmpl_key not in st.session_state:
    st.session_state[cover_tmpl_key] = TEMPLATES[current_template]["cover_letter"]

with st.expander(f"🛠️ Customise {current_template} LaTeX template (advanced)", expanded=False):
    st.caption("Edit the raw LaTeX template. Claude will fill your content into this structure.")
    tab_resume, tab_cover = st.tabs(["Resume template", "Cover letter template"])
    with tab_resume:
        edited_resume_tmpl = st.text_area(
            "Resume LaTeX",
            value=st.session_state[resume_tmpl_key],
            height=350,
            key=f"tmpl_resume_area_{current_template}",
            label_visibility="collapsed"
        )
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Save resume template", key="save_rtmpl", use_container_width=True):
                st.session_state[resume_tmpl_key] = edited_resume_tmpl
                st.success("Resume template saved.")
        with col2:
            if st.button("↩️ Reset resume template", key="reset_rtmpl", use_container_width=True):
                st.session_state[resume_tmpl_key] = TEMPLATES[current_template]["resume"]
                st.rerun()
    with tab_cover:
        edited_cover_tmpl = st.text_area(
            "Cover letter LaTeX",
            value=st.session_state[cover_tmpl_key],
            height=350,
            key=f"tmpl_cover_area_{current_template}",
            label_visibility="collapsed"
        )
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Save cover template", key="save_ctmpl", use_container_width=True):
                st.session_state[cover_tmpl_key] = edited_cover_tmpl
                st.success("Cover letter template saved.")
        with col2:
            if st.button("↩️ Reset cover template", key="reset_ctmpl", use_container_width=True):
                st.session_state[cover_tmpl_key] = TEMPLATES[current_template]["cover_letter"]
                st.rerun()

st.markdown("<br>", unsafe_allow_html=True)


# ── Step 3: Job Description ──────────────────────────────────────────────
st.markdown('<div class="step-label"><div class="step-num">3</div><div class="step-title">Paste Job Description</div></div>', unsafe_allow_html=True)
job_description = st.text_area(
    label="",
    height=220,
    placeholder="Paste the full job description here — the more detail, the better the tailoring...",
    label_visibility="collapsed"
)

# ── Optional extra instructions ──────────────────────────────────────────
with st.expander("💬 Additional instructions for the AI (optional)", expanded=False):
    st.caption("Give Claude extra guidance — e.g. 'Emphasise Python skills', 'Make tone more formal', 'Target a senior-level role', 'Keep it under 400 words'.")
    st.text_area(
        "Extra instructions",
        height=100,
        placeholder="e.g. Focus on data visualisation experience. Use a confident, direct tone. Highlight leadership.",
        label_visibility="collapsed",
        key="extra_instructions"
    )

st.markdown("<br>", unsafe_allow_html=True)


# ── Load saved credentials ───────────────────────────────────────────────
_saved_anthropic    = st.secrets.get("ANTHROPIC_API_KEY", "")
_saved_cloud_name   = st.secrets.get("CLOUDINARY_CLOUD_NAME", "")
_saved_cloud_preset = st.secrets.get("CLOUDINARY_UPLOAD_PRESET", "")

with st.sidebar:
    st.markdown("### ⚙️ Configuration")

    # Anthropic
    st.markdown("**Claude API**")
    if _saved_anthropic:
        st.success("✓ Anthropic key loaded")
        anthropic_key = _saved_anthropic
        if st.checkbox("Override API key", key="override_anthropic"):
            anthropic_key = st.text_input("Anthropic API Key", type="password")
    else:
        st.warning("No Anthropic key found")
        anthropic_key = st.text_input("Anthropic API Key", type="password",
                                       help="console.anthropic.com → API Keys")
        st.caption("Save permanently: add to `.streamlit/secrets.toml`")

    st.markdown("---")

    # Cloudinary
    st.markdown("**Cloudinary**")
    if _saved_cloud_name and _saved_cloud_preset:
        st.success("✓ Cloudinary configured")
        cloud_name   = _saved_cloud_name
        cloud_preset = _saved_cloud_preset
        if st.checkbox("Override Cloudinary settings", key="override_cloud"):
            cloud_name   = st.text_input("Cloud Name",      value=_saved_cloud_name)
            cloud_preset = st.text_input("Upload Preset",   value=_saved_cloud_preset)
    else:
        st.warning("Cloudinary not configured")
        cloud_name   = st.text_input("Cloud Name",     placeholder="e.g. my-cloud")
        cloud_preset = st.text_input("Upload Preset",  placeholder="e.g. resume_preset")
        st.caption("Save permanently: add to `.streamlit/secrets.toml`")

    cloudinary_ready = bool(cloud_name and cloud_preset)
    if not cloudinary_ready:
        st.error("Cloudinary is required to generate Overleaf links.")

    # Google Sheet quick link
    _sheet_id = st.secrets.get("GOOGLE_SHEET_ID", "")
    if _sheet_id and _sheet_id != "paste-your-sheet-id-here":
        st.markdown("---")
        st.markdown(
            f'<a href="https://docs.google.com/spreadsheets/d/{_sheet_id}" target="_blank" '
            f'style="display:block;background:#1a73e8;color:white;text-align:center;'
            f'padding:9px 12px;border-radius:8px;text-decoration:none;font-weight:600;font-size:13px;">'
            f'📊 Open Generation Log</a>',
            unsafe_allow_html=True
        )


# ── Generate Button ──────────────────────────────────────────────────────
selected_person_data = RESUMES[st.session_state.selected_person]
active_resume_text   = st.session_state.get(f"resume_edit_{current_person}", selected_person_data["content"]).strip()
active_resume_tmpl   = st.session_state.get(resume_tmpl_key, TEMPLATES[current_template]["resume"])
active_cover_tmpl    = st.session_state.get(cover_tmpl_key,  TEMPLATES[current_template]["cover_letter"])
extra_instr          = st.session_state.get("extra_instructions", "").strip()

generate_clicked = st.button(
    f"✨ Generate CV + Cover Letter for {current_person.split()[0]}",
    type="primary",
    use_container_width=True
)

if generate_clicked:
    if not anthropic_key:
        st.error("Add your Anthropic API key in the sidebar.")
        st.stop()
    if not cloudinary_ready:
        st.error("Add your Cloudinary credentials in the sidebar to generate Overleaf links.")
        st.stop()
    if not job_description.strip():
        st.error("Please paste a job description.")
        st.stop()

    st.session_state.results = None
    progress_bar = st.progress(0, text="Starting...")

    try:
        progress_bar.progress(15, text="Optimising resume and writing cover letter...")
        optimized_resume, cover_letter = generate_content(
            resume_text=active_resume_text,
            job_description=job_description,
            api_key=anthropic_key,
            extra_instructions=extra_instr
        )

        progress_bar.progress(45, text="Converting resume to LaTeX...")
        resume_latex = convert_to_latex(
            plain_text=optimized_resume,
            template=active_resume_tmpl,
            doc_type="resume/CV",
            api_key=anthropic_key
        )

        progress_bar.progress(70, text="Converting cover letter to LaTeX...")
        cover_latex = convert_to_latex(
            plain_text=cover_letter,
            template=active_cover_tmpl,
            doc_type="cover letter",
            api_key=anthropic_key
        )

        progress_bar.progress(88, text="Uploading to Cloudinary...")
        resume_cloud_url = upload_to_cloudinary(resume_latex, "resume.tex", cloud_name, cloud_preset)
        cover_cloud_url  = upload_to_cloudinary(cover_latex, "cover_letter.tex", cloud_name, cloud_preset)
        resume_overleaf_url = make_overleaf_url(resume_cloud_url)
        cover_overleaf_url  = make_overleaf_url(cover_cloud_url)

        # Log to Google Sheet if configured
        _sheet_id   = st.secrets.get("GOOGLE_SHEET_ID", "")
        _sheet_creds = st.secrets.get("gcp_service_account", None)
        if _sheet_id and _sheet_creds:
            try:
                log_to_sheet(
                    sheet_id=_sheet_id,
                    credentials=dict(_sheet_creds),
                    person=current_person,
                    template=current_template,
                    job_description=job_description,
                    resume_url=resume_overleaf_url,
                    cover_url=cover_overleaf_url,
                )
            except Exception as e:
                st.warning(f"Could not save to Google Sheet: {e}")

        progress_bar.progress(100, text="Done!")
        progress_bar.empty()

        st.session_state.results = {
            "person":           current_person,
            "template":         current_template,
            "optimized_resume": optimized_resume,
            "cover_letter":     cover_letter,
            "resume_latex":     resume_latex,
            "cover_latex":      cover_latex,
            "resume_overleaf":  resume_overleaf_url,
            "cover_overleaf":   cover_overleaf_url,
        }
        st.rerun()

    except Exception as e:
        progress_bar.empty()
        st.error(f"Something went wrong: {e}")
        st.exception(e)


# ── Results (rendered from session_state — persists across reruns/downloads) ─
if st.session_state.results:
    r = st.session_state.results
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#f0fdf4,#dcfce7);border:1px solid #86efac;border-radius:12px;padding:14px 20px;margin-bottom:20px;display:flex;align-items:center;gap:10px;">
      <span style="font-size:20px">✅</span>
      <span style="font-weight:600;color:#166534">Generated for {r['person']} &nbsp;·&nbsp; {r['template']} template</span>
    </div>
    """, unsafe_allow_html=True)

    col_resume, col_cover = st.columns(2, gap="medium")

    with col_resume:
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        st.markdown('<div class="result-title">📋 Optimised CV / Resume</div>', unsafe_allow_html=True)
        with st.expander("Preview optimised text"):
            st.text(r["optimized_resume"])
        with st.expander("View LaTeX source"):
            st.code(r["resume_latex"], language="latex")
        st.markdown(f'<a class="overleaf-btn" href="{r["resume_overleaf"]}" target="_blank">📝 Open in Overleaf</a>', unsafe_allow_html=True)
        st.markdown("<div style='margin-top:8px'>", unsafe_allow_html=True)
        st.download_button(
            label="⬇️ Download resume.tex",
            data=r["resume_latex"].encode("utf-8"),
            file_name=f"{r['person'].split()[0]}_resume.tex",
            mime="text/plain",
            use_container_width=True,
            key="dl_resume"
        )
        st.markdown('</div></div>', unsafe_allow_html=True)

    with col_cover:
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        st.markdown('<div class="result-title">✉️ Cover Letter</div>', unsafe_allow_html=True)
        with st.expander("Preview cover letter text"):
            st.text(r["cover_letter"])
        with st.expander("View LaTeX source"):
            st.code(r["cover_latex"], language="latex")
        st.markdown(f'<a class="overleaf-btn" href="{r["cover_overleaf"]}" target="_blank">📝 Open in Overleaf</a>', unsafe_allow_html=True)
        st.markdown("<div style='margin-top:8px'>", unsafe_allow_html=True)
        st.download_button(
            label="⬇️ Download cover_letter.tex",
            data=r["cover_latex"].encode("utf-8"),
            file_name=f"{r['person'].split()[0]}_cover_letter.tex",
            mime="text/plain",
            use_container_width=True,
            key="dl_cover"
        )
        st.markdown('</div></div>', unsafe_allow_html=True)

    st.divider()
    if st.button("🗑️ Clear results", use_container_width=False):
        st.session_state.results = None
        st.rerun()


# ── Footer ───────────────────────────────────────────────────────────────
_sheet_id = st.secrets.get("GOOGLE_SHEET_ID", "")
sheet_link = f'&nbsp;·&nbsp; <a href="https://docs.google.com/spreadsheets/d/{_sheet_id}" target="_blank" style="color:#64748b;text-decoration:none;">📊 Generation Log</a>' if _sheet_id and _sheet_id != "paste-your-sheet-id-here" else ""

st.markdown(f"""
<div style="text-align:center;color:#94a3b8;font-size:12px;padding:20px 0 8px;">
  Powered by Claude Sonnet 4.6 &nbsp;·&nbsp; Built with Streamlit &nbsp;·&nbsp; LaTeX via Overleaf{sheet_link}
</div>
""", unsafe_allow_html=True)
