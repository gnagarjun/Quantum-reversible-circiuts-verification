import pdfplumber

with pdfplumber.open("Research_paper_reversible_circuits.pdf") as pdf:
    print(f"Total pages: {len(pdf.pages)}")
    for i, page in enumerate(pdf.pages):
        print(f"\n{'='*60}")
        print(f"PAGE {i+1}")
        print('='*60)
        t = page.extract_text()
        print(t if t else "(no extractable text on this page)")

