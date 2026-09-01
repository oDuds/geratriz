# Geratriz — Backend

Sistema de geração automática de grade horária para estudantes de Engenharia de Computação. O Geratriz recebe o histórico acadêmico do aluno e as ofertas de disciplinas de um semestre, e monta a melhor combinação possível de disciplinas sem conflito de horário, respeitando pré-requisitos, co-requisitos e regras de acúmulo de créditos/horas.

Projeto pessoal desenvolvido como parte do meu portfólio, inspirado num problema real que enfrentei como estudante: montar a grade horária manualmente, testando combinação por combinação.
## Stack

- **Python 3.12** + **FastAPI** — API REST
- **PostgreSQL** + **SQLAlchemy** + **Alembic** — banco de dados e controle de migrations
- **JWT** (python-jose) + **bcrypt** (passlib) — autenticação
- **Pydantic** — validação de dados

## O problema, em termos técnicos

Montar uma grade horária é uma instância do **Course Timetabling Problem**, um problema clássico de satisfação de restrições (CSP): dado um conjunto de disciplinas candidatas, selecionar um subconjunto sem conflito de horário, respeitando dependências entre elas.

O algoritmo (em `app/services/otimizador.py`) resolve isso em três fases:

1. **Elegibilidade** — a partir do histórico do aluno, determina quais disciplinas ele pode cursar agora, verificando pré-requisitos diretos, co-requisitos direcionais e requisitos de acúmulo (percentual de créditos ou horas relógio concluídas, dependendo da matriz curricular).
2. **Cruzamento com ofertas** — filtra as elegíveis pelas que realmente têm turma aberta no semestre solicitado.
3. **Seleção sem conflito** — usa uma heurística gulosa, priorizando disciplinas mais atrasadas no fluxo curricular, para montar a maior grade possível sem sobreposição de horário, respeitando um limite opcional de créditos.

A estratégia gulosa foi escolhida deliberadamente para a primeira versão: é simples de implementar e explicar, e resolve bem o problema na prática. Uma evolução natural seria comparar com uma abordagem por backtracking ou programação por restrições (CSP solver), avaliando se a qualidade da solução melhora o suficiente para justificar a complexidade extra.

## Modelagem de dados

O desafio central de modelagem foi suportar **duas matrizes curriculares diferentes** (2018 e 2023) coexistindo no mesmo sistema, com regras de pré-requisito estruturalmente diferentes:

- A matriz 2018 mede carga em **créditos**, e alguns pré-requisitos são expressos como **percentual mínimo de créditos concluídos** (ex: só é possível cursar Estágio após completar 65% do curso).
- A matriz 2023 mede carga em **horas relógio**, e usa o mesmo tipo de regra, mas com valores absolutos de horas em vez de percentual.

Isso levou a uma tabela `pre_requisito` com um design semi-polimórfico: cada linha representa uma exigência (`tipo = "direto"` ou `"acumulo"`), com colunas condicionais dependendo do tipo. Essa estrutura também permite naturalmente que uma disciplina tenha múltiplos requisitos combinados (ex: "precisa ter passado em X **e** ter 70% dos créditos").

Outras decisões de modelagem:
- Disciplinas sem grade fixa (como Estágio) são marcadas com `ocupa_grade = False`, permitindo que contem na carga do aluno sem participar da checagem de conflito de horário.
- O histórico do aluno (`aluno_disciplina`) usa upsert (atualiza se existe, cria se não existe), refletindo que o status de uma disciplina evolui ao longo do tempo (cursando → aprovado/reprovado).

## Endpoints principais

| Rota | Descrição |
|---|---|
| `POST /alunos/cadastro` | Cadastro de aluno |
| `POST /alunos/login` | Login, retorna JWT |
| `GET /alunos/me` | Dados do aluno autenticado |
| `GET /aluno-disciplinas/` | Histórico do aluno logado |
| `POST /aluno-disciplinas/lote` | Atualiza o histórico em lote |
| `GET /grade/gerar` | Gera a grade otimizada para o aluno autenticado |

Documentação interativa completa disponível em `/docs` (Swagger UI).

## Rodando localmente

```bash
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt

# configurar .env com DATABASE_URL e SECRET_KEY

alembic upgrade head
python seed_completo.py       # popula as duas matrizes curriculares completas
python seed_ofertas_completo.py  # popula ofertas de exemplo

uvicorn app.main:app --reload
```

## Próximos passos

- Sugestão de preenchimento inteligente de brechas na grade via IA, quando não houver combinação perfeita sem conflito
- Suporte a equivalência entre disciplinas de diferentes matrizes (relevante para alunos com DP de longa data)
- Deploy em produção