-- Schema do projeto agente-ads
-- DigitalTech — Michel Freitas

CREATE TABLE IF NOT EXISTS produtos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT,
    preco DECIMAL(10, 2) NOT NULL CHECK (preco >= 0),
    estoque INT NOT NULL DEFAULT 0 CHECK (estoque >= 0),
    ativo BOOLEAN DEFAULT TRUE,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS historico_chat (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(50) NOT NULL,
    papel VARCHAR(20) NOT NULL CHECK (papel IN ('usuario', 'agente')),
    conteudo TEXT NOT NULL,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_historico_session ON historico_chat(session_id);
CREATE INDEX IF NOT EXISTS idx_produtos_ativo ON produtos(ativo);

-- Dados de exemplo para testes
INSERT INTO produtos (nome, descricao, preco, estoque) VALUES
('Notebook Linux', 'Notebook para desenvolvimento com Linux', 3500.00, 10),
('Mouse Gamer', 'Mouse ergonômico para longas horas de código', 150.00, 45),
('Teclado Mecânico', 'Teclado mecânico switch brown', 250.00, 0),
('Monitor 24"', 'Monitor Full HD para produtividade', 1200.00, 8),
('SSD 1TB', 'SSD NVMe para alta performance', 450.00, 20);
