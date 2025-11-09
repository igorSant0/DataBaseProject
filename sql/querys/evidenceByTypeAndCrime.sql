SELECT tc.categoria AS tipo_crime, tp.nome AS tipo_prova, COUNT(p.id_prova) AS total_provas
FROM crime c
JOIN tipo_crime tc ON c.fk_id_tipo_crime = tc.id_tipo_crime
JOIN prova p ON p.fk__crime_id_crime = c.id_crime
JOIN tipo_prova tp ON tp.fk_prova_id_prova = p.id_prova
GROUP BY tc.categoria, tp.nome
ORDER BY tc.categoria, total_provas DESC;