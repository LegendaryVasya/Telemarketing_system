import bcrypt

password = 'sergey'
# admin/admin
# user/qwer
# val/val1

bytes = password.encode('utf-8')

salt = bcrypt.gensalt()
hashed = bcrypt.hashpw(bytes, salt)
print(salt)
print(hashed)


result = bcrypt.checkpw(bytes, hashed)
print(hashed.decode('utf-8'))
print(result)
