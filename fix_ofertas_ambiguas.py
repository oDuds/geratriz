from datetime import time
from app.database import SessionLocal
from app.models import Matriz, Disciplina, Oferta

db = SessionLocal()

SEMESTRE = "2026.2"
CODIGOS_AMBIGUOS = ["EFL100A", "ELE100A", "EFL101A"]

matriz_2018 = db.query(Matriz).filter(Matriz.nome == "2018").first()
matriz_2023 = db.query(Matriz).filter(Matriz.nome == "2023").first()

disciplinas_2018 = {
    d.codigo: d
    for d in db.query(Disciplina)
    .filter(Disciplina.matriz_id == matriz_2018.id, Disciplina.codigo.in_(CODIGOS_AMBIGUOS))
    .all()
}
disciplinas_2023 = {
    d.codigo: d
    for d in db.query(Disciplina)
    .filter(Disciplina.matriz_id == matriz_2023.id, Disciplina.codigo.in_(CODIGOS_AMBIGUOS))
    .all()
}

ids_disciplinas_ambiguas = [d.id for d in disciplinas_2018.values()] + [d.id for d in disciplinas_2023.values()]

# --- 1. Apaga todas as ofertas existentes dessas disciplinas ambíguas (nas duas matrizes) ---
removidas = (
    db.query(Oferta)
    .filter(Oferta.disciplina_id.in_(ids_disciplinas_ambiguas), Oferta.semestre == SEMESTRE)
    .delete(synchronize_session=False)
)
db.commit()
print(f"{removidas} ofertas ambíguas removidas")

# --- 2. Recria corretamente, com matriz explícita ---
ofertas_corretas = [
    # (dicionario_disciplinas, codigo, dia, inicio, fim, professor, vagas)
    (disciplinas_2018, "EFL100A", "segunda", time(8, 0), time(10, 0), "Prof. A definir", 40),
    (disciplinas_2018, "ELE100A", "segunda", time(16, 0), time(18, 0), "Prof. A definir", 40),
    (disciplinas_2018, "EFL101A", "segunda", time(14, 0), time(16, 0), "Prof. A definir", 40),

    (disciplinas_2023, "EFL100A", "segunda", time(8, 0), time(10, 0), "Prof. A definir", 40),
    (disciplinas_2023, "ELE100A", "quinta", time(8, 0), time(10, 0), "Prof. A definir", 40),
    (disciplinas_2023, "EFL101A", "quarta", time(14, 0), time(16, 0), "Prof. A definir", 40),
]

criadas = 0
for disciplinas_dict, codigo, dia, inicio, fim, professor, vagas in ofertas_corretas:
    oferta = Oferta(
        disciplina_id=disciplinas_dict[codigo].id,
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
print(f"{criadas} ofertas recriadas corretamente (3 para matriz 2018, 3 para matriz 2023)")
db.close()
