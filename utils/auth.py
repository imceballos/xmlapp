from typing import Dict, Optional
import datetime

from fastapi import Depends, FastAPI, HTTPException, Request, Response, status
from fastapi.security import OAuth2, OAuth2PasswordRequestForm
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from passlib.handlers.sha2_crypt import sha512_crypt as crypto
from jose import JWTError, jwt

from .models import User, get_user


class OAuth2PasswordBearerWithCookie(OAuth2):
    def __init__(
        self,
        tokenUrl: str,
        scheme_name: Optional[str] = None,
        scopes: Optional[Dict[str, str]] = None,
        description: Optional[str] = None,
        auto_error: bool = True,
        settings: Optional[str] = None
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl, "scopes": scopes})
        super().__init__(
            flows=flows,
            scheme_name=scheme_name,
            description=description,
            auto_error=auto_error,
        )
        self.settings = settings


    async def __call__(self, request: Request) -> Optional[str]:
        authorization: str = request.cookies.get(self.settings.COOKIE_NAME)
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None
        return param

class AuthenticationMethods:

    def __init__(self, settings):
        self.settings = settings

    def create_access_token(self, data: Dict) -> str:
        to_encode = data.copy()
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=self.settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, 
            self.settings.SECRET_KEY, 
            algorithm=self.settings.ALGORITHM
        )
        return encoded_jwt

    def authenticate_user(self, username: str, plain_password: str) -> User:
        user = get_user(username)
        if not user:
            return False
        if not crypto.verify(plain_password, user.hashed_password):
            return False
        return user

    def decode_token(self, token: str) -> User:
        if token:
            credentials_exception = HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Could not validate credentials."
            )
            token = token.removeprefix("Bearer").strip()
            try:
                payload = jwt.decode(token, self.settings.SECRET_KEY, algorithms=[self.settings.ALGORITHM])
                username: str = payload.get("username")
                if username is None:
                    raise credentials_exception
            except JWTError as e:
                print(e)
                raise credentials_exception
            
            user = get_user(username)
            return user


    def get_current_user_from_cookie(self, request: Request) -> User:
        """
        Get the current user from the cookies in a request.
        
        Use this function from inside other routes to get the current user. Good
        for views that should work for both logged in, and not logged in users.
        """
        token = request.cookies.get(self.settings.COOKIE_NAME)
        user = self.decode_token(token)
        return user

    def get_current_user_from_token(self, token: str) -> User:
        """
        Get the current user from the cookies in a request.

        Use this function when you want to lock down a route so that only 
        authenticated users can see access the route.
        """
        user = self.decode_token(token)
        return user