from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import json
from truco import Match
from randomico import AlgoritmoRandomico
from monte_carlo import AlogritmoMonteCarloTreeSearch
from baseline import AlgoritmoBaseline

app = Flask(__name__)
CORS(app)

@app.post('/match')
@cross_origin(supports_credentials=True)
def match_post_route():
    data = json.loads(request.data)
    return jsonify(runMatch(data[0], data[1]))


def runMatch(algorithmA, algorithmB):
    match = Match(getAlgorithm(algorithmA), getAlgorithm(algorithmB))
    return match.playMatch()


def getAlgorithm(algorithm):
    if algorithm['algorithm'] == 'RANDOM':
        return AlgoritmoRandomico(algorithm['id'])
    elif algorithm['algorithm'] == 'BASELINE':
        return AlgoritmoBaseline(algorithm['id'])
    else:
        return AlogritmoMonteCarloTreeSearch(algorithm['id'])

if __name__ == '__main__':
    app.run()