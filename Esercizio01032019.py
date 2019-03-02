# coding=utf-8
def vocale(c):
    vocali = 'AEIOU'
    if c in vocali:
        return True
    else:
        return False


input_vocale = raw_input('Inserisci la lettera:\n')
if input_vocale.isalpha():
    if vocale(input_vocale.upper()):
        print "Vocale"
    else:
        print "Consonante"
else:
    print "Non è una lettera!"
