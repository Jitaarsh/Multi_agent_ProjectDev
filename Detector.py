# Detector =  llama3-8b-8192 GROQ
import json
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

CLIENT = Groq(api_key=os.getenv("GROQ_API"))
SUPOORTED_Tools=["python","flask","fastapi","express","django","mern","android","java"]

def detect(requirement: str) ->dict:
    response = CLIENT.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": """You are an expert software architect. 
        Analyze the project requirement and return ONLY a valid JSON object describing the complete technical setup a developer would need.
        
        Return this exact structure (fill every field based on the project):
        {
            "platform": "android | ios | web | desktop | backend | cross-platform",
            "type": "mobile_app | web_app | api | cli | desktop_app | library",
            "ide": "Android Studio | VS Code | IntelliJ IDEA | Xcode | PyCharm | etc",
            "language": "java | kotlin | python | javascript | typescript | swift | etc",
            "framework": "React | Flask | Django | Express | Spring Boot | None | etc",
            "runtime": "Node.js | JVM | Python | Browser | Android Runtime | etc",
            "build_tool": "Gradle | Maven | npm | pip | webpack | etc",
            "sdk": "Android SDK | iOS SDK | None | etc",
            "min_sdk": "API level or version if applicable else null",
            "features": ["list", "of", "core", "features"],
            "dependencies": ["key", "libraries", "or", "APIs", "needed"],
            "database": "SQLite | MongoDB | Firebase | MySQL | None | etc",
            "deployment": "Google Play | App Store | Vercel | AWS | Local | etc"
        }
        
        Rules:
        - Be specific, think like a senior developer setting up the project from scratch
        - features and dependencies must reflect exactly what the requirement needs
        - Return JSON only, no explanation, no markdown
        """
            },
            {
                "role": "user",
                "content": requirement
            }
        ],
        temperature=0.1
    )
    raw =response.choices[0].message.content.strip()

    try:
        result= json.loads(raw)
        if result["stack"] not in SUPOORTED_Tools:
            result["stack"] ="flask"
        return result
    except Exception as e:
        start = raw.find("{")
        end = raw.rfind("}") + 1
        return json.loads(raw[start:end])

