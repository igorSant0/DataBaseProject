-- total de provas por agente relacionadas aos respectivos crimes 

SELECT
    a.cargo_agente,
    COUNT(DISTINCT p.id_prova) AS total_provas
FROM
    agente a
JOIN agente_crime ac ON ac.fk_agente_id_agente = a.id_agente AND ac.is_deleted = FALSE
JOIN crime c ON ac.fk_crime_id_crime = c.id_crime AND c.is_deleted = FALSE
LEFT JOIN prova p ON p.fk_crime_id_crime = c.id_crime AND p.is_deleted = FALSE
WHERE
    a.is_deleted = FALSE
GROUP BY
    a.cargo_agente
ORDER BY
    total_provas DESC;