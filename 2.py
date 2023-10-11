# import bcrypt
#
# # example password
# password = 'passwordabc'
#
# # converting password to array of bytes
# bytes = password.encode('utf-8')
#
# # generating the salt
# salt = bcrypt.gensalt()
#
# # Hashing the password
# hash = bcrypt.hashpw(bytes, salt)
#
# # Taking user entered password
# userPassword = 'passwordabc'
#
# # encoding user password
# userBytes = userPassword.encode('utf-8')
#
# # checking password
# result = bcrypt.checkpw(userBytes, hash)
#
# print(result)
from tkinter.tix import Select

# from sqlalchemy import Select
# from sqlalchemy.orm import Session
# 
# from db.connect import engine
# from db.models import User
# 
# with Session(engine) as session:
#     data = session.scalars(Select(User)).all()
#     for i in data:
#         print(i)


# if '$2b$12$DOCGeM/r/mjXeMRE8uN.yOkWQgo0.WetlhRKta6XZYFYjPJevSviK'=='$2b$12$ettV3vdYBLUZPDWJ5k/XyuRNORX4DACc17J4fTJCbxyal6WJIy2RG':
#     print(True)
# else:
#     print(False)