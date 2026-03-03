# utils/llm_interface.py
import openai

openai.api_key = "YOUR_OPENAI_API_KEY"

def generate_ai_response(query, context_text, llm_option="OpenAI-GPT4"):
    prompt = f"以下の文献をもとに、創薬に関するAI仮説を作成してください。\n文献:\n{context_text}\n質問:\n{query}\n回答:"
    
    if llm_option == "OpenAI-GPT4":
        resp = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role":"user","content":prompt}],
            temperature=0.2
        )
        return resp.choices[0].message.content.strip()
    else:
        return "【ローカルLLM仮説】ここにAI仮説が生成されます。"
