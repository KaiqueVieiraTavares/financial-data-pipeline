CREATE OR REPLACE VIEW vw_cotacao_mais_recente AS
with cotacoes_ordenadas as (
    SELECT id, moeda, nome, maxima, minima, compra, venda, data_cotacao,
    ROW_NUMBER() OVER (PARTITION BY moeda ORDER BY data_cotacao DESC) as posicao
    from cotacoes_moedas
)
select id,moeda, nome, maxima, minima, compra, venda, data_cotacao 
from cotacoes_ordenadas
where posicao = 1 


CREATE OR REPLACE VIEW vw_variacao_consecutiva AS 
WITH cotacoes_com_anterior AS (
    SELECT id, moeda, nome, maxima, minima, compra, venda, data_cotacao,
    LAG(compra) OVER (PARTITION BY moeda ORDER BY data_cotacao) AS compra_anterior
    from cotacoes_moedas
)
select id, moeda, nome, maxima, minima,compra_anterior, compra, venda, data_cotacao,
ROUND(compra - compra_anterior, 4) AS variacao_absoluta,
ROUND(((compra - compra_anterior) / NULLIF(compra_anterior, 0) * 100), 4) AS variacao_percentual
from cotacoes_com_anterior 
