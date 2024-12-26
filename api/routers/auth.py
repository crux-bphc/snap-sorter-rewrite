from fastapi import APIRouter, Depends, status, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from ..database import get_db
from .. import db_models, oauth2

router = APIRouter(
    tags = ["Auth"]
)

config = Config(".env")
oauth = OAuth(config)
google = oauth.register(
    name="google",
    client_id=config.get("GOOGLE_CLIENT_ID"),
    client_secret=config.get("GOOGLE_CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

    
@router.get("/google-login")
async def google_login(request: Request):
    """
    Redirects the user to Google's OAuth
    """
    redirect_uri = request.url_for("google_auth")
    return await google.authorize_redirect(request, redirect_uri)


@router.get("/google-auth")
async def google_auth(request: Request, db: Session = Depends(get_db)):
    """
    Handles the callback from Google OAuth and redirects the user to the frontend along with the access token
    """
    try:
        token = await google.authorize_access_token(request)
        user_info = token.get("userinfo", {})
        email = user_info.get("email")

        if not email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unable to fetch user information from Google",
            )

        user = db.query(db_models.User).filter(db_models.User.email == email).first()
        if not user:
            user = db_models.User(email=email)
            db.add(user)
            db.commit()
            db.refresh(user)

        access_token = oauth2.create_access_token(data={"user_id": user.id})
        frontend_redirect_url = f'{config.get("FRONTEND_REDIRECT_URI")}?token={access_token}'
        print(frontend_redirect_url)
        return RedirectResponse(frontend_redirect_url)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Authentication failed: {str(e)}",
        )