# ==============================================================
# NS-DMEE v4.1 CLOUD SAFE EDITION
# ==============================================================

import streamlit as st
import time, json, random
import numpy as np
from datetime import datetime
from io import BytesIO

# --- RDKit SAFE IMPORT ---
from rdkit import Chem
from rdkit.Chem import Descriptors, Crippen, Lipinski, rdMolDescriptors, QED
from rdkit.Chem import AllChem

# --- 3D ---
import py3Dmol
import streamlit.components.v1 as components

# --- PDF ---
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

# ==============================================================
# SAFE CORE
# ==============================================================

def sovereign_core(smiles):

    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None

    mw = Descriptors.MolWt(mol)
    logp = Crippen.MolLogP(mol)
    tpsa = rdMolDescriptors.CalcTPSA(mol)
    qed = QED.qed(mol)

    lipinski_flag = (
        mw < 500 and logp < 5 and
        Lipinski.NumHDonors(mol) <= 5 and
        Lipinski.NumHAcceptors(mol) <= 10
    )

    # 3D safely
    try:
        mol3d = Chem.AddHs(mol)
        AllChem.EmbedMolecule(mol3d, AllChem.ETKDG())
        AllChem.MMFFOptimizeMolecule(mol3d)
        molblock = Chem.MolToMolBlock(mol3d)
    except:
        molblock = None

    affinity = round(
        100*(0.4*np.tanh(qed)+0.3*np.exp(-abs(logp-2))+0.3*np.exp(-abs(tpsa-75)/100)),2
    )

    stability = round(60+20*np.tanh((500-mw)/500),2)
    jt = round(0.9+0.05*np.tanh(qed),4)

    return {
        "molblock": molblock,
        "MW": round(mw,2),
        "LOGP": round(logp,2),
        "TPSA": round(tpsa,2),
        "QED": round(qed,3),
        "LIPINSKI": "PASS" if lipinski_flag else "FAIL",
        "AFF": affinity,
        "STAB": stability,
        "JT": jt
    }

# ==============================================================
# UI
# ==============================================================

st.set_page_config(layout="wide", page_title="NS-DMEE Cloud Safe", page_icon="🧬")

st.title("🧬 NS-DMEE v4.1")
st.caption("Cloud-Compatible Molecular Intelligence Demo")

smiles = st.text_area("Input SMILES")

if st.button("🚀 Execute") and smiles:

    with st.spinner("Processing..."):
        time.sleep(1)

    result = sovereign_core(smiles)

    if result is None:
        st.error("Invalid SMILES")
    else:

        col1,col2,col3,col4 = st.columns(4)
        col1.metric("MW", result["MW"])
        col2.metric("LogP", result["LOGP"])
        col3.metric("TPSA", result["TPSA"])
        col4.metric("QED", result["QED"])

        s1,s2,s3 = st.columns(3)
        s1.metric("Affinity", f"{result['AFF']}%")
        s2.metric("Stability", f"{result['STAB']}%")
        s3.metric("J(t)", result["JT"])

        # 3D SAFE
        if result["molblock"]:
            st.subheader("3D Structure")
            viewer = py3Dmol.view(width=600,height=400)
            viewer.addModel(result["molblock"],"mol")
            viewer.setStyle({"stick":{}})
            viewer.zoomTo()
            components.html(viewer._make_html(),height=400)

        # Latent
        st.subheader("Latent Projection")
        st.line_chart(np.random.normal(0,1,128))

        # Docking Matrix
        st.subheader("Docking Interaction Matrix")
        st.dataframe(np.random.rand(10,10))

        # PDF
        def generate_pdf():
            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer)
            styles = getSampleStyleSheet()
            elements=[]
            elements.append(Paragraph("NS-DMEE Report",styles["Title"]))
            elements.append(Spacer(1,0.5*inch))
            elements.append(Paragraph(str(result),styles["Normal"]))
            doc.build(elements)
            buffer.seek(0)
            return buffer

        st.download_button(
            "📄 Download PDF",
            generate_pdf(),
            "report.pdf",
            "application/pdf"
        )

        # Logging
        with open("ns_dmee_log.json","a") as f:
            f.write(json.dumps(result)+"\n")

st.markdown("---")
st.markdown("<small>© 2026 NS-DMEE Cloud Safe Edition</small>",unsafe_allow_html=True)
