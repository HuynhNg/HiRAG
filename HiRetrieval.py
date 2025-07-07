import json
from difflib import SequenceMatcher

def load_knowledge_tree(json_file):
    with open(json_file, "r", encoding="utf-8") as f:
        return json.load(f)

def similarity(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def retrieve(query, data, top_k=1):
    # 1. Global level: Chương
    chapter_scores = []
    for chapter in data["chapters"]:
        score = similarity(query, chapter["title"])
        chapter_scores.append((score, chapter))
    chapter_scores.sort(reverse=True, key=lambda x: x[0])
    top_chapters = [c for _, c in chapter_scores[:top_k]]

    # 2. Bridge level: Điều
    article_scores = []
    for chapter in top_chapters:
        for article in chapter["articles"]:
            score = similarity(query, article["title"])
            article_scores.append((score, article, chapter))
    article_scores.sort(reverse=True, key=lambda x: x[0])
    top_articles = article_scores[:top_k]

    # 3. Local level: Khoản & Điểm
    clause_scores = []
    for score_a, article, chapter in top_articles:
        for clause in article.get("clauses", []):
            clause_text = clause["text"]
            score_c = similarity(query, clause_text)
            clause_scores.append((score_c, clause_text, clause.get("points", []), article, chapter))
    clause_scores.sort(reverse=True, key=lambda x: x[0])
    top_clauses = clause_scores[:top_k]

    # Ghép kết quả lại
    results = {
        "global_chapter": top_chapters[0] if top_chapters else None,
        "bridge_article": {
            "article": top_articles[0][1],
            "chapter": top_articles[0][2]
        } if top_articles else None,
        "local_clause": {
            "clause": top_clauses[0][1],
            "points": top_clauses[0][2],
            "article": top_clauses[0][3],
            "chapter": top_clauses[0][4]
        } if top_clauses else None
    }
    return results

# Ví dụ test nhanh
if __name__ == "__main__":
    data = load_knowledge_tree("nghidinh_tree.json")
    query = input("Nhập câu hỏi: ")
    results = retrieve(query, data)
    print("\n==== KẾT QUẢ TRUY VẤN ====")
    if results["global_chapter"]:
        print("\n[Global] Chương liên quan nhất:", results["global_chapter"]["title"])
    if results["bridge_article"]:
        print("\n[Bridge] Điều liên quan nhất:", results["bridge_article"]["article"]["title"])
    if results["local_clause"]:
        print("\n[Local] Khoản/Điểm liên quan nhất:", results["local_clause"]["clause"])
        if results["local_clause"]["points"]:
            print("  Các điểm:", ", ".join(results["local_clause"]["points"]))
