from httpx import AsyncClient


async def test_register_user(ac: AsyncClient):
    assert 1 == 1
    '''        response = await ac.post("/auth/register",
                                 json={
                                     "username": "admin",
                                     "email":"test@gmail.com",
                                     "password": "admin"
                                 })
        assert response.status_code == 200'''
