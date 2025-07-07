import re
import json

# Regex để phát hiện Chương, Điều, Khoản/Điểm
chapter_pattern = re.compile(r"^CHƯƠNG\s+\w+\.?\s+.*", re.IGNORECASE)
article_pattern = re.compile(r"^Điều\s+\d+\.?.*", re.IGNORECASE)
clause_pattern = re.compile(r"^\d+\.\s+.*")  # Khoản 1. xxx
point_pattern = re.compile(r"^[a-z]\)\s+.*") # Điểm a) xxx

# Khởi tạo cấu trúc dữ liệu
data = {"title": "Nghị định 1102025NĐ-CP", "chapters": []}
current_chapter = None
current_article = None

with open("Nghị định 1102025NĐ-CP.txt", "r", encoding="utf-8") as file:
    for line in file:
        line = line.strip()
        if not line:
            continue

        if chapter_pattern.match(line):
            current_chapter = {"title": line, "articles": []}
            data["chapters"].append(current_chapter)
            current_article = None  # reset article
        elif article_pattern.match(line):
            current_article = {"title": line, "clauses": []}
            if current_chapter:
                current_chapter["articles"].append(current_article)
        elif clause_pattern.match(line):
            if current_article:
                current_article["clauses"].append({"text": line, "points": []})
        elif point_pattern.match(line):
            if current_article and current_article["clauses"]:
                current_article["clauses"][-1]["points"].append(line)

# Ghi ra file JSON
with open("nghidinh_tree.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)