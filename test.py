from truco import Game
from baseline import AlgoritmoBaseline

a = AlgoritmoBaseline(1)
a2 = AlgoritmoBaseline(2)

g = Game(a, a2)

print(a.hand)

powerOrderNumbers = ['4', '5', '6', '7', '10', '11', '12', '1', '2', '3']
powerOrderNaipe = ['MOLES', 'ESPADAS', 'COPAS', 'PAUS']
manilha = '5'
# numeroA = cartaA.split('_')[0]
# naipeA = cartaA.split('_')[1]
# numeroB = cartaB.split('_')[0]
# naipeB = cartaB.split('_')[1]

handd = ['3_PAUS', '5_MOLES', '5_COPAS']
a = sorted(handd, key=lambda a : powerOrderNumbers.index(a.split('_')[0]) + (10 * int(a.split('_')[0]) if a.split('_')[0] == manilha else 0 + (10 * powerOrderNaipe.index(a.split('_')[1]))))
a.reverse()
print(a)
