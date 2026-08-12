from app.database import SessionLocal
from app.models import AlunoDisciplina

db = SessionLocal()

# Marca "Modelagem de Sistemas" (id 10, conferir no seed) como cursando
registro = AlunoDisciplina(aluno_id=1, disciplina_id=10, status="cursando")
db.add(registro)
db.commit()
print("Modelagem de Sistemas marcada como 'cursando'")
db.close()