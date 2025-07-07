from HiRetrieval import load_knowledge_tree, retrieve
import google.generativeai as genai

# Cấu hình API key
genai.configure(api_key="AIzaSyB98uoPTEmCa081EwCqjyQSlrtoFiPfgZ4")

def build_prompt(query, context_data):
    prompt = f"""
## Bối cảnh luật
- [Global / Chương]: {context_data['global_chapter']['title'] if context_data['global_chapter'] else ''}
- [Bridge / Điều]: {context_data['bridge_article']['article']['title'] if context_data['bridge_article'] else ''}
- [Local / Khoản]: {context_data['local_clause']['clause'] if context_data['local_clause'] else ''}
## Câu hỏi
{query}
"""
    return prompt

def answer_question(query, data):
    context_data = retrieve(query, data)
    prompt = build_prompt(query, context_data)
    
    model = genai.GenerativeModel('gemini-2.5-pro')
    response = model.generate_content(prompt)
    return response.text.strip()

if __name__ == "__main__":
    data = load_knowledge_tree("nghidinh_tree.json")
    while True:
        query = input("\nNhập câu hỏi pháp luật: ")
        answer = answer_question(query, data)
        print("\n==== CÂU TRẢ LỜI ====\n")
        print(answer)
