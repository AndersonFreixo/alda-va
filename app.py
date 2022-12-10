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
    self.you_string = 'YOU'
    #if sleeping feature is enabled
    self.sleeps = False
    #if is sleeping right now
    self.is_sleeping = False
    self.sleep_after = 0
    self.wake_up_key = ''
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

  #called by RawStreamInput
  def input_callback(self, indata, frames, time, status):
    self.queue.put(bytes(indata))

  def config_sleep(self, sleep_after, wake_up_key):
    self.sleeps = True
    self.sleep_after = sleep_after
    self.wake_up_key = wake_up_key

  def run(self):
    self.print_title()
    with sd.RawInputStream(dtype='int16', channels=1, callback=self.input_callback) as stream:
      try:
        last_word = time.time()
        while True:
          data = self.queue.get()
          self.rec.feed(data)
          text = self.rec.get_text()
          if text:
            if self.sleeps and self.is_sleeping:
              if self.wake_up_key in text:
                self.is_sleeping = False
                last_word = time.time()
                answer = self.reasoner.wake_up()
              else:
                answer = ""
            else:
              answer = self.reasoner.reason(text)

            print(Style.BRIGHT+Fore.BLUE+self.you_string+": "+Style.RESET_ALL+Fore.BLUE+text.capitalize()+Style.RESET_ALL)
                        #print(Fore.GREEN+answer.capitalize()+Style.RESET_ALL)
            if answer:
                print(Style.BRIGHT+Fore.GREEN+self.name.upper()+": "+ Style.RESET_ALL+Fore.GREEN+answer+Style.RESET_ALL)
                stream.stop()
                synthesis.say(answer)
                time.sleep(0.5)
                stream.start()
                last_word = time.time()
          elif self.sleeps and not self.is_sleeping:
            now = time.time()
            if now - last_word >= self.sleep_after:
              self.is_sleeping = True
              print(Style.BRIGHT+Fore.GREEN+self.name.upper()+": "+ Style.RESET_ALL+Fore.GREEN+"Zzzzz...."+Style.RESET_ALL)


      except KeyboardInterrupt:
        print("Encerrando a captura de áudio...")

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--script", "-s", help = "path to script file")
  parser.add_argument("--model", "-m", help = "path to model file")
  parser.add_argument("--name", "-n", help = "change name of the assistant")
  parser.add_argument("--reasoner", "-r", help = "reasoning engine for the chatbot")
  parser.add_argument("--you", "-y", help = "the string printed by the prompt before user messages")
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

  if not args.you:
    app.you_string = config["ARGUMENTS"]["you_string"]
  else:
    app.you_string = args.you

  try:
    sleep = int(config['SLEEP']['wait'])
    wakeup = config['SLEEP']['wakeup_key']
    app.config_sleep(sleep, wakeup)
  except:
    pass

  app.run()
