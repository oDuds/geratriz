from app.database import SessionLocal
from app.models import Matriz, Disciplina, PreRequisito, Aluno
from app.security import hash_senha
from sqlalchemy import text

db = SessionLocal()

# --- 1. Limpar tudo ---
db.execute(text("TRUNCATE TABLE aluno_disciplina, oferta, pre_requisito, aluno, disciplina, matriz RESTART IDENTITY CASCADE"))
db.commit()

# --- 2. Criar as duas matrizes ---
matriz_2018 = Matriz(nome="2018", unidade_carga="creditos", total_carga=250)
matriz_2023 = Matriz(nome="2023", unidade_carga="horas_relogio", total_carga=3585)
db.add_all([matriz_2018, matriz_2023])
db.commit()
db.refresh(matriz_2018)
db.refresh(matriz_2023)

# --- 3. Disciplinas da matriz 2018 ---
# (codigo, nome, periodo, carga, tipo, ocupa_grade)
disciplinas_2018_data = [
    ("EFL100A", "Filosofia", 1, 4, "obrigatoria", True),
    ("P122A", "Concepção e Design em Engenharia", 1, 4, "obrigatoria", True),
    ("P123A", "Modelagem e Simulação do Mundo Físico", 1, 6, "obrigatoria", True),
    ("P124A", "Química dos Materiais", 1, 6, "obrigatoria", True),
    ("P125A", "Tecnologias em um Mundo em Transformação", 1, 4, "obrigatoria", True),

    ("ETO100A", "Cultura Religiosa", 2, 2, "obrigatoria", True),
    ("P101A", "Computação Aplicada à Engenharia", 2, 4, "obrigatoria", True),
    ("P106A", "Engenharia no Mundo Biológico", 2, 4, "obrigatoria", True),
    ("P108A", "Física do Movimento", 2, 6, "obrigatoria", True),
    ("P118A", "Modelagem de Sistemas", 2, 6, "obrigatoria", True),

    ("EFL101A", "Ética", 3, 2, "obrigatoria", True),
    ("ELE100A", "Leitura e Escrita Acadêmica", 3, 4, "obrigatoria", True),
    ("P102A", "Concepção de Soluções Baseadas em Aplicativos", 3, 4, "obrigatoria", True),
    ("P104A", "Eletricidade e Aplicações", 3, 6, "obrigatoria", True),
    ("P105A", "Empreendedorismo Inovador", 3, 4, "obrigatoria", True),
    ("P117A", "Modelagem Avançada de Sistemas", 3, 6, "obrigatoria", True),

    ("PCP113A", "Programação Imperativa", 4, 4, "obrigatoria", True),
    ("P107A", "Fenômenos de Transporte e Aplicações", 4, 6, "obrigatoria", True),
    ("P111A", "Instrumentação, Transdutores e Medição", 4, 4, "obrigatoria", True),
    ("P114A", "Mecânica dos Sólidos", 4, 4, "obrigatoria", True),
    ("P115A", "Métodos Numéricos Computacionais", 4, 4, "obrigatoria", True),
    ("P116A", "Métodos Quantitativos para Engenharia", 4, 4, "obrigatoria", True),

    ("PCO125A", "Programação Orientada a Objetos", 5, 4, "obrigatoria", True),
    ("PCP102A", "Concepção e Design de Sistemas Digitais", 5, 6, "obrigatoria", True),
    ("PEL101A", "Análise de Circuitos Elétricos", 5, 6, "obrigatoria", True),
    ("P100A", "Administração para Engenharia", 5, 4, "obrigatoria", True),
    ("P113A", "Investigação Científica", 5, 4, "obrigatoria", True),

    ("PCP112A", "Programação com Estruturas de Dados Avançadas", 6, 4, "obrigatoria", True),
    ("PCP114A", "Projeto de Sistemas Microprocessados", 6, 4, "obrigatoria", True),
    ("PSI107A", "Banco de Dados", 6, 4, "obrigatoria", True),
    ("PSI124A", "Resolução de Problemas com Lógica Matemática", 6, 4, "obrigatoria", True),
    ("P119A", "Modelagem e Análise de Projeto de Investimentos", 6, 4, "obrigatoria", True),
    ("P121A", "Projeto de Engenharia", 6, 6, "obrigatoria", True),

    ("PCA100A", "Análise de Sinais e Sistemas", 7, 4, "obrigatoria", True),
    ("PCP100A", "Arquitetura e Organização de Computadores", 7, 4, "obrigatoria", True),
    ("PCP110A", "Modelagem de Sistemas Computacionais", 7, 4, "obrigatoria", True),
    ("PCP116A", "Sistemas de Computação", 7, 4, "obrigatoria", True),
    ("PEL116A", "Projeto de Circuitos Eletrônicos", 7, 6, "obrigatoria", True),
    ("P109A", "Gestão Socioambiental", 7, 4, "obrigatoria", True),

    ("PCA102A", "Concepção e Design de Sistemas de Controle", 8, 4, "obrigatoria", True),
    ("PCP105A", "Engenharia de Software", 8, 4, "obrigatoria", True),
    ("PCP106A", "Estágio Curricular de Engenharia de Computação", 8, 11, "obrigatoria", False),
    ("PCP108A", "Inteligência Artificial e Computacional", 8, 4, "obrigatoria", True),
    ("PEL100A", "Algoritmos Probabilísticos", 8, 2, "obrigatoria", True),
    ("PEL104A", "Conectividade de Dispositivos e Sistemas", 8, 4, "obrigatoria", True),

    ("PCA109A", "Implementação e Operação de Sistemas de Controle", 9, 4, "obrigatoria", True),
    ("PCP109A", "Linguagens Formais e Compiladores", 9, 4, "obrigatoria", True),
    ("PCP115A", "Projeto e Análise de Algoritmos", 9, 2, "obrigatoria", True),
    ("PCP117A", "Sistemas Distribuídos e Concorrentes", 9, 4, "obrigatoria", True),
    ("PEL115A", "Processamento Digital de Sinais", 9, 4, "obrigatoria", True),
    ("P103A", "Concepção e Design de Projeto Transformador", 9, 2, "obrigatoria", True),

    ("PCP107A", "Gestão de Projetos de Tecnologia da Informação", 10, 4, "obrigatoria", True),
    ("PCP111A", "Otimização de Sistemas Lineares", 10, 2, "obrigatoria", True),
    ("PEL113A", "Legislação, Ergonomia e Segurança do Trabalho", 10, 4, "obrigatoria", True),
    ("PSE102A", "Segurança da Informação", 10, 4, "obrigatoria", True),
    ("P110A", "Implementação e Operação de Projeto Transformador", 10, 1, "obrigatoria", True),
]

