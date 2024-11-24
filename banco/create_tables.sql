DROP TABLE IF EXISTS acessos;
DROP TABLE IF EXISTS alunos;
DROP TABLE IF EXISTS usuarios;

CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'admin'
);


CREATE TABLE alunos (
    id SERIAL PRIMARY KEY,
    nome_completo VARCHAR(100) NOT NULL,
    ra VARCHAR(20) UNIQUE NOT NULL,
    email VARCHAR(100),
    foto BYTEA,
    matricula VARCHAR(50),
    turno VARCHAR(20),
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE acessos (
    id SERIAL PRIMARY KEY,
    aluno_id INT NOT NULL REFERENCES alunos(id),
    usuario_id INT NOT NULL REFERENCES usuarios(id),
    status VARCHAR(20) NOT NULL,
    data_acesso TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
