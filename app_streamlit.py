import streamlit as st
import pandas as pd
from utils.rag_search import rag_search
from utils.llm_interface import generate_ai_response
from utils.pdf_export import export_pdf

st.title("🔬 Suzuki創薬AI MVP（統合版）")
st.write("文献検索 + GPT仮説 + PDF出力を一括処理")

query = st.text_input("質問を入力してください:")

if st.button("実行") and query.strip():
    # 1. 文献検索
    retrieved = rag_search(query, top_k=5)
    
    # 2. 結果表示
    df = pd.DataFrame(retrieved)[["title","score"]]
    st.subheader("📚 検索結果 (Top 5)")
    st.dataframe(df)
    st.bar_chart(df.set_index('title')['score'])
    
    # 3. GPTによる創薬仮説
    context_text = "\n".join([r["content"] for r in retrieved])
    ai_response = generate_ai_response(query, context_text)
    st.subheader("🤖 AI創薬仮説")
    st.write(ai_response)
    
    # 4. PDF出力
    pdf_file = export_pdf(query, retrieved, ai_response)
    st.download_button("📄 PDFダウンロード", data=open(pdf_file,"rb"), file_name=pdf_file)
