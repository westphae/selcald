"""
Calculate the optimum bin sizes to fit the selcal tone assignments
"""

import math
from string import ascii_uppercase


class SelcalParams:
    """
    Contains the specifications and parameters for the
    set of 16 selcal tones. The specified frequencies,
    tolerances, and associated DFT bins are attributes.
    """

    def __init__(self):
        self.log_tone_step = 0.045
        self.log_tone_tolerance = 0.0015
        self.letters = [i for i in ascii_uppercase if i not in 'INO' and i<'T']
        self.selcal_tones = {l: 10**(2+(11+self.letters.index(l))*self.log_tone_step)
                             for l in self.letters}
        self.tone_lower = {l: self.selcal_tones[l]*(1-self.log_tone_tolerance)
                           for l in self.selcal_tones}
        self.tone_upper = {l: self.selcal_tones[l]*(1+self.log_tone_tolerance)
                           for l in self.selcal_tones}
        self.tone_window = {l: self.tone_upper[l]-self.tone_lower[l]
                            for l in self.letters}
        self.bin_center = {}
        self.bin_error = {}
        self.samplerate = None
        self.samplesize = None
        self.binsize = None
        self.bintime = None

    def calc_bin_error(self, samplerate, samplesize):
        """
        For a given sampling rate and block size, calculate the freqency error
        between the derived DFT frequency bins and the selcal tones. Return an
        arbitrary score for the net frequency error across all of the selcal
        tones. Currently, this is set to a log10 value, so more negative scores
        are better.
        """

        self.samplerate = samplerate
        self.samplesize = samplesize
        self.binsize = (self.samplerate / self.samplesize)
        self.bintime = 1/self.binsize
        self.bin_center = {l: (math.floor(self.selcal_tones[l]/self.binsize)+0.5)*
                              self.binsize for l in self.letters}
        self.bin_error = {l: abs(self.selcal_tones[l]-self.bin_center[l])
                          for l in self.letters}
        return sum([math.log10(v) for v in self.bin_error.values()])/len(self.bin_error)

    def print_bin_error(self, samplerate, samplesize):
        """
        Given a sample rate and size, print out the frequency error for
        each DFT bin versus the selcal tone frequency.

        """
        self.calc_bin_error(samplerate, samplesize)
        binsize = (samplerate / samplesize)
        print("=== Rate: ", samplerate, " size : ", samplesize,
              " time: ", 1/binsize, " ===")
        for l in self.letters:
            print("Tone: ", self.letters.index(l),
                  " freq: ", self.selcal_tones[l],
                  " bin: ", self.bin_center[l],
                  " err: ", self.bin_error[l])
        print()
 
    def search_err(self, samplerate, upper_bound):
        """
        Search sample sizes starting from a given upper bound to a 
        set lower bound, recursively. Return when the upper bound
        equals the lower bound.

        """
        self.samplerate = samplerate
        lower_bound = int(self.samplerate / 40)
        if upper_bound > lower_bound:
            min_err = 10000.0
            min_size = upper_bound
            for size in range(lower_bound, upper_bound):
                err = params.calc_bin_error(samplerate, size)
                if err < min_err:
                    min_err = err
                    min_size = size
            print("rate: ", rate, " size ", min_size, " time ",
                  (min_size/rate), " error ", min_err)
            self.search_err(samplerate, min_size)
            
if __name__ == '__main__':
    _samplerates = [44100, 32000, 22050, 16000, 11025, 8000, 4000]
    params = SelcalParams()
    for rate in _samplerates:
        upper_bound = int(rate / 9)
        params.search_err(rate, upper_bound)
        print()
        
    # rate:  44100  size  4580  time  0.103854875283  error  -3.60366543025
    params.print_bin_error(44100, 4580)
    # rate:  32000  size  3553  time  0.11103125  error  -3.36174781256
    params.print_bin_error(32000, 3553)
    # rate:  22050  size  2290  time  0.103854875283  error  -3.60366543025
    params.print_bin_error(22050, 2290)
    # rate:  16000  size  1662  time  0.103875  error  -2.49558719312
    params.print_bin_error(16000, 1662)
    # rate:  11025  size  1145  time  0.103854875283  error  -3.60366543025
    params.print_bin_error(11025, 1145)
    # rate:  8000  size  831  time  0.103875  error  -2.49558719312
    params.print_bin_error(8000, 831)
    # rate:  4000  size  361  time  0.09025  error  -1.53481794027
    params.print_bin_error(4000, 361)
