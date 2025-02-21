from fastapi import HTTPException, status


access_token_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate access token",
    headers={"WWW-Authenticate": "Bearer"},
    )

refresh_token_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate refresh token",
    headers={"WWW-Authenticate": "Bearer"},
    )


logout_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="refresh token error",
    headers={"WWW-Authenticate": "Bearer"},
    )
