SELECT
	a.cargo_agente,
    COUNT(DISTINCT ac.fk_crime_id_crime) AS total_crimes
FROM
    agente a
JOIN agente_crime ac ON ac.fk_agente_id_agente = a.id_agente AND ac.is_deleted = FALSE
JOIN crime c ON ac.fk_crime_id_crime = c.id_crime AND c.is_deleted = FALSE
WHERE
    a.is_deleted = FALSE
GROUP BY
    a.cargo_agente
ORDER BY
    total_crimes DESC;