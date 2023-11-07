    -- se a tabela produtos nao existir = cria a tabela: ↧
CREATE TABLE IF NOT EXISTS produtos (
    -- atributo da tabela - todo produto que sera cadastrado tera um atributo id / INTEIRO / é definido uma chave primaria = nao aceita registros duplicados - atibutos exclusivos ↧ 
    id_prod INTEGER PRIMARY KEY,
    -- nao pode cadastrar um produto no banco de dados sem ter um nome ↧
    nome_prod TEXT NOT NULL, 
    desc_prod TEXT NOT NULL,
    -- nao pode cadastrar um produto no banco de dados sem ter um preço / REAL valor decimal (float) ↧
    preco_prod REAL NOT NULL,
    -- nao pode cadastrar um produto no banco de dados sem ter imagem / é text porque vai colocar endereço da imagem, é isso o que ele lê ↧
    img_prod TEXT NOT NULL
);