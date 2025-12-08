"""Files Router - FastAPI file upload and static file serving."""

from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil
import uuid
from pathlib import Path
from datetime import datetime

# Import security validation functions
from app.utils.security import validate_uploaded_file, SecurityValidationError, validate_filename

# Allowed file extensions for different types
ALLOWED_IMAGE_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'webp'}
ALLOWED_DOCUMENT_EXTENSIONS = {'pdf', 'txt', 'doc', 'docx'}
ALLOWED_DATA_EXTENSIONS = {'csv', 'json', 'xml'}

# Union of all allowed extensions
ALLOWED_EXTENSIONS = ALLOWED_IMAGE_EXTENSIONS | ALLOWED_DOCUMENT_EXTENSIONS | ALLOWED_DATA_EXTENSIONS

# Maximum file size (10MB)
MAX_FILE_SIZE = 10 * 1024 * 1024

router = APIRouter(tags=["File Management"])

def generate_secure_filename(original_filename: str) -> str:
    """
    Generate a secure filename to prevent path traversal and file system attacks.
    
    Args:
        original_filename: Original filename from user
        
    Returns:
        Secure filename with UUID prefix
    """
    # Validate original filename
    if not validate_filename(original_filename):
        raise SecurityValidationError("Invalid filename format")
    
    # Get file extension
    if '.' in original_filename:
        extension = original_filename.rsplit('.', 1)[1].lower()
        
        # Validate extension
        if extension not in ALLOWED_EXTENSIONS:
            raise SecurityValidationError(f"File extension '{extension}' not allowed")
    else:
        raise SecurityValidationError("File must have an extension")
    
    # Generate UUID-based filename to prevent conflicts and attacks
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    secure_filename = f"{timestamp}_{uuid.uuid4().hex}.{extension}"
    
    return secure_filename

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload a file with comprehensive security validation."""
    try:
        # Validate filename
        if not file.filename:
            raise HTTPException(status_code=400, detail="Filename is required")
        
        # Check file size by reading the first chunk
        content = await file.read()
        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(status_code=413, detail="File too large (max 10MB)")
        
        # Validate uploaded file content and metadata
        validate_uploaded_file(
            file_content=content,
            filename=file.filename,
            allowed_extensions=ALLOWED_EXTENSIONS
        )
        
        # Create uploads directory if it doesn't exist
        upload_dir = Path("uploads")
        upload_dir.mkdir(exist_ok=True)
        
        # Generate secure filename
        secure_filename = generate_secure_filename(file.filename)
        file_path = upload_dir / secure_filename
        
        # Ensure the path is within the uploads directory (extra security)
        try:
            file_path = file_path.resolve()
            upload_dir_resolved = upload_dir.resolve()
            if not str(file_path).startswith(str(upload_dir_resolved)):
                raise SecurityValidationError("Path traversal attempt detected")
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid file path")
        
        # Save the file
        with open(file_path, "wb") as buffer:
            buffer.write(content)
        
        # Verify file was saved correctly
        if not file_path.exists():
            raise HTTPException(status_code=500, detail="Failed to save file")
        
        return {
            "original_filename": file.filename,
            "secure_filename": secure_filename,
            "status": "uploaded",
            "size": len(content),
            "upload_path": str(file_path.relative_to(upload_dir))
        }
        
    except SecurityValidationError as e:
        raise HTTPException(status_code=400, detail=f"File validation failed: {str(e)}")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")

@router.get("/download/{filename}")
async def download_file(filename: str):
    """Download a file with security validation."""
    # Validate filename format
    if not validate_filename(filename):
        raise HTTPException(status_code=400, detail="Invalid filename")
    
    # Prevent path traversal
    if '..' in filename or filename.startswith('.'):
        raise HTTPException(status_code=400, detail="Invalid filename")
    
    upload_dir = Path("uploads")
    file_path = upload_dir / filename
    
    # Ensure path is within uploads directory
    try:
        file_path = file_path.resolve()
        upload_dir_resolved = upload_dir.resolve()
        if not str(file_path).startswith(str(upload_dir_resolved)):
            raise HTTPException(status_code=403, detail="Access denied")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid file path")
    
    # Check file exists
    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(path=file_path, filename=filename)

@router.get("/list")
async def list_files():
    """List uploaded files with security validation."""
    upload_dir = Path("uploads")
    if not upload_dir.exists():
        return {"files": []}
    
    try:
        files = []
        for f in upload_dir.iterdir():
            if f.is_file() and validate_filename(f.name):
                files.append({
                    "name": f.name,
                    "size": f.stat().st_size,
                    "modified": datetime.fromtimestamp(f.stat().st_mtime).isoformat()
                })
        return {"files": files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing files: {str(e)}")
