def func(var_dict, name):
    #Essa função é chamada para o padrão "meu nome é",
    #então é bom checar se a pessoa não está falando algo sobre o próprio nome
    #Num mundo ideal, o Reasoner teria um banco de dados de adjetivos.
    #Enquanto isso não acontece...
    qualities = ["bonito", "feio", "complicado", "legal", "estranho", "exótico", "difícil"]
    if name in qualities:
        return "Realmente, ele é um pouco " + name +"."
    else:
        name = name.capitalize()
        if "NAME" in var_dict.keys():
            #Usuário já informou o nome
            if name== var_dict["NAME"]:
                return "Acho que você já me disse isso."
            #Usuário informou um nome diferente de um informado anteriormente
            if name != var_dict["NAME"]:
                return name + "? Mas você disse que seu nome era " + var_dict["NAME"] + "!"
        else:
            var_dict["NAME"] = name
            return name + "? É um nome bonito."
