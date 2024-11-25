from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, Date
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import func

Base = declarative_base()

class Role(Base):
    """
    representa a tabela 'roles' no banco de dados.
    
    a classe role define os papéis (roles) dos usuários, como administrador, usuário padrão, etc.
    cada papel tem uma descrição associada.
    """
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String, nullable=False)

    users = relationship('User', back_populates='role')

class Claim(Base):
    """
    representa a tabela 'claims' no banco de dados.
    
    a classe claim define as permissões ou reivindicações que os usuários podem ter, como 'visualizar relatórios', 'editar dados', etc.
    cada permissão possui uma descrição e um estado (ativo ou inativo).
    """
    __tablename__ = 'claims'
    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String, nullable=False)
    active = Column(Boolean, nullable=False, default=True)

    user_claims = relationship('UserClaim', back_populates='claim')

class User(Base):
    """
    representa a tabela 'users' no banco de dados.
    
    a classe user define os usuários do sistema, incluindo informações como nome, e-mail, senha e o papel associado.
    cada usuário está associado a um papel (role) e pode ter várias permissões (claims).
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    role_id = Column(Integer, ForeignKey('roles.id'), nullable=False)
    created_at = Column(Date, nullable=False)
    updated_at = Column(Date, nullable=True)

    role = relationship('Role', back_populates='users')
    user_claims = relationship('UserClaim', back_populates='user')

class UserClaim(Base):
    """
    representa a tabela 'user_claims' no banco de dados.
    
    a classe userclaim associa um usuário a uma permissão específica (claim).
    cada associação entre usuário e permissão é única.
    """
    __tablename__ = 'user_claims'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    claim_id = Column(Integer, ForeignKey('claims.id'), primary_key=True)

    user = relationship('User', back_populates='user_claims')
    claim = relationship('Claim', back_populates='user_claims')


DATABASE_URL = "postgresql+psycopg2://<usuario>:<senha>@localhost:5432/<nome-do-banco>"
"""
a url de conexão com o banco de dados, especificando o tipo de banco (postgresql), 
usuário, senha, host e nome do banco.
"""
engine = create_engine(DATABASE_URL)

Session = sessionmaker(bind=engine)
session = Session()

results = session.query(
    User.name.label('user_name'),
    User.email.label('user_email'),
    Role.description.label('role_description'),
    func.array_agg(Claim.description).label('claims_descriptions')
).join(
    Role, Role.id == User.role_id
).outerjoin(
    UserClaim, UserClaim.user_id == User.id
).outerjoin(
    Claim, Claim.id == UserClaim.claim_id
).group_by(
    User.name, User.email, Role.description
).order_by(
    User.name
).all()

"""
a consulta utiliza joins para combinar os dados das tabelas de 'users', 'roles', 
'claims' e 'user_claims', e retorna informações sobre cada usuário, incluindo:
- nome do usuário
- e-mail do usuário
- descrição do papel (role) do usuário
- lista das descrições das permissões (claims) associadas ao usuário

os resultados são agrupados por usuário e papel, e ordenados pelo nome do usuário.
"""

for result in results:
    print(f"user: {result.user_name}, email: {result.user_email}, role: {result.role_description}, claims: {', '.join(result.claims_descriptions)}")
    """
    para cada usuário no resultado da consulta, exibe-se o nome, e-mail, 
    papel e as permissões associadas a ele. as permissões são apresentadas
    como uma lista separada por vírgulas.
    """
