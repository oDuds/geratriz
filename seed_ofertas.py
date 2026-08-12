from datetime import time
from app.database import SessionLocal
from app.models import Disciplina, Oferta

db = SessionLocal()

# Busca as disciplinas pelo código, pra não depender de decorar IDs
codigos = ["ETO100A", "P101A", "P106A", "P108A", "P118A", "EFL101A", "ELE100A", "P105A"]
disciplinas = {d.codigo: d for d in db.query(Disciplina).filter(Disciplina.codigo.in_(codigos)).all()}

ofertas_data = [
    # (codigo, dia, hora_inicio, hora_fim)
    ("ETO100A", "segunda", time(8, 0), time(10, 0)),
    ("P101A", "segunda", time(10, 0), time(12, 0)),
    ("P106A", "segunda", time(8, 0), time(10, 0)),  # conflita com ETO100A de propósito
    ("P108A", "terca", time(8, 0), time(10, 0)),
    ("P118A", "terca", time(10, 0), time(12, 0)),
    ("EFL101A", "quarta", time(8, 0), time(10, 0)),
    ("ELE100A", "quarta", time(8, 0), time(10, 0)),  # conflita com EFL101A de propósito
    ("P105A", "quinta", time(14, 0), time(16, 0)),
]

for codigo, dia, inicio, fim in ofertas_data:
    oferta = Oferta(
        disciplina_id=disciplinas[codigo].id,
        semestre="2026.2",
        professor="A definir",
        dia_semana=dia,
        horario_inicio=inicio,
        horario_fim=fim,
        vagas=40,
    )
    db.add(oferta)

db.commit()
print(f"{len(ofertas_data)} ofertas criadas para o semestre 2026.2")
db.close()