alphabet = "ABCDEFGHIJKLMNOPQRSTUVWYZ"

def crypt_text():
    alphabet_option = "0"
    while alphabet_option not in ["1", "2", ""]:
        alphabet_option = raw_input("Do you want to use standard 26 Alphabet (ABCDEFGHIJKLMNOPQRSTUVWYZ) ? \n[1] Yes\n[2] No\nor press Enter for standard\n")
    if alphabet_option == 2:
        alphabet = raw_input("Please type your Alphabet: \n")
    text_to_crypt = raw_input("Type the text to be encrypted: ").upper()
    shift_crypt = int(raw_input("Type the shift value: "))

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
    alphabet_option = "0"
    while alphabet_option not in ["1", "2", ""]:
        alphabet_option = raw_input("Do you want to use standard 26 Alphabet (ABCDEFGHIJKLMNOPQRSTUVWYZ) ? \n[1] Yes\n[2] No\nor press Enter for standard\n")
    if alphabet_option == "1":
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWYZ"
    else:
        alphabet = raw_input("Please type your Alphabet: \n")
    text_to_decrypt = raw_input("Type the text to be decrypted: ").upper()
    shift_decrypt = int(raw_input("Type the shift value: "))

    text_length = len(text_to_decrypt)
    text_decrypted = ""

    for i in range(text_length):
        location_char = alphabet.find(text_to_decrypt[i])
        new_location_char = (location_char - shift_decrypt) %len(alphabet) #option 2
        text_decrypted += alphabet[new_location_char]
    return text_decrypted  

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





