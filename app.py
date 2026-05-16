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
  .block-container { padding-top: 2rem; padding-bottom: 2rem; }

  .person-card {
    border: 2px solid #e0e0e0;
    border-radius: 12px;
    padding: 20px 16px;
    text-align: center;
    background: white;
    height: 130px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }
  .person-card.selected { border-color: #2D4A6B !important; background: #f0f4f8; }

  .avatar {
    width: 44px; height: 44px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 18px; font-weight: bold; color: white;
    margin: 0 auto 8px;
  }
  .person-name { font-weight: 600; font-size: 14px; margin-bottom: 2px; }
  .person-role { color: #666; font-size: 12px; }

  .template-card {
    border: 2px solid #e0e0e0;
    border-radius: 12px;
    padding: 12px;
    background: white;
  }
  .template-card.selected { border-color: #2D4A6B !important; background: #f0f4f8; }
  .template-name { font-weight: 600; font-size: 14px; margin-top: 8px; margin-bottom: 2px; }
  .template-desc { color: #666; font-size: 12px; }

  .step-label {
    font-size: 12px;
    font-weight: 600;
    color: #888;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-bottom: 10px;
  }

  .overleaf-btn {
    display: inline-block;
    background: #4CAF88;
    color: white !important;
    padding: 10px 20px;
    border-radius: 6px;
    text-decoration: none !important;
    font-weight: 600;
    font-size: 14px;
    margin-top: 8px;
  }
  .overleaf-btn:hover { background: #3d9970; }

  div[data-testid="stButton"] button { border-radius: 8px; }
</style>
""", unsafe_allow_html=True)


# ── Session state defaults ───────────────────────────────────────────────
if "selected_person" not in st.session_state:
    st.session_state.selected_person = list(RESUMES.keys())[0]
if "selected_template" not in st.session_state:
    st.session_state.selected_template = "Modern"
if "results" not in st.session_state:
    st.session_state.results = None


# ── Header ──────────────────────────────────────────────────────────────
st.markdown("## 📄 CV & Cover Letter Generator")
st.markdown("Select a person, paste the job description, pick a template — get a polished CV and cover letter ready for Overleaf.")
st.divider()


# ── Step 1: Select Person ────────────────────────────────────────────────
st.markdown('<div class="step-label">Step 1 — Select Person</div>', unsafe_allow_html=True)

person_cols = st.columns(3)
for i, (name, data) in enumerate(RESUMES.items()):
    with person_cols[i]:
        is_selected = st.session_state.selected_person == name
        card_class = "person-card selected" if is_selected else "person-card"
        initials = "".join(p[0] for p in name.split()[:2]).upper()
        st.markdown(f"""
        <div class="{card_class}">
          <div class="avatar" style="background:{data['avatar_color']}">{initials}</div>
          <div class="person-name">{name.split()[0]} {name.split()[-1]}</div>
          <div class="person-role">{data['role']}</div>
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
st.markdown('<div class="step-label">Step 2 — Choose Template Style</div>', unsafe_allow_html=True)

tmpl_cols = st.columns(3)
for i, (tname, tdata) in enumerate(TEMPLATES.items()):
    with tmpl_cols[i]:
        is_sel = st.session_state.selected_template == tname
        card_class = "template-card selected" if is_sel else "template-card"
        st.markdown(f"""
        <div class="{card_class}">
          {tdata['preview_html']}
          <div class="template-name">{tname}</div>
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
st.markdown('<div class="step-label">Step 3 — Paste Job Description</div>', unsafe_allow_html=True)
job_description = st.text_area(
    label="",
    height=220,
    placeholder="Paste the full job description here — the more detail, the better the tailoring...",
    label_visibility="collapsed"
)

# ── Optional extra instructions ──────────────────────────────────────────
with st.expander("💬 Additional instructions for the AI (optional)", expanded=False):
    st.caption("Give Claude extra guidance — e.g. 'Emphasise Python skills', 'Make tone more formal', 'Target a senior-level role', 'Keep it under 400 words'.")
    extra_instructions = st.text_area(
        "Extra instructions",
        height=100,
        placeholder="e.g. Focus on data visualisation experience. Use a confident, direct tone. Highlight leadership.",
        label_visibility="collapsed"
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


# ── Generate Button ──────────────────────────────────────────────────────
selected_person_data = RESUMES[st.session_state.selected_person]
active_resume_text   = st.session_state.get(f"resume_edit_{current_person}", selected_person_data["content"]).strip()
active_resume_tmpl   = st.session_state.get(resume_tmpl_key, TEMPLATES[current_template]["resume"])
active_cover_tmpl    = st.session_state.get(cover_tmpl_key,  TEMPLATES[current_template]["cover_letter"])
extra_instr          = st.session_state.get("extra_instructions", "")

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
            extra_instructions=extra_instructions if extra_instructions.strip() else ""
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
    st.success(f"Generated for **{r['person']}** using the **{r['template']}** template.")
    st.divider()

    col_resume, col_cover = st.columns(2)

    with col_resume:
        st.markdown("### 📋 Optimised CV / Resume")
        with st.expander("Preview optimised text", expanded=False):
            st.text(r["optimized_resume"])
        with st.expander("View LaTeX code", expanded=False):
            st.code(r["resume_latex"], language="latex")

        st.markdown(f'<a class="overleaf-btn" href="{r["resume_overleaf"]}" target="_blank">📝 Open Resume in Overleaf</a>', unsafe_allow_html=True)
        st.download_button(
            label="⬇️ Download resume.tex",
            data=r["resume_latex"].encode("utf-8"),
            file_name=f"{r['person'].split()[0]}_resume.tex",
            mime="text/plain",
            use_container_width=True,
            key="dl_resume"
        )

    with col_cover:
        st.markdown("### ✉️ Cover Letter")
        with st.expander("Preview cover letter text", expanded=False):
            st.text(r["cover_letter"])
        with st.expander("View LaTeX code", expanded=False):
            st.code(r["cover_latex"], language="latex")

        st.markdown(f'<a class="overleaf-btn" href="{r["cover_overleaf"]}" target="_blank">📝 Open Cover Letter in Overleaf</a>', unsafe_allow_html=True)
        st.download_button(
            label="⬇️ Download cover_letter.tex",
            data=r["cover_latex"].encode("utf-8"),
            file_name=f"{r['person'].split()[0]}_cover_letter.tex",
            mime="text/plain",
            use_container_width=True,
            key="dl_cover"
        )

    st.divider()
    if st.button("🗑️ Clear results", use_container_width=False):
        st.session_state.results = None
        st.rerun()


# ── Footer ───────────────────────────────────────────────────────────────
st.caption("Powered by Claude Sonnet 4.6 · Built with Streamlit · LaTeX compiled via Overleaf")
