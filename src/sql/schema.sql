CREATE TABLE IF NOT EXISTS cotacoes_moedas (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    moeda VARCHAR(10) NOT NULL,
    nome VARCHAR(100) NOT NULL,
    maxima NUMERIC(15, 4) NOT NULL,
    minima NUMERIC(15, 4) NOT NULL,
    compra NUMERIC(15, 4) NOT NULL,
    venda NUMERIC(15, 4) NOT NULL,
    data_cotacao TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_cotacoes_moeda_data 
ON cotacoes_moedas (moeda, data_cotacao);