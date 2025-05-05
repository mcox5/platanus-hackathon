import aiofiles
from typing import List, Dict


async def proses_file_function(file_path: str) -> Dict:
    """
    Reads the file at file_path and runs OCR/Text extraction logic.
    Returns a dict with job_status and result text.
    """
    # Example stub: read file locally
    async with aiofiles.open(file_path, mode="r") as f:
        text = await f.read()
    return {"job_status": "SUCCEEDED", "result": text}


def parse_ocr_function(ocr_results: str) -> Dict[int, Dict[str, str]]:
    """
    Parses raw OCR string into a mapping of question index to
    a dict with 'question' and 'answer'.
    """
    parsed: Dict[int, Dict[str, str]] = {}
    lines = ocr_results.splitlines()
    for idx, line in enumerate(lines):
        # simplistic parsing example: split question and answer by '--'
        if '--' in line:
            q, a = line.split('--', 1)
        else:
            q, a = line, ''
        parsed[idx] = {"question": q.strip(), "answer": a.strip()}
    return parsed