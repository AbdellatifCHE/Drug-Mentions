SELECT 
    date AS date_commande,
    SUM(prod_price * prod_qty) AS CA
FROM TRANSACTIONS
WHERE 
    date BETWEEN '2019-01-01' AND '2019-12-31'
GROUP BY date
ORDER BY date_commande;
