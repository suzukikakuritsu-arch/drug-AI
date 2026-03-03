import streamlit as st
import openai
import json

st.set_page_config(layout="wide", page_title="Suzuki創薬AI")
st.title("🔬 **Suzuki創薬AI** - IPS理論創薬支援")
st.markdown("### 鈴木悠起也理論 × GPT-4で即仮説生成")

# OpenAI APIキー
api_key = st.sidebar.text_input("🔑 OpenAI APIキー", type="password")
if not api_key:
    st.info("👈 サイドバーでOpenAI APIキーを入力")
    st.stop()

openai.api_key = api_key

# 鈴木理論プロンプト
query = st.text_area("🔍 創薬課題を入力", 
                    placeholder="例：次世代抗がん剤設計の課題と解決策")
llm_model = st.sidebar.selectbox("モデル", ["gpt-4", "gpt-3.5-turbo"])

if st.button("🚀 **鈴木理論で解析**", type="primary"):
    with st.spinner("IPS理論解析中..."):
        prompt = f"""
        あなたは鈴木悠起也博士（IPS情報創発理論創始者）です。
        
        鈴木理論の3原則：
        1. 非Markovian長期記憶（過去履歴全記憶）
        2. 情報密度J(t)最大化  
        3. 黄金比φ最適化（1.618）
        
        課題：{query}
        
        出力形式：
        1. 課題分析（IPS理論視点）
        2. 創薬ターゲット提案
        3. 分子設計指針（SMILES推奨）
        4. 鈴木理論適用根拠
        """
        
        try:
            response = openai.ChatCompletion.create(
                model=llm_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=2000
            )
            
            answer = response.choices[0].message.content
            
            # 結果表示
            st.subheader("🎯 **鈴木創薬解析結果**")
            st.markdown(answer)
            
            # PDFダウンロード
            pdf_content = f"""
# Suzuki創薬AI解析レポート

## 課題
{query}

## IPS理論解析
{answer}

---
生成：Suzuki創薬AI v1.0 | {st.session_state.get('timestamp', '今日')}
            """
            
            st.download_button(
                "📄 PDF保存",
                data=pdf_content.encode(),
                file_name=f"suzuki_analysis_{int(time.time())}.txt",
                mime="text/plain"
            )
            
            st.session_state.last_result = answer
            
        except Exception as e:
            st.error(f"エラー：{str(e)}")
            st.info("APIキーの確認をお願いします")

# 履歴
if 'last_result' in st.session_state:
    with st.expander("📋 前回の解析"):
        st.markdown(st.session_state.last_result[:500] + "...")
