from datetime import datetime, timezone


def parsed_resume_schema(analysis_id: str, raw_text: str, extracted_data: dict) -> dict:
    return {
        "analysis_id": analysis_id,
        "raw_text": raw_text,
        "extracted_data": extracted_data,
        "created_at": datetime.now(timezone.utc),
    }