# --- 4. Disciplinas da matriz 2023 (carga em horas relógio) ---
disciplinas_2023_data = [
    ("EFL100A", "Filosofia", 1, 60, "obrigatoria", True),
    ("P145A", "Design de Soluções para Engenharia", 1, 60, "obrigatoria", True),
    ("P146A", "Modelagem do Mundo Físico", 1, 60, "obrigatoria", True),
    ("P147A", "Raciocínio Computacional na Engenharia", 1, 60, "obrigatoria", True),
    ("P148A", "Modelagem de Problemas Usando Cálculo Diferencial", 1, 60, "obrigatoria", True),
    ("P184A", "Eletricidade Instrumental", 1, 60, "obrigatoria", True),

    ("ELE100A", "Leitura e Escrita Acadêmica", 2, 60, "obrigatoria", True),
    ("P149A", "Química Geral Aplicada", 2, 60, "obrigatoria", True),
    ("P150A", "Modelagem de Problemas Usando Álgebra Linear", 2, 60, "obrigatoria", True),
    ("P151A", "Modelagem de Problemas Usando Cálculo a Várias Variáveis", 2, 60, "obrigatoria", True),
    ("P152A", "Fenômenos Mecânicos e Térmicos", 2, 90, "obrigatoria", True),
    ("P185A", "Princípios de Robótica", 2, 60, "obrigatoria", True),

    ("EFL101A", "Ética", 3, 30, "obrigatoria", True),
    ("PCO148A", "Programação Imperativa", 3, 60, "obrigatoria", True),
    ("P153A", "Fenômenos Elétricos", 3, 60, "obrigatoria", True),
    ("P154A", "Modelagem de Problemas usando Equações Diferenciais", 3, 60, "obrigatoria", True),
    ("P155A", "Introdução à Ciência dos Materiais", 3, 30, "obrigatoria", True),
    ("P156A", "Administração e Economia para Engenharia", 3, 30, "obrigatoria", True),
    ("P157A", "Pesquisa e Análise Científica", 3, 60, "obrigatoria", True),

    ("ETO102A", "Teologia e Sociedade", 4, 30, "obrigatoria", True),
    ("PCO149A", "Programação Orientada a Objetos", 4, 60, "obrigatoria", True),
    ("P159A", "Métodos Numéricos Computacionais", 4, 60, "obrigatoria", True),
    ("P160A", "Gestão Ambiental", 4, 60, "obrigatoria", True),
    ("P161A", "Introdução à Mecânica dos Sólidos", 4, 60, "obrigatoria", True),
    ("P162A", "Introdução aos Fenômenos de Transporte", 4, 60, "obrigatoria", True),
    ("P163A", "Princípios de Física Moderna", 4, 30, "obrigatoria", True),
    ("P164A", "Concepção de Circuitos Elétricos", 4, 60, "obrigatoria", True),

    ("PCO150A", "Programação com Estrutura de Dados Avançadas", 5, 60, "obrigatoria", True),
    ("P165A", "Projeto de Produto", 5, 60, "obrigatoria", True),
    ("P166A", "Análise De Viabilidade de Projetos", 5, 30, "obrigatoria", True),
    ("P167A", "Métodos Quantitativos para Engenharia", 5, 60, "obrigatoria", True),
    ("P168A", "Projeto de Circuitos Elétricos", 5, 60, "obrigatoria", True),
    ("P169A", "Análise de Sinais e Sistemas", 5, 60, "obrigatoria", True),
    ("P170A", "Concepção e Design de Sistemas Digitais", 5, 90, "obrigatoria", True),

    ("PCO151A", "Banco de Dados", 6, 60, "obrigatoria", True),
    ("PCO152A", "Resolução de Problemas com Lógica Matemática", 6, 60, "obrigatoria", True),
    ("P171A", "Projeto de Negócio Inovador", 6, 60, "obrigatoria", True),
    ("P172A", "Concepção e Design de Sistemas de Controle", 6, 60, "obrigatoria", True),
    ("P173A", "Projeto de Circuitos Eletrônicos", 6, 90, "obrigatoria", True),
    ("P186A", "Sistemas de Computação", 6, 60, "obrigatoria", True),

    ("PCO154A", "Ciência de Dados", 7, 60, "obrigatoria", True),
    ("PCO158A", "Modelagem de Sistemas Computacionais", 7, 60, "obrigatoria", True),
    ("P174A", "Implementação e Operação de Sistemas de Controle", 7, 60, "obrigatoria", True),
    ("P175A", "Processamento Digital de Sinais", 7, 60, "obrigatoria", True),
    ("P176A", "Implementação de Circuitos Eletrônicos", 7, 60, "obrigatoria", True),
    ("P177A", "Projeto de Sistemas Microprocessados", 7, 60, "obrigatoria", True),

    ("PCO153A", "Arquitetura e Organização de Computadores", 8, 60, "obrigatoria", True),
    ("PCO155A", "Algoritmos Probabilísticos", 8, 30, "obrigatoria", True),
    ("PCO156A", "Inteligência Artificial e Computacional", 8, 60, "obrigatoria", True),
    ("PCO157A", "Estágio Curricular de Engenharia de Computação", 8, 165, "obrigatoria", False),
    ("PCO159A", "Sistemas Embarcados", 8, 60, "obrigatoria", True),
    ("P187A", "Conectividade de Dispositivos e Sistemas", 8, 60, "obrigatoria", True),

    ("PCO160A", "Engenharia de Software", 9, 60, "obrigatoria", True),
    ("PCO161A", "Linguagens Formais e Compiladores", 9, 60, "obrigatoria", True),
    ("PCO162A", "Projeto e Análise de Algoritmos", 9, 30, "obrigatoria", True),
    ("PCO163A", "Projeto Final de Curso em Engenharia de Computação I", 9, 30, "obrigatoria", True),
    ("PCO164A", "Sistemas Distribuídos e Concorrentes", 9, 60, "obrigatoria", True),

    ("PCO165A", "Gestão de Projetos de Tecnologia da Informação", 10, 60, "obrigatoria", True),
    ("PCO166A", "Otimização de Sistemas Lineares", 10, 30, "obrigatoria", True),
    ("PCO167A", "Projeto Final de Curso em Engenharia de Computação II", 10, 30, "obrigatoria", True),
    ("PCO168A", "Segurança da Informação", 10, 60, "obrigatoria", True),
    ("P178A", "Legislação, Ergonomia e Segurança do Trabalho", 10, 30, "obrigatoria", True),
    ("P188A", "Automação Industrial", 10, 30, "obrigatoria", True),
]


