from fpdf import FPDF

def export_pdf(query, retrieved, ai_response, filename="Suzuki_AI_Report.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "🔬 Suzuki創薬AI レポート", ln=True, align="C")
    pdf.set_font("Arial", "", 12)
    pdf.ln(5)
    pdf.multi_cell(0, 8, f"質問: {query}")
    pdf.ln(5)
    pdf.multi_cell(0, 8, "🔍 検索結果:")
    for r in retrieved:
        pdf.multi_cell(0, 8, f"- {r['title']} (スコア: {r['score']:.4f})")
    pdf.ln(5)
    pdf.multi_cell(0, 8, "🤖 AI仮説:")
    pdf.multi_cell(0, 8, ai_response)
    pdf.output(filename)
    return filename
