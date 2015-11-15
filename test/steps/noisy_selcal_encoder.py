from behave import *
from selcald.binsize import SelcalParams
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
    context.dur = [float(dur)]


@when("the tone generation function is run")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.samp = gs.genfreq(context.freq[-1], context.dur[-1])


@then("a sample is generated for (?:that|the corresponding) " +
      "frequency (?P<freq>.+)")
def step_impl(context, freq):
    """
    :type context: behave.runner.Context
    :type freq: str
    """
    print(freq, type(freq))
    print(context.freq[-1], type(context.freq))
    assert round(context.freq[-1]-float(freq), 1) == 0
    context.buf = gs.buffer(context.samp)


@step("when fed to an audio generation library, " +
      "sounds the correct frequenc(?:y|ies)?")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    gs.playsound(context.samp)


@given("the SELCAL tones? (?P<tones>.+)")
def step_impl(context, tones):
    """
    :type context: behave.runner.Context
    :type tones: str
    """
    for t in tones:
        assert t in context.params.letters
    context.letters = list(tones)
    context.freq = [context.params.selcal_tones[l] for l in context.letters]
    context.dur = [1 for l in context.letters]