def criar_disciplinas(dados, matriz_id):
    criadas = {}
    for codigo, nome, periodo, carga, tipo, ocupa_grade in dados:
        d = Disciplina(
            matriz_id=matriz_id,
            codigo=codigo,
            nome=nome,
            periodo_sugerido=periodo,
            carga=carga,
            tipo=tipo,
            ocupa_grade=ocupa_grade,
        )
        db.add(d)
        db.commit()
        db.refresh(d)
        criadas[codigo] = d
    return criadas


disc_2018 = criar_disciplinas(disciplinas_2018_data, matriz_2018.id)
disc_2023 = criar_disciplinas(disciplinas_2023_data, matriz_2023.id)

# --- 5. Pré-requisitos da matriz 2018 ---
# (disciplina_exige, tipo, disciplina_exigida_ou_None, natureza_ou_None, valor_minimo_ou_None)
requisitos_2018 = [
    ("P108A", "direto", "P118A", "co_requisito_direcional", None),
    ("P118A", "direto", "P123A", "co_requisito_direcional", None),
    ("P102A", "direto", "P101A", "requisito_especial", None),
    ("P104A", "direto", "P108A", "co_requisito_direcional", None),
    ("P117A", "direto", "P118A", "pre_requisito", None),

    ("PCP113A", "direto", "P101A", "co_requisito_direcional", None),
    ("P107A", "direto", "P118A", "co_requisito_direcional", None),
    ("P111A", "direto", "P104A", "co_requisito_direcional", None),
    ("P114A", "direto", "P108A", "co_requisito_direcional", None),
    ("P115A", "direto", "P101A", "co_requisito_direcional", None),
    ("P115A", "direto", "P117A", "co_requisito_direcional", None),

    ("PCP102A", "direto", "P111A", "co_requisito_direcional", None),
    ("PEL101A", "direto", "P104A", "requisito_especial", None),
    ("P113A", "direto", "ELE100A", "pre_requisito", None),
    ("P113A", "direto", "P125A", "co_requisito_direcional", None),
    ("P113A", "acumulo", None, None, 30),

    ("PCP112A", "direto", "PCO125A", "requisito_especial", None),
    ("PCP114A", "direto", "PCP102A", "co_requisito_direcional", None),
    ("P119A", "direto", "P100A", "co_requisito_direcional", None),
    ("P121A", "direto", "P122A", "pre_requisito", None),
    ("P121A", "acumulo", None, None, 35),

    ("PCA100A", "direto", "P117A", "requisito_especial", None),
    ("PCP100A", "direto", "PCP102A", "co_requisito_direcional", None),
    ("PCP116A", "acumulo", None, None, 50),
    ("PEL116A", "direto", "PEL101A", "requisito_especial", None),
    ("P109A", "direto", "P119A", "co_requisito_direcional", None),
    ("P109A", "acumulo", None, None, 50),

    ("PCA102A", "direto", "PEL101A", "co_requisito_direcional", None),
    ("PCA102A", "direto", "PCA100A", "requisito_especial", None),
    ("PCP105A", "direto", "PCP110A", "requisito_especial", None),
    ("PCP106A", "acumulo", None, None, 65),
    ("PCP108A", "direto", "PCP112A", "co_requisito_direcional", None),
    ("PEL100A", "direto", "P116A", "co_requisito_direcional", None),
    ("PEL104A", "direto", "PCP116A", "co_requisito_direcional", None),

    ("PCA109A", "direto", "PCA102A", "requisito_especial", None),
    ("PCP109A", "direto", "PCP112A", "co_requisito_direcional", None),
    ("PCP115A", "direto", "PCP113A", "pre_requisito", None),
    ("PCP117A", "direto", "PCP116A", "requisito_especial", None),
    ("PEL115A", "direto", "PCA100A", "requisito_especial", None),
    ("P103A", "direto", "P113A", "pre_requisito", None),
    ("P103A", "acumulo", None, None, 70),

    ("PCP107A", "direto", "PCP105A", "requisito_especial", None),
    ("PCP111A", "direto", "P116A", "pre_requisito", None),
    ("PEL113A", "acumulo", None, None, 50),
    ("P110A", "direto", "P103A", "pre_requisito", None),
]

