import os
import random
from itertools import chain
from behave import *
import selcale.gensounds as gs

use_step_matcher("re")
random.seed(1)


var = {'code_dur': 0.25,
       'pause_dur': 0.1,
       'tone': 0.0015}


@given("the frequency (?P<freq>.+) and a duration (?P<dur>.+)")
def step_impl(context, freq, dur):
    """
    :type context: behave.runner.Context
    :type freq: str
    :type dur: str
    """
    context.freq = [float(freq)]
    context.dur = float(dur)


@when("the tone generation function is run")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    if len(context.freq) <= 2:
        d0, d1, d2, d3, d4 = context.delays[0], context.dur, 0.2, context.dur,\
                             context.delays[-1]
        if 'rand' in context and context.rand:
            context.freq = [(1-var['tone']*2*(random.random()-0.5))*f
                            for f in context.freq]
            d0 *= random.random()
            d1 += var['code_dur']*2*(random.random()-0.5)
            d2 += var['pause_dur']*2*(random.random()-0.5)
            d3 += var['code_dur']*2*(random.random()-0.5)
            d4 *= random.random()
            print(d0, d1, d2, d3, d4)
        samp = gs.genfreq(context.freq[:2], d1, noise_level=context.noise_level,
                          samprate=context.samprate)
        pause1 = gs.genfreq([0], d0, noise_level=context.noise_level,
                          samprate=context.samprate)
        pause2 = gs.genfreq([0], d4, noise_level=context.noise_level,
                          samprate=context.samprate)
        if len(context.freq) > 2:
            pause = gs.genfreq([0], d2, noise_level=context.noise_level,
                          samprate=context.samprate)
            samp = chain(samp, pause, gs.genfreq(context.freq[2:], d3,
                                             noise_level=context.noise_level,
                          samprate=context.samprate))
        context.samp = chain(pause1, samp, pause2)
    else:
        context.samp = gs.genSELCALSample(''.join(context.letters),
                                          noise_level=context.noise_level,
                                          delays = context.delays,
                                          rand=context.rand,
                                          samprate=context.samprate)


@then("a sample is generated for th(?:at|e corresponding) " +
      "frequency (?P<freq>.+)")
def step_impl(context, freq=None):
    """
    :type context: behave.runner.Context
    :type freq: str
    """
    assert round(context.freq[-1]-float(freq), 1) == 0
    context.buf = gs.buffer(context.samp, context.n)


@then("a sample is generated(?:| for the corresponding frequenc(?:y|ies))")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.buf = gs.buffer(context.samp, context.n)


@step("when fed to an audio generation library, makes the correct sound.")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    gs.playsound(context.buf, context.samprate)
    if 'fn' in context:
        gs.playwav(context.fn)


@given("the SELCAL tones? (?P<tones>.+)")
def step_impl(context, tones):
    """
    :type context: behave.runner.Context
    :type tones: str
    """
    assert len(tones) in (1, 2, 4)
    for t in tones:
        assert t.upper() in context.params.letters
    context.letters = list(tones.upper())
    context.freq = [context.params.selcal_tones[l] for l in context.letters]
    context.dur = 1
    if len(tones) == 4:
        context.fn = os.path.join('test', 'res', tones.lower()+'.wav')


@step("a chosen noise level (?P<noise_level>.+)")
def step_impl(context, noise_level):
    """
    :type context: behave.runner.Context
    :type noise_level: str
    """
    context.noise_level = float(noise_level)


@step("a choice of (?P<randomization>.+)")
def step_impl(context, randomization):
    """
    :type context: behave.runner.Context
    :type randomization: str
    """
    context.rand = (randomization == "True")
