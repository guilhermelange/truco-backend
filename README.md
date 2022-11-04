# Truco Backend
Backend para o jogo de truco da matéria de PIN3


# Endpoints:
POST /match
- REQUEST:
```
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
```

- RESPONSE
```
[{
	"winner": 1,
	"points": [3,12]
	"matchs": [
		{
			"joker": "2_COPAS",
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
			"plays": [
				{
					"type": "PLAY",
					"card": "2_COPAS",
					"player": 0,
					"point": 1
				},
				{
					"type": "PLAY",
					"card": "2_COPAS",
					"player": 1,
					"point": 1
				},
				{
					"type": "PLAY",
					"card": "2_COPAS",
					"player": 1,
					"point": 1
				},
				{
					"type": "TRUCO",
					"player": 1,
					"point": 1
				},
				{
					"type": "ACCEPT",
					"player": 2,
					"point": 3
				},
				{
					"type": "RUN",
					"player": 1,
					"point": 3
				},
				{
					"type": "WIN",
					"player": 2,
					"point": 3
				}
			]
		}
	]
}]
```

CURL
```
curl --request POST \
  --url http://127.0.0.1:5000/match \
  --header 'Content-Type: application/json' \
  --data '[
    {
        "id": 1,
        "algorithm": "RANDOM"
    },
    {
        "id": 2,
        "algorithm": "RANDOM"
    }
]'

```

## Deploy

Para o deploy, deve-se utilizar implementação WSGI `mod_wsgi` (https://pypi.org/project/mod-wsgi/), usar servidor do flask apenas para desenvolvimento.
