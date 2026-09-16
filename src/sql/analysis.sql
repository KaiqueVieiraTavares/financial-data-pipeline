-- cotação mais recente de cada moeda
WITH cotacoes_ordenadas AS (
    SELECT
        id,
        moeda,
        nome,
        maxima,
        minima,
        compra,
        venda,
        data_cotacao,
        ROW_NUMBER() OVER (
            PARTITION BY moeda
            ORDER BY data_cotacao DESC, id DESC
        ) AS posicao
    FROM cotacoes_moedas
)
SELECT
    id,
    moeda,
    nome,
    maxima,
    minima,
    compra,
    venda,
    data_cotacao
FROM cotacoes_ordenadas
WHERE posicao = 1
ORDER BY moeda;


-- spread médio de cada moeda
SELECT
    moeda,
    nome,
    ROUND(AVG(venda - compra), 4) AS spread_medio,
    ROUND(
        AVG(((venda - compra) / NULLIF(compra, 0)) * 100),
        4
    ) AS spread_percentual_medio
FROM cotacoes_moedas
GROUP BY moeda, nome
ORDER BY spread_percentual_medio DESC;


-- resumo do histórico de cada moeda
SELECT
    moeda,
    nome,
    COUNT(*) AS quantidade_cotacoes,
    ROUND(AVG(compra), 4) AS media_compra,
    MIN(compra) AS menor_compra,
    MAX(compra) AS maior_compra,
    MIN(data_cotacao) AS primeira_cotacao,
    MAX(data_cotacao) AS ultima_cotacao
FROM cotacoes_moedas
GROUP BY moeda, nome
ORDER BY moeda;


-- amplitude percentual média de cada moeda
SELECT
    moeda,
    nome,
    ROUND(
        AVG(
            ((maxima - minima) / NULLIF(minima, 0)) * 100
        ),
        2
    ) AS amplitude_percentual_media
FROM cotacoes_moedas
GROUP BY moeda, nome
ORDER BY amplitude_percentual_media DESC;


-- variação entre cotações consecutivas
WITH cotacoes_com_anterior AS (
    SELECT
        id,
        moeda,
        nome,
        data_cotacao,
        compra,
        LAG(compra) OVER (
            PARTITION BY moeda
            ORDER BY data_cotacao, id
        ) AS compra_anterior
    FROM cotacoes_moedas
)
SELECT
    moeda,
    nome,
    data_cotacao,
    compra_anterior,
    compra,
    ROUND(compra - compra_anterior, 4) AS diferenca_absoluta,
    ROUND(
        ((compra - compra_anterior) /
        NULLIF(compra_anterior, 0)) * 100,
        2
    ) AS variacao_percentual
FROM cotacoes_com_anterior
WHERE compra_anterior IS NOT NULL
ORDER BY moeda, data_cotacao;


-- três maiores valores de compra de cada moeda
WITH ranking_compras AS (
    SELECT
        moeda,
        nome,
        compra,
        data_cotacao,
        DENSE_RANK() OVER (
            PARTITION BY moeda
            ORDER BY compra DESC
        ) AS posicao
    FROM cotacoes_moedas
)
SELECT
    moeda,
    nome,
    compra,
    data_cotacao,
    posicao
FROM ranking_compras
WHERE posicao <= 3
ORDER BY moeda, posicao, data_cotacao;


--  spread percentual de cada cotação
SELECT
    moeda,
    nome,
    compra,
    venda,
    ROUND(venda - compra, 4) AS spread_absoluto,
    ROUND(
        ((venda - compra) / NULLIF(compra, 0)) * 100,
        4
    ) AS spread_percentual,
    CASE
        WHEN ((venda - compra) / NULLIF(compra, 0)) * 100 >= 1
            THEN 'SPREAD ALTO'
        WHEN ((venda - compra) / NULLIF(compra, 0)) * 100 >= 0.5
            THEN 'SPREAD MEDIO'
        ELSE 'SPREAD BAIXO'
    END AS classificacao_spread,
    data_cotacao
FROM cotacoes_moedas
ORDER BY data_cotacao DESC, moeda;


-- Compara a primeira cotação com a última de cada moeda
WITH cotacoes_rankeadas AS (
    SELECT
        moeda,
        nome,
        compra,
        data_cotacao,
        ROW_NUMBER() OVER (
            PARTITION BY moeda
            ORDER BY data_cotacao, id
        ) AS ordem_crescente,
        ROW_NUMBER() OVER (
            PARTITION BY moeda
            ORDER BY data_cotacao DESC, id DESC
        ) AS ordem_decrescente
    FROM cotacoes_moedas
),
primeira_ultima AS (
    SELECT
        moeda,
        MAX(nome) AS nome,
        MAX(compra) FILTER (
            WHERE ordem_crescente = 1
        ) AS primeira_compra,
        MAX(compra) FILTER (
            WHERE ordem_decrescente = 1
        ) AS ultima_compra,
        MAX(data_cotacao) FILTER (
            WHERE ordem_crescente = 1
        ) AS data_primeira_compra,
        MAX(data_cotacao) FILTER (
            WHERE ordem_decrescente = 1
        ) AS data_ultima_compra
    FROM cotacoes_rankeadas
    GROUP BY moeda
)
SELECT
    moeda,
    nome,
    primeira_compra,
    ultima_compra,
    ROUND(ultima_compra - primeira_compra, 4) AS variacao_absoluta,
    ROUND(
        ((ultima_compra - primeira_compra) /
        NULLIF(primeira_compra, 0)) * 100,
        2
    ) AS variacao_percentual,
    data_primeira_compra,
    data_ultima_compra
FROM primeira_ultima
ORDER BY variacao_percentual DESC;


-- registros duplicados
SELECT
    moeda,
    data_cotacao,
    COUNT(*) AS quantidade
FROM cotacoes_moedas
GROUP BY moeda, data_cotacao
HAVING COUNT(*) > 1
ORDER BY quantidade DESC, moeda, data_cotacao;


-- inconsistências
SELECT
    id,
    moeda,
    nome,
    maxima,
    minima,
    compra,
    venda,
    data_cotacao,
    CASE
        WHEN maxima < minima
            THEN 'MAXIMA MENOR QUE MINIMA'
        WHEN compra <= 0
            THEN 'COMPRA MENOR OU IGUAL A ZERO'
        WHEN venda <= 0
            THEN 'VENDA MENOR OU IGUAL A ZERO'
        WHEN maxima <= 0
            THEN 'MAXIMA MENOR OU IGUAL A ZERO'
        WHEN minima <= 0
            THEN 'MINIMA MENOR OU IGUAL A ZERO'
        WHEN venda < compra
            THEN 'VENDA MENOR QUE COMPRA'
    END AS status_validacao
FROM cotacoes_moedas
WHERE maxima < minima
   OR compra <= 0
   OR venda <= 0
   OR maxima <= 0
   OR minima <= 0
   OR venda < compra
ORDER BY data_cotacao DESC;