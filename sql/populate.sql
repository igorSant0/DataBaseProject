INSERT INTO delegacia (id_delegacia, chefe_delagacia)
VALUES  (1, 'Igor Santana'), (2, 'Gabriel da Silva'), (3, 'João Gabriel');

INSERT INTO departamento (id_departamento, nome_departamento, localicacao, telefone, email, area_atuacao, fk_delegacia_id_delegacia)
VALUES  (1, 'Investigação', 'Rua A, 123', 123456789, 'investigacao@delegacia.com', 'Crimes graves', 1),
        (2, 'Administração', 'Rua B, 456', 987654321, 'administracao@delegacia.com', 'Gestão interna', 2),
        (3, 'Tecnologia', 'Rua C, 789', 456789123, 'tecnologia@delegacia.com', 'Suporte técnico', 3);

INSERT INTO veiculo (id_veiculo, modelo, uso, status_veiculo, fk_delegacia_id_delegacia)
VALUES  (1, 'Corsa', 'Perseguição', 'Disponível', 1), 
        (2, 'Tracker', 'Investigação', 'Em manutenção', 2), 
        (3, 'Ferrari', 'Perseguição', 'Em operação', 3),
        (4, 'Hilux', 'Investigação', 'Disponível', 1),
        (5, 'Gol', 'Perseguição', 'Em operação', 2),
        (6, 'Duster', 'Investigação', 'Disponível', 3);

INSERT INTO agente (id_agente, cargo_agente, fk_delegacia_id_delegacia)
VALUES  (1, 'Investigador', 1), (2, 'Delegado', 2), (3, 'Perito', 3);

INSERT INTO envolvido (id_envolvido, nome, idade)
VALUES  (1, 'Carlos Pereira', 35), 
        (2, 'Ana Souza', 28), 
        (3, 'Roberto Lima', 40),
        (4, 'Joaozinho', 21), 
        (5, 'Mariazinha', 50),
        (6, 'Pedro Alves', 33),
        (7, 'Fernanda Costa', 27),
        (8, 'Lucas Martins', 45),
        (9, 'Marcos Oliveira', 42),
        (10, 'Juliana Ribeiro', 31),
        (11, 'Thiago Mendes', 29),
        (12, 'Patrícia Santos', 37),
        (13, 'Rafael Castro', 26),
        (14, 'Bruna Ferreira', 32),
        (15, 'Renato Gomes', 48),
        (16, 'Luciana Alves', 22);

INSERT INTO testemunha (relato, fk_envolvido_id_envolvido)
VALUES  ('Vi o suspeito fugindo.', 1), 
        ('Ouvi tiros na rua.', 2),
        ('Ouvi gritos vindos da casa.', 9),
        ('Vi um carro em alta velocidade fugindo.', 10);

INSERT INTO criminoso (pena, data_condenacao, fk_envolvido_id_envolvido)
VALUES  ('5 anos', '2025-01-15', 3), 
        ('10 anos', '2025-02-20', 4),
        ('2 anos', '2025-03-18', 11),
        ('20 anos', '2025-04-10', 12);

INSERT INTO suspeito (antecedentes, status_suspeito, fk_envolvido_id_envolvido)
VALUES  ('Roubo', 'Em investigação', 5), 
        ('Furto', 'Em liberdade', 6),
        ('Estelionato', 'Em investigação', 13),
        ('Violência doméstica', 'Detido', 14);

INSERT INTO vitima (status_vitima, fk_envolvido_id_envolvido)
VALUES  ('Recuperado', 7), 
        ('Falecido', 8),
        ('Grave', 15),
        ('Recuperando-se', 16);

INSERT INTO Tipo_Crime (id_tipo_crime, categoria, descricao)
VALUES  (1, 'Roubo', 'Roubo de veículo'), 
        (2, 'Assalto', 'Assalto à mão armada'), 
        (3, 'Furto', 'Furto de objetos pessoais'),
        (4, 'Homicídio', 'Crime contra a vida'),
        (5, 'Tráfico', 'Tráfico de drogas'),
        (6, 'Fraude', 'Fraude financeira'),
        (7, 'Sequestro', 'Sequestro de pessoas'),
        (8, 'Vandalismo', 'Danos ao patrimônio público');

