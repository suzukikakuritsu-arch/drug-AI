# drug-AI
suzuki_drug_ai/
│
├─ app_streamlit.py       # Streamlitフロントエンド（質問入力 → GPT仮説 → PDF）
├─ backend_api.py         # FastAPIバックエンド（ユーザー認証・ログ・課金）
├─ 1600_articles.json     # 文献データ
├─ embeddings.npy         # 事前計算済み埋め込み
├─ requirements.txt
└─ utils/
   ├─ rag_search.py       # FAISS検索関数
   ├─ pdf_export.py       # PDF出力関数
   ├─ llm_interface.py    # GPT-4 / ローカルLLM呼び出し
   └─ auth.py             # JWT/OAuth認証
