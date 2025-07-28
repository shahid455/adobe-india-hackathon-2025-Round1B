import os
import fitz  # PyMuPDF
import json
from sentence_transformers import SentenceTransformer, util
import numpy as np

def extract_sections(pdf_folder):
    sections = []
    for filename in os.listdir(pdf_folder):
        if filename.endswith(".pdf"):
            doc = fitz.open(os.path.join(pdf_folder, filename))
            text = ""
            for page in doc:
                text += page.get_text()
            sections.append({
                "document": filename,
                "page": 1,
                "section_title": "Untitled",
                "importance_rank": 1
            })
    return sections

def rank_sections(sections, prompt_text, top_k=5):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    sentences = [f"{s['section_title']} - {s['document']}" for s in sections]
    embeddings = model.encode(sentences, convert_to_tensor=True)
    query_embedding = model.encode(prompt_text, convert_to_tensor=True)
    cos_scores = util.pytorch_cos_sim(query_embedding, embeddings)[0]
    top_results = np.argpartition(-cos_scores, range(top_k))[:top_k]

    ranked_sections = [sections[idx] for idx in top_results]
    return ranked_sections

def main(pdf_dir, output_path, persona, job):
    print("🔍 Extracting sections from PDFs...")
    sections = extract_sections(pdf_dir)

    print("🧠 Loading persona + job...")
    prompt_text = f"{persona}. {job}"

    print("📊 Ranking sections...")
    ranked = rank_sections(sections, prompt_text)

    print("💾 Saving output...")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump({
            "metadata": {
                "input_documents": os.listdir(pdf_dir),
                "persona": persona,
                "job": job
            },
            "sections": ranked,
            "sub_sections": []
        }, f, indent=2)

    print("✅ Done.")