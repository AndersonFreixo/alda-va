from colorama import Fore, Back, Style
import os
import queue
import sounddevice as sd
import time
from vosk import SetLogLevel
SetLogLevel(-1)
import argparse
import configparser
import vosk
import json
import importlib
from speech import recognition, synthesis

DEFAULT_CONFIG = "config/smarter_alda.ini"
REASONERS_PATH = "reasoners."
class App:
    def __init__(self, name, script_path, model_path, reasoner):
        self.name = name
        self.reasoner = importlib.import_module(REASONERS_PATH + reasoner).Reasoner(script_path)
        self.queue = queue.Queue()
        #Find samplerate 
        device_info = sd.query_devices(sd.default.device[0], 'input')
        samplerate = device_info['default_samplerate']
        self.rec = recognition.Recognizer(model_path, samplerate)

    def print_title(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        f = open("title.txt")
        for line in f:
            line = line[:-1]
            print(Fore.GREEN + line + Style.RESET_ALL)

        subtitle = "Uma assistente virtual pythonica"
        #Number of blanks to centralize text in a screen with 80 columns
        space = int((80 - len(subtitle))/2)

        print(Fore.BLACK + Back.GREEN + " " * space + subtitle + " " * space, Style.RESET_ALL)

    #Função chamada pelo RawStreamInput
    def input_callback(self, indata, frames, time, status):
        self.queue.put(bytes(indata))

    def run(self):
        self.print_title()
        with sd.RawInputStream(dtype='int16', channels=1, callback=self.input_callback) as stream:
            try:
                while True:
                    data = self.queue.get()
                    self.rec.feed(data)
                    text = self.rec.get_text()
                    if text:
               	        print(Style.BRIGHT+Fore.BLUE+"VOCÊ: "+Style.RESET_ALL+Fore.BLUE+text.capitalize()+Style.RESET_ALL)
                        answer = self.reasoner.reason(text)
                        print(Style.BRIGHT+Fore.GREEN+self.name.upper()+": "+ Style.RESET_ALL+Fore.GREEN+answer+Style.RESET_ALL)
                        #print(Fore.GREEN+answer.capitalize()+Style.RESET_ALL)
                        stream.stop()
                        synthesis.say(answer)
                        time.sleep(0.5)
                        stream.start()
            except KeyboardInterrupt:
                print("Encerrando a captura de áudio...")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--script", "-s", help = "path to script file")
    parser.add_argument("--model", "-m", help = "path to model file")
    parser.add_argument("--name", "-n", help = "change name of the assistant")
    parser.add_argument("--reasoner", "-r", help = "reasoning engine for the chatbot")
    parser.add_argument("--config", "-c", type = argparse.FileType("r"), help = "config file")
    args = parser.parse_args()
    
    config = configparser.ConfigParser()
    if args.config:
        config.read_file(args.config)
    else:
        config.read(DEFAULT_CONFIG)
    if not args.script:
        args.script = config["ARGUMENTS"]["script"]
    if not args.model:
        args.model = config["ARGUMENTS"]["model"]
    if not args.name:
        args.name = config["ARGUMENTS"]["name"]
    if not args.reasoner:
        args.reasoner = config["ARGUMENTS"]["reasoner"]
    app = App(args.name, args.script, args.model, args.reasoner)
    app.run()
