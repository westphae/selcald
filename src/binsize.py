'''
Calculate the optimum bin sizes to fit the selcal tone assignments
  
'''
import math

class SelcalParams:
    """
    Contains the specifications and parameters for the
    set of 16 selcal tones. The specified frequencies,
    tolerances, and associated DFT bins are attributes.

    """
    def __init__(self, samplerate):
        self.samplerate = samplerate * 1.0
        self.selcal_tones = [312.6, 346.7, 384.6, 426.6,
                             473.2, 524.8, 582.1, 645.7,
                             716.1, 794.3, 881.0, 977.2,
                             1083.9, 1202.3, 1333.5, 1479.1,]
        self.log_tone_step = 0.045
        self.log_tone_tolerance = 0.0015
        self.tone_lower = {}
        self.tone_upper = {}
        self.tone_step = {}
        self.tone_window = {}
        self.bin_center = {}
        self.bin_error = {}

        for tone in range(len(self.selcal_tones)):
            self.tone_lower[tone] = self.selcal_tones[tone] * (1 - self.log_tone_tolerance)
            self.tone_upper[tone] = self.selcal_tones[tone] * (1 + self.log_tone_tolerance)
            self.tone_window[tone] = self.tone_upper[tone] - self.tone_lower[tone]
            
        for tone in range(12, 28):
            index = tone - 12
            lower = math.pow(10, (2.0 + ((tone - 1) * self.log_tone_step)))
            upper = math.pow(10, (2.0 + (tone * self.log_tone_step)))
            self.tone_step[index] = (upper - lower)
            
    def calc_bin_error(self, binsize):
        """
        For a given sample block size, calculate the freqency error between the
        derived DFT frequency bins and the selcal tones. Return an arbitrary
        score for the net frequency error across all of the selcal tones.
        Currently, this is set to a log10 value, so more negative scores are
        better.

        """
        self.samplesize = binsize
        self.binsize = (self.samplerate / self.samplesize)
        self.bintime = (self.samplesize / self.samplerate)
        avg_err = 0.0
        for tone in range(len(self.selcal_tones)):
            self.bin_center[tone] = ((1.0 * int(self.selcal_tones[tone] / self.binsize)) + 0.5) * self.binsize
            bin_err = abs(self.selcal_tones[tone] - self.bin_center[tone])
            self.bin_error[tone] = bin_err
            if bin_err > 0:
                avg_err = avg_err + math.log10(bin_err)
        return(avg_err)
    
    def print_bin_error(self, samplerate, samplesize):
        """
        Given a sample rate and size, print out the frequency error for
        each DFT bin versus the selcal tone frequency.

        """
        binsize = (samplerate / samplesize)
        print "=== Rate: ", samplerate, " size : ", samplesize, " time: ", samplesize * 1.0 / samplerate, " ==="
        for tone in range(len(self.selcal_tones)):
            self.bin_center[tone] = ((1.0 * int(self.selcal_tones[tone] / binsize)) + 0.5) * binsize
            bin_err = self.selcal_tones[tone] - self.bin_center[tone]
            print "Tone: ", tone, " freq: ", self.selcal_tones[tone], " bin: ", self.bin_center[tone], " err: ", bin_err
        print
 
    def search_err(self, upper_bound):
        """
        Search sample sizes starting from a given upper bound to a 
        set lower bound, recursively. Return when the upper bound
        equals the lower bound.

        """
        lower_bound = int(self.samplerate / 40)
        if upper_bound > lower_bound:
            min_err = 10000.0
            min_size = upper_bound
            for size in range(lower_bound, upper_bound):
                err = params.calc_bin_error(size)
                if err < min_err:
                    min_err = err;
                    min_size = size
            print "rate: ", rate, " size ", min_size, " time ", (min_size * 1.0 / rate), " error ", min_err
            self.search_err(min_size)
            
if __name__ == '__main__':
    _samplerates = [44100, 32000, 22050, 16000, 11025, 8000, 4000]
    for rate in _samplerates:
        params = SelcalParams(rate)
        upper_bound = int(rate / 9)
        params.search_err(upper_bound)
        print
        
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
