from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()
def hash_password(password) ->str:
    return password_hash.hash(password)

def verify_password(user_pass,db_pass) ->bool:
    return password_hash.verify(user_pass,db_pass)

#  thait