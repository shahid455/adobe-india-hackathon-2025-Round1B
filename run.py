import os
import json
import fitz  # PyMuPDF
from datetime import datetime
from sentence_transformers import SentenceTransformer, util
import re


def extract_first_sentence(text):
    match = re.match(r'(.{10,200}?\.)', text)
    return match.group(1).strip() if match else text[:100].strip()


def extract_relevant_sections(pdf_path, model, query_embedding):
    doc = fitz.open(pdf_path)
    seen_titles = set()
    extracted = []

    for page_num, page in enumerate(doc, start=1):
        text = page.get_text()
        lines = text.split("\n")
        for line in lines:
            line = line.strip()
            if len(line) < 10 or line.lower() in seen_titles:
                continue
            try:
                line_embedding = model.encode(line, convert_to_tensor=True)
                score = util.pytorch_cos_sim(query_embedding, line_embedding).item()
                if score > 0.45:
                    seen_titles.add(line.lower())
                    extracted.append({
                        "document": os.path.basename(pdf_path),
                        "page_number": page_num,
                        "title": line,
                        "importance_score": round(score, 3)
                    })
            except:
                continue

    return sorted(extracted, key=lambda x: -x["importance_score"])


def refine_text(pdf_path, page_number):
    try:
        doc = fitz.open(pdf_path)
        page = doc.load_page(page_number - 1)
        text = page.get_text().replace("\n", " ").strip()
        return text[:1000]
    except:
        return ""


def process_collection(collection_name, model):
    input_dir = os.path.join("app", "input", collection_name)
    output_dir = os.path.join("app", "output", collection_name)
    os.makedirs(output_dir, exist_ok=True)

    input_json_path = os.path.join(input_dir, "challenge1b_input.json")
    output_json_path = os.path.join(output_dir, "challenge1b_output.json")

    with open(input_json_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    persona = config.get("persona", {}).get("role", "")
    job = config.get("job_to_be_done", {}).get("task", "")
    documents = config.get("documents", [])
    doc_names = [doc["filename"] for doc in documents]

    query = f"{persona} {job}"
    query_embedding = model.encode(query, convert_to_tensor=True)

    all_extracted = []
    seen_snippets = set()

    for pdf_file in doc_names:
        pdf_path = os.path.join("app", "input", "PDFs", pdf_file)
        if not os.path.exists(pdf_path):
            continue

        extracted = extract_relevant_sections(pdf_path, model, query_embedding)
        for e in extracted:
            snippet = refine_text(pdf_path, e["page_number"])
            if snippet and snippet not in seen_snippets:
                seen_snippets.add(snippet)
                e["refined_text"] = snippet
                e["title"] = extract_first_sentence(snippet)
                all_extracted.append(e)

    top_sections = sorted(all_extracted, key=lambda x: -x["importance_score"])[:10]

    extracted_sections = []
    subsection_analysis = []

    for rank, sec in enumerate(top_sections, 1):
        extracted_sections.append({
            "document": sec["document"],
            "section_title": sec["title"],
            "importance_rank": rank,
            "page_number": sec["page_number"]
        })
        subsection_analysis.append({
            "document": sec["document"],
            "refined_text": sec["refined_text"],
            "page_number": sec["page_number"]
        })

    result = {
        "metadata": {
            "input_documents": doc_names,
            "persona": persona,
            "job_to_be_done": job,
            "processing_timestamp": datetime.utcnow().isoformat()
        },
        "extracted_sections": extracted_sections,
        "subsection_analysis": subsection_analysis
    }

    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"[✅] {collection_name} output saved to {output_json_path}")


def main():
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    for collection in ["collection1", "collection2", "collection3"]:
        process_collection(collection, model)


if __name__ == "__main__":
    main()
