# Truco Backend
Backend para o jogo de truco da matéria de PIN3

# Setup do projeto

1. Criar virtual environment com ```python -m venv env```
2. Ativar o virtual environment rodando o script `env/Scripts/activate`
3. instalar dependências com ```pip install -r .\requirements.txt```
4. rodar ```flask --app index run``` no terminal para iniciar o server de desenvolvimento
5. Endpoint de produção: https://truco-server.vercel.app
# Endpoints:
POST /match
### REQUEST:
```
[
    {
        "id": 0,
        "algorithm": "RANDOM"
    },
    {
        "id": 1,
        "algorithm": "BASELINE1"
    }
]
```

### RESPONSE
```
{
	"points": [9,12],
	"winner": 1,
	"matches": [
		{
			"joker": "3_COPAS",
			"match_id": "bc430f73",
			"player_1": [
				"11_PAUS",
				"4_MOLES",
				"12_MOLES"
			],
			"player_2": [
				"4_ESPADAS",
				"12_ESPADAS",
				"10_ESPADAS"
			],
			"plays": [
				{
					"card": "12_MOLES",
					"player": 0,
					"type": "PLAY"
				},
				{
					"card": "12_ESPADAS",
					"player": 1,
					"type": "PLAY"
				},
				{
					"type": "TIE"
				},
				{
					"card": "4_MOLES",
					"player": 0,
					"type": "PLAY"
				},
				{
					"card": "4_ESPADAS",
					"player": 1,
					"type": "PLAY"
				},
				{
					"player": 1,
					"points": 1,
					"type": "WIN"
				}
			],
			"points": 1,
			"winner": 1
		}, ...
	],
}
```

### Exemplo de requisição CURL
```
curl --request POST \
  --url http://127.0.0.1:5000/match \
  --header 'Content-Type: application/json' \
  --data '[
    {
        "id": 0,
        "algorithm": "RANDOM"
    },
    {
        "id": 1,
        "algorithm": "RANDOM"
    }
]'

```


