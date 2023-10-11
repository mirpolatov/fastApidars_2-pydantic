import smtplib
from email.mime.text import MIMEText

import bcrypt
from fastapi import FastAPI, HTTPException
from fastapi import Request, Depends
from fastapi.security.http import HTTPBase
from sqlalchemy import Select
from sqlalchemy.orm import Session
from starlette import status
from starlette.authentication import AuthenticationBackend, AuthCredentials, SimpleUser, AuthenticationError
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from db.connect import engine
from db.models import Base, User, Email, SendMessages

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory='templates')


@app.on_event('startup')
async def startup():
    # pass
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


class BearerTokenAuthBackend(AuthenticationBackend):
    async def authenticate(self, request):

        if "Authorization" not in request.headers:
            return
        with Session(engine) as session:
            date = session.scalars(Select(User)).all()
            for i in date:
                if username := request.headers.get("Authorization"):
                    i.username = username.replace('Bearer ', '')
                    with Session(engine) as session:
                        data = session.scalars(Select(User)).all()
                        for user in data:
                            if username == user.username:
                                return AuthCredentials(['authenticated']), SimpleUser(username)
            raise AuthenticationError({'detail': 'Invalid Authorization'})


app.add_middleware(AuthenticationMiddleware, backend=BearerTokenAuthBackend())
security = HTTPBase(scheme='bearer')


@app.post('/signup')
async def create(username, password, confirm_password):
    if password != confirm_password:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, 'Invalid password provided')
    with Session(engine) as session:
        data = session.scalars(Select(User)).all()
        for user in data:
            users = user.username
            if username == users:
                raise HTTPException(status.HTTP_400_BAD_REQUEST, 'Username already in use')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode()
    s: User = User(username=username, password=hash)
    session.add(s)
    session.commit()
    return {'message': 'Sign Up Successfully'}


@app.post('/add_email')
async def create(email, user_id):
    with Session(engine) as session:
        data = session.scalars(Select(Email)).all()

        for user in data:

            users = user.email
            if email == users and user.user_id == user_id:
                raise HTTPException(status.HTTP_400_BAD_REQUEST, 'Email already in use/user_id not found')

        s: Email = Email(email=email, user_id=user_id)
        session.add(s)
        session.commit()
        return {'message': 'Sign Up Successfully'}


# @app.get('/signin')
# async def signin(request: Request):
#     return request


@app.post('/signin')
async def check(username, password):
    with Session(engine) as session:
        data = session.scalars(Select(User)).all()
        for user in data:
            if username == user.username:
                result = bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8'))
                if not result:
                    break
                return {'message': 'Successfully signed with %s' % username}

    raise HTTPException(status.HTTP_400_BAD_REQUEST, 'Invalid username/password provided')


@app.get('/profile', dependencies=[Depends(security)])
async def profile(request: Request):
    if request.user.is_authenticated:
        return request.user
    raise HTTPException(status.HTTP_401_UNAUTHORIZED)


#
#
@app.patch('/profile-password', dependencies=[Depends(security)])
async def profile_password(username, password, confirm_password):
    with Session(engine) as session:
        data = session.scalars(Select(User)).all()
        for i in data:
            if password != confirm_password:
                raise HTTPException(status.HTTP_400_BAD_REQUEST, 'Password does not match')

            if username == i.username:
                salt = bcrypt.gensalt()
                hash = bcrypt.hashpw(i.password.encode('utf-8'), salt).decode()
                i.password = hash
                password = password

        session.commit()
        return {'Parol o''gartirildi'}


@app.post('/send_messages')
def send_email(subject: str, body: str):

    try:
        sender_email = "mirazizmirpolatov9@gmail.com"
        sender_password = "imqw yvja iizv ytww"
        with Session(engine) as session:
            data = session.scalars(Select(Email)).all()
            for i in data:
                message = MIMEText(body)
                message["Subject"] = subject
                message["From"] = sender_email
                message["To"] = i.email

            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, i.email, message.as_string())

                s: SendMessages = SendMessages(subject=subject, body=body, send=sender_email)
                session.add(s)
                session.commit()

            print(f"Email sent to {i.email} successfully!")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sending email: {str(e)}")

# @app.post("/send_message/")
# async def send_message(message: MessageModel):
#     try:
#         from_email = "tannagashevalisher07@gmail.com"
#         from_password = "urzkgppngnfuuhns"
#         subject = message.subject
#         body = message.body
#
#         msg = MIMEText(body)
#         msg['Subject'] = subject
#         msg['From'] = from_email
#
#         db = SessionLocal()
#         emails = db.query(Email).all()
#         recipient_emails = [email.email for email in emails]
#         db.close()
#
#         for to_email in recipient_emails:
#             msg['To'] = to_email
#             server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
#             server.login(from_email, from_password)
#             server.sendmail(from_email, [to_email], msg.as_string())
#             server.quit()
#
#         db = SessionLocal()
#         db_message = Message(subject=subject, body=body)
#         db.add(db_message)
#         db.commit()
#         db.refresh(db_message)
#         db.close()
#
#         return {"message": "Message sent and saved successfully."}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
