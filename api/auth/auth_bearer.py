from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from .auth_handler import decodeJWT


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    def __call__(self, request: Request):
        authorization = request.headers.get("Authorization")
        if not authorization:
            raise HTTPException(status_code=403, detail="Not authenticated")

        try:
            scheme, credentials = authorization.split(" ")
            if scheme.lower() != "bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme")

            if not self.verify_jwt(credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token")

            return credentials
        except (ValueError, IndexError):
            raise HTTPException(status_code=403, detail="Invalid authorization header")

    def verify_jwt(self, jwtoken: str) -> bool:
        try:
            payload = decodeJWT(jwtoken)
        except:
            payload = None
        return bool(payload)
