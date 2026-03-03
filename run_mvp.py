# run_mvp.py
"""
🔹 Suzuki創薬AIクラウドMVP 起動スクリプト
- Streamlitフロントエンド
- FastAPIバックエンド
- 1600記事RAG検索
- GPT-4 / ローカルLLM
- PDF出力
"""

import subprocess
import os
import threading

def start_fastapi():
    # FastAPI起動
    subprocess.run(["uvicorn", "backend_api:app", "--host", "0.0.0.0", "--port", "8000", "--reload"])

def start_streamlit():
    # Streamlit起動
    subprocess.run(["streamlit", "run", "app_streamlit.py"])

if __name__ == "__main__":
    # スレッドで同時起動
    t1 = threading.Thread(target=start_fastapi)
    t2 = threading.Thread(target=start_streamlit)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
