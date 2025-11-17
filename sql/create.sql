CREATE TABLE delegacia (
    id_delegacia INTEGER PRIMARY KEY,
    chefe_delagacia VARCHAR,
    is_deleted BOOLEAN DEFAULT FALSE
);

CREATE TABLE departamento (
    id_departamento INTEGER PRIMARY KEY,
    nome_departamento VARCHAR,
    localicacao VARCHAR,
    telefone INTEGER,
    email VARCHAR,
    area_atuacao VARCHAR,
    fk_delegacia_id_delegacia INTEGER,
    is_deleted BOOLEAN DEFAULT FALSE
);

CREATE TABLE veiculo (
    id_veiculo INTEGER PRIMARY KEY,
    status_veiculo VARCHAR,
    modelo VARCHAR,
    uso VARCHAR,
    fk_delegacia_id_delegacia INTEGER,
    is_deleted BOOLEAN DEFAULT FALSE
);

CREATE TABLE agente (
    id_agente INTEGER PRIMARY KEY,
    cargo_agente VARCHAR,
    fk_delegacia_id_delegacia INTEGER,
    is_deleted BOOLEAN DEFAULT FALSE
);

CREATE TABLE envolvido (
    id_envolvido INTEGER PRIMARY KEY,
    nome VARCHAR,
    idade INTEGER,
    is_deleted BOOLEAN DEFAULT FALSE
);

CREATE TABLE testemunha (
    relato VARCHAR,
    fk_envolvido_id_envolvido INTEGER PRIMARY KEY,
    is_deleted BOOLEAN DEFAULT FALSE
);

CREATE TABLE criminoso (
    pena VARCHAR,
    data_condenacao VARCHAR,
    fk_envolvido_id_envolvido INTEGER PRIMARY KEY,
    is_deleted BOOLEAN DEFAULT FALSE
);

CREATE TABLE suspeito (
    antecedentes VARCHAR,
    status_suspeito VARCHAR,
    fk_envolvido_id_envolvido INTEGER PRIMARY KEY,
    is_deleted BOOLEAN DEFAULT FALSE
);

CREATE TABLE vitima (
    status_vitima VARCHAR,
    fk_envolvido_id_envolvido INTEGER PRIMARY KEY,
    is_deleted BOOLEAN DEFAULT FALSE
);

CREATE TABLE prova (
    id_prova INTEGER PRIMARY KEY,
    descricao_prova VARCHAR,
    tipo_prova VARCHAR,
    data_coleta VARCHAR,
    fk__crime_id_crime INTEGER,
    is_deleted BOOLEAN DEFAULT FALSE
);

CREATE TABLE crime (
    data_crime VARCHAR,
    id_crime INTEGER PRIMARY KEY,
    descricao_crime VARCHAR,
    local_crime VARCHAR,
    status_crime VARCHAR,
    fk_delegacia_id_delegacia INTEGER,
    fk_id_tipo_crime INTEGER,
    is_deleted BOOLEAN DEFAULT FALSE
);

CREATE TABLE Tipo_Crime (
    id_tipo_crime INTEGER PRIMARY KEY,
    categoria VARCHAR,
    descricao VARCHAR,
    is_deleted BOOLEAN DEFAULT FALSE
);

CREATE TABLE tipo_prova (
    id_tipo INTEGER PRIMARY KEY,
    nome VARCHAR,
    descricao VARCHAR,
    fk_prova_id_prova INTEGER,
    is_deleted BOOLEAN DEFAULT FALSE
);

CREATE TABLE envolvido_crime (
    fk__crime_id_crime INTEGER,
    fk_envolvido_id_envolvido INTEGER
);

CREATE TABLE agente_crime (
    fk_agente_id_agente INTEGER,
    fk__crime_id_crime INTEGER
);
 
ALTER TABLE departamento ADD CONSTRAINT FK_departamento_2
    FOREIGN KEY (fk_delegacia_id_delegacia)
    REFERENCES delegacia (id_delegacia)
    ON DELETE RESTRICT;
 
ALTER TABLE veiculo ADD CONSTRAINT FK_veiculo_2
    FOREIGN KEY (fk_delegacia_id_delegacia)
    REFERENCES delegacia (id_delegacia)
    ON DELETE RESTRICT;
 
ALTER TABLE agente ADD CONSTRAINT FK_agente_2
    FOREIGN KEY (fk_delegacia_id_delegacia)
    REFERENCES delegacia (id_delegacia)
    ON DELETE RESTRICT;
 
ALTER TABLE testemunha ADD CONSTRAINT FK_testemunha_2
    FOREIGN KEY (fk_envolvido_id_envolvido)
    REFERENCES envolvido (id_envolvido)
    ON DELETE CASCADE;
 
ALTER TABLE criminoso ADD CONSTRAINT FK_criminoso_2
    FOREIGN KEY (fk_envolvido_id_envolvido)
    REFERENCES envolvido (id_envolvido)
    ON DELETE CASCADE;
 
ALTER TABLE suspeito ADD CONSTRAINT FK_suspeito_2
    FOREIGN KEY (fk_envolvido_id_envolvido)
    REFERENCES envolvido (id_envolvido)
    ON DELETE CASCADE;
 
ALTER TABLE vitima ADD CONSTRAINT FK_vitima_2
    FOREIGN KEY (fk_envolvido_id_envolvido)
    REFERENCES envolvido (id_envolvido)
    ON DELETE CASCADE;
 
ALTER TABLE prova ADD CONSTRAINT FK_prova_2
    FOREIGN KEY (fk__crime_id_crime)
    REFERENCES crime (id_crime)
    ON DELETE RESTRICT;
 
ALTER TABLE crime ADD CONSTRAINT FK_crime_delegacia
    FOREIGN KEY (fk_delegacia_id_delegacia)
    REFERENCES delegacia (id_delegacia)
    ON DELETE RESTRICT;

ALTER TABLE crime ADD CONSTRAINT FK_crime_tipo_crime
    FOREIGN KEY (fk_id_tipo_crime)
    REFERENCES Tipo_Crime (id_tipo_crime)
    ON DELETE RESTRICT;
 
ALTER TABLE tipo_prova ADD CONSTRAINT FK_tipo_prova_2
    FOREIGN KEY (fk_prova_id_prova)
    REFERENCES prova (id_prova)
    ON DELETE RESTRICT;
 
ALTER TABLE envolvido_crime ADD CONSTRAINT FK_envolvido_crime_1
    FOREIGN KEY (fk__crime_id_crime)
    REFERENCES crime (id_crime)
    ON DELETE RESTRICT;
 
ALTER TABLE envolvido_crime ADD CONSTRAINT FK_envolvido_crime_2
    FOREIGN KEY (fk_envolvido_id_envolvido)
    REFERENCES envolvido (id_envolvido)
    ON DELETE RESTRICT;
 
ALTER TABLE agente_crime ADD CONSTRAINT FK_agente_crime_1
    FOREIGN KEY (fk_agente_id_agente)
    REFERENCES agente (id_agente)
    ON DELETE RESTRICT;
 
ALTER TABLE agente_crime ADD CONSTRAINT FK_agente_crime_2
    FOREIGN KEY (fk__crime_id_crime)
    REFERENCES crime (id_crime)
    ON DELETE RESTRICT;