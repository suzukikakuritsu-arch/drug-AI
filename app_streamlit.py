# app_streamlit.py
import streamlit as st
import pandas as pd
import requests

st.title("🔬 Suzuki創薬AI クラウドMVP (GPT-4対応)")
st.write("文献1600件RAG + GPT仮説 + PDFレポート + ダッシュボード")

query = st.text_input("質問を入力してください:")
llm_option = st.selectbox("使用するLLMを選択", ["OpenAI-GPT4", "ローカルLLM"])

if st.button("実行") and query.strip():
    response = requests.post("http://localhost:8000/query", json={"query": query, "llm_option": llm_option})
    data = response.json()
    
    # 🔍 検索結果
    df = pd.DataFrame(data["retrieved"])[["title","score"]]
    st.subheader("📚 検索結果 (Top 5)")
    st.dataframe(df)
    st.bar_chart(df.set_index('title')['score'])
    
    # 🤖 AI仮説
    st.subheader("GPT-4による創薬仮説")
    st.write(data["ai_response"])
    
    # 📄 PDFダウンロード
    pdf_file = data["pdf_file"]
    st.download_button("📄 PDFレポートをダウンロード", data=open(pdf_file,"rb"), file_name=pdf_file)
