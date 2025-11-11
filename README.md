# alda-va

## About the project

Alda VA is intended to be a virtual assistant/chatbot with speech recognition and synthesis. 

The goal of the project is to provide a simple and fun chatbot that doesn't rely on huge language models nor requests to AI APIs, so it can be executed locally on PCs with modest hardware. 

At the moment,there are two "reasoning" modules. One of them is a simplified version of Weizenbaum's ELIZA, and the other one is an extended version of the later which allows templates to call functions using parts of the utterance as arguments. The "smarter_alda" script uses this feature to do basic arithmetic operations. 

Although brazilian portuguese is the only language supported up to now, the project may be easely extended to other languages by 

1. Writting a script for the target language following the structure of Alda's default script
2. Downloading the propper vosk model for the language 
3. Download a mbrola voice for the language and 
4. Writing an appropriate config file for the new chatbot.     

## Installation instructions

You should have portaudio, espeak and mbrola installed on your system. In a Debian/Ubuntu system, you may install them with the apt-get command:

<pre>sudo apt-get install portaudio19-dev espeak mbrola</pre> 

Also, you should install the mbrola voices you'd like to use. The voice used in the standard configuration is br-4:

<pre> sudo apt-get install mbrola-br4</pre>

Note: If your distro doesn't provide packages for mbrola and mbrola voices, you may install them manually. To compile and install mbrola:

<pre>
git clone https://github.com/numediart/MBROLA
cd MBROLA/
make
sudo cp Bin/mbrola /usr/bin/mbrola
</pre>

To install br4 voice:
1. Go to https://github.com/numediart/MBROLA-voices
2. Find br4 voice link and save to computer
3. Move the voice to the proper directory:
<pre>
sudo mkdir -p /usr/share/mbrola
sudo mv br4 /usr/share/mbrola/br4/
</pre>

To install python dependencies, cd to the top level directory of the project and run:

<pre>pip3 install -r requirements.txt</pre>

Currently, the 3rd party libraries used in the project are:

-vosk (speech recognition)

-voxpopuli (speech synthesis)

-colorama (colored terminal)

-sounddevice (voice recording and playing)

-scipy (just for a workaround to play the synthesized sounds without voxpopuli interfering with sounddevice) 

Note: You'll probably want/need to create a virtual environment for the project. IMO the simplest option would be to use venv. 

Finally, you should create a directory called "models" to put the language models used by vosk. For the default configuration, you should download the model for portuguese in  https://alphacephei.com/vosk/models/vosk-model-small-pt-0.3.zip, unzip it in alda-va/models/pt-br.

On Linux, you may do this in the terminal with the commands:
<pre>
cd to top level directory of the project
wget https://alphacephei.com/vosk/models/vosk-model-small-pt-0.3.zip
unzip vosk-model-small-pt-0.3.zip
mv vosk-model-small-pt-0.3 models/pt-br
</pre>


