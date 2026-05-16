# CV & Cover Letter Generator

Streamlit app that generates an ATS-optimised CV and tailored cover letter for 3 people using Claude Sonnet 4.6.

## Deploy to Streamlit Cloud (free, public URL)

1. Push this folder to a GitHub repo
2. Go to [share.streamlit.io](https://share.streamlit.io) → New app → connect your repo
3. Set main file: `app.py`
4. In **Settings → Secrets**, add:

```toml
ANTHROPIC_API_KEY = "sk-ant-..."
```

5. Click Deploy — you'll get a public URL in ~2 minutes

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## How to use

1. Select a person (Dhanush / Kumudha / Cindrella)
2. Pick a template style (Modern / Classic / Minimal) — visual preview shown
3. Paste the job description
4. Add your Anthropic API key in the sidebar
5. Click Generate
6. Download the `.tex` files and drag them into [Overleaf](https://overleaf.com) for PDF

## Cloudinary (optional — for direct Overleaf links)

If you want a one-click Overleaf button instead of a download:

1. Create a free [Cloudinary](https://cloudinary.com) account
2. Create an **unsigned upload preset** in Settings → Upload
3. In the sidebar, enable Cloudinary and enter your Cloud Name + Preset
