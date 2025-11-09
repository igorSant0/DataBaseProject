SELECT d.chefe_delagacia AS delegacia, COUNT(c.id_crime) AS total_crimes
FROM crime c
JOIN delegacia d ON c.fk_delegacia_id_delegacia = d.id_delegacia
JOIN tipo_crime tc ON c.fk_id_tipo_crime = tc.id_tipo_crime
GROUP BY d.chefe_delagacia
ORDER BY total_crimes DESC;