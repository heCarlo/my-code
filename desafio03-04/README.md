# Documentação de Execução Local e Deploy Produtivo

Este documento descreve os passos necessários para executar o projeto em ambiente local com **FastAPI** e **PostgreSQL** e como realizar o deploy em um ambiente produtivo utilizando **Docker**.

## 1. Executar o Projeto Localmente com FastAPI e PostgreSQL

### Pré-requisitos

Antes de rodar o projeto localmente, verifique se as seguintes ferramentas estão instaladas:

- **Python** (versão 3.8 ou superior)
- **PostgreSQL** (instalação local)
- **pip** para gerenciar pacotes Python
- **Alembic** para migrações do banco de dados

### Passo 1: Criar e Ativar o Ambiente Virtual

Antes de instalar as dependências, é necessário criar e ativar o ambiente virtual.

1. **Criar o Ambiente Virtual** (caso não tenha feito isso anteriormente):

   - Se estiver utilizando **venv** (pip):
   
     ```bash
     python -m venv .venv
     ```

2. **Ativar o Ambiente Virtual**:

   - **Windows**:
     ```bash
     .\.venv\Scripts\activate
     ```

   - **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```

### Passo 2: Instalar as Dependências

Após ativar o ambiente virtual, instale as dependências do projeto utilizando o gerenciador de pacotes Python (pip):

- Se estiver utilizando **pip**, execute o comando:
  
  `pip install -r requirements.txt`

### Passo 3: Configurar o Banco de Dados PostgreSQL

1. **Instalar o PostgreSQL**:
   
   Caso o PostgreSQL não esteja instalado, faça o download e siga as instruções no [site oficial](https://www.postgresql.org/download/).

2. **Configurar o Banco de Dados**:

   - Crie um banco de dados para o projeto.
   - Configure as variáveis de ambiente para o banco de dados, como **DB_HOST**, **DB_NAME**, **DB_USER**, **DB_PASSWORD**.

3. **Ajustar o `DATABASE_URL` no arquivo `.env`**:

   Dependendo de onde você está rodando o projeto (local ou Docker), é necessário ajustar a variável `DATABASE_URL` no arquivo `.env`.

   - Se estiver rodando localmente, altere o valor para:

     `DATABASE_URL=postgresql+psycopg2://postgres:tata1212@localhost:5432/postgres`

   - Se estiver rodando no Docker, altere o valor para:

     `DATABASE_URL=postgresql+psycopg2://postgres:tata1212@db:5432/postgres`

### Passo 4: Rodar as Migrações do Banco de Dados

No ambiente local, antes de rodar a aplicação, é necessário aplicar as migrações manualmente. Utilize o Alembic para isso.

- Para rodar as migrações manualmente, execute o comando:

  `alembic upgrade head`

Este comando aplicará as migrações necessárias para o banco de dados, atualizando-o para a versão mais recente.

### Passo 5: Rodar o Projeto Localmente

Com as dependências instaladas, as migrações aplicadas e o banco de dados configurado, você pode rodar o projeto localmente com FastAPI:

- Para rodar o servidor localmente, execute o comando:

  `uvicorn app.main:app --reload`

Isso iniciará o servidor FastAPI, geralmente acessível em `http://localhost:8000/docs/`.

---

## 2. Executar 'deploy' do Projeto em Ambiente Produtivo (Docker)

### Pré-requisitos

Antes de rodar o projeto em Docker, certifique-se de que as seguintes ferramentas estão instaladas:

- **Docker** (versão 20.10 ou superior)
- **Docker Compose** (se necessário)

### Passo 1: Construir as Imagens Docker

No diretório raiz do projeto, construa a imagem Docker usando o comando:

`docker-compose build`

Isso irá construir as imagens Docker conforme definidas no arquivo `docker-compose.yml`.

### Passo 2: Rodar o Projeto com Docker Compose

Com as imagens construídas, você pode iniciar o ambiente com Docker Compose:

`docker-compose up`

Para rodar os containers em segundo plano (modo "detached"), use a opção `-d`:

`docker-compose up -d`

Este comando irá inicializar a aplicação e o banco de dados (PostgreSQL) conforme configurado no `docker-compose.yml`. No caso do ambiente Docker, o comando `docker-compose` já está configurado para rodar as migrações automaticamente.

### **Uso do `wait-for-it` no Ambiente Docker**

O `wait-for-it` é utilizado para garantir que o serviço do banco de dados PostgreSQL esteja totalmente disponível antes da aplicação FastAPI ser iniciada. Isso é necessário porque, em ambientes Docker, a ordem de inicialização dos containers não é garantida, e o serviço de banco de dados pode não estar pronto para aceitar conexões no momento em que a aplicação tenta acessá-lo. Ao usar o `wait-for-it`, o processo de inicialização da aplicação é automaticamente adiado até que o banco de dados esteja totalmente operacional, evitando falhas de conexão e melhorando a confiabilidade do deploy. Essa abordagem facilita o gerenciamento da ordem de execução dos serviços no Docker e assegura que a comunicação entre a aplicação e o banco de dados ocorra sem problemas de sincronização.

### Passo 3: Acessar o Banco de Dados

Para acessar o banco de dados PostgreSQL em execução no Docker:

1. **Identifique o nome do container**: Utilize o comando `docker ps` para listar os containers ativos.

2. **Acessar o container do PostgreSQL**: Use o comando `docker exec -it <nome_do_container> bash`.

3. **Acessar o PostgreSQL dentro do container**: Após acessar o container, use o comando `psql -U postgres -d postgres` para acessar o banco de dados PostgreSQL.

4. **Executar Consultas SQL**: Para verificar que o banco de dados já contém dados, execute a seguinte consulta SQL para visualizar os registros da tabela `users`:

   `SELECT * FROM users LIMIT 10;`

   Isso irá retornar os primeiros 10 registros da tabela `users`, caso existam dados pré-populados no banco.

### Passo 4: Parar os Containers

Para parar os containers, use o comando:

`docker-compose down`

Isso irá parar e remover todos os containers, redes e volumes definidos no `docker-compose.yml`.

### Passo 5: Limpar Containers e Volumes (Opcional)

Se você deseja remover os containers e volumes, use:

`docker-compose down -v`

Isso irá limpar os containers e volumes de dados, útil para resetar o banco de dados.

---

## 3. Testes e Cobertura com pytest

O projeto utiliza **pytest** para garantir a qualidade do código por meio de testes automatizados. Para rodar os testes:

1. **Rodar os testes**:

   Para rodar todos os testes do projeto, execute o seguinte comando:

   `pytest`

2. **Verificar a cobertura dos testes**:

   Para verificar a cobertura de testes, execute o seguinte comando:

   `pytest --cov=app`

   Este comando executará os testes e, ao final, mostrará um relatório de cobertura, indicando quais partes do código foram cobertas pelos testes.


### Aviso Importante para Ambiente de Desenvolvimento:

- **Em ambiente de desenvolvimento(localhost)**, é necessário usar o banco de dados local para garantir que os testes funcionem corretamente. Certifique-se de que a variável `DATABASE_URL` esteja configurada para o banco local no arquivo `.env` como:

  `DATABASE_URL=postgresql+psycopg2://postgres:tata1212@localhost:5432/postgres`

Isso assegura que os testes de banco de dados e as consultas realizadas localmente funcionem como esperado.