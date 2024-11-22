from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Configuração do banco de dados
DATABASE_URL = "postgresql+psycopg2://postgres:tata1212@localhost:5432/desafio01"
engine = create_engine(DATABASE_URL)

# Criar a SessionLocal, que vai ser usada para gerar sessões de banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Função para obter uma sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
