from math import sin, cos, pi


def goertzel(sampling_rate, target_frequencies, n, optimized=True):
    omega = [2*pi*freq/sampling_rate for freq in target_frequencies]
    sine = [sin(o) for o in omega]
    cosine = [cos(o) for o in omega]
    coeff = [2*c for c in cosine]
    q2, q1 = [0 for freq in target_frequencies],\
             [0 for freq in target_frequencies]
    for i in range(n):
        sample = yield
        q2, q1 = q1, [(c*qq1 - qq2 + sample)
                      for c, qq1, qq2 in zip(coeff, q1, q2)]
    return [qq1**2 + qq2**2 - qq1*qq2*c
            for c, qq1, qq2 in zip(coeff, q1, q2)] if optimized else\
        [complex(qq1 - qq2*c, qq2*s)
         for c, s, qq1, qq2 in zip(cosine, sine, q1, q2)]


def scanner(result, target_frequencies, sampling_rate, n, optimized=True):
    while True:
        res = yield from goertzel(sampling_rate, target_frequencies, n,
                                  optimized)
        for i in range(len(target_frequencies)):
            result[i].append(res[i])
