from math import ceil

int_to_word = {0: "zero",
            1:"um", 
            2: "dois", 
            3: "três", 
            4: "quatro",
            5: "cinco",
            6: "seis",
            7: "sete",
            8: "oito",
            9: "nove",
            10: "dez",
            11: "onze",
            12: "doze",
            13: "treze",
            14: "catorze",
            15: "quinze",
            16: "dezesseis",
            17: "dezessete",
            18: "dezoito",
            19: "dezenove",
            20: "vinte",
            30: "trinta",
            40: "quarenta",
            50: "cinquenta",
            60: "sessenta",
            70: "setenta",
            80: "oitenta",
            90: "noventa",
            100: "cento",
            200: "duzentos",
            300: "trezentos",
            400: "quatrocentos",
            500: "quinhentos",
            600: "seiscentos",
            700: "setecentos",
            800: "oitocentos",
            900: "novecentos"}

#Create word_to_int as the inverse of the int_to_word dict
word_to_int  = dict()
for key, value in int_to_word.items():
    word_to_int[value] = key

word_to_int["cem"] =        100

thousands = dict()

thousands["mil"] =        1000
thousands["milhão"] =     1000000
thousands["milhões"] =    1000000
thousands["bilhão"] =     1000000000
thousands["bilhões"] =    1000000000
thousands["trilhão"] =    1000000000000
thousands["trilhões"] =   1000000000000
thousands["quadrilhão"] = 1000000000000000
thousands["quadrihões"] = 1000000000000000

def int_to_verbal_hundred(num):
    """Gets an integer from 0 to 999 and converts it into its
    verbal representation in Portuguese."""
    word_seq = []
    num = int(num) 
    if num == 100:
        return 'cem'
     
    elif num % 100 == 0 or num < 20:    
        return int_to_word[num]
    else:
        hundred_digit = (num // 100) 
        tens = num  % 100
        units = tens % 10
        if hundred_digit > 0:
            word_seq.append(int_to_word[hundred_digit * 100])
        if tens < 20 or tens % 10 == 0:
            word_seq.append(int_to_word[tens])
        else:
            word_seq.append(int_to_word[(tens//10) * 10])
            word_seq.append(int_to_word[units])
    return " e ".join(word_seq)

def integer_to_words(num):
    """Converts an integer to a well formed phrase in 
    Portuguese representing that number"""
    snum = str(num)
    slen = len(snum)
    #Divides the string into 3 digit blocks 
    blocks_num = ceil(slen/3)
    blocks = []
    blocks.append(int(snum[-3:]))
    for i in range(1, blocks_num):
            blocks.append(int(snum[-(3 + (i*3)):-(3*i)]))
    sentence = []
    millions = [("milhão", "milhões"), ("bilhão", "bilhões"), ("trilhão", "trilhões"), ("quadrilhão", "quadrilhões")]
    
    decs = len(blocks)
    counter = 0
    
    #Hundreds part
    hundreds = blocks.pop(0)
    if hundreds > 0:
        sentence.append(int_to_verbal_hundred(hundreds))
    
    #Thousands part
    if blocks:
        thousands = blocks.pop(0)
        if (hundreds % 100 == 0 or hundreds < 100) and hundreds != 0:
            #For values which are not multiple of 100, we have to add an 'e'
            #as in "mil e um". Other values do not use the 'e'
            #such as as "mil cento e oitenta" or "mil duzentos e noventa".
            sentence.insert(0, "e")
        if thousands > 0: 
            #In case we have millions but the thousands part is empty
            #the script would write something as "one million zero thousands"
            #so we must check if thousands is 0. 
            sentence.insert(0, "mil")
            if int(thousands) != 1:
                #We usually ommit the number one when talking about
                #thousands.
                sentence.insert(0, int_to_verbal_hundred(thousands))
    
    #Millions, billions, etc.
    #We must use the singular form if we are talking about
    #one million or 1 billion and use the plural form 
    #to talk about more than 1 million, billion, and so on.
    for b in blocks:
        if b != 0:
            if b > 1:
                sentence.insert(0, millions[counter][1])
            else:
                sentence.insert(0, millions[counter][0])
            sentence.insert(0, int_to_verbal_hundred(b))
        counter += 1
    return " ".join(sentence)
        
def words_to_integer(sentence):
    """Receives a well formed phrase in Portuguese containing the verbal
    representation of a number and converts it to integer"""
    tokens = sentence.split()
    total = 0
    current = 0
    while tokens:
        t = tokens.pop(0)
        if t in word_to_int.keys():
            current = word_to_int[t]
        elif t == 'e':
            t = tokens.pop(0)
            current += word_to_int[t]
        elif t in thousands.keys():
            if t == "mil" and current == 0: 
                current = 1
            current *= thousands[t]
            total += current
            current = 0
    if current != 0:
        total += current
    return total      
    
def func(op1, op2, opt):
    operations = {"mais" : lambda x, y: x+y,
                "menos": lambda x, y: x-y,
                "vezes": lambda x, y: x * y,
                "dividido por": lambda x, y: (x//y, x % y)}

    op1 = words_to_integer(op1)
    op2 = words_to_integer(op2) 
    result = operations[opt](op1, op2)
    query = "{} {} {}".format(integer_to_words(op1), opt, integer_to_words(op2))
    if opt == "dividido por":
        result_str = query + " é igual a " + integer_to_words(result[0])
        if result[1]:
            result_str += " e sobra "+ integer_to_words(result[1])
        return result_str
    else: 
        return query + " é igual a " + integer_to_words(result)


if __name__ == "__main__":
    while True:
        op1 = input("operand 1>").lower()
        operator = input("operator>").lower()
        op2 = input("operand 2>").lower()
        print(func(op1, op2, operator))

    
