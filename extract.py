import json
import os
import time
from groq import Groq
from dotenv import load_dotenv
from schemas import ShipmentExtraction
from prompt import SYSTEM_PROMPT

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def call_llm(prompt: str):
    for attempt in range(3):
        try:
            response = client.chat.completions.create(
                model="llama-3.1-70b-versatile",
                temperature=0,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
            )
            return response.choices[0].message.content
        except Exception:
            time.sleep(2 ** attempt)
    return None


def extract_email(email: dict, ports_reference: str):
    prompt = f"""
Subject:
{email['subject']}

Body:
{email['body']}

UN/LOCODE Ports Reference:
{ports_reference}
"""

    raw_output = call_llm(prompt)

    if not raw_output:
        return ShipmentExtraction(
            id=email["id"],
            product_line=None,
            origin_port_code=None,
            origin_port_name=None,
            destination_port_code=None,
            destination_port_name=None,
            incoterm=None,
            cargo_weight_kg=None,
            cargo_cbm=None,
            is_dangerous=False
        ).dict()

    data = json.loads(raw_output)
    data["id"] = email["id"]

    return ShipmentExtraction(**data).dict()
