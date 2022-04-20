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




def int_str_to_hundred(num):
    num_seq = []
    if num[0] != '0':
        if int(num[1:]) == 0:
            if num[0] == '1':
                #100 is represented by 'cem', other numbers from 101 to 199
                #are represented as 'cento e...' + the rest of the number. 
                return 'cem'
            else:
                return int_to_word[int(num[0])*100]
        else:
            num_seq.append(int_to_word[int(num[0])*100])
            num_seq.append("e")
    if int(num[1:]) < 20:
    #Each number from 0 to 19 have an individual name
        num_seq.append(int_to_word[int(num[1:])])
        return " ".join(num_seq)
    else:
        num_seq.append(int_to_word[int(num[1])*10])

    if num[2] != '0':
        num_seq.append("e")
        num_seq.append(int_to_word[int(num[2])])
        
    return " ".join(num_seq)

def integer_to_words(num):
    #This function should be refactored!!!!

    #Assures it is a string and remove eventual extra spaces. 
    num = str(int(num))
    slen = len(num)
    #Divides the string into 3 digit blocks 
    blocks_num = ceil(slen/3)
    blocks = [] 
    for i in range(0, blocks_num):
        if i == 0:
            b = num[-(3 + (i*3)):]
    
        else:
            b = num[-(3 + (i*3)):-(3*i)]
        while len(b) < 3:
            b = "0"+b
        blocks.insert(0, b)


    sentence = []
    millions = [("milhão", "milhões"), ("bilhão", "bilhões"), ("trilhão", "trilhões")]
    
    decs = len(blocks)
    counter = 0
    
    #Hundreds part
    hundreds = blocks.pop(-1)
    if int(hundreds) > 0:
        sentence.append(int_str_to_hundred(hundreds))
    
    #Thousands part
    if blocks:
        thousands = blocks.pop(-1)
        if 0 < int(hundreds) < 100:
            #For values lesser than 100, we have to add an 'e'
            #as in "mil e um". 
            #For values greater than 100, we do not use the 'e'
            #as in "mil cento e oitenta".
            sentence.insert(0, "e")
        if int(thousands) > 0: 
            #In case we have millions but the thousands part is empty
            #the script would write something as "one million zero thousands"
            #so we must check if thousands is 0. 
            sentence.insert(0, "mil")
        
            if int(thousands) != 1:
                #We usually ommit the number one when talking about
                #thousands.
                sentence.insert(0, int_str_to_hundred(thousands))
    
    #Millions, billions, etc.
    #We must use the singular form if we are talking about
    #one million or 1 billion and use the plural form 
    #to talk about more than 1 million, billion, and so on.
    blocks.reverse()
    for b in blocks:
        if int(b) > 1:
            sentence.insert(0, millions[counter][1])
        else:
            sentence.insert(0, millions[counter][0])
        sentence.insert(0, int_str_to_hundred(b))
        counter += 1
    return " ".join(sentence)
        
def words_to_integer(sentence):
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
        return query + " é igual a " + integer_to_words(result[0]) +" e sobra "+ integer_to_words(result[1])
    else: 
        return query + " é igual a " + integer_to_words(result)


if __name__ == "__main__":
    while True:
        ipt = input(">>").lower()
        print(verbal_arithmetics(ipt))
    
