from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import json
from truco import Match
from randomico import RandomAlgorithm
from monte_carlo import MonteCarloTreeSearchAlgorithm
from baseline import BaselineAlgorithm

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
        print('RANDOM')
        return RandomAlgorithm(algorithm['id'])
    elif algorithm['algorithm'] == 'BASELINE':
        print('BASELINE')
        return BaselineAlgorithm(algorithm['id'])
    else:
        print('MONTECARLO')
        return MonteCarloTreeSearchAlgorithm(algorithm['id'])

if __name__ == '__main__':
    app.run()