from math import sin, pi, sqrt
from src.goertzel import goertzel


def generate(frequency, sampling_rate, n):
    # Synthesize some test data at a given frequency.
    step = 2*pi*frequency/sampling_rate
    return [int(100*(sin(index*step)+1)) for index in range(n)]


def generate_and_test(frequency, target_frequency, sampling_rate, n):
    # Test 1
    print("For test frequency %f:" % frequency)
    test_data = generate(frequency, sampling_rate, n)

    # Do the "basic Goertzel" processing.
    gtz = goertzel(sampling_rate, target_frequency, n, optimized=False)
    next(gtz)
    try:
        for d in test_data:
            gtz.send(d)
    except StopIteration as exc:
        res = exc.value
    print("real = %f imag = %f" % (res.real, res.imag))
    magnitude2 = (res * res.conjugate()).real
    print("Relative magnitude squared = %f" % magnitude2)
    magnitude = sqrt(magnitude2)
    print("Relative magnitude = %f" % magnitude)

    # Do the "optimized Goertzel" processing
    gtz = goertzel(sampling_rate, target_frequency, n)
    next(gtz)
    try:
        for d in test_data:
            gtz.send(d)
    except StopIteration as exc:
        magnitude2 = exc.value
    print("Relative magnitude squared = %f" % magnitude2)
    magnitude = sqrt(magnitude2)
    print("Relative magnitude = %f" % magnitude)
    print("")


def generate_and_test2(frequency, target_frequency, sampling_rate, n):
    # Test 2
    print("Freq=%7.1f   " % frequency)
    test_data = generate(frequency, sampling_rate, n)
    gtz = goertzel(sampling_rate, target_frequency, n, optimized=False)
    next(gtz)
    try:
        for d in test_data:
            gtz.send(d)
    except StopIteration as exc:
        res = exc.value
    magnitude2 = (res * res.conjugate()).real
    print("rel mag^2=%16.5f   " % magnitude2)
    magnitude = abs(res)
    print("rel mag=%12.5f" % magnitude)
    print("")


if __name__ == '__main__':

    test_sample_rate = 8000.0  # 8kHz
    test_target_frequency = 941.0  # 941 Hz
    test_n = 205  # Block size

    # Test 1
    generate_and_test(test_target_frequency - 250, test_target_frequency,
                      test_sample_rate, test_n)
    generate_and_test(test_target_frequency, test_target_frequency,
                      test_sample_rate, test_n)
    generate_and_test(test_target_frequency + 250, test_target_frequency,
                      test_sample_rate, test_n)

    # Test 2
    for freq in range(int(test_target_frequency-300),
                      int(test_target_frequency+301), 15):
        generate_and_test2(freq, test_target_frequency,
                           test_sample_rate, test_n)