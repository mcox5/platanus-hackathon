import json
from typing import Dict, Any, Union
from services.aws import AWS_BEDROCK_CLIENT
from services.prompts import get_correct_exam_system_prompt
from utils.json_utils import fixjson
from dotenv import load_dotenv
import os


load_dotenv()

MODEL_ID = os.getenv("MODEL_ID")


async def correct_exam(
    guideline: Dict[int, Dict[str, str]],
    answer: Dict[int, Dict[str, str]]
) -> Union[Dict[str, Any], str]:
    """
    Calls AWS Bedrock to compare student answers against guideline.
    Returns parsed JSON dict with scores and feedback per question,
    or a raw string if parsing fails.
    """
    system_prompt = get_correct_exam_system_prompt(guideline, answer)
    response = AWS_BEDROCK_CLIENT.converse(
        modelId=MODEL_ID,
        messages=[
            {"role": "user", "content": [{"text": "Corrige la prueba según la pauta y respuestas."}]}  # Spanish prompt
        ],
        system=[{"text": system_prompt}],
        inferenceConfig={"temperature": 0.0}
    )
    content = response.get('output', {}).get('message', {}).get('content', [])[0].get('text', '')
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return fixjson(content)
