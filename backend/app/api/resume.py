from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.services.resume_parser import extract_text_from_pdf
from app.services.resume_analyzer import analyze_resume


router = APIRouter(
    prefix="/api/resumes",
    tags=["Resume Intelligence"],
)


# Directory where uploaded resumes are stored
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


# Maximum allowed resume size: 10 MB
MAX_FILE_SIZE = 10 * 1024 * 1024


# Currently supporting PDF resumes
ALLOWED_CONTENT_TYPES = {
    "application/pdf",
}


@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    """
    Upload, validate, store, extract, and analyze a resume PDF.
    """

    # ---------------------------------------------------------
    # 1. Validate content type
    # ---------------------------------------------------------

    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Only PDF resumes are currently supported.",
        )

    # ---------------------------------------------------------
    # 2. Read uploaded file
    # ---------------------------------------------------------

    contents = await file.read()

    # Check empty file
    if not contents:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty.",
        )

    # ---------------------------------------------------------
    # 3. Validate file size
    # ---------------------------------------------------------

    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="Resume must be 10 MB or smaller.",
        )

    # ---------------------------------------------------------
    # 4. Verify PDF signature
    # ---------------------------------------------------------

    if not contents.startswith(b"%PDF"):
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is not a valid PDF.",
        )

    # ---------------------------------------------------------
    # 5. Prepare filename
    # ---------------------------------------------------------

    original_filename = Path(
        file.filename or "resume.pdf"
    ).name

    stored_filename = f"{uuid4()}.pdf"

    destination = UPLOAD_DIR / stored_filename

    # ---------------------------------------------------------
    # 6. Save + Extract + Analyze
    # ---------------------------------------------------------

    try:

        # Save uploaded PDF
        destination.write_bytes(contents)

        # Extract raw text from PDF
        extracted_text = extract_text_from_pdf(
            destination
        )

        # Analyze resume structure
        resume_analysis = analyze_resume(
            extracted_text
        )

    except ValueError as exc:

        # Remove file if resume processing fails
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

    # ---------------------------------------------------------
    # 7. Return result
    # ---------------------------------------------------------

    return {
        "success": True,
        "message": "Resume uploaded and analyzed successfully.",

        "file": {
            "original_filename": original_filename,
            "stored_filename": stored_filename,
            "size_bytes": len(contents),
        },

        "extraction": {
            "characters_extracted": len(extracted_text),
            "extracted_text": extracted_text,
        },

        "analysis": resume_analysis,
    }