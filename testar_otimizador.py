from app.database import SessionLocal
from app.services.otimizador import listar_disciplinas_elegiveis

db = SessionLocal()

elegiveis = listar_disciplinas_elegiveis(db, aluno_id=1)
print(f"Disciplinas elegíveis para o aluno 1: {len(elegiveis)}")
for d in elegiveis:
    print(f"  - {d.codigo} | {d.nome} | período sugerido: {d.periodo_sugerido}")

db.close()