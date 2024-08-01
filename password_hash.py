from bcrypt import hashpw, gensalt, checkpw

get_hashed_password = lambda plain_text_password: hashpw(plain_text_password.encode('utf-8'), bytes(gensalt())).decode('utf-8')
check_password = lambda plain_text_password, hashed_password: checkpw(plain_text_password.encode('utf-8'), hashed_password.encode('utf-8'))