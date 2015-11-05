from math import sin, cos, pi, sqrt


class Goertzel:
    def __init__(self, sampling_rate, target_frequency, n):
        self.q2, self.q1 = 0, 0

        # precompute the constants
        k = round(n*target_frequency/sampling_rate)
        omega = (2*pi/n)*k
        self.sine = sin(omega)
        self.cosine = cos(omega)
        self.coeff = 2*self.cosine

        print("k: %f" % k)
        print("coeff: %f" % self.coeff)

    def process_block(self, sample):
        """Call this routine for every sample block (size n)."""
        self.q2, self.q1 = 0, 0
        for s in sample:
            self.q2, self.q1 = self.q1, (self.coeff*self.q1 - self.q2 + s)

    def get_complex_result(self):
        """
        Basic Goertzel:
        Call this routine after every block to get the complex result.
        """
        return complex(self.q1 - self.q2*self.cosine, self.q2*self.sine)

    def get_magnitude_squared(self):
        """
        Optimized Goertzel:
        Call this after every block to get the RELATIVE magnitude squared.
        """
        return self.q1**2 + self.q2**2 - self.q1*self.q2*self.coeff


# Test code

def generate(frequency, sampling_rate, n):
    # Synthesize some test data at a given frequency.
    step = 2*pi*frequency/sampling_rate
    return [int(100*(sin(index*step)+1)) for index in range(n)]


def generate_and_test(frequency, target_frequency, sampling_rate, n):
    # Test 1
    print("For test frequency %f:" % frequency)
    test_data = generate(frequency, sampling_rate, n)
    gtz = Goertzel(sampling_rate, target_frequency, n)

    # Process the samples
    gtz.process_block(test_data)

    # Do the "basic Goertzel" processing.
    res = gtz.get_complex_result()

    print("real = %f imag = %f" % (res.real, res.imag))
    magnitude2 = (res * res.conjugate()).real
    print("Relative magnitude squared = %f" % magnitude2)
    magnitude = sqrt(magnitude2)
    print("Relative magnitude = %f" % magnitude)

    # Do the "optimized Goertzel" processing
    magnitude2 = gtz.get_magnitude_squared()
    print("Relative magnitude squared = %f" % magnitude2)
    magnitude = sqrt(magnitude2)
    print("Relative magnitude = %f" % magnitude)
    print("")


def generate_and_test2(frequency, target_frequency, sampling_rate, n):
    # Test 2
    print("Freq=%7.1f   " % frequency)
    test_data = generate(frequency, sampling_rate, n)
    gtz = Goertzel(sampling_rate, target_frequency, n)

    # Process the samples.
    gtz.process_block(test_data)

    # Do the "standard Goertzel" processing.
    res = gtz.get_complex_result()

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
