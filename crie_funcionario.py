from app import app, db, bcrypt
from app.models import Usuario

with app.app_context():
    username_administrador = str(input("Digite o Nome do Administrador"))
    senha_input = str(input("Digite Sua Senha:"))
    hashed_password = bcrypt.generate_password_hash(senha_input).decode('utf-8')
    
    # Crie o usuário funcionário
    funcionario = Usuario(
        username= username_administrador,
        password_hash=hashed_password,
        is_funcionario=True
    )
    
    db.session.add(funcionario)
    db.session.commit()
    print(f"Usuário {funcionario.username} criado com sucesso!")