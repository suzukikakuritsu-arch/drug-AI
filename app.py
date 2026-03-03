import streamlit as st
import pandas as pd

# drug-AIのutilsモジュール（既に存在）
from utils.rag_search import rag_search
from utils.llm_interface import generate_ai_response
from utils.pdf_export import export_pdf

st.set_page_config(page_title="Suzuki創薬AI", layout="wide")
st.title("🔬 **Suzuki創薬AI**")
st.markdown("鈴木理論 × RAG × GPT-4 で創薬仮説を即生成")

# サイドバー
st.sidebar.header("設定")
top_k = st.sidebar.slider("検索数", 3, 10, 5)

# メイン入力
query = st.text_input("🔍 創薬質問を入力（例：次世代抗がん剤設計）")
if st.button("🚀 実行", type="primary") and query:
    
    with st.spinner("鈴木理論で解析中..."):
        # 1. RAG検索
        retrieved = rag_search(query, top_k=top_k)
        
        # 2. 結果表示
        if retrieved:
            df = pd.DataFrame(retrieved)[["title", "score"]]
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("📚 検索結果")
                st.dataframe(df)
            with col2:
                st.subheader("📈 類似度")
                st.bar_chart(df.set_index("title")["score"])
            
            # 3. AI回答生成
            context = "\n".join([r.get("content", "") for r in retrieved])
            answer = generate_ai_response(query, context)
            
            st.subheader("🎯 **鈴木創薬仮説**")
            st.markdown(answer)
            
            # 4. PDFダウンロード
            pdf_data = export_pdf(query, retrieved, answer)
            st.download_button(
                "📄 PDFレポート保存", 
                pdf_data, 
                f"suzuki_drug_report_{int(time.time())}.pdf"
            )
        else:
            st.warning("関連文献が見つかりませんでした")
    
    st.success("✅ 解析完了！")

st.markdown("---")
st.caption("© 2026 Suzuki創薬AI. Powered by IPS理論")
