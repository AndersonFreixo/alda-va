import random

def func(var_dict):
    answers = ["Eu me chamo Alda.", 
        "Meu nome é Alda.", 
        "Ué, eu sou a Alda.", 
        "Tinha a impressão de que já nos conhecíamos. Eu me chamo Alda."]
    
    questions = ["E você, quem é?", "E qual é o seu nome?", "E como você se chama?"]
    answer = random.choice(answers)
    if "NAME" not in var_dict.keys():
        answer = answer + " " + random.choice(questions)
    return answer