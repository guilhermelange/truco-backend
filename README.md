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
        "algorithm": "BASELINE"
    }
]
```

### RESPONSE
```
{
	"matches": [
		{
			"joker": "2_MOLES",
			"match_id": "894ffb5d",
			"player_1": [
				"7_COPAS",
				"1_PAUS",
				"11_COPAS"
			],
			"player_2": [
				"1_ESPADAS",
				"2_PAUS",
				"3_MOLES"
			],
			"plays": [
				{
					"card": "3_MOLES",
					"player": 1,
					"type": "PLAY"
				},
				{
					"card": "7_COPAS",
					"player": 0,
					"type": "PLAY"
				},
				{
					"card": "1_ESPADAS",
					"player": 1,
					"type": "PLAY"
				},
				{
					"card": "1_PAUS",
					"player": 0,
					"type": "PLAY"
				},
				{
					"type": "TIE"
				},
				{
					"player": 1,
					"points": 1,
					"type": "WIN"
				}
			],
			"points": 1,
			"winner": 1
		},
		[...]
	],
	"points": [
		5,
		13
	],
	"winner": 1
}
```

### Exemplo de requisição CURL
```
curl --location --request POST 'https://truco-server.vercel.app/match' \
--header 'Content-Type: application/json' \
--data-raw '[
    {
        "id": 0,
        "algorithm": "RANDOM"
    },
    {
        "id": 1,
        "algorithm": "BASELINE"
    }
]'

```


