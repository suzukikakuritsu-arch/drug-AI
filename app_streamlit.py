# app_streamlit.py
import streamlit as st
import pandas as pd
from utils.rag_search import rag_search
from utils.llm_interface import generate_ai_response
from utils.pdf_export import export_pdf

st.title("🔬 Suzuki創薬AI クラウドMVP")
st.write("文献1600件RAG + GPT仮説 + PDFレポート (GitHubだけで動作)")

query = st.text_input("質問を入力してください:")
llm_option = st.selectbox("使用するLLMを選択", ["OpenAI-GPT4", "ローカルLLM"])

if st.button("実行") and query.strip():
    # 1️⃣ RAG検索
    retrieved = rag_search(query, top_k=5)
    df = pd.DataFrame(retrieved)[["title","score"]]
    st.subheader("📚 検索結果 (Top 5)")
    st.dataframe(df)
    st.bar_chart(df.set_index('title')['score'])
    
    # 2️⃣ AI仮説生成
    context_text = "\n".join([r["content"] for r in retrieved])
    ai_response = generate_ai_response(query, context_text, llm_option)
    st.subheader("🤖 AIによる創薬仮説")
    st.write(ai_response)
    
    # 3️⃣ PDF出力
    pdf_file = export_pdf(query, retrieved, ai_response)
    st.download_button("📄 PDFレポートをダウンロード", data=open(pdf_file,"rb"), file_name=pdf_file)
