# Planner = gemini-2.0-flash GEMINI
# planner.py
import json
import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API"))

def plan(requirement: str, project_info: dict) -> dict:
    prompt = f"""
You are a senior software architect.
Given the project requirement and technical info, generate a complete project plan.

Requirement: {requirement}

Technical Info:
{json.dumps(project_info, indent=2)}

Return ONLY a valid JSON object with this structure:
{{
    "project_name": "snake_case_name",
    "folder_structure": {{
        "root": "project-name/",
        "folders": ["list", "of", "all", "folders"],
        "files": ["list", "of", "all", "files", "with", "paths"]
    }},
    "tasks": [
        {{
            "id": 1,
            "file": "exact/file/path.ext",
            "description": "what this file does",
            "depends_on": [],
            "code_hints": ["key things to implement"]
        }}
    ],
    "setup_commands": ["npm install"],
    "env_variables": ["ENV_VAR_1"],
    "order_of_execution": [1, 2, 3]
}}

IMPORTANT: Be concise. Max 15 tasks. Cover only core files, not every single file.
Return JSON only, no markdown.
"""

    # streaming so you see output live
    print("Planner thinking", end="", flush=True)
    
    response = client.models.generate_content_stream(
        model="gemini-3.8-flash",
        contents=prompt
    )

    raw = ""
    for chunk in response:
        if chunk.text:
            raw += chunk.text
            print(".", end="", flush=True)  # progress dots

    print()  # newline after dots

    try:
        result = json.loads(raw)
        return result
    except json.JSONDecodeError:
        start = raw.find("{")
        end = raw.rfind("}") + 1
        return json.loads(raw[start:end])

