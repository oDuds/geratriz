from app.database import SessionLocal
from app.models.matriz import Matriz
from app.models.disciplina import Disciplina
from app.models.pre_requisito import PreRequisito
from app.models.aluno import Aluno
from app.models.aluno_disciplina import AlunoDisciplina
from app.models.oferta import Oferta
from app.security import hash_senha
from sqlalchemy import text

db = SessionLocal()

# --- 1. Limpar tudo (ordem importa por causa das foreign keys) ---
db.execute(text("TRUNCATE TABLE aluno_disciplina, oferta, pre_requisito, aluno, disciplina, matriz RESTART IDENTITY CASCADE"))
db.commit()

# --- 2. Criar a matriz 2018 ---
matriz_2018 = Matriz(nome="2018", unidade_carga="creditos", total_carga=250)
db.add(matriz_2018)
db.commit()
db.refresh(matriz_2018)

# --- 3. Criar disciplinas dos 3 primeiros períodos ---
disciplinas_data = [
    # (codigo, nome, periodo, carga, tipo)
    ("EFL100A", "Filosofia", 1, 4, "obrigatoria"),
    ("P122A", "Concepção e Design em Engenharia", 1, 4, "obrigatoria"),
    ("P123A", "Modelagem e Simulação do Mundo Físico", 1, 6, "obrigatoria"),
    ("P124A", "Química dos Materiais", 1, 6, "obrigatoria"),
    ("P125A", "Tecnologias em um Mundo em Transformação", 1, 4, "obrigatoria"),

    ("ETO100A", "Cultura Religiosa", 2, 2, "obrigatoria"),
    ("P101A", "Computação Aplicada à Engenharia", 2, 4, "obrigatoria"),
    ("P106A", "Engenharia no Mundo Biológico", 2, 4, "obrigatoria"),
    ("P108A", "Física do Movimento", 2, 6, "obrigatoria"),
    ("P118A", "Modelagem de Sistemas", 2, 6, "obrigatoria"),

    ("EFL101A", "Ética", 3, 2, "obrigatoria"),
    ("ELE100A", "Leitura e Escrita Acadêmica", 3, 4, "obrigatoria"),
    ("P102A", "Concepção de Soluções Baseadas em Aplicativos", 3, 4, "obrigatoria"),
    ("P104A", "Eletricidade e Aplicações", 3, 6, "obrigatoria"),
    ("P105A", "Empreendedorismo Inovador", 3, 4, "obrigatoria"),
    ("P117A", "Modelagem Avançada de Sistemas", 3, 6, "obrigatoria"),
]

disciplinas = {}
for codigo, nome, periodo, carga, tipo in disciplinas_data:
    d = Disciplina(
        matriz_id=matriz_2018.id,
        codigo=codigo,
        nome=nome,
        periodo_sugerido=periodo,
        carga=carga,
        tipo=tipo,
    )
    db.add(d)
    db.commit()
    db.refresh(d)
    disciplinas[codigo] = d

# --- 4. Criar os pré-requisitos reais ---
pre_requisitos_data = [
    # (disciplina_que_exige, tipo, disciplina_exigida, natureza)
    ("P108A", "direto", "P118A", "co_requisito_direcional"),
    ("P118A", "direto", "P123A", "co_requisito_direcional"),
    ("P102A", "direto", "P101A", "requisito_especial"),
    ("P104A", "direto", "P108A", "co_requisito_direcional"),
    ("P117A", "direto", "P118A", "pre_requisito"),
]

for cod_exige, tipo, cod_exigida, natureza in pre_requisitos_data:
    pr = PreRequisito(
        disciplina_id=disciplinas[cod_exige].id,
        tipo=tipo,
        disciplina_requisito_id=disciplinas[cod_exigida].id,
        natureza=natureza,
    )
    db.add(pr)
db.commit()

# --- 5. Recriar seu usuário de teste ---
aluno = Aluno(
    nome="Eduardo",
    email="eduardo.orives@pucpr.edu.br",
    senha_hash=hash_senha("senhateste"),
    matriz_id=matriz_2018.id,
)
db.add(aluno)
db.commit()
db.refresh(aluno)

print(f"Matriz criada: id={matriz_2018.id}")
print(f"Disciplinas criadas: {len(disciplinas)}")
print(f"Aluno criado: id={aluno.id}")
db.close()