SELECT
    c.id_crime,
    c.descricao_crime,
    COUNT(DISTINCT ac.fk_agente_id_agente) AS total_agentes,
    COUNT(DISTINCT p.id_prova) AS total_provas,
    CASE WHEN COUNT(DISTINCT ac.fk_agente_id_agente) > 0
         THEN ROUND(COUNT(DISTINCT p.id_prova)::numeric / COUNT(DISTINCT ac.fk_agente_id_agente), 2)
         ELSE 0 END AS media_provas_por_agente
FROM
    crime c
LEFT JOIN agente_crime ac ON ac.fk_crime_id_crime = c.id_crime AND ac.is_deleted = FALSE
LEFT JOIN prova p ON p.fk_crime_id_crime = c.id_crime AND p.is_deleted = FALSE
WHERE
    c.is_deleted = FALSE
GROUP BY
    c.id_crime, c.descricao_crime
ORDER BY
    c.id_crime;