# Challenge 1b: Multi-Collection PDF Analysis

## 🧠 Overview

An advanced AI-powered PDF analysis engine that processes multiple document collections and extracts the most relevant content based on specific personas and use-case goals. It uses semantic similarity techniques to identify and rank key sections from unstructured PDFs, generating clean, structured JSON output.

---

## 📁 Project Structure

```
adobe-hackathon-ai-planner/
├── app/
│   ├── input/
│   │   ├── collection1/
│   │   │   └── challenge1b_input.json
│   │   ├── collection2/
│   │   │   └── challenge1b_input.json
│   │   ├── collection3/
│   │   │   └── challenge1b_input.json
│   │   └── PDFs/                      # All source PDFs go here
│   ├── output/
│   │   ├── collection1/
│   │   │   └── challenge1b_output.json
│   │   ├── collection2/
│   │   │   └── challenge1b_output.json
│   │   └── collection3/
│   │       └── challenge1b_output.json
├── run.py         # Core script
├── README.md                       
```

---

## 📚 Collections

### ✅ Collection 1: Travel Planning
- **Challenge ID**: `round_1b_001`
- **Persona**: Travel Planner  
- **Task**: Plan a 4-day trip for 10 college friends to the South of France  
- **Documents**: 7 travel guides (`Cities`, `Cuisine`, `Things to Do`, etc.)

### ✅ Collection 2: Adobe Acrobat Learning
- **Challenge ID**: `round_1b_002`
- **Persona**: HR Professional  
- **Task**: Create and manage fillable forms for onboarding and compliance  
- **Documents**: 15 Acrobat tutorials and guides

### ✅ Collection 3: Recipe Collection
- **Challenge ID**: `round_1b_003`
- **Persona**: Food Contractor  
- **Task**: Prepare a vegetarian buffet-style dinner menu for a corporate gathering  
- **Documents**: 9 cooking PDFs (breakfast, lunch, dinner, sides)

---

## 📥 Input / Output Format

### 📌 Input JSON
```json
{
  "challenge_info": {
    "challenge_id": "round_1b_XXX",
    "test_case_name": "specific_test_case"
  },
  "documents": [{"filename": "doc.pdf", "title": "Document Title"}],
  "persona": {"role": "User Persona"},
  "job_to_be_done": {"task": "Description of the task"}
}
```

### 📤 Output JSON
```json
{
  "metadata": {
    "input_documents": ["doc1.pdf", "doc2.pdf"],
    "persona": "User Persona",
    "job_to_be_done": "Task description",
    "processing_timestamp": "UTC ISO Timestamp"
  },
  "extracted_sections": [
    {
      "document": "source.pdf",
      "section_title": "Title or Sentence",
      "importance_rank": 1,
      "page_number": 1
    }
  ],
  "subsection_analysis": [
    {
      "document": "source.pdf",
      "refined_text": "Cleaned relevant paragraph(s)",
      "page_number": 1
    }
  ]
}
```

---

## 🔍 Key Features

- ✅ Persona- and task-aware extraction
- ✅ Importance ranking using semantic similarity
- ✅ Clean section extraction with minimal redundancy
- ✅ Handles any number of PDF collections
- ✅ Timestamped structured JSON output for each collection

---

## 🚀 How to Run

```bash
pip install -r requirements.txt
python run.py
```

This will:
- Read each `challenge1b_input.json`
- Load matching PDFs from `app/input/PDFs/`
- Create a corresponding `challenge1b_output.json` in `app/output/`

---

## 🧠 Technology

- Python 3.8+
- `PyMuPDF` (for reading PDFs)
- `sentence-transformers` (`MiniLM-L6-v2`)
- `json`, `re`, `os`, `datetime`

---

## 🧪 Evaluation Tips

- Check `challenge1b_output.json` for each collection
- Ensure section titles are human-readable and snippets are relevant
- Output is readable, de-duplicated, and aligned with the persona's goal

---

## 📝 Notes

This provides a complete overview of the **Challenge 1b** multi-collection analysis engine built for the Adobe-India-Hackathon25.

---

### 🧑‍💻 Author
- Shahidul Hasan
- Deepta Chakravarty

