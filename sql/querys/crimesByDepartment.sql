SELECT 
    d.nome_departamento AS Departamento,
    dg.chefe_delagacia AS Chefe_Delegacia,
    COUNT(c.id_crime) AS Total_Crimes
FROM departamento d
JOIN delegacia dg 
    ON d.fk_delegacia_id_delegacia = dg.id_delegacia
JOIN crime c 
    ON c.fk_delegacia_id_delegacia = dg.id_delegacia
GROUP BY d.nome_departamento, dg.chefe_delagacia
ORDER BY Total_Crimes DESC;
