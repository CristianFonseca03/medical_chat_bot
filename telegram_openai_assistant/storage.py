# storage.py

import json
from pathlib import Path

qa_file = Path("questions_answers.json")

if not qa_file.is_file():
    with open(qa_file, "w") as file:
        json.dump([], file)

def save_qa(telegram_id, username, question, answer):
    with open(qa_file, "r+") as file:
        data = json.load(file)
        data.append({
            "telegram_id": telegram_id,
            "username": username,
            "question": question,
            "answer": answer
        })
        file.seek(0)
        json.dump(data, file, indent=4)
