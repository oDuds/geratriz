from app.database import SessionLocal
from app.services.otimizador import montar_grade

db = SessionLocal()

resultado = montar_grade(db, aluno_id=1, semestre="2026.2")

print(f"Total de disciplinas na grade: {resultado['total_disciplinas']}")
print(f"Total de créditos: {resultado['total_creditos']}")
print()
for oferta in resultado["grade"]:
    d = oferta.disciplina
    print(f"  - {d.codigo} | {d.nome} | {oferta.dia_semana} {oferta.horario_inicio}-{oferta.horario_fim}")

db.close()