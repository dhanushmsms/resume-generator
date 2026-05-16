import gspread
from datetime import datetime


def log_to_sheet(
    sheet_id: str,
    credentials: dict,
    person: str,
    template: str,
    job_description: str,
    resume_url: str,
    cover_url: str,
):
    """Append one row to the Google Sheet with the generated links."""
    gc = gspread.service_account_from_dict(credentials)
    sheet = gc.open_by_key(sheet_id).sheet1

    # Create header row if the sheet is empty
    if sheet.row_count == 0 or not sheet.row_values(1):
        sheet.append_row(
            ["Timestamp", "Person", "Template", "Job Description (first 80 chars)",
             "Resume (Overleaf)", "Cover Letter (Overleaf)"],
            value_input_option="RAW"
        )

    jd_preview = job_description.strip().replace("\n", " ")[:80] + "..."

    sheet.append_row(
        [
            datetime.now().strftime("%Y-%m-%d %H:%M"),
            person,
            template,
            jd_preview,
            resume_url,
            cover_url,
        ],
        value_input_option="RAW"
    )
