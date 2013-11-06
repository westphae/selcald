selcald
=======

Selcal decoder daemon
---------------------

A Linux/BSD daemon that monitors an audio stream and looks for selcal 
(Selective Calling; see <https://en.wikipedia.org/wiki/SELCAL>) calls and 
emits a timestamp, followed by the selcal code received. The daemon is 
intended to be as simple and lightweight as possible, and should rely 
on existing frameworks such as fftw where possible.

Selective Calling (SELCAL)[1]
--------------------------

SELCAL is a technique that allows a ground radio operator to alert an 
aircrew that the operator wishes to communicate with that aircraft.

Because of the background noise level experienced on HF radio frequencies, 
aircrews usually prefer to turn down the audio level of their HF receiver 
until alerted via SELCAL of a message specifically intended for their 
aircraft. When the ground station operator wishes to communicate with an 
aircraft, he enters into the SELCAL encoder the 4-letter code of that aircraft, 
which is usually included in its flight plan, and transmits that code over the 
assigned radio channel. All aircraft monitoring that channel receive the 
SELCAL broadcast, but only those (preferably only one) that have been 
programmed with that 4-letter code will respond by sounding a chime or 
otherwise alerting the crew. The crew will then set their volume control 
higher to listen to the voice traffic and, using ICAO recommended radio 
procedures, assure that the message is intended for them.

Selcal Specification[2]
--------------------
The official specification for the selcal system is found in 
"ARINC Characteristic 714-6-1990", published on August 15, 1990. The key 
attributes of selcal codes are as follows:

### General

Selective calling is accomplished by the coder of the ground transmitter 
sending coded tone pulses to the aircraft receiver and decoder. Each 
transmitted code is made up of two consecutive tone pulses, with each pulse 
containing two simultaneously-transmitted tones.

### Transmitted Code

When the ground operator desires to call a particular aircraft, he depresses 
the buttons corresponding to the code assigned to that aircraft. The coder 
then keys the transmitter on the air causing to be transmitted two 
consecutive tone pulses of 1.0 +/- 0.25 sec. duration, separated by an 
interval of 0.2 +/- 0.1 sec. which makes up the code. Each tone pulse 
consists of two simultaneously-transmitted tones. The call should consist 
of one transmitted code without repetition.

### Stability

The frequency of transmitted codes should be held to +/- 0.15% tolerance to 
insure proper operation of the airborne decoder.

### Distortion

Overall audio distortion present on the transmitted RF signal should not 
exceed 15%.

### Percent Modulation

The RF signals transmitted by the ground radio station should contain within 
3 dB of equal amounts of the two modulating tones. The combination of tones 
should result in a modulation envelope having a nominal modulation percentage 
of 90% and in no case less than 60%.

### Transmitted Tones

Tone codes are made up of various combinations of the following tones and 
are designated by letter as indicated:

Note: The tones are spaced by log-1 0.045 (approximately 10.9%)

<table>
<th>Designation</th><th>Frequency (Hz)</th>
</tr>
<tr>
<td>A</td><td>312.6</td>
</tr>
<tr>
<td>B</td><td>346.7</td>
</tr>
<tr>
<td>C</td><td>384.6</td>
</tr>
<tr>
<td>D</td><td>426.6</td>
</tr>
<tr>
<td>E</td><td>473.2</td>
</tr>
<tr>
<td>F</td><td>524.8</td>
</tr>
<tr>
<td>G</td><td>582.1</td>
</tr>
<tr>
<td>H</td><td>645.7</td>
</tr>
<tr>
<td>J</td><td>716.1</td>
</tr>
<tr>
<td>K</td><td>794.3</td>
</tr>
<tr>
<td>L</td><td>881.0</td>
</tr>
<tr>
<td>M</td><td>977.2</td>
</tr>
<tr>
<td>P</td><td>1083.9</td>
</tr>
<tr>
<td>Q</td><td>1202.3</td>
</tr>
<tr>
<td>R</td><td>1333.5</td>
</tr>
<tr>
<td>S</td><td>1479.1</td>
</tr>
</table>

### Table of Tone Frequencies and Derivation of the Frequencies

fN = log-1 / 0.045 (N-1) + 2.00/. For the first tone, N=12, second N=13, etc.

<table>
<tr>
<th>Designation</th><th>Log</th><th>Frequency (Hz)</th>
</tr>
<tr>
<td>A</td><td>2.495</td><td>312.6</td>
<tr>
<td>B</td><td>2.540</td><td>346.7</td>
</tr>
<tr>
<td>C</td><td>2.585</td><td>384.6</td>
</tr>
<tr>
<td>D</td><td>2.630</td><td>426.6</td>
</tr>
<tr>
<td>E</td><td>2.675</td><td>473.2</td>
</tr>
<tr>
<td>F</td><td>2.720</td><td>524.8</td>
</tr>
<tr>
<td>G</td><td>2.765</td><td>582.1</td>
</tr>
<tr>
<td>H</td><td>2.810</td><td>645.7</td>
</tr>
<tr>
<td>J</td><td>2.855</td><td>716.1</td>
</tr>
<tr>
<td>K</td><td>2.900</td><td>794.3</td>
</tr>
<tr>
<td>L</td><td>2.945</td><td>881.0</td>
</tr>
<tr>
<td>M</td><td>2.990</td><td>977.2</td>
</tr>
<tr>
<td>P</td><td>3.035</td><td>1083.9</td>
</tr>
<tr>
<td>Q</td><td>3.080</td><td>1202.3</td>
</tr>
<tr>
<td>R</td><td>3.125</td><td>1333.5</td>
</tr>
<tr>
<td>S</td><td>3.170</td><td>1479.1</td>
</tr>
</table>

Signal Processing
-----------------

Detection of the selcal tones is quite similar to DTMF tone detection, and 
this has been well documented. There are several approaches available:

1. Bandpass filter bank and energy detectors (i.e. analog implementation approach)
2. Discrete FFT and energy detection in bins containing selcal tones
3. Goertzl algorithm for fast DFT (see <https://en.wikipedia.org/wiki/Goertzel_algorithm>)
4. Chirp-Z transform for DFT (see <https://en.wikipedia.org/wiki/Bluestein%27s_FFT_algorithm>)
5. MUSIC algorithm (see <https://en.wikipedia.org/wiki/Multiple_signal_classification>)
6. ESPRIT algorithm (see <https://en.wikipedia.org/wiki/Estimation_of_signal_parameters_via_rotational_invariance_techniques>)
7. Wavelet transform and convolution (seems highly advanced)

The implementation should take into account characteristics of the HF radio medium:

* Often poor signal/noise ratio
* Frequent ionospheric and auroral fading and flutter
* Slight doppler due to relative ionospheric motion

These imply that unlike DTMF decoder implementations, a series of measurements should 
be made during the signal and a final decision determined from statistical analysis 
of the raw measurements.

The normal source of sampled audio is the soundcard interface. Standard sampling rates
of 44100, 22050, 10025, and 8000 samples/second are supported. Lower sampling rates are
preferred due to the lover processing load, as are fixed point DSP implementations
versus floating point implementations.

### Pseudocode

    Calculate numnber of samples per interval
    While true
      Clear signal table
      set signal table row to 0
      read audio samples for one interval
      perform time to frequency conversion of samples
      add tones detected to signal table
      if two tones detected
        For remaining number of intervals
          increment signal table row
          read audio samples for one interval
          perform time to frequency conversion of samples
          add tones detected to signal table
        Read signal table and determine selcal code

References
----------
[1]: http://www.asri.aero/our-services/selcal/ "Aviation Spectrum Resources Inc. website, retrieved 3, Nov 2013"
[2]: "ARINC Characteristic 714-6-1990, chapter 2; August 15, 1990"

