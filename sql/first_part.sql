-- The target date format is %d/%m/%Y' (01/01/2020)
/* 
    If the t.date column is not DATE type we should ALWAYS convert this
    column to DATE type by using the function PARSE_DATE('%d/%m/%y', `t.date`)
    instead of calling the t.date column directly.
*/
SELECT 
    FORMAT_DATE('%d/%m/%Y', t.date) AS date_commande
    ,SUM(t.prod_price * t.prod_qty) AS CA
FROM TRANSACTIONS t
WHERE t.date BETWEEN '01/01/19' AND '31/12/19'
GROUP BY t.date
ORDER BY date_commande;