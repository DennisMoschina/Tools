# Tools
This is a small oscilloscope, biult using an Arduino and a computer with a python script. The base is simply the oscilloscope
in created in <a href="https://maker.pro/arduino/tutorial/how-to-make-a-basic-arduino-pc-oscilloscope">this tutorial</a>.
However, I changed it to fit my purpose and I added some functionality. 


<p>
The A0 port of the arduino is configured as the input of the oscilloscope.
In order to get the voltages right, I recommend attaching the ground pin of the Arduino to ground of the measured voltage.
The range of the oscilloscope is limited between 0V and 5V, due to the hardware limitations of the Arduino.
While the resolution can be changed in the Arduino source code by changing the timeBase, the standard is set to 10000 Hz.
</p>
<p>
Before you start the python script, you have to make sure all needed libraries are installed, which are PyGame,
PySerial and Time (time should be installed by default).
In the python code, the port, the Arduino is connect to, has to be changed to fit your setup. 
</p>
<p>
The oscilloscope is also capable of recording data to examine it afterwards.
To start a recording simply press the R key on your keyboard. To stop the recording press S. To view the recorded data press P
and to quit press Q. When the recorded data is displayed, you can zoom by pressing + and - and you can move through the 
recorded data by pressing the arrow keys.
</p>
