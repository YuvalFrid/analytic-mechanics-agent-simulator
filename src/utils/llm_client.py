import os
import base64
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def encode_image(image_path: str) -> str:
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def call_llm(system_prompt: str, user_prompt: str, model: str, image_path: str = None) -> dict:
    if image_path:
        base64_image = encode_image(image_path)
        user_content = [
            {"type": "text", "text": user_prompt},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
        ]
    else:
        user_content = user_prompt
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
                ],response_format={"type":"json_object"}
        )
    except Exception as e:
        print(f"API call failed: {e}")
        return None
    raw = response.choices[0].message.content
    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"LLM returned invalid JSON: {e}")
        print(f"Raw response was: {raw}")
        return None


def call_llm_raw(system_prompt: str, user_prompt: str, model: str) -> str:
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
    except Exception as e:
        print(f"API call failed: {e}")
        return None
    
    return response.choices[0].message.content
