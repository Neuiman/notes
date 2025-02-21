from fastapi import HTTPException, status


access_exception = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Access denied",
    headers={"WWW-Authenticate": "Bearer"},
    )

not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="note not founded",
    headers={"WWW-Authenticate": "Bearer"}
)