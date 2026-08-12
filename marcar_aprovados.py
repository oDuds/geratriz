from app.database import SessionLocal
from app.models import Aluno, Disciplina, AlunoDisciplina

db = SessionLocal()

aprovadas = [1, 2, 3, 4, 5]

for disciplina_id in aprovadas:
    registro = AlunoDisciplina(aluno_id=1, disciplina_id=disciplina_id, status="aprovado")
    db.add(registro)

db.commit()
print(f"{len(aprovadas)} disciplinas marcadas como aprovadas para o aluno 1")
db.close()