from flask import Flask, jsonify

app = Flask(__name__)

jogadas = [
    {"jogador": 1, "carta": 3, "truco" : False},
    {"jogador": 2, "carta": 6, "truco" : False},
    {"jogador": 1, "carta": 8, "truco" : False},
    {"jogador": 2, "carta": 4, "truco" : False},
    {"jogador": 1, "carta": 12, "truco" : False},
    {"jogador": 2, "carta": 7, "truco" : True},
    {"jogador": 1, "carta": 1, "truco" : False},
]

@app.get('/jogadas')
def get_test():
    return jsonify(jogadas)

# 1 - Ativar o virtual_envoroment rodando o env/Scripts/Activate.ps1 no powerShell
# 2 - rodar "flask --app server run" no terminal para iniciar o server de desenvolvimento