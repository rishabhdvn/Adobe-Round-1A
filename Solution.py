import fitz  # PyMuPDF
import json
import os
import re

class PDFStructureExtractor:
    """
    Processes a PDF to extract its structure using a fast, heuristic-based approach
    optimized for the Adobe Hackathon Round 1A constraints.
    """
    def __init__(self, pdf_path):
        """Initializes the processor and opens the PDF document."""
        self.doc = fitz.open(pdf_path)
        self.body_size = self._find_dominant_font_size()

    def _find_dominant_font_size(self):
        """Finds the most common font size, assumed to be the body text."""
        font_counts = {}
        for page in self.doc:
            for block in page.get_text("dict")["blocks"]:
                if block['type'] == 0:  # Text block
                    for line in block["lines"]:
                        for span in line["spans"]:
                            size = int(span["size"])
                            font_counts[size] = font_counts.get(size, 0) + len(span["text"])
        if not font_counts: return 10
        return max(font_counts, key=font_counts.get)

    def _score_line(self, text, size, font):
        """Scores a line of text based on heuristic rules."""
        score = 0
        if size > self.body_size:
            score += (size - self.body_size)
        if "bold" in font.lower():
            score += 2
        if re.match(r'^((\d+\.)*\d+|[A-Z]\.|Chapter\s\d+|Section\s\d+)', text):
            score += 3
        if text.isupper() and len(text.split()) < 7:
            score += 1
        return score

    def extract_structure(self):
        """Extracts the title and a hierarchical outline (H1, H2, H3)."""
        candidates = []
        for page_num, page in enumerate(self.doc):
            for block in page.get_text("dict")["blocks"]:
                if block['type'] == 0:
                    for line in block["lines"]:
                        line_text = " ".join(s["text"] for s in line["spans"]).strip()
                        if not line_text:
                            continue
                        main_span = line["spans"][0]
                        score = self._score_line(line_text, int(main_span["size"]), main_span["font"])
                        if score > 2:
                            candidates.append({
                                "text": line_text,
                                "score": score,
                                "size": int(main_span["size"]),
                                "page": page_num + 1
                            })

        if not candidates:
            return {"title": "Untitled Document", "outline": []}

        page1_candidates = [c for c in candidates if c["page"] == 1]
        doc_title = max(page1_candidates, key=lambda x: x["score"])["text"] if page1_candidates else candidates[0]["text"]

        heading_sizes = sorted(list(set([c["size"] for c in candidates])), reverse=True)
        level_map = {size: f"H{i+1}" for i, size in enumerate(heading_sizes[:3])}

        outline = []
        for c in candidates:
            if c["size"] in level_map:
                if c["text"] == doc_title and c["page"] == 1:
                    continue
                outline.append({
                    "level": level_map[c["size"]],
                    "text": c["text"],
                    "page": c["page"]
                })

        return {"title": doc_title, "outline": outline}

def main():
    """Main function to run the processor on all PDFs."""
    input_dir = "/app/input"
    output_dir = "/app/output"

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(input_dir, filename)
            try:
                extractor = PDFStructureExtractor(pdf_path)
                result = extractor.extract_structure()
                output_filename = os.path.splitext(filename)[0] + ".json"
                output_path = os.path.join(output_dir, output_filename)
                with open(output_path, "w") as f:
                    json.dump(result, f, indent=4)
                print(f"Successfully processed {filename}")
            except Exception as e:
                print(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    main()