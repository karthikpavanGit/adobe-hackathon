import json
from pathlib import Path
import fitz  # PyMuPDF
from typing import List, Dict, Any, Tuple
import re


def is_generic_title(title: str) -> bool:
    """Detects if a title is generic (e.g., 'Microsoft Word - ...')."""
    if not title:
        return True
    generic_patterns = [
        r"^Microsoft Word",
        r"^Document[0-9]*$",
        r"^Untitled",
        r"\.docx?$",
        r"\.pdf$",
    ]
    for pat in generic_patterns:
        if re.search(pat, title, re.IGNORECASE):
            return True
    return False


def clean_heading_text(text: str) -> str:
    """Cleans up heading text: strips whitespace, removes trailing punctuation, collapses spaces."""
    text = text.strip()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[\s\-:]+$", "", text)
    return text


def is_table_header(text: str) -> bool:
    """Detects if a heading is a table column header."""
    table_headers = {"s.no", "name", "age", "relationship"}
    return text.lower() in table_headers


def is_number_only(text: str) -> bool:
    """Detects if a heading is just a number or number with dot (e.g., '10.', '11')."""
    return bool(re.fullmatch(r"\d+\.?", text.strip()))


def merge_multiline_headings(lines: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Merge consecutive lines/spans with same font size and close vertical positions into one heading."""
    if not lines:
        return []
    merged = []
    buffer = []
    last = None
    for line in lines:
        if not buffer:
            buffer.append(line)
            last = line
            continue
        # Same page, same font size, close vertical position
        if (
            line['page'] == last['page'] and
            abs(line['size'] - last['size']) < 0.1 and
            abs(line['y'] - last['y']) < 25  # 25 pixels vertical gap
        ):
            buffer.append(line)
            last = line
        else:
            # Merge buffer
            merged_text = ' '.join([l['text'] for l in buffer])
            merged.append({
                'page': buffer[0]['page'],
                'size': buffer[0]['size'],
                'is_bold': any(l['is_bold'] for l in buffer),
                'y': buffer[0]['y'],
                'text': merged_text
            })
            buffer = [line]
            last = line
    # Merge last buffer
    if buffer:
        merged_text = ' '.join([l['text'] for l in buffer])
        merged.append({
            'page': buffer[0]['page'],
            'size': buffer[0]['size'],
            'is_bold': any(l['is_bold'] for l in buffer),
            'y': buffer[0]['y'],
            'text': merged_text
        })
    return merged


def get_document_title(pdf_doc) -> str:
    """Extract the document title from metadata or the largest, topmost heading on the first page."""
    title = pdf_doc.metadata.get("title")
    if not is_generic_title(title):
        return title.strip()
    # Fallback: use largest, topmost text on first page
    first_page = pdf_doc[0]
    candidates = []
    for block in first_page.get_text("dict").get('blocks', []):
        for line in block.get("lines", []):
            for span in line.get("spans", []):
                text = clean_heading_text(span["text"])
                if len(text) > 3:
                    candidates.append((span["size"], -span["bbox"][1], text))
    if not candidates:
        return "Untitled Document"
    # Sort by size (desc), then y (asc, i.e., top of page)
    candidates.sort(reverse=True)
    return candidates[0][2]


def group_font_sizes(font_sizes: List[float]) -> Dict[float, str]:
    """Assign font sizes to heading levels H1, H2, H3 based on their relative size."""
    unique_sizes = sorted(set(font_sizes), reverse=True)
    heading_map = {}
    for idx, size in enumerate(unique_sizes[:3]):
        heading_map[size] = f"H{idx+1}"
    return heading_map


def extract_headings_from_pdf(pdf_doc) -> List[Dict[str, Any]]:
    """Extract and merge headings (H1, H2, H3) from the PDF using font size, boldness, and position."""
    raw_lines = []
    for page_number, page in enumerate(pdf_doc, start=1):
        for block in page.get_text("dict").get('blocks', []):
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    text = clean_heading_text(span["text"])
                    if len(text) < 3:
                        continue
                    size = span["size"]
                    font_name = span["font"]
                    is_bold = "Bold" in font_name or "bold" in font_name
                    y_position = span["bbox"][1]
                    raw_lines.append({
                        'page': page_number,
                        'text': text,
                        'size': size,
                        'is_bold': is_bold,
                        'y': y_position
                    })
    # Merge multi-line headings
    merged_lines = merge_multiline_headings(raw_lines)
    font_sizes = [line['size'] for line in merged_lines]
    heading_levels = group_font_sizes(font_sizes)
    if not heading_levels:
        return []
    headings = []
    seen = set()
    for line in merged_lines:
        level = heading_levels.get(line['size'])
        if not level:
            continue
        text = line['text']
        # Filter out table headers and number-only headings
        if is_table_header(text) or is_number_only(text):
            continue
        # Heuristic: heading if bold, or near top, or largest size
        if line['is_bold'] or line['y'] < 200 or level == "H1":
            key = (level, text.lower(), line['page'])
            if key not in seen:
                headings.append({
                    "level": level,
                    "text": text,
                    "page": line['page']
                })
                seen.add(key)
    return headings


def get_data_dirs():
    """Detects whether to use Docker-style or local-style input/output directories."""
    docker_input = Path("/app/input")
    docker_output = Path("/app/output")
    local_input = Path("app/input")
    local_output = Path("app/output")
    if docker_input.exists():
        return docker_input, docker_output
    else:
        return local_input, local_output


def process_all_pdfs(input_dir: Path, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    pdf_files = list(input_dir.glob("*.pdf"))
    if not pdf_files:
        print(f"No PDF files found in {input_dir}")
        return
    for pdf_path in pdf_files:
        try:
            with fitz.open(pdf_path) as pdf_doc:
                title = get_document_title(pdf_doc)
                outline = extract_headings_from_pdf(pdf_doc)
            output_data = {"title": title, "outline": outline}
            output_file = output_dir / f"{pdf_path.stem}.json"
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)
            print(f"Processed {pdf_path.name} -> {output_file.name}")
        except Exception as error:
            print(f"Error processing {pdf_path.name}: {error}")


def main():
    input_dir, output_dir = get_data_dirs()
    print("Starting PDF outline extraction...")
    process_all_pdfs(input_dir, output_dir)
    print("Completed PDF outline extraction.")


if __name__ == "__main__":
    main()