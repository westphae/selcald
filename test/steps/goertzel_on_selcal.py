from behave import *
import struct
from math import ceil
import filter.goertzel as gf

use_step_matcher("re")


@step("a Goertzel filter tuned for tones? (?P<ftones>.+)")
def step_impl(context, ftones):
    """
    :type context: behave.runner.Context
    :type ftones: str
    """
    context.result = [[] for i in ftones]
    context.fletters = list(ftones.upper())
    context.ffreq = [context.params.selcal_tones[l] for l in context.fletters]
    context.scanner = gf.scanner(context.result, context.ffreq, context.samprate,
                                context.n)
    next(context.scanner)


@step("the sample is fed into the Goertzel filter")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    for chunk in context.buf:
        dat = struct.unpack(str(int(len(chunk)/2))+'H', chunk)
        for d in dat:
            context.scanner.send(d/(2**15-1))


@step("the Goertzel filter (?P<does>.+) detect that frequency\.")
def step_impl(context, does):
    """
    :type context: behave.runner.Context
    :type does: str
    """
    success = (does == "does")
    res = [s/context.n for s in context.result[0]]
    noise = res[:ceil(context.delays[0]*(context.samprate/context.n))] +\
        res[-ceil(context.delays[-1]*(context.samprate/context.n)):]
    noise = sum(noise)/len(noise) or 0.1 # 0.1 is arbitrary, ok for this test
    signal = res[ceil(context.delays[0]*(context.samprate/context.n)):
        -ceil(context.delays[-1]*(context.samprate/context.n))]
    signal = sum(signal)/len(signal)
    print(noise, signal)
    print('\n')
    # Curve-fitting here, no big deal since this isn't the actual algorithm
    assert signal > 2.015*noise if success else signal < 2.015*noise



@given("a noise level (?P<noise_level>.+)")
def step_impl(context, noise_level):
    """
    :type context: behave.runner.Context
    :type noise_level: str
    """
    context.noise_level = float(noise_level)
