from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.services.resume_parser import extract_text_from_pdf


router = APIRouter(
    prefix="/api/resumes",
    tags=["Resume Intelligence"],
)


UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

ALLOWED_CONTENT_TYPES = {
    "application/pdf",
}


@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    # Check file type
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Only PDF resumes are currently supported.",
        )

    # Read uploaded file
    contents = await file.read()

    # Check empty file
    if not contents:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty.",
        )

    # Check file size
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="Resume must be 10 MB or smaller.",
        )

    # Verify PDF signature
    if not contents.startswith(b"%PDF"):
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is not a valid PDF.",
        )

    # Original filename
    original_filename = Path(
        file.filename or "resume.pdf"
    ).name

    # Generate unique filename
    stored_filename = f"{uuid4()}.pdf"

    # Save location
    destination = UPLOAD_DIR / stored_filename

    try:
        # Save PDF
        destination.write_bytes(contents)

        # Extract text
        extracted_text = extract_text_from_pdf(destination)

    except ValueError as exc:
        # Delete PDF if parsing fails
        destination.unlink(missing_ok=True)

        raise HTTPException(
            status_code=422,
            detail=str(exc),
        ) from exc

    except OSError as exc:
        destination.unlink(missing_ok=True)

        raise HTTPException(
            status_code=500,
            detail="Unable to save or process the resume.",
        ) from exc

    finally:
        await file.close()

    return {
        "success": True,
        "message": "Resume uploaded and text extracted successfully.",
        "original_filename": original_filename,
        "stored_filename": stored_filename,
        "size_bytes": len(contents),
        "characters_extracted": len(extracted_text),
        "extracted_text": extracted_text,
    }