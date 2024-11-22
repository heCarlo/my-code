--===>>> Roles:
-- Tabela destinada a armazenar os papéis ou funções que os usuários podem assumir no sistema.
CREATE TABLE roles (
	id int4 NOT NULL GENERATED ALWAYS AS IDENTITY,
	description varchar NOT NULL,
	CONSTRAINT roles_pk PRIMARY KEY (id)
);

--===>>> Claims:
-- Tabela que contém as permissões (claims) disponíveis no sistema e um indicador de ativação.
CREATE TABLE claims (
	id int8 NOT NULL GENERATED ALWAYS AS IDENTITY,
	description varchar NOT NULL,
	active bool NOT NULL DEFAULT true,
	CONSTRAINT claims_pk PRIMARY KEY (id)
);

--===>>> Users:
-- Tabela que armazena os dados dos usuários cadastrados no sistema.
CREATE TABLE users (
	id int8 NOT NULL GENERATED ALWAYS AS IDENTITY,
	"name" varchar NOT NULL,
	email varchar NOT NULL,
	"password" varchar NOT NULL,
	role_id int4 NOT NULL,
	created_at date NOT NULL,
	updated_at date NULL,
	CONSTRAINT users_pk PRIMARY KEY (id)
);

-- Foreign key associando cada usuário a um papel.
ALTER TABLE users ADD CONSTRAINT users_fk FOREIGN KEY (role_id) REFERENCES roles(id);

--===>>> UserClaims:
-- Tabela intermediária que associa usuários a suas permissões específicas.
CREATE TABLE user_claims (
	user_id int8 NOT NULL,
	claim_id int8 NOT NULL,
	CONSTRAINT user_claims_un UNIQUE (user_id, claim_id)
);

-- Foreign keys associando usuários a permissões.
ALTER TABLE user_claims ADD CONSTRAINT user_claims_fk FOREIGN KEY (user_id) REFERENCES users(id);
ALTER TABLE user_claims ADD CONSTRAINT user_claims_fk_1 FOREIGN KEY (claim_id) REFERENCES claims(id);

--===>>> Insert Test Data for Roles
-- Inserção de papéis disponíveis no sistema.
INSERT INTO roles (description) VALUES 
('Administrador'),
('Usuário Padrão');

--===>>> Insert Test Data for Claims
-- Inserção de permissões no sistema.
INSERT INTO claims (description, active) VALUES 
('Visualizar Relatórios', true),
('Editar Dados', true),
('Excluir Registros', true);

--===>>> Insert Test Data for Users
-- Inserção de usuários fictícios para testes.
INSERT INTO users ("name", email, "password", role_id, created_at) VALUES 
('Carlos Henrique', 'carlos@example.com', 'password123', 1, CURRENT_DATE),
('Gabrielly Nunes', 'gabrielly@example.com', 'password123', 2, CURRENT_DATE);

--===>>> Associate Users with Claims
-- Associação de permissões a usuários para configurar acesso.
INSERT INTO user_claims (user_id, claim_id) VALUES 
(1, 1), -- Carlos pode visualizar relatórios
(1, 2), -- Carlos pode editar dados
(2, 1); -- Gabrielly pode visualizar relatórios




-- Desafio01
--===>>> Query to Retrieve User Information
-- Consulta para retornar os usuários com seus papéis e as permissões associadas.
SELECT 
	u."name" AS user_name,
	u.email AS user_email,
	r.description AS role_description,
	ARRAY_AGG(c.description) AS claims_descriptions
FROM 
	users u
JOIN 
	roles r ON u.role_id = r.id
LEFT JOIN 
	user_claims uc ON u.id = uc.user_id
LEFT JOIN 
	claims c ON uc.claim_id = c.id
GROUP BY 
	u."name", u.email, r.description
ORDER BY 
	u."name";
