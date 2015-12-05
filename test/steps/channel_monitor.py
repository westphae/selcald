from behave import *
from math import ceil
import struct
from random import choice, random
from itertools import chain
import selcale.gensounds as gs
import selcald.detector as sd
from selcald.binsize import SelcalParams

use_step_matcher("re")


@given("a source with noise (?P<noise>.+) playing random SELCAL tones for (?P<t>.+) seconds")
def step_impl(context, noise, t):
    """
    :type context: behave.runner.Context
    :type noise: str
    :type t: str
    """
    t = float(t)
    f = context.samprate/context.n
    nl = float(noise)  # Noise level
    context.noise_level = nl
    sp = SelcalParams()
    freqs = list(sp.selcal_tones.values())
    context.sfreq = [0]*int(f*t)
    # Initial pause
    dur = 0.2+4.8*random()
    samp = [gs.genfreq([0], dur, noise_level=nl,
                       samprate=context.samprate)]
    s = dur
    while s < t:
        dur = min(t-s, 0.75+0.5*random())
        freq = [choice(freqs)]
        samp += [gs.genfreq(freq, dur, noise_level=nl,
                            samprate=context.samprate)]
        # The answer for assert
        i1,i2 = int(f*s), int(ceil(f*(s+dur)))
        context.sfreq[i1:i2] = freq*(i2-i1)
        s += dur
        dur = min(t-s, 0.2+4.8*random())
        samp += [gs.genfreq([0], dur, noise_level=nl,
                            samprate=context.samprate)]
        s += dur
    context.samp = chain(*samp)


@step("a channel monitor tuned for tones? (?P<ftones>.+) with sensitivity (?P<sensitivity>.+)")
def step_impl(context, ftones, sensitivity):
    """
    :type context: behave.runner.Context
    :type ftones: str
    :type sensitivity: str
    """
    context.sensitivity = float(sensitivity)
    context.fletters = list(ftones.upper())
    context.ffreq = [context.params.selcal_tones[l] for l in context.fletters]
    context.scanner = sd.channel_monitor(context.ffreq[0],
                                         context.samprate,
                                         context.n,
                                         sensitivity=context.sensitivity,
                                         noise_duration=10)
    next(context.scanner)


@when("the source is fed into the channel monitor")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.buf = gs.buffer(context.samp, context.n)


@then("the channel monitor correctly detects the tones\.")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    # gs.playsound(context.buf, context.samprate)
    fp, fn, tp, tn = 0, 0, 0, 0
    for chunk, act in zip(context.buf, context.sfreq):
        dat = struct.unpack(str(int(len(chunk)/2))+'H', chunk)
        for d in dat:
            res = context.scanner.send(d/(2**15-1))
        next(context.scanner)
        should = (act == context.ffreq[0])
        tp += should and res
        tn += not should and not res
        fp += not should and res
        fn += should and not res
    print('signal: %3d/%3d (%3.0f)%%; noise: %3d/%3d (%3.0f)%%; noise: %1.1f; sensitivity: %1.1f\n'%
          (tp, tp+fn, (tp+0.01)/(tp+fn+0.01)*100,
           tn, tn+fp, (tn+0.01)/(tn+fp+0.01)*100,
           context.noise_level, context.sensitivity))
    assert (tp+0.01)/(tp+fn+0.01) > 0.65 and (tn+0.01)/(tn+fp+0.01) > 0.85


