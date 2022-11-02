from flask import Flask, jsonify
from model import Deck, AlgoritmoRandomico, Partida

app = Flask(__name__)



@app.get('/jogadas')
def getJogadas():
    partida = Partida(AlgoritmoRandomico(1), AlgoritmoRandomico(2))
    return jsonify(partida.play())

# 1 - Ativar o virtual_envoroment rodando o env/Scripts/Activate.ps1 no powerShell
# 2 - rodar "flask --app server run" no terminal para iniciar o server de desenvolvimento