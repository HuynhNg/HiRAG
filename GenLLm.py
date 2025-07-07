from HiRetrieval import load_knowledge_tree, retrieve
import google.generativeai as genai
import time

# Cấu hình API key
genai.configure(api_key="api_key_here") 

def build_prompt(query, context_data):
    prompt = f"""
## Bối cảnh luật
- [Global / Chương]: {context_data['global_chapter']['title'] if context_data['global_chapter'] else 'Không có thông tin chương'}
- [Bridge / Điều]: {context_data['bridge_article']['article']['title'] if context_data['bridge_article'] else 'Không có thông tin điều'}
- [Local / Khoản]: {context_data['local_clause']['clause'] if context_data['local_clause'] else 'Không có thông tin khoản'}
## Câu hỏi
{query.strip()}
"""
    return prompt

def answer_question(query, data):
    try:
        context_data = retrieve(query, data)
        prompt = build_prompt(query, context_data)
        print("Prompt:", prompt)

        model = genai.GenerativeModel('gemini-2.5-flash') 
        response = model.generate_content(prompt, generation_config={"max_output_tokens": 500})

        if response.candidates and response.candidates[0].finish_reason == 2:
            return "Lỗi: Yêu cầu bị chặn do chính sách an toàn của Google. Vui lòng thử lại với câu hỏi khác hoặc kiểm tra nội dung prompt."
        if not response.parts:
            return "Lỗi: Không nhận được nội dung hợp lệ từ mô hình. Vui lòng kiểm tra câu hỏi hoặc dữ liệu đầu vào."
        time.sleep(60)
        return response.text.strip()
    except Exception as e:
        return f"Lỗi: {str(e)}. Vui lòng kiểm tra API key, dữ liệu đầu vào, hoặc câu hỏi."

if __name__ == "__main__":
    data = load_knowledge_tree("nghidinh_tree.json")
    while True:
        query = input("\nNhập câu hỏi pháp luật (hoặc 'thoát' để dừng): ")
        if query.lower() == "thoát":
            break
        cleaned_query = query.replace("Nhập câu hỏi pháp luật: ", "").strip()
        answer = answer_question(cleaned_query, data)
        print("\n==== CÂU TRẢ LỜI ====\n")
        print(answer)