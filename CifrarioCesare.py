alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWYZ"

testo_da_cryptare = raw_input("Digita un testo: ").upper()

lunghezza_testo = len(testo_da_cryptare)

testo_cryptato = ""

for i in range(lunghezza_testo):
    location_char = alfabeto.find(testo_da_cryptare[i])
    new_location_char = location_char + 3
    testo_cryptato += alfabeto[new_location_char]

print("Testo cryptato: %s") %testo_cryptato

