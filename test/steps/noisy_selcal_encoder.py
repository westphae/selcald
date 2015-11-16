import os
from itertools import chain
from behave import *
import selcale.gensounds as gs


use_step_matcher("re")


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
    noise_level = 0 if 'noise_level' not in context else context.noise_level
    samp = gs.genfreq(context.freq[:2], context.dur, noise_level=noise_level)
    if len(context.freq) > 2:
        pause = gs.genfreq([0], 0.2, noise_level=noise_level)
        samp = chain(samp, pause, gs.genfreq(context.freq[2:], context.dur,
                                             noise_level=noise_level))
    context.samp = samp


@then("a sample is generated for th(?:at|e corresponding) " +
      "frequency (?P<freq>.+)")
def step_impl(context, freq=None):
    """
    :type context: behave.runner.Context
    :type freq: str
    """
    assert round(context.freq[-1]-float(freq), 1) == 0
    context.buf = gs.buffer(context.samp)


@then("a sample is generated for the corresponding frequencies")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.buf = gs.buffer(context.samp)


@step("when fed to an audio generation library, makes the correct sound.")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    gs.playsound(context.samp)
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
    noise_level = float(noise_level)
    context.noise_level = noise_level


@step("a choice of (?P<randomization>.+)")
def step_impl(context, randomization):
    """
    :type context: behave.runner.Context
    :type randomization: str
    """
    context.rand = (randomization=="True")