INSERT INTO crime (data_crime, id_crime, descricao_crime, local_crime, status_crime, fk_delegacia_id_delegacia, fk_id_tipo_crime)
VALUES  ('2025-11-01', 1, 'Assalto ao banco', 'Rua C, 789', 'Resolvido', 1, 2),
        ('2025-11-02', 2, 'Assalto à loja', 'Rua D, 321', 'Em investigação', 2, 2),
        ('2025-11-03', 3, 'Homicídio culposo', 'Rua E, 456', 'Em aberto', 3, 4),
        ('2025-11-04', 4, 'Homicídio em residência', 'Rua F, 123', 'Resolvido', 1, 4),
        ('2025-11-05', 5, 'Tráfico de drogas', 'Rua G, 456', 'Em investigação', 2, 5),
        ('2025-11-06', 6, 'Tráfico de drogas', 'Rua H, 789', 'Em aberto', 3, 6),
        ('2025-11-07', 7, 'Assalto à residência', 'Rua I, 321', 'Resolvido', 1, 2),
        ('2025-11-08', 8, 'Vandalismo em praça pública', 'Rua J, 654', 'Em aberto', 2, 8),
        ('2025-11-09', 9, 'Furto em residência', 'Rua L, 111', 'Em investigação', 1, 3),
        ('2025-11-10', 10, 'Sequestro de empresário', 'Rua M, 222', 'Em aberto', 2, 7),
        ('2025-11-11', 11, 'Fraude bancária', 'Rua N, 333', 'Resolvido', 3, 6),
        ('2025-11-12', 12, 'Assalto em mercado', 'Rua O, 444', 'Em aberto', 1, 2),
        ('2025-11-13', 13, 'Vandalismo em escola', 'Rua P, 555', 'Resolvido', 2, 8),
        ('2025-11-14', 14, 'Roubo de carga', 'Rodovia Q, KM 19', 'Em investigação', 3, 1),
        ('2025-11-15', 15, 'Homicídio em bar', 'Rua R, 666', 'Em aberto', 1, 4),
        ('2025-11-16', 16, 'Tráfico de drogas', 'Rua S, 777', 'Resolvido', 2, 5);

INSERT INTO prova (id_prova, descricao_prova, tipo_prova, data_coleta, fk_crime_id_crime)
VALUES  (1, 'Impressões digitais', 'Digital', '2025-11-03', 1),
        (2, 'Câmeras de segurança', 'Visual', '2025-11-04', 2),
        (3, 'Testemunho', 'Oral', '2025-11-05', 3),
        (4, 'DNA encontrado', 'Biológico', '2025-11-06', 4),
        (5, 'Gravação telefônica', 'Áudio', '2025-11-07', 5),
        (6, 'Extrato bancário', 'Documental', '2025-11-08', 6),
        (7, 'Relato de vítima', 'Oral', '2025-11-09', 7),
        (8, 'Fotos do local', 'Visual', '2025-11-10', 8),
        (9, 'Pegadas no local', 'Visual', '2025-11-10', 9),
        (10, 'Ligação gravada', 'Áudio', '2025-11-11', 10),
        (11, 'Depoimento de vizinho', 'Oral', '2025-11-12', 11),
        (12, 'Análise de sangue', 'Biológico', '2025-11-13', 12),
        (13, 'Documentos adulterados', 'Documental', '2025-11-14', 13),
        (14, 'Vídeo de celular', 'Visual', '2025-11-15', 14),
        (15, 'Digital em arma', 'Digital', '2025-11-16', 15),
        (16, 'Relato de testemunha', 'Oral', '2025-11-17', 16);

INSERT INTO tipo_prova (id_tipo, nome, descricao, fk_prova_id_prova)
VALUES  (1, 'Digital', 'Impressões digitais coletadas', 1),
        (2, 'Visual', 'Imagens de câmeras de segurança', 2),
        (3, 'Oral', 'Relatos de testemunhas', 3),
        (4, 'Biológico', 'DNA encontrado no local', 4),
        (5, 'Áudio', 'Gravações telefônicas', 5),
        (6, 'Documental', 'Extratos bancários e documentos', 6),
        (7, 'Oral', 'Relatos de vítimas', 7),
        (8, 'Visual', 'Fotos do local do crime', 8);

INSERT INTO envolvido_crime (fk_crime_id_crime, fk_envolvido_id_envolvido)
VALUES  (1, 1),(2, 2),(3, 3),(4, 4),(5, 5),(6, 6),(7, 7),(8, 8),
        (9, 9),(10, 10),(11, 11),(12, 12),(13, 13),(14, 14),(15, 15),(16, 16);

INSERT INTO agente_crime (fk_agente_id_agente, fk_crime_id_crime)
VALUES  (1, 1),(2, 2),(3, 3),(1, 4),(2, 5),(3, 6),(1, 7),(2, 8),
        (1, 9),(3, 10),(2, 11),(1, 12),(3, 13),(2, 14),(1, 15),(3, 16);
