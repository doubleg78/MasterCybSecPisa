alphabet = "ABCDEFGHIJKLMNOPQRSTUVWYZ"

text_to_crypt = raw_input("Digita un testo: ").upper()
shift_crypt = int(raw_input("Digita valore avanzamento: "))

#while (len(alphabet) + shift_crypt) > len(alphabet): #option 1
#    shift_crypt -= len(alphabet)

text_length = len(text_to_crypt)

text_crypted = ""

for i in range(text_length):
    location_char = alphabet.find(text_to_crypt[i])
    new_location_char = (location_char + shift_crypt) %len(alphabet) #option 2
    #new_location_char = (location_char + shift_crypt) #option 1
    text_crypted += alphabet[new_location_char]

print("Testo cryptato: %s") %text_crypted

