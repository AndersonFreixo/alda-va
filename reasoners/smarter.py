from collections import defaultdict
import re
import random
import json
import importlib

FUNCS_PATH = "reasoners.smarter_funcs."

class Rule:
    def __init__(self, pattern):
        self.pattern = pattern
        self.templates = []

class Reasoner:
    def __init__(self, script_filename):
        self.rules = defaultdict(lambda: list())
        self.miss = None
        self._load_script(script_filename)
        self.functions = dict()

    def _re_replace(self, rule):
        """Replace symbols of script source for regex special characters"""
        r = rule.replace("*", "(.*)")
        r = r.replace("+", "(\\w*)")
        return r

    def _load_script(self, filename):

        with open(filename) as f:
            s = f.read()
            doc = json.loads(s)
        self.miss = doc["miss"]
        
        for key in doc["rules"].keys():
            for rule in doc["rules"][key].keys():
                pattern = self._re_replace(rule)
                rule_obj = Rule(pattern)
                rule_obj.templates = doc["rules"][key][rule]
                self.rules[key].append(rule_obj)
    
    def print_all_rules(self):
        for key in self.rules.keys():
            print(key)
            for rule in self.rules[key]:
                print("\t"+rule.pattern)
                for template in rule.templates:
                    print("\t\t"+ template)

    def get_key(self, sentence):
        for key in self.rules.keys():
            if key in sentence:
                return key
        return None


    def find_rule(self, sentence, key):
        for rule in self.rules[key]:
            match = re.search(rule.pattern, sentence)
            if match:
                return (rule, match.groups())
        return None

    def reason(self, sentence):
        sentence = sentence.lower()

        for key in self.rules.keys():
                if key in sentence:
                    match = self.find_rule(sentence, key)

                    if match:
                        rule, words = match
                        #Provisory (and maybe definitive) solution:
                        #If the first template of a rule is a function, then
                        #it is always fired. All other possibilites are ignored. 
                        if "$func" in rule.templates[0]:
                            #A function template has the form:
                            #$func:func_name:0,1,2 (where 0,1,2 is an example order
                            #of args.
                            _, func_name, args_order = rule.templates[0].split(":")
                            if func_name not in self.functions.keys():
                                self.functions[func_name] = importlib.import_module(FUNCS_PATH+func_name)
                            
                            args_order = [int(x) for x in args_order.split(',')]
                            args = [words[i] for i in args_order]
                            return self.functions[func_name].func(* args)
                        else:

                            return random.choice(rule.templates).format(*words)
                    
        return random.choice(self.miss)

if __name__ == '__main__':
    reasoner = Reasoner("../scripts/smarter_alda.json")
    reasoner.print_all_rules()
    q = input(">>").lower()
    while (q != "sair"):
        a = reasoner.reason(q)
        if a:
            print(">>", a)
        q = input(">>").lower()
