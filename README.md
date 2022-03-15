# alda-va
Alda VA is a virtual assistant with speech recognition and synthesis written in Python.

*Instalation instructions*

You should have portaudio, espeak and mbrola installed on your system. In a Debian/Ubuntu system, you may install it with the apt-get command:

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
-scipy (just for a trick to play the synthesized sounds) 

Finally, you should create a directory called "models" to put the language models used by vosk. For the default configuration, you should download the model for portuguese in  https://alphacephei.com/vosk/models/vosk-model-small-pt-0.3.zip, unzip it in alda-va/models/pt-br.


