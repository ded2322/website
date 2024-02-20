from typing import Optional

from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse

from app.users.auth import authenticate_user, create_access_token
from app.users.dependencies import get_current_user


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]
        user = await authenticate_user(username, password)
        try:
            access_token = create_access_token({"sub": user["id"]})
            request.session.update({"access_token": access_token})
        except Exception as e:
            raise f"{str(e)}"

        return True

    async def logout(self, request: Request) -> bool:
        # Usually you'd want to just clear the session
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> Optional[RedirectResponse] | bool:
        token = request.cookies.get("access_token")
        print(token)
        if not token:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)
        print("Получение токена")
        user = await get_current_user(token)
        if not user:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)
        return True


authentication_backend = AdminAuth(secret_key="...")
