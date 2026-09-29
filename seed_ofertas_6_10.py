from datetime import time
from app.database import SessionLocal
from app.models import Disciplina, Oferta

db = SessionLocal()

SEMESTRE = "2026.2"

# (codigo, dia_ou_None, hora_inicio_ou_None, hora_fim_ou_None, professor, vagas)
ofertas_data = [
    # 6º período
    ("PCP112A", "segunda", time(8, 0), time(10, 0), "Prof. A definir", 40),
    ("PCP114A", "segunda", time(10, 0), time(12, 0), "Prof. A definir", 40),
    ("PSI107A", "terca", time(8, 0), time(10, 0), "Prof. A definir", 40),
    ("PSI124A", "terca", time(10, 0), time(12, 0), "Prof. A definir", 40),
    ("P119A", "quarta", time(8, 0), time(10, 0), "Prof. A definir", 40),
    ("P121A", "quarta", time(10, 0), time(12, 0), "Prof. A definir", 40),

    # 7º período
    ("PCA100A", "quinta", time(14, 0), time(16, 0), "Prof. A definir", 40),
    ("PCP100A", "quinta", time(16, 0), time(18, 0), "Prof. A definir", 40),
    ("PCP110A", "sexta", time(14, 0), time(16, 0), "Prof. A definir", 40),
    ("PCP116A", "sexta", time(16, 0), time(18, 0), "Prof. A definir", 40),
    ("PEL116A", "segunda", time(14, 0), time(16, 0), "Prof. A definir", 40),
    ("P109A", "terca", time(14, 0), time(16, 0), "Prof. A definir", 40),

    # 8º período
    ("PCA102A", "quarta", time(14, 0), time(16, 0), "Prof. A definir", 40),
    ("PCP105A", "quinta", time(19, 0), time(21, 0), "Prof. A definir", 40),
    ("PCP106A", None, None, None, "Coordenação de Estágio", None),  # Estágio, sem horário fixo
    ("PCP108A", "sexta", time(19, 0), time(21, 0), "Prof. A definir", 40),
    ("PEL100A", "segunda", time(19, 0), time(21, 0), "Prof. A definir", 40),
    ("PEL104A", "terca", time(19, 0), time(21, 0), "Prof. A definir", 40),

    # 9º período
    ("PCA109A", "quarta", time(19, 0), time(21, 0), "Prof. A definir", 40),
    ("PCP109A", "quinta", time(8, 0), time(10, 0), "Prof. A definir", 40),
    ("PCP115A", "quinta", time(10, 0), time(12, 0), "Prof. A definir", 40),
    ("PCP117A", "sexta", time(8, 0), time(10, 0), "Prof. A definir", 40),
    ("PEL115A", "sexta", time(10, 0), time(12, 0), "Prof. A definir", 40),
    ("P103A", "segunda", time(21, 0), time(22, 0), "Prof. A definir", 40),

    # 10º período
    ("PCP107A", "terca", time(21, 0), time(22, 0), "Prof. A definir", 40),
    ("PCP111A", "quarta", time(21, 0), time(22, 0), "Prof. A definir", 40),
    ("PEL113A", "quinta", time(21, 0), time(22, 0), "Prof. A definir", 40),
    ("PSE102A", "sexta", time(21, 0), time(22, 0), "Prof. A definir", 40),
    ("P110A", "quinta", time(12, 0), time(13, 0), "Prof. A definir", 40),
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
print(f"{criadas} ofertas criadas para o semestre {SEMESTRE} (períodos 6 a 10)")
if puladas:
    print(f"Códigos não encontrados (puladas): {puladas}")
db.close()
