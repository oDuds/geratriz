from datetime import time
from app.database import SessionLocal
from app.models import Matriz, Disciplina, Oferta

db = SessionLocal()

SEMESTRE = "2026.2"

matriz_2023 = db.query(Matriz).filter(Matriz.nome == "2023").first()
if not matriz_2023:
    raise SystemExit("Matriz 2023 não encontrada. Rode o seed_completo.py primeiro.")

# (codigo, dia_ou_None, hora_inicio_ou_None, hora_fim_ou_None, professor, vagas)
ofertas_data = [
    # 1º período
    ("EFL100A", "segunda", time(8, 0), time(10, 0), "Prof. A definir", 40),
    ("P145A", "segunda", time(10, 0), time(12, 0), "Prof. A definir", 40),
    ("P146A", "terca", time(8, 0), time(10, 0), "Prof. A definir", 40),
    ("P147A", "terca", time(10, 0), time(12, 0), "Prof. A definir", 40),
    ("P148A", "quarta", time(8, 0), time(10, 0), "Prof. A definir", 40),
    ("P184A", "quarta", time(10, 0), time(12, 0), "Prof. A definir", 40),

    # 2º período
    ("ELE100A", "quinta", time(8, 0), time(10, 0), "Prof. A definir", 40),
    ("P149A", "quinta", time(10, 0), time(12, 0), "Prof. A definir", 40),
    ("P150A", "sexta", time(8, 0), time(10, 0), "Prof. A definir", 40),
    ("P151A", "sexta", time(10, 0), time(12, 0), "Prof. A definir", 40),
    ("P152A", "segunda", time(14, 0), time(16, 0), "Prof. A definir", 40),
    ("P185A", "terca", time(14, 0), time(16, 0), "Prof. A definir", 40),

    # 3º período
    ("EFL101A", "quarta", time(14, 0), time(16, 0), "Prof. A definir", 40),
    ("PCO148A", "quarta", time(16, 0), time(18, 0), "Prof. A definir", 40),
    ("P153A", "quinta", time(14, 0), time(16, 0), "Prof. A definir", 40),
    ("P154A", "quinta", time(16, 0), time(18, 0), "Prof. A definir", 40),
    ("P155A", "sexta", time(14, 0), time(16, 0), "Prof. A definir", 40),
    ("P156A", "sexta", time(16, 0), time(18, 0), "Prof. A definir", 40),
    ("P157A", "segunda", time(16, 0), time(18, 0), "Prof. A definir", 40),

    # 4º período
    ("ETO102A", "terca", time(16, 0), time(18, 0), "Prof. A definir", 40),
    ("PCO149A", "quarta", time(19, 0), time(21, 0), "Prof. A definir", 40),
    ("P159A", "quinta", time(19, 0), time(21, 0), "Prof. A definir", 40),
    ("P160A", "sexta", time(19, 0), time(21, 0), "Prof. A definir", 40),
    ("P161A", "segunda", time(19, 0), time(21, 0), "Prof. A definir", 40),
    ("P162A", "terca", time(19, 0), time(21, 0), "Prof. A definir", 40),
    ("P163A", "quarta", time(21, 0), time(22, 0), "Prof. A definir", 40),
    ("P164A", "quinta", time(21, 0), time(22, 0), "Prof. A definir", 40),

    # 5º período
    ("PCO150A", "segunda", time(8, 0), time(10, 0), "Prof. A definir", 40),
    ("P165A", "terca", time(8, 0), time(10, 0), "Prof. A definir", 40),
    ("P166A", "quarta", time(8, 0), time(10, 0), "Prof. A definir", 40),
    ("P167A", "quinta", time(8, 0), time(10, 0), "Prof. A definir", 40),
    ("P168A", "sexta", time(8, 0), time(10, 0), "Prof. A definir", 40),
    ("P169A", "segunda", time(10, 0), time(12, 0), "Prof. A definir", 40),
    ("P170A", "terca", time(10, 0), time(12, 0), "Prof. A definir", 40),

    # 6º período
    ("PCO151A", "quarta", time(10, 0), time(12, 0), "Prof. A definir", 40),
    ("PCO152A", "quinta", time(10, 0), time(12, 0), "Prof. A definir", 40),
    ("P171A", "sexta", time(10, 0), time(12, 0), "Prof. A definir", 40),
    ("P172A", "segunda", time(14, 0), time(16, 0), "Prof. A definir", 40),
    ("P173A", "terca", time(14, 0), time(16, 0), "Prof. A definir", 40),
    ("P186A", "quarta", time(14, 0), time(16, 0), "Prof. A definir", 40),

    # 7º período
    ("PCO154A", "quinta", time(14, 0), time(16, 0), "Prof. A definir", 40),
    ("PCO158A", "sexta", time(14, 0), time(16, 0), "Prof. A definir", 40),
    ("P174A", "segunda", time(16, 0), time(18, 0), "Prof. A definir", 40),
    ("P175A", "terca", time(16, 0), time(18, 0), "Prof. A definir", 40),
    ("P176A", "quarta", time(16, 0), time(18, 0), "Prof. A definir", 40),
    ("P177A", "quinta", time(16, 0), time(18, 0), "Prof. A definir", 40),

    # 8º período
    ("PCO153A", "sexta", time(16, 0), time(18, 0), "Prof. A definir", 40),
    ("PCO155A", "segunda", time(19, 0), time(21, 0), "Prof. A definir", 40),
    ("PCO156A", "terca", time(19, 0), time(21, 0), "Prof. A definir", 40),
    ("PCO157A", None, None, None, "Coordenação de Estágio", None),  # Estágio, sem horário fixo
    ("PCO159A", "quarta", time(19, 0), time(21, 0), "Prof. A definir", 40),
    ("P187A", "quinta", time(19, 0), time(21, 0), "Prof. A definir", 40),

    # 9º período
    ("PCO160A", "sexta", time(19, 0), time(21, 0), "Prof. A definir", 40),
    ("PCO161A", "segunda", time(21, 0), time(22, 0), "Prof. A definir", 40),
    ("PCO162A", "terca", time(21, 0), time(22, 0), "Prof. A definir", 40),
    ("PCO163A", "quarta", time(12, 0), time(13, 0), "Prof. A definir", 40),
    ("PCO164A", "quinta", time(12, 0), time(13, 0), "Prof. A definir", 40),

    # 10º período
    ("PCO165A", "sexta", time(12, 0), time(13, 0), "Prof. A definir", 40),
    ("PCO166A", "segunda", time(12, 0), time(13, 0), "Prof. A definir", 40),
    ("PCO167A", "terca", time(12, 0), time(13, 0), "Prof. A definir", 40),
    ("PCO168A", "quarta", time(22, 0), time(23, 0), "Prof. A definir", 40),
    ("P178A", "quinta", time(22, 0), time(23, 0), "Prof. A definir", 40),
    ("P188A", "sexta", time(22, 0), time(23, 0), "Prof. A definir", 40),
]

codigos = [item[0] for item in ofertas_data]
disciplinas = {
    d.codigo: d
    for d in db.query(Disciplina)
    .filter(Disciplina.matriz_id == matriz_2023.id, Disciplina.codigo.in_(codigos))
    .all()
}

criadas = 0
puladas = []
for codigo, dia, inicio, fim, professor, vagas in ofertas_data:
    if codigo not in disciplinas:
        puladas.append(codigo)
        continue
    oferta = Oferta(
        disciplina_id=disciplinas[codigo].id,
        semestre=SEMESTRE,
        professor=professor,
        dia_semana=dia,
        horario_inicio=inicio,
        horario_fim=fim,
        vagas=vagas,
    )
    db.add(oferta)
    criadas += 1

db.commit()
print(f"{criadas} ofertas criadas para a matriz 2023, semestre {SEMESTRE}")
if puladas:
    print(f"Códigos não encontrados (puladas): {puladas}")
db.close()
