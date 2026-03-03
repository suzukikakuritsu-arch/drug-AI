import openai
import os

# Streamlit Cloud の Secrets から OPENAI_API_KEY を設定
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_ai_response(query, context_text):
    prompt = f"以下の文献を元に創薬仮説を作成してください。\n文献:\n{context_text}\n質問:\n{query}\n回答:"
    resp = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role":"user","content":prompt}],
        temperature=0.2
    )
    return resp.choices[0].message.content.strip()
