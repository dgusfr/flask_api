# SalesNexus API - Gerenciamento de Vendas e Produtos

Esta aplicação foi construída para simular um back-end real de e-commerce, resolvendo problemas comuns como autenticação segura, validação rigorosa de dados e processamento em lote de grandes volumes de informações via CSV.

---

## Tabela de Conteúdos

* [Arquitetura e Design Patterns](#arquitetura-e-design-patterns)
* [Tech Stack](#tech-stack)
* [Documentação da API](#documentação-da-api)
    * [Autenticação](#autenticação)
    * [Produtos](#produtos)
    * [Vendas (Upload CSV)](#vendas-e-uploads)
    * [Usuários](#usuários)
* [Estrutura do Projeto](#estrutura-do-projeto)
* [Melhorias Futuras](#melhorias-futuras)

---
___

## Arquitetura

O projeto segue estritamente o padrão **MVC (Model-View-Controller)** adaptado para APIs REST.

### Destaques Técnicos:
* **Modularização com Blueprints:** Separação lógica de rotas (auth, products, users) para facilitar a escalabilidade horizontal do código.
* **Validação com Pydantic:** Schemas fortes que impedem a entrada de dados inválidos ("Dirty Data") no MongoDB.
* **Autenticação Stateless:** Uso de JWT (JSON Web Tokens) para segurança escalável.
* **Bulk Operations:** O endpoint `/sales/upload` utiliza streaming de dados para processar arquivos CSV grandes sem estourar a memória RAM, realizando inserções em lote (`insert_many`).

---

## Tech Stack

* **Linguagem:** Python 3.10+
* **Framework:** Flask
* **Banco de Dados:** MongoDB (PyMongo)
* **Autenticação:** PyJWT
* **Validação:** Pydantic V2
* **Ambiente:** Python-dotenv

---
---

## Documentação da API

### Autenticação

Geração de token de acesso para rotas protegidas.
**Endpoint:** `POST /login`

```bash
curl -X POST http://localhost:5000/login \
-H "Content-Type: application/json" \
-d '{
    "username": "admin",
    "password": "123"
}'

```

**Respostas:**

* ✅ **200 OK**:

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6..."
}

```

* ❌ **400 Bad Request**:

```json
{
  "message": [
    {
      "type": "missing",
      "loc": ["body", "password"],
      "msg": "Field required"
    }
  ]
}

```

* ❌ **401 Unauthorized**:

```json
{
  "message": "Credenciais inválidas"
}

```

---
___

### Produtos

Gerenciamento do catálogo. Requer token Bearer para operações de escrita.

**Endpoints Principais:**

* `GET /products` (Público)
* `POST /products` (Protegido)
* `PUT /products/<id>` (Protegido)
* `DELETE /products/<id>` (Protegido)

**Exemplo: Criar Produto (cURL):**

```bash
curl -X POST http://localhost:5000/products \
-H "Authorization: Bearer SEU_TOKEN_AQUI" \
-H "Content-Type: application/json" \
-d '{
    "name": "Notebook Gamer",
    "price": 4500.00,
    "stock": 10,
    "description": "i7, 16GB RAM, RTX 3060"
}'

```

**Respostas:**

* ✅ **201 Created**:

```json
{
  "message": "Add a new product by user admin with id 659f8a..."
}

```

* ❌ **400 Bad Request**:

```json
{
  "message": [
    {
      "type": "less_than_equal",
      "loc": ["body", "price"],
      "msg": "Input should be less than or equal to 0"
    }
  ]
}

```

* ❌ **401 Unauthorized**:

```json
{
  "message": "Token is missing!"
}

```

* ❌ **404 Not Found**:

```json
{
  "message": "Product not found"
}

```

---
___

### Vendas e Uploads

Processamento em lote de vendas via arquivo.
**Endpoint:** `POST /sales/upload`

**Exemplo de Requisição (cURL):**

```bash
curl -X POST http://localhost:5000/sales/upload \
-H "Authorization: Bearer SEU_TOKEN_AQUI" \
-F "file=@/caminho/para/vendas.csv"

```

**Formato CSV Esperado:**

```csv
sale_date,product_id,quantity,total_value
2023-10-01,65123abcde,2,150.50

```

**Respostas:**

* ✅ **201 Created**:

```json
{
  "message": "Processamento concluído",
  "vendas_importadas": 150,
  "total_erros": 2,
  "detalhes_erros": [
    "Linha 4: Dados inválidos - value is not a valid float"
  ]
}

```

* ❌ **400 Bad Request**:

```json
{
  "error": "O arquivo deve ser um CSV"
}

```

* ❌ **500 Internal Server Error**:

```json
{
  "error": "Erro crítico ao salvar no banco: connection timed out"
}

```

---
___

### 👤 Usuários

Gestão de usuários do sistema.

**Endpoints Principais:**

* `GET /users` (Protegido)
* `POST /users` (Público - Registro)
* `DELETE /users/<id>` (Protegido)

**Exemplo: Listar Usuários (cURL):**

```bash
curl -X GET http://localhost:5000/users \
-H "Authorization: Bearer SEU_TOKEN_AQUI"

```

**Respostas:**

* ✅ **200 OK**:

```json
[
  {
    "_id": "659f8a...",
    "username": "admin",
    "email": "admin@example.com"
  }
]

```

* ✅ **201 Created**:

```json
{
  "message": "User created with ID: 659f8a..."
}

```

* ❌ **409 Conflict**:

```json
{
  "message": "Username already exists"
}

```

---
___

## 📂 Estrutura do Projeto

```text
/
├── app/
│   ├── config.py
│   ├── decorators.py
│   ├── __init__.py
│   ├── models/
│   │   ├── products.py
│   │   ├── sales.py
│   │   └── user.py
│   └── routes/
│       ├── auth.py
│       ├── products.py
│       └── users.py
├── .env
├── .gitignore
├── requirements.txt
└── run.py

```

---

## Melhorias Futuras

* Implementação de Testes Unitários (pytest).
* Containerização (Docker e Docker Compose).
* Documentação automática (Swagger/OpenAPI).

---

Desenvolvido por **Diego Franco**

