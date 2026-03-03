# backend_api.py
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from utils.auth import get_current_user
from utils.rag_search import rag_search
from utils.llm_interface import generate_ai_response
from utils.pdf_export import export_pdf
from utils.db import log_query, User

app = FastAPI(title="Suzuki創薬AI API")

class QueryRequest(BaseModel):
    query: str
    llm_option: str  # "OpenAI-GPT4" または "ローカルLLM"

@app.post("/query")
def query_endpoint(req: QueryRequest, user: User = Depends(get_current_user)):
    # 1️⃣ RAG検索
    retrieved = rag_search(req.query, top_k=5)
    context_text = "\n".join([r["content"] for r in retrieved])
    
    # 2️⃣ GPT-4生成
    ai_response = generate_ai_response(req.query, context_text, req.llm_option)
    
    # 3️⃣ PDF生成
    pdf_file = export_pdf(req.query, retrieved, ai_response)
    
    # 4️⃣ ログ保存
    log_query(user.id, req.query, retrieved, ai_response)
    
    return {"retrieved": retrieved, "ai_response": ai_response, "pdf_file": pdf_file}
