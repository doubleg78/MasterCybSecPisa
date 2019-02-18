alphabet = "ABCDEFGHIJKLMNOPQRSTUVWYZ"

def crypt_text():
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
    return text_crypted


def uncrypt_text():
    print()

def menu():
    print "Welcome to CEASER Crypt Module"
    print "What do you want to do?"
    print "[1] Crypt a Text"
    print "[2] DeCrypt a Text"
    choose = (int(raw_input("Make your choose: \n")))
    if choose == 1:
        print "Testo cryptato: %s" % crypt_text()
    elif choose == 2:
        print "DeCrypted Text: %s" % uncrypt_text()
    else:
        print "Wrong option, please choose it again."
        menu()


if __name__ == '__main__':
    menu()





