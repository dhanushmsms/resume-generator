import anthropic
import re


def generate_content(resume_text: str, job_description: str, api_key: str, extra_instructions: str = "") -> tuple[str, str]:
    """Generate optimized resume + cover letter text in one call."""
    client = anthropic.Anthropic(api_key=api_key)

    extra_block = f"\n=== ADDITIONAL INSTRUCTIONS ===\n{extra_instructions.strip()}\n" if extra_instructions.strip() else ""

    prompt = f"""You are an expert career coach, ATS optimization specialist, and professional writer.

Given a resume and a job description, produce TWO outputs:

1. An ATS-optimized resume in clean plain text
2. A professional, tailored cover letter in plain text

=== RULES FOR RESUME ===
- Rewrite/rephrase existing bullet points to match JD keywords naturally
- Do NOT invent experience, metrics, or skills that aren't in the original
- Keep all sections: Summary, Experience, Education, Skills, Certifications, Achievements
- Use strong action verbs, keep it to 2 pages worth of content
- Return plain text only, no LaTeX, no markdown

=== LENGTH RULES (target exactly TWO full pages, no more) ===
- Summary: 3-4 sentences, detailed and impactful
- Each job role: exactly 3 bullet points with metrics where possible
- Projects: exactly 2 bullet points each
- Dissertation: exactly 2 bullet points — most impactful ones only
- Skills: comprehensive, grouped by category
- Certifications: include all, names only, no descriptions
- Achievements: maximum 1, kept to a single concise line
- Languages: do NOT put on a separate section — append inline after Achievements as "Languages: English – Fluent, Hindi – Advanced"
- Everything must fit within 2 pages — Achievements and Languages must sit at the bottom of page 2, not spill onto page 3

=== RULES FOR COVER LETTER ===
- 3-4 paragraphs, professional tone
- Opening: enthusiasm for the role + brief why you're a great fit
- Middle: 2-3 specific achievements from the resume that match the JD
- Closing: thank the reader, request interview, confident call to action
- Address to "Hiring Manager" if no name is given
- DO NOT fabricate anything not in the resume
- Return plain text only
{extra_block}
=== OUTPUT FORMAT ===
Return your response EXACTLY in this format with no extra text before or after:

=== OPTIMIZED RESUME ===
[full optimized resume in plain text]

=== COVER LETTER ===
[full cover letter in plain text]

=== INPUT ===

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}
"""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4000,
        messages=[{"role": "user", "content": prompt}]
    )

    response = message.content[0].text

    resume_match = re.search(r"=== OPTIMIZED RESUME ===\n(.*?)\n=== COVER LETTER ===", response, re.DOTALL)
    cover_match = re.search(r"=== COVER LETTER ===\n(.*?)$", response, re.DOTALL)

    optimized_resume = resume_match.group(1).strip() if resume_match else response
    cover_letter = cover_match.group(1).strip() if cover_match else ""

    return optimized_resume, cover_letter


def convert_to_latex(plain_text: str, template: str, doc_type: str, api_key: str) -> str:
    """Convert plain text resume or cover letter into filled LaTeX using the given template."""
    client = anthropic.Anthropic(api_key=api_key)

    prompt = f"""You are an expert LaTeX formatter.

You will be given:
1. A {doc_type} in plain text
2. A LaTeX template

Your task: fill the template with the content from the plain text. Replace all placeholder text with the real content.

CRITICAL RULES:
- Keep ALL LaTeX commands, packages, and structure exactly as-is
- Only replace the placeholder text content (names, bullet points, dates, etc.)
- Preserve every \\usepackage, \\newcommand, \\definecolor, and structural LaTeX command
- Ensure the output is valid, compilable LaTeX
- Do NOT include markdown code fences (no ```)
- Do NOT include any explanation — output ONLY the LaTeX code

TWO PAGE RULES:
- The document should fill TWO pages — use all the content provided
- Include every section, role, project, skill, and certification from the plain text
- Use normal spacing — do not compress or shrink spacing to fit one page
- If content naturally ends before 2 pages, add appropriate spacing to fill neatly

LATEX TEMPLATE:
{template}

PLAIN TEXT CONTENT TO INSERT:
{plain_text}
"""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4000,
        messages=[{"role": "user", "content": prompt}]
    )

    latex = message.content[0].text.strip()
    # Remove markdown fences if Claude adds them
    latex = re.sub(r"^```latex\n?", "", latex)
    latex = re.sub(r"^```\n?", "", latex)
    latex = re.sub(r"\n?```$", "", latex)
    return latex.strip()


def upload_to_cloudinary(latex_code: str, filename: str, cloud_name: str, upload_preset: str) -> str:
    """Upload .tex file to Cloudinary using an unsigned preset. Returns the secure URL."""
    import requests

    response = requests.post(
        f"https://api.cloudinary.com/v1_1/{cloud_name}/raw/upload",
        files={"file": (filename, latex_code.encode("utf-8"), "text/plain")},
        data={"upload_preset": upload_preset}
    )
    response.raise_for_status()
    return response.json()["secure_url"]


def make_overleaf_url(cloudinary_url: str) -> str:
    from urllib.parse import quote
    return f"https://www.overleaf.com/docs?snip_uri={quote(cloudinary_url)}"
