from app.database import SessionLocal
from app.services.otimizador import listar_disciplinas_elegiveis, listar_candidatas_com_oferta

db = SessionLocal()

elegiveis = listar_disciplinas_elegiveis(db, aluno_id=1)
print(f"Disciplinas elegíveis para o aluno 1: {len(elegiveis)}")
for d in elegiveis:
    print(f"  - {d.codigo} | {d.nome} | período sugerido: {d.periodo_sugerido}")

print()

candidatas = listar_candidatas_com_oferta(db, aluno_id=1, semestre="2026.2")
print(f"Candidatas com oferta no semestre 2026.2: {len(candidatas)}")
for o in candidatas:
    print(f"  - {o.disciplina.codigo} | {o.disciplina.nome} | {o.dia_semana} {o.horario_inicio}-{o.horario_fim}")

db.close()