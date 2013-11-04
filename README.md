selcald
=======

Selcal decoder daemon

A Linux/BSD daemon that monitors an audio stream and looks for selcal 
(Selective Calling; see https://en.wikipedia.org/wiki/SELCAL) calls and 
emits a timestamp, followed by the selcal code. The daemon is intended 
to be as simple and lightweight as possible, and should rely on existing 
frameworks such as fftw where possible.

Selcal specification

The official specification for the selcal system is found in 
"ARINC Characteristic 714-6-1990", published on August 15, 1990. The key 
attributes of selcal codes are as follows:

General

Selective calling is accomplished by the coder of the ground transmitter 
sending coded tone pulses to the aircraft receiver and decoder. Each 
transmitted code is made up of two consecutive tone pulses, with each pulse 
containing two simultaneously-transmitted tones.

Transmitted Code

When the ground operator desires to call a particular aircraft, he depresses 
the buttons corresponding to the code assigned to that aircraft. The coder 
then keys the transmitter on the air causing to be transmitted two 
consecutive tone pulses of 1.0 +/- 0.25 sec. duration, separated by an 
interval of 0.2 +/- 0.1 sec. which makes up the code. Each tone pulse 
consists of two simultaneously-transmitted tones. The call should consist 
of one transmitted code without repetition.

Stability

The frequency of transmitted codes should be held to +/- 0.15% tolerance to 
insure proper operation of the airborne decoder.

Distortion

Overall audio distortion present on the transmitted RF signal should not 
exceed 15%.

Percent Modulation

The RF signals transmitted by the ground radio station should contain within 
3 dB of equal amounts of the two modulating tones. The combination of tones 
should result in a modulation envelope having a nominal modulation percentage 
of 90% and in no case less than 60%.

Transmitted Tones

Tone codes are made up of various combinations of the following tones and 
are designated by letter as indicated:

Note: The tones are spaced by log-1 0.045 (approximately 10.9%)

Designation  Frequency (Hz)
A 312.6
B 346.7
C 384.6
D 426.6
E 473.2
F 524.8
G 582.1
H 645.7
J 716.1
K 794.3
L 881.0
M 977.2
P 1083.9
Q 1202.3
R 1333.5
S 1479.1

Table of Tone Frequencies and Derivation of the Frequencies

fN = log-1 / 0.045 (N-1) + 2.00/. For the first tone, N=12, second N=13, etc.

Designation Log Frequency (Hz)
A 2.495 312.6
B 2.540 346.7
C 2.585 384.6
D 2.630 426.6
E 2.675 473.2
F 2.720 524.8
G 2.765 582.1
H 2.810 645.7
J 2.855 716.1
K 2.900 794.3
L 2.945 881.0
M 2.990 977.2
P 3.035 1083.9
Q 3.080 1202.3
R 3.125 1333.5
S 3.170 1479.1

Detection of the selcal tones is quite similar to DTMF tone detection, and 
this has been well documented. There are several approaches available:

1. Bandpass filter bank and energy detectors (i.e. analog implementation approach)
2. Discrete FFT and energy detection in bins containing selcal tones
3. Goertzl algorithm for fast DFT (see https://en.wikipedia.org/wiki/Goertzel_algorithm)
4. Chirp-Z transform for DFT (see https://en.wikipedia.org/wiki/Bluestein%27s_FFT_algorithm)
5. Wavelet transform and convolution (seems highly advanced)

The implementation should take into account characteristics of the HF radio medium:

- Often poor signal/noise ratio
- Frequent ionospheric and auroral fading and flutter
- Slight doppler due to relative ionospheric motion

These imply that unlike a DTMF decoder implementation, a series of measurements should 
be made and a final decision determined from statistical analysis of the raw measurements.
