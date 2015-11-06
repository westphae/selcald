from math import sin, cos, pi


def goertzel(sampling_rate, target_frequency, n, optimized=True):
    k = round(n*target_frequency/sampling_rate)
    omega = (2*pi/n)*k
    sine = sin(omega)
    cosine = cos(omega)
    coeff = 2*cosine
    q2, q1 = 0, 0
    for i in range(n):
        sample = yield
        q2, q1 = q1, (coeff*q1 - q2 + sample)
    return (q1**2 + q2**2 - q1*q2*coeff).real if optimized else \
        complex(q1 - q2*cosine, q2*sine)


def scanner(result, target_frequencies, sampling_rate, n, optimized=True):
    for freq in target_frequencies:
        result[freq] = []
    while True:
        for freq in target_frequencies:
            res = yield from goertzel(sampling_rate, freq, n, optimized)
            result[freq].append(res)
