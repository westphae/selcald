from unittest import TestCase
from math import sin, pi, sqrt
from src.goertzel import scanner
import csv


def generate(frequency, sampling_rate, n):
    # Synthesize some test data at a given frequency.
    step = 2*pi*frequency/sampling_rate
    return [int(100*(sin(index*step)+1)) for index in range(n)]


def generate_and_test0(sample_frequency, target_frequency, sampling_rate, n):
    # Generate sample
    test_data = generate(sample_frequency, sampling_rate, n)

    # Do the "basic Goertzel" processing
    results = [[]]
    scan = scanner(results, [target_frequency], sampling_rate, n,
                   optimized=False)
    next(scan)
    for d in test_data:
        scan.send(d)

    res = results[0][-1]
    return res


def generate_and_test1(sample_frequency, target_frequency, sampling_rate, n):
    # Generate sample
    test_data = generate(sample_frequency, sampling_rate, n)

    # Do the "optimized Goertzel" processing
    results = [[]]
    scan = scanner(results, [target_frequency], sampling_rate, n)
    next(scan)
    for d in test_data:
        scan.send(d)

    magnitude2 = results[0][-1]
    return magnitude2


def generate_and_test2(sample_frequencies, target_frequency, sampling_rate, n):
    # Generate samples
    results = [[]]
    scan = scanner(results, [target_frequency], sampling_rate, n,
                   optimized=False)
    next(scan)
    for freq in sample_frequencies:
        test_data = generate(freq, sampling_rate, n)
        for d in test_data:
            scan.send(d)

    return results[0]


def read_test_results_csv(filename):
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)

        should = dict.fromkeys(reader.fieldnames, [])
        for r in reader:
            for k, v in r.items():
                should[k] = [float(v)]+should[k]
    return should


class Test_From_Lyons(TestCase):

    def setUp(self):
        self.test_sample_rate = 8000.0  # 8kHz
        self.test_target_frequency = 941.0  # 941 Hz
        self.test_n = 205  # Block size

    def test0_below_frequency(self):
        res = generate_and_test0(self.test_target_frequency - 250,
                                 self.test_target_frequency,
                                 self.test_sample_rate, self.test_n)
        m2 = (res * res.conjugate()).real
        m = sqrt(m2)
        self.assertAlmostEqual(res.real, -360.392059, 1)
        self.assertAlmostEqual(res.imag, -45.871609, 1)
        self.assertAlmostEqual(m2, 131986.640625, 0)
        self.assertAlmostEqual(m, 363.299652, 1)

    def test0_at_frequency(self):
        res = generate_and_test0(self.test_target_frequency,
                                 self.test_target_frequency,
                                 self.test_sample_rate, self.test_n)
        m2 = (res * res.conjugate()).real
        m = sqrt(m2)
        self.assertAlmostEqual(res.real, -3727.528076, 1)
        self.assertAlmostEqual(res.imag, -9286.238281, 1)
        self.assertAlmostEqual(m2, 100128688.000000, -3)
        self.assertAlmostEqual(m, 10006.432617, 1)

    def test0_above_frequency(self):
        res = generate_and_test0(self.test_target_frequency + 250,
                                 self.test_target_frequency,
                                 self.test_sample_rate, self.test_n)
        m2 = (res * res.conjugate()).real
        m = sqrt(m2)
        self.assertAlmostEqual(res.real, 424.038116, 1)
        self.assertAlmostEqual(res.imag, -346.308716, 1)
        self.assertAlmostEqual(m2, 299738.062500, -1)
        self.assertAlmostEqual(m, 547.483398, 1)

    def test1_below_frequency(self):
        m2 = generate_and_test1(self.test_target_frequency - 250,
                                self.test_target_frequency,
                                self.test_sample_rate, self.test_n)
        m = sqrt(m2)
        self.assertAlmostEqual(m2, 131986.640625, -1)
        self.assertAlmostEqual(m, 363.299652, 0)

    def test1_at_frequency(self):
        m2 = generate_and_test1(self.test_target_frequency,
                                self.test_target_frequency,
                                self.test_sample_rate, self.test_n)
        m = sqrt(m2)
        self.assertAlmostEqual(m2, 100128688.000000, -3)
        self.assertAlmostEqual(m, 10006.432617, 0)

    def test1_above_frequency(self):
        m2 = generate_and_test1(self.test_target_frequency + 250,
                                self.test_target_frequency,
                                self.test_sample_rate, self.test_n)
        m = sqrt(m2)
        self.assertAlmostEqual(m2, 299738.062500, -1)
        self.assertAlmostEqual(m, 547.483398, 0)

    def test2(self):
        should = read_test_results_csv('goertzel_test_results.csv')

        res = generate_and_test2(should['freq'],
                                 self.test_target_frequency,
                                 self.test_sample_rate, self.test_n)
        m2 = [(r*r.conjugate()).real for r in res]
        m = [sqrt(r) for r in m2]
        for m2a, m2s in zip(m2, should['m2']):
            self.assertAlmostEqual(m2a/m2s, 1, 2)
        for ma, ms in zip(m, should['m']):
            self.assertAlmostEqual(ma/ms, 1, 2)
