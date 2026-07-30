from pathlib import Path

import fitz


def extract_text_from_pdf(pdf_path: Path) -> str:
    """Extract readable text from a PDF file."""

    try:
        with fitz.open(pdf_path) as document:
            pages = []

            for page in document:
                page_text = page.get_text("text")
                pages.append(page_text)

        extracted_text = "\n".join(pages).strip()

        if not extracted_text:
            raise ValueError(
                "No readable text was found in the PDF."
            )

        return extracted_text

    except (fitz.FileDataError, fitz.EmptyFileError) as exc:
        raise ValueError(
            "Unable to read the PDF file."
        ) from exc