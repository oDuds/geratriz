import urllib.request
import json

TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzg3ODY0ODgxfQ.CPoAEBsso_74WLxe8N2bF5XIUpa7VBCd2oXyGzbVinE"

url = "http://127.0.0.1:8000/matrizes/1"
dados = {
    "nome": "2018",
    "unidade_carga": "creditos",
    "total_carga": 250,
}

req = urllib.request.Request(
    url,
    data=json.dumps(dados).encode("utf-8"),
    method="PUT",
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {TOKEN}",
    },
)

try:
    with urllib.request.urlopen(req) as resposta:
        print("Status:", resposta.status)
        print("Resposta:", resposta.read().decode("utf-8"))
except urllib.error.HTTPError as e:
    print("Erro:", e.code)
    print(e.read().decode("utf-8"))