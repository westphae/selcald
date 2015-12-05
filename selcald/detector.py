from filter.goertzel import goertzel
from selcald.binsize import SelcalParams

sp = SelcalParams()


def channel_monitor(target_frequency, sampling_rate, n, noise_duration=10,
                    sensitivity=4):
    """
    Track rolling background noise statistics in target_frequency channel
    using an exponential decay of noise_duration seconds.
    Channel is noise if power p^2 < sensitivity*q,
        where q is the ewms noise power.
    Noise stats aren't updated if sample is an outlier.
    :param target_frequency: float frequency of channel to be detected, in Hz
    :param sampling_rate: float frequency at which samples are taken, in Hz
    :param n: int number of samples per chunk
    :param noise_duration: float number of seconds decay for noise power^2 ewma;
    should be much shorter than n/sampling_frequency
    :param sensitivity: float threshold ratio of (signal power^2/(noise power^2)
    :return: yields boolean whether sample is a signal relative to noise level
    """
    a = (n/sampling_rate)/noise_duration # ewma multiplier

    # # Use first sample to prime the noise power ewma
    # noise_power2 = (yield from goertzel(sampling_rate, [target_frequency], n))[0]
    # yield False
    noise_power2 = 100

    # Main generator loop, never ends
    while True:
        sample_power2 =\
            (yield from goertzel(sampling_rate, [target_frequency], n))[0]
        # print("noise_power2: %0.1f, sample_power2: %0.1f"%
        #       (noise_power2, sample_power2))
        noise = (sample_power2 < sensitivity*noise_power2)
        noise_power2 = a*sample_power2 + (1-a)*noise_power2
        yield not noise


def selcal_monitor(code, sampling_rate, n, noise_duration, sensitivity):
    """
    Monitor for specified SELCAL code. Here is the algorithm:
    1.  Pass n-sample to channel_monitor and get back any outlier channel
        numbers.
    2.  If timer isn't running:
        a. If < 2 outlier channels then continue.
        b. Else first sample, so start timer and initialize count and power
            dicts.
    3.  If timer > 1.25 seconds then stop the timer and reprocess with higher
        threshold.
    4.  If timer < 0.75 seconds or > 0 outlier channels: Update dict of outlier
        count per tone, then continue at step 1.
    5.  Candidate channels are those with count >= g=70%.  If < 2 candidate
        channels then continue.
    6.  Tone is two channels with highest count or highest power (if count is
        tied).
    (same process to look for 0.2 second pause, then to look for second pair of
        tones.)
    :param code: SELCAL code to be listened for
    :param sampling_rate: float frequency at which samples are taken, in Hz
    :param n: int number of samples per chunk
    :param noise_duration: float number of seconds decay for noise power^2 ewma;
    should be much shorter than n/sampling_frequency
    :param sensitivity: float threshold ratio of (signal power^2/(noise power^2)
    :return: yields boolean if code has been detected
    """
    code = list(code.upper())
    freqs = [sp.selcal_tones[l] for l in code]
    mons = [channel_monitor(f, sampling_rate, n, noise_duration, sensitivity)
            for f in freqs]

