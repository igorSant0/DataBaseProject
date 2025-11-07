ALTER TABLE agente_crime DROP CONSTRAINT FK_agente_crime_2;
ALTER TABLE agente_crime DROP CONSTRAINT FK_agente_crime_1;

ALTER TABLE envolvido_crime DROP CONSTRAINT FK_envolvido_crime_2;
ALTER TABLE envolvido_crime DROP CONSTRAINT FK_envolvido_crime_1;

ALTER TABLE tipo_prova DROP CONSTRAINT FK_tipo_prova_2;

ALTER TABLE crime DROP CONSTRAINT FK_crime_tipo_crime;
ALTER TABLE crime DROP CONSTRAINT FK_crime_delegacia;

ALTER TABLE prova DROP CONSTRAINT FK_prova_2;

ALTER TABLE vitima DROP CONSTRAINT FK_vitima_2;

ALTER TABLE suspeito DROP CONSTRAINT FK_suspeito_2;

ALTER TABLE criminoso DROP CONSTRAINT FK_criminoso_2;

ALTER TABLE testemunha DROP CONSTRAINT FK_testemunha_2;

ALTER TABLE agente DROP CONSTRAINT FK_agente_2;

ALTER TABLE veiculo DROP CONSTRAINT FK_veiculo_2;

ALTER TABLE departamento DROP CONSTRAINT FK_departamento_2;

DROP TABLE agente_crime;
DROP TABLE envolvido_crime;
DROP TABLE tipo_prova;
DROP TABLE Tipo_Crime;
DROP TABLE crime;
DROP TABLE prova;
DROP TABLE vitima;
DROP TABLE suspeito;
DROP TABLE criminoso;
DROP TABLE testemunha;
DROP TABLE envolvido;
DROP TABLE agente;
DROP TABLE veiculo;
DROP TABLE departamento;
DROP TABLE delegacia;