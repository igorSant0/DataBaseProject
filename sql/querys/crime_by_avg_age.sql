-- media de idade dos envolvidos em cada tipo de crime

SELECT
    tc.categoria AS tipo_crime,
    ROUND(AVG(e.idade), 2) AS media_idade_envolvidos
FROM
    envolvido e
JOIN envolvido_crime ec ON ec.fk_envolvido_id_envolvido = e.id_envolvido
JOIN crime c ON ec.fk_crime_id_crime = c.id_crime AND c.is_deleted = FALSE
JOIN Tipo_Crime tc ON c.fk_id_tipo_crime = tc.id_tipo_crime AND tc.is_deleted = FALSE
WHERE
    e.is_deleted = FALSE
GROUP BY
    tc.categoria
ORDER BY
    media_idade_envolvidos DESC;