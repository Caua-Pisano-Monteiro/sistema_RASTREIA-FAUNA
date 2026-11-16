# sistema_RASTREIA-FAUNA
# 🐾 Rastreia Fauna

Sistema web para registro, consulta e análise de ocorrências de apreensão de fauna silvestre.

---

## 1. Descrição do sistema e do problema

O combate ao tráfico e à posse ilegal de animais silvestres gera muitos registros de apreensão (espécie, quantidade, local, tipo de infração, autuado, multa). Quando esses dados ficam em planilhas soltas, é difícil saber onde as apreensões se concentram, quais espécies são mais afetadas e como o cenário evolui ao longo do tempo. Também é difícil manter equipe de campo e escritório trabalhando sobre a mesma base.

O **Rastreia Fauna** centraliza esses registros em um banco de dados único, com cadastro de usuários, login, formulário para novas ocorrências e um dashboard que transforma os dados em indicadores, mapa e gráficos.

## 2. Objetivo

Oferecer um sistema simples e acessível que permita **registrar ocorrências de apreensão de fauna** e **visualizar, de forma consolidada, os dados** para apoiar o acompanhamento e a tomada de decisão de pesquisadores, equipes de campo e instituições de conservação.

## 3. Principais funcionalidades

- **Página inicial (landing page)** com apresentação do sistema e acesso a login e cadastro.
- **Cadastro de usuários** com usuário, função, e-mail (com confirmação) e senha (com confirmação).
- **Login** com verificação de senha criptografada (hash bcrypt) e bloqueio após 3 tentativas incorretas.
- **Navegação condicionada à autenticação:** páginas internas só aparecem para usuários logados.
- **Registro de nova ocorrência** com validações:
  - data, tipo de infração, UF, município, código IBGE (7 dígitos), latitude e longitude;
  - espécie (o nome científico, a classe e o status de ameaça são preenchidos automaticamente);
  - quantidade, estado do animal, destinação, autuado, tipo de pessoa, valor da multa e unidade de controle;
  - geração automática da descrição quando o campo fica vazio;
  - geração do código sequencial da apreensão, com nova tentativa em caso de conflito.
- **Dashboard** com:
  - indicadores (animais apreendidos, total de ocorrências, valor total de multas);
  - mapa da América do Sul com a quantidade de apreensões por estado;
  - ranking de espécies apreendidas;
  - top 5 tipos de infração;
  - evolução mensal por ano;
  - tabela completa com os dados.
- **API REST** para login, usuários, consulta de apreensões e cadastro de apreensões.

## 4. Tecnologias utilizadas

| Camada | Tecnologia |
|---|---|
| Linguagem | Python 3 |
| Interface (front-end) | **Streamlit** (o sistema **não utiliza Tkinter**) |
| API (back-end) | FastAPI + Uvicorn |
| Banco de dados | PostgreSQL |
| ORM | SQLAlchemy |
| Validação de dados | Pydantic |
| Segurança de senhas | bcrypt |
| Análise e gráficos | pandas e Plotly |
| Comunicação front ↔ API | requests |

## 5. Estrutura do projeto

```
├── app.py            # Ponto de entrada do Streamlit e navegação
├── landing.py        # Página inicial
├── cadastro.py       # Tela de criação de conta
├── login.py          # Tela de login
├── dashboard.py      # Dashboard com indicadores e gráficos
├── ocorrencias.py    # Formulário de nova ocorrência
├── main.py           # API FastAPI (rotas)
├── database.py       # Conexão com o PostgreSQL
├── models.py         # Tabelas (SQLAlchemy)
├── schema.py         # Schemas (Pydantic)
└── docs/img/         # Imagens das telas usadas neste README
```

## 6. Instalação e execução

### Pré-requisitos

- Python 3.10 ou superior
- PostgreSQL em execução

### Passo a passo

**1. Clone o repositório e entre na pasta**

```bash
git clone <URL-DO-REPOSITORIO>
cd <NOME-DA-PASTA>
```

**2. Crie e ative um ambiente virtual**

```bash
python -m venv .venv

# Linux/macOS
source .venv/bin/activate
# Windows
.venv\Scripts\activate
```

**3. Instale as dependências**

```bash
pip install streamlit fastapi "uvicorn[standard]" sqlalchemy psycopg2-binary pydantic bcrypt pandas plotly requests
```

**4. Crie o banco de dados**

```sql
CREATE DATABASE db_rf;
```

**5. Configure as variáveis de ambiente (opcional)**

Se nada for definido, o sistema usa os valores padrão abaixo.

```bash
export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/db_rf"
export API_URL="http://127.0.0.1:8000"
```

As tabelas `usuarios_login` e `apreensoes_fauna` são criadas automaticamente na primeira execução da API.

**6. Inicie a API** (terminal 1)

```bash
uvicorn main:app --reload
```

A documentação interativa da API fica em `http://127.0.0.1:8000/docs`.

**7. Inicie a interface** (terminal 2)

```bash
streamlit run app.py
```

Acesse `http://localhost:8501`, crie uma conta e faça login.

> **Observação:** o dashboard e o formulário de ocorrências usam os registros já existentes na tabela `apreensoes_fauna` (por exemplo, para listar espécies e UFs). Carregue a base inicial de apreensões antes de usar essas telas.

### Rotas da API

| Método | Rota | Descrição |
|---|---|---|
| POST | `/login` | Autentica o usuário |
| POST | `/usuarios` | Cria um novo usuário |
| GET | `/data-usuarios` | Lista usuários |
| GET | `/data-request` | Lista as apreensões |
| POST | `/formulario-apreensao` | Registra uma nova apreensão |

## 7. Telas do sistema

> Salve os prints na pasta `docs/img/` com os nomes abaixo (ou ajuste os caminhos).

### Página inicial
![Página inicial](docs/img/landing.png)

### Cadastro
![Cadastro](docs/img/cadastro.png)

### Login
![Login](docs/img/login.png)

### Dashboard
![Dashboard](docs/img/dashboard.png)

### Nova ocorrência
![Nova ocorrência](docs/img/ocorrencia.png)

## 8. Integrantes do grupo

| Nome | 
|---|
| Nome do integrante 1 |
| Nome do integrante 2 |
| Nome do integrante 3 |

## 9. Instituição e disciplina

- **Instituição:** *(nome da instituição)*
- **Curso:** *(nome do curso)*
- **Disciplina:** *(nome da disciplina)*
- **Professor(a):** *(nome do professor)*
- **Semestre/Ano:** *(ex.: 2026.2)*
