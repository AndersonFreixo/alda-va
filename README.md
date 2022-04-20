# alda-va

*About the project*

Alda VA is intended to be a virtual assistant written in Python, but currently it's just a chatbot with speech recognition and synthesis. 

At the moment,there are two "reasoning" modules. One of them is a simplified version of Weizenbaum's ELIZA, and the other one is an extended version of the later which allows templates to call functions using parts of the utterance as arguments. The "smarter_alda" script uses this feature to do basic arithmetic operations. 

Although brazilian portuguese is the only language supported up to now, the project may be easely extended to other languages by 1)  writting a script for the target language following the structure of Alda's default script, 2) downloading the propper vosk model for the language, 3) download a mbrola voice for the language and 4) writing an appropriate config file for the new chatbot.     

*Installation instructions*

You should have portaudio, espeak and mbrola installed on your system. In a Debian/Ubuntu system, you may install them with the apt-get command:

<pre>sudo apt-get install portaudio19-dev espeak mbrola</pre> 

Also, you should install the mbrola voices you'd like to use. The voice used in the standard configuration is br-4:

<pre> sudo apt-get install mbrola-br4</pre>

To install python dependencies, cd to the top level directory of the project and run:

<pre>pip3 install -r requirements.txt</pre>

Currently, the 3rd party libraries used in the project are:

-vosk (speech recognition)

-voxpopuli (speech synthesis)

-colorama (colored terminal)

-sounddevice (voice recording and playing)

-scipy (just for a workaround to play the synthesized sounds without voxpopuli interfering with sounddevice) 

Finally, you should create a directory called "models" to put the language models used by vosk. For the default configuration, you should download the model for portuguese in  https://alphacephei.com/vosk/models/vosk-model-small-pt-0.3.zip, unzip it in alda-va/models/pt-br.

On Linux, you may do this in the terminal with the commands:
<pre>
cd to top level directory of the project
wget https://alphacephei.com/vosk/models/vosk-model-small-pt-0.3.zip
unzip vosk-model-small-pt-0.3.zip
mv vosk-model-small-pt-0.3 models/pt-br
</pre>


