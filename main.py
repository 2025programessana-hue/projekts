import os
import json
from pathlib import Path
from google import genai
from config import API_KEY


BASE_DIR = Path(__file__).resolve().parent
INPUT_DIR = BASE_DIR / "sample_inputs"
OUTPUT_DIR = BASE_DIR / "outputs"
PROMPT_FILE = BASE_DIR / "prompt.md"


OUTPUT_DIR.mkdir(exist_ok=True)

def load_text(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def save_json(data, file_path):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def save_report(data, file_path):
    report = f"""# CV atbilstības pārskats

**Atbilstības procents:** {data['match_score']}  
**Verdikts:** {data['verdict']}  


{data['summary']}


- """ + "\\n- ".join(data['strengths']) + """


- """ + "\\n- ".join(data['missing_requirements']) + "\\n"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(report)


client = genai.Client(api_key=API_KEY)

while True:
    word = input("Enter a word (or 'quit' to exit): ").strip()
    if word.lower() == "quit":
        break

    prompt = f"Define the word '{word}' in simple and concise terms."

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )


def analyze_cv(model, jd_text, cv_text):
    prompt_template = load_text(PROMPT_FILE)
    prompt = prompt_template.replace("{{JD_TEXT}}", jd_text).replace("{{CV_TEXT}}", cv_text)

    response = model.generate_content(prompt)
    text = response.text.strip()

    try:
        result = json.loads(text)
    except json.JSONDecodeError:
        print("Gemini did not return valid JSON. Saving raw output instead.")
        result = {
            "match_score": 0,
            "summary": "Invalid response format.",
            "strengths": [],
            "missing_requirements": [],
            "verdict": "not a match",
            "raw_output": text
        }
    return result

def main():
    print(" AI CV Vērtētājs (Gemini Flash 2.5)")
    model = genai.Client()
    jd_text = load_text(INPUT_DIR / "jd.txt")

    for i in range(1, 4):
        cv_text = load_text(INPUT_DIR / f"cv{i}.txt")
        print(f" Analizēju CV{i}...")
        result = analyze_cv(model, jd_text, cv_text)

        save_json(result, OUTPUT_DIR / f"cv{i}.json")
        save_report(result, OUTPUT_DIR / f"cv{i}_report.md")
        print(f" CV{i} apstrādāts! Rezultāts saglabāts outputs/")

if __name__ == "__main__":
    main()
