# from json import loads, dump
#
# import bcrypt
# from fastapi import FastAPI, HTTPException, Depends
# from fastapi.security.http import HTTPBase
# from pydantic import BaseModel
# from starlette import status
# from starlette.authentication import AuthenticationBackend, AuthenticationError, AuthCredentials, SimpleUser
# from starlette.middleware.authentication import AuthenticationMiddleware
# from starlette.requests import Request
# from starlette.responses import HTMLResponse, Response
# from starlette.staticfiles import StaticFiles
# from starlette.templating import Jinja2Templates
#
# app = FastAPI()
# app.mount("/static", StaticFiles(directory="static"), name="static")
#
# templates = Jinja2Templates(directory="templates")
#
#
# class BearerTokenAuthBackend(AuthenticationBackend):
#
#     async def authenticate(self, request):
#         if "Authorization" not in request.headers:
#             return
#         if username := request.headers.get('Authorization'):
#             username = username.replace('Bearer ', '')
#             with open('test.json') as f:
#                 data = f.read()
#                 data = loads(data) if data else []
#                 for user in data:
#                     if username == user['username']:
#                         return AuthCredentials(["authenticated"]), SimpleUser(username)
#
#         raise AuthenticationError({'detail': 'Invalid authorization'})
#
#
# #
# app.add_middleware(AuthenticationMiddleware, backend=BearerTokenAuthBackend())
#
# security = HTTPBase(scheme='bearer')
#
#
# class User(BaseModel):
#     username: str
#     password: str
#
#
# class SignUp(User):
#     confirm_password: str
#
#     @classmethod
#     async def create(cls, username, password, confirm_password):
#         if password != confirm_password:
#             raise HTTPException(status.HTTP_400_BAD_REQUEST, 'Invalid password provided')
#         with open('test.json') as f:
#             data = f.read()
#             data = loads(data) if data else []
#             for user in data:
#                 if username == user['username']:
#                     raise HTTPException(status.HTTP_400_BAD_REQUEST, 'Username already in use')
#         salt = bcrypt.gensalt()
#         hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode()
#         return data, User(username=username, password=hash)
#
#
# class SignIn(User):
#     @classmethod
#     async def check(cls, username, password):
#         with open('test.json') as f:
#             data = f.read()
#             data = loads(data) if data else []
#             for user in data:
#                 if username == user['username']:
#                     result = bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8'))
#                     if not result:
#                         break
#                     return {'message': 'Successfully signed with %s' % username}
#         raise HTTPException(status.HTTP_400_BAD_REQUEST, 'Invalid username/password provided')
#
#
# class ChangePassword(BaseModel):
#     password: str
#     confirm_password: str
#
#
# @app.get('/', response_class=HTMLResponse)
# async def signup(request: Request):
#     return templates.TemplateResponse('sign-up.html', context={'request': request})
#
#
# @app.post('/signup')
# async def signup(request: Request):
#     data, user = await SignUp.create(**await request.form())
#     if not data:
#         data = []
#     with open('test.json', 'w') as f:
#         data.append(user.model_dump())
#         dump(data, f, indent=4)
#     return {'message': 'Sign Up Successfully'}
#
#
# @app.get('/signin', response_class=HTMLResponse)
# async def signin(request: Request):
#     return templates.TemplateResponse('sign-in.html', context={'request': request})
#
#
# @app.post('/signin')
# async def signup(request: Request, response: Response):
#     form = await request.form()
#     r = await SignIn.check(**form)
#     if r:
#         response.set_cookie('Authorization', form["username"])
#     return
#
#
# @app.get('/profile', dependencies=[Depends(security)])
# async def profile(request: Request):
#     if request.user.is_authenticated:
#         return request.user
#     raise HTTPException(status.HTTP_401_UNAUTHORIZED)
#
#
# @app.patch('/profile-password', dependencies=[Depends(security)])
# async def profile(request: Request, form: ChangePassword):
#     user = request.user
#     username = user.username
#     if form.password != form.confirm_password:
#         raise HTTPException(status.HTTP_400_BAD_REQUEST, "password does not match")
#     with open('test.json', 'r+') as f:
#         data = f.read()
#         data = loads(data) if data else []
#         for user in data:
#             if username == user['username']:
#                 salt = bcrypt.gensalt()
#                 hash = bcrypt.hashpw(form.password.encode('utf-8'), salt).decode()
#                 user['password'] = hash
#
#         f.seek(0)
#         dump(data, f, indent=4)
#
# #
# # import bcrypt
# #
# # # example password
# # password = 'password123'
# #
# # # converting password to array of bytes
# # bytes = password.encode('utf-8')
# # print(bytes)
# # # generating the salt
# # salt = bcrypt.gensalt()
# # print(salt)
# #
# # # Hashing the password
# # hash = bcrypt.hashpw(bytes, salt)
# #
# # print(hash)
from sqlalchemy.orm import session

