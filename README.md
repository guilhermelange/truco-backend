# Truco Backend
Backend para o jogo de truco da matéria de PIN3


# Endpoints:
POST /match
- REQUEST:
[
    {
        "id": 1,
        "algorithm": "RANDOM"
    },
    {
        "id": 2,
        "algorithm": "BASELINE1"
    }
]


- RESPONSE
{
	"winner": 1,
	"points": [3,12]
	"matchs": [
		{
			"manilha": "2_COPAS",
			"winner": 2,
			"points": 3,
			"player1": [
				"2_COPAS",
				"2_COPAS",
				"2_COPAS"
			],
			"player2": [
				"2_COPAS",
				"2_COPAS",
				"2_COPAS"
			],
			"jogadas": [
				{
					"type": "PLAY",
					"card": "2_COPAS",
					"ponto": 1
				},
				{
					"type": "PLAY",
					"card": "2_COPAS",
					"ponto": 1
				},
				{
					"type": "PLAY",
					"card": "2_COPAS",
					"ponto": 1
				},
				{
					"type": "TRUCO",
					"user": 1
				},
				{
					"type": "ACCEPT",
					"user": 2
				},
				{
					"type": "RUN",
					"user": 1
				}
			]
		}
	]
}
