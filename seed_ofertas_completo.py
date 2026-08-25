from datetime import time
from app.database import SessionLocal
from app.models import Disciplina, Oferta

db = SessionLocal()

SEMESTRE = "2026.2"

# (codigo, dia, hora_inicio, hora_fim, professor, vagas)
ofertas_data = [
    # 1º período
    ("EFL100A", "segunda", time(8, 0), time(10, 0), "Prof. A definir", 40),
    ("P122A", "segunda", time(10, 0), time(12, 0), "Prof. A definir", 40),
    ("P123A", "terca", time(8, 0), time(10, 0), "Prof. A definir", 40),
    ("P124A", "terca", time(10, 0), time(12, 0), "Prof. A definir", 40),
    ("P125A", "quarta", time(8, 0), time(10, 0), "Prof. A definir", 40),

    # 2º período
    ("ETO100A", "quarta", time(10, 0), time(12, 0), "Prof. A definir", 40),
    ("P101A", "quinta", time(8, 0), time(10, 0), "Prof. A definir", 40),
    ("P106A", "quinta", time(10, 0), time(12, 0), "Prof. A definir", 40),
    ("P108A", "sexta", time(8, 0), time(10, 0), "Prof. A definir", 40),
    ("P118A", "sexta", time(10, 0), time(12, 0), "Prof. A definir", 40),

    # 3º período
    ("EFL101A", "segunda", time(14, 0), time(16, 0), "Prof. A definir", 40),
    ("ELE100A", "segunda", time(16, 0), time(18, 0), "Prof. A definir", 40),
    ("P102A", "terca", time(14, 0), time(16, 0), "Prof. A definir", 40),
    ("P104A", "terca", time(16, 0), time(18, 0), "Prof. A definir", 40),
    ("P105A", "quarta", time(14, 0), time(16, 0), "Prof. A definir", 40),
    ("P117A", "quarta", time(16, 0), time(18, 0), "Prof. A definir", 40),

    # 4º período
    ("PCP113A", "quinta", time(14, 0), time(16, 0), "Prof. A definir", 40),
    ("P107A", "quinta", time(16, 0), time(18, 0), "Prof. A definir", 40),
    ("P111A", "sexta", time(14, 0), time(16, 0), "Prof. A definir", 40),
    ("P114A", "sexta", time(16, 0), time(18, 0), "Prof. A definir", 40),
    ("P115A", "segunda", time(19, 0), time(21, 0), "Prof. A definir", 40),
    ("P116A", "terca", time(19, 0), time(21, 0), "Prof. A definir", 40),

    # 5º período
    ("PCO125A", "quarta", time(19, 0), time(21, 0), "Prof. A definir", 40),
    ("PCP102A", "quinta", time(19, 0), time(21, 0), "Prof. A definir", 40),
    ("PEL101A", "sexta", time(19, 0), time(21, 0), "Prof. A definir", 40),
    ("P100A", "segunda", time(21, 0), time(22, 0), "Prof. A definir", 40),
    ("P113A", "terca", time(21, 0), time(22, 0), "Prof. A definir", 40),
]

codigos = [item[0] for item in ofertas_data]
disciplinas = {d.codigo: d for d in db.query(Disciplina).filter(Disciplina.codigo.in_(codigos)).all()}

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
print(f"{criadas} ofertas criadas para o semestre {SEMESTRE}")
if puladas:
    print(f"Códigos não encontrados (puladas): {puladas}")
db.close()