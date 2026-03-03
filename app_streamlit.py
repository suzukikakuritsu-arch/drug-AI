import streamlit as st
import pandas as pd
import io
import time
from typing import List, Dict, Any
import streamlit.components.v1 as components

# 自作モジュール
from utils.rag_search import rag_search
from utils.llm_interface import generate_ai_response
from utils.pdf_export import export_pdf
from utils.auth import get_current_user  # 簡易版

# ページ設定
st.set_page_config(
    page_title="Suzuki創薬AI", 
    page_icon="🔬",
    layout="wide"
)

st.title("🔬 Suzuki創薬AI MVP v2.0")
st.markdown("**文献RAG + GPT仮説 + PDF一括出力**")

# サイドバー（設定）
st.sidebar.header("⚙️ 設定")
llm_option = st.sidebar.selectbox("LLM選択", ["OpenAI-GPT4", "ローカルLLM"])
top_k = st.sidebar.slider("検索数", 3, 10, 5)

# 認証（簡易版）
if 'user_id' not in st.session_state:
    st.session_state.user_id = "guest_" + str(int(time.time()))

# メイン入力
col1, col2 = st.columns([3,1])
with col1:
    query = st.text_input("🔍 創薬質問を入力:", max_chars=1000)
with col2:
    run_button = st.button("🚀 実行", type="primary", use_container_width=True)

if run_button and query.strip():
    with st.spinner("鈴木理論で解析中..."):
        # 進捗バー
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # 1. RAG検索（進捗20%）
        status_text.text("📚 鈴木理論RAG検索中...")
        progress_bar.progress(0.2)
        retrieved: List[Dict[str, Any]] = rag_search(query, top_k=top_k)
        
        # 2. 結果表示（進捗50%）
        progress_bar.progress(0.5)
        status_text.text("📊 結果整理中...")
        
        df = pd.DataFrame(retrieved)[["title", "score"]].head(top_k)
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("📚 Top検索結果")
            st.dataframe(df.style.format({"score": "{:.3f}"}), use_container_width=True)
        with col2:
            st.subheader("📈 スコア分布")
            st.bar_chart(df.set_index('title')['score'])
        
        # 3. GPT仮説生成（進捗80%）
        progress_bar.progress(0.8)
        status_text.text("🤖 鈴木IPS理論で仮説生成中...")
        context_text = "\n".join([r["content"] for r in retrieved])
        ai_response = generate_ai_response(query, context_text, llm_option)
        
        st.subheader("🎯 **鈴木創薬仮説**")
        st.markdown(ai_response)
        
        # 4. PDF生成＋ダウンロード（100%）
        progress_bar.progress(1.0)
        status_text.text("📄 PDFレポート生成完了！")
        
        # PDFバイナリ直接生成（ファイル不要）
        pdf_bytes = export_pdf(query, retrieved, ai_response)
        st.download_button(
            label="📥 PDFレポート保存",
            data=pdf_bytes,
            file_name=f"suzuki_drug_report_{int(time.time())}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
        
        # セッション記録
        st.session_state.last_query = query
        st.session_state.last_response = ai_response
        st.success("✅ 解析完了！")

# 履歴表示
if 'last_query' in st.session_state:
    st.subheader("📋 実行履歴")
    with st.expander("最終結果"):
        st.write(f"**クエリ**: {st.session_state.last_query}")
        st.write(f"**仮説**: {st.session_state.last_response[:500]}...")
