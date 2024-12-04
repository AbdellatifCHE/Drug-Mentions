SELECT 
    t.client_id
    ,SUM(CASE WHEN p.product_type = 'MEUBLE' 
        THEN t.prod_price * t.prod_qty ELSE 0 END) AS ventes_meuble
    ,SUM(CASE WHEN p.product_type = 'DECO' 
        THEN t.prod_price * t.prod_qty ELSE 0 END) AS ventes_deco
FROM 
    TRANSACTIONS t
JOIN 
    PRODUCT_NOMENCLATURE p ON t.prod_id = p.product_id
WHERE
    /* 
        If the t.date column is not DATE type we should convert this column
        to DATE type by using the function PARSE_DATE('%d/%m/%y', `t.date`)
        instead of calling the t.date column directly.
    */
    t.date BETWEEN '01/01/19' AND '31/12/19'
    AND p.product_type IN ('MEUBLE', 'DECO')
GROUP BY 
    t.client_id
ORDER BY 
    t.client_id;
