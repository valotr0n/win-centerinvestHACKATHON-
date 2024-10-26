# app/templates/router.py
from fastapi import APIRouter, Request, status, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from app.users.schemas import UserLogin
from app.users.services import UserService
from app.users.authorization import create_access_token, create_refresh_token, authenticate_user, get_password_hash
from fastapi import Response
from app.exceptions import IncorrectEmailOrPasswordException
from fastapi import Form


from datetime import datetime
from fastapi import Request, Depends
from jose import jwt, JWTError

from app.users.services import UserService
from app.config import settings
from app.exceptions import TokenAbsentException, IncorrectFormatTokenException, TokenExpiredException, UserIsNotPresentException, NotEnoughAuthorityException
from app.users.models import Users

router = APIRouter(prefix="/pages", tags=["Страницы"])
templates = Jinja2Templates(directory="app/templates")


async def get_token(request: Request) -> str:
    """
    Получение токена из cookie запроса.
    """
    token = request.cookies.get("access_token")
    if not token:
        return None
    return token


async def get_current_user(token: str = Depends(get_token)):
    """
    Получение текущего пользователя по токену.
    """
    if not token:
        return None
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
    except JWTError:
        return None

    expire: str = payload.get("exp")
    if not expire or datetime.utcnow().timestamp() > expire:
        return None

    user_id: str = payload.get("sub")
    if not user_id:
        return None

    user = await UserService.find_by_id(user_id)
    if not user:
        return None 

    return user

@router.get("/auth", response_class=HTMLResponse)
async def get_auth_page(request: Request, user: str = Depends(get_current_user)):
    # Попробуем получить информацию о пользователе из токена
    # user = await UserService.get_current_user(token)
    
    if user:  # Если пользователь найден, он авторизован
        # Здесь вы можете отобразить новый блок для авторизованных пользователей
        return templates.TemplateResponse("auth.html", {"request": request, "user": user, "authorized": True})
    
    # Если пользователь не авторизован, отображаем форму авторизации
    return templates.TemplateResponse("auth.html", {"request": request, "authorized": False})


@router.get("/bot", response_class=HTMLResponse)
async def get_auth_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})




# @router.post("/register", status_code=status.HTTP_201_CREATED)
# async def register_user(email: str = Form(...), password: str = Form(...)):
#     existing_user = await UserService.find_one_or_none(email=email)
#     if existing_user:
#         return {"message": "Пользователь с таким email уже существует"}, status.HTTP_400_BAD_REQUEST

#     hashed_password = get_password_hash(password)
#     await UserService.add(
#         email=email,
#         hashed_password=hashed_password,
#         is_confirmed=False
#     )

#     return {"message": f"Для подтверждения пользователя {email} было отправлено письмо с ссылкой для завершения регистрации"}



# @router.post("/login", status_code=status.HTTP_200_OK)
# async def login_user(
#     response: Response,
#     email: str = Form(...),
#     password: str = Form(...)
# ):
#     user_data = UserLogin(email=email, password=password)
#     user = await authenticate_user(user_data.email, user_data.password)
#     if not user:
#         raise IncorrectEmailOrPasswordException

#     access_token = create_access_token({"sub": str(user.id)})
#     refresh_token = create_refresh_token({"sub": str(user.id)})

#     response.set_cookie(
#         key="access_token",
#         value=access_token,
#         httponly=True
#     )
#     response.set_cookie(
#         key="refresh_token",
#         value=refresh_token,
#         httponly=True
#     )

#     return {"message": f"Пользователь {user_data.email} успешно авторизован"}

@router.post("/login", status_code=status.HTTP_200_OK)
async def login_user(
    response: Response,
    email: str = Form(...),
    password: str = Form(...)
):
    user_data = UserLogin(email=email, password=password)
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise IncorrectEmailOrPasswordException

    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True
    )

    return {
        "message": f"Пользователь {user_data.email} успешно авторизован",
        "user": {"email": user_data.email},  # Отправляем информацию о пользователе
        "authorized": True
    }


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(email: str = Form(...), password: str = Form(...)):
    existing_user = await UserService.find_one_or_none(email=email)
    if existing_user:
        return {"message": "Пользователь с таким email уже существует"}, status.HTTP_400_BAD_REQUEST

    hashed_password = get_password_hash(password)
    await UserService.add(
        email=email,
        hashed_password=hashed_password,
        is_confirmed=False
    )

    return {"message": f"Пользователь {email} успешно зарегистрирован", "authorized": True}