# --- 6. Pré-requisitos da matriz 2023 (acumulo em horas absolutas) ---
requisitos_2023 = [
    ("P151A", "direto", "P148A", "pre_requisito", None),
    ("P151A", "direto", "P150A", "co_requisito_direcional", None),
    ("P152A", "direto", "P151A", "co_requisito_direcional", None),
    ("P152A", "direto", "P146A", "requisito_especial", None),

    ("PCO148A", "direto", "P147A", "pre_requisito", None),
    ("P153A", "direto", "P152A", "requisito_especial", None),
    ("P154A", "direto", "P150A", "requisito_especial", None),
    ("P154A", "direto", "P151A", "requisito_especial", None),
    ("P155A", "direto", "P149A", "pre_requisito", None),
    ("P155A", "direto", "P148A", "requisito_especial", None),

    ("PCO149A", "direto", "PCO148A", "requisito_especial", None),
    ("P159A", "direto", "P147A", "pre_requisito", None),
    ("P159A", "direto", "P148A", "co_requisito_direcional", None),
    ("P160A", "acumulo", None, None, 500),
    ("P161A", "direto", "P146A", "pre_requisito", None),
    ("P162A", "direto", "P152A", "pre_requisito", None),
    ("P162A", "direto", "P151A", "requisito_especial", None),
    ("P163A", "direto", "P153A", "co_requisito_direcional", None),

    ("PCO150A", "direto", "PCO149A", "requisito_especial", None),
    ("P165A", "direto", "P145A", "pre_requisito", None),
    ("P165A", "direto", "P167A", "co_requisito_direcional", None),
    ("P166A", "direto", "P156A", "pre_requisito", None),
    ("P167A", "direto", "P151A", "pre_requisito", None),
    ("P168A", "direto", "P164A", "requisito_especial", None),
    ("P169A", "direto", "P154A", "requisito_especial", None),
    ("P170A", "direto", "P184A", "pre_requisito", None),

    ("P171A", "direto", "P166A", "pre_requisito", None),
    ("P172A", "direto", "P168A", "requisito_especial", None),
    ("P172A", "direto", "P169A", "requisito_especial", None),
    ("P173A", "direto", "P168A", "requisito_especial", None),
    ("P186A", "direto", "P147A", "pre_requisito", None),

    ("PCO154A", "direto", "PCO151A", "requisito_especial", None),
    ("P174A", "direto", "P172A", "requisito_especial", None),
    ("P176A", "direto", "P173A", "requisito_especial", None),
    ("P177A", "direto", "P170A", "requisito_especial", None),

    ("PCO153A", "direto", "P177A", "requisito_especial", None),
    ("PCO155A", "direto", "P167A", "requisito_especial", None),
    ("PCO157A", "acumulo", None, None, 2500),
    ("PCO159A", "direto", "P177A", "requisito_especial", None),
    ("P187A", "direto", "P186A", "requisito_especial", None),

    ("PCO160A", "direto", "PCO158A", "requisito_especial", None),
    ("PCO161A", "direto", "PCO150A", "requisito_especial", None),
    ("PCO162A", "direto", "PCO150A", "pre_requisito", None),
    ("PCO163A", "direto", "P157A", "co_requisito_direcional", None),
    ("PCO163A", "acumulo", None, None, 2500),
    ("PCO164A", "direto", "P186A", "requisito_especial", None),

    ("PCO166A", "direto", "PCO148A", "requisito_especial", None),
    ("PCO166A", "direto", "P167A", "requisito_especial", None),
    ("PCO167A", "direto", "PCO163A", "pre_requisito", None),
    ("P188A", "direto", "P187A", "requisito_especial", None),
]


def criar_requisitos(lista, disciplinas_dict):
    for cod_exige, tipo, cod_exigida, natureza, valor in lista:
        pr = PreRequisito(
            disciplina_id=disciplinas_dict[cod_exige].id,
            tipo=tipo,
            disciplina_requisito_id=disciplinas_dict[cod_exigida].id if cod_exigida else None,
            natureza=natureza,
            valor_minimo=valor,
        )
        db.add(pr)
    db.commit()


criar_requisitos(requisitos_2018, disc_2018)
criar_requisitos(requisitos_2023, disc_2023)

# --- 7. Recriar seu usuário de teste ---
aluno = Aluno(
    nome="Eduardo",
    email="eduardo.orives@pucpr.edu.br",
    senha_hash=hash_senha("senhateste"),
    matriz_id=matriz_2018.id,
)
db.add(aluno)
db.commit()
db.refresh(aluno)

print(f"Matriz 2018: id={matriz_2018.id}, {len(disc_2018)} disciplinas, {len(requisitos_2018)} requisitos")
print(f"Matriz 2023: id={matriz_2023.id}, {len(disc_2023)} disciplinas, {len(requisitos_2023)} requisitos")
print(f"Aluno criado: id={aluno.id}")
db.close()