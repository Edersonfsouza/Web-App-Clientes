import bcrypt

# Senha que você deseja hash
password = "123"

# Gerar o hash da senha
hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

# Exibir o hash
print(hashed_password.decode())
