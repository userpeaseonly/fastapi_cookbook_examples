from fastapi import WebSocket, WebSocketException, status
from fastapi.security import OAuth2PasswordBearer


class OAuth2WebSocketPasswordBearer(OAuth2PasswordBearer):
    async def __call__(self, websocket: WebSocket) -> str:
        """
        Extract the token from the WebSocket connection.
        """
        authorization = websocket.headers.get("Authorization")
        if not authorization:
            raise WebSocketException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing authorization header",
                headers={"WWW-Authenticate": "Bearer"},
            )
        scheme, _, param = authorization.partition(" ")
        if scheme.lower() != "bearer":
            raise WebSocketException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authorization scheme",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if not param:
            raise WebSocketException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return param