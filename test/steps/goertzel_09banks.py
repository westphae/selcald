from behave import *
from filter.goertzel import scanner
from math import pi, sin, sqrt

use_step_matcher("re")


@given("a sampling rate 8000 Hz")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.sample_rate = 8000


@step("a chunk size of 205")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.n = 205


@given("I have an? (?P<ftype>.+) Goertzel filter for target frequency 941 Hz")
def step_impl(context, ftype):
    """
    :type context: behave.runner.Context
    :type ftype: str
    """
    context.target_freq = 941
    context.results = [[]]
    context.ftype = ftype
    context.scanner = scanner(context.results, [context.target_freq],
                              context.sample_rate, context.n,
                              optimized=(ftype == "optimized"))
    next(context.scanner)


@when("I pass a sample of frequency (?P<sample_freq>.+) through the filter")
def step_impl(context, sample_freq):
    """
    :type context: behave.runner.Context
    :type sample_freq: str
    """
    sample_freq = float(sample_freq)
    fstep = 2*pi*sample_freq/context.sample_rate
    test_data = [int(100*(sin(index*fstep)+1)) for index in range(context.n)]
    for d in test_data:
        context.scanner.send(d)
    val = context.results[0][-1]
    if context.ftype == 'basic':
        context.res = {'real': val.real, 'imag': val.imag,
                       'm2': (val*val.conjugate()).real}
    else:
        context.res = {'m2': val}
    context.res['m'] = sqrt(context.res['m2'])


@then("I get a real value (?P<real>.+)")
def step_impl(context, real):
    """
    :type context: behave.runner.Context
    :type real: str
    """
    real = float(real)
    assert round(context.res['real'] - real, 1) == 0


@step("an imaginary value (?P<imag>.+)")
def step_impl(context, imag):
    """
    :type context: behave.runner.Context
    :type imag: str
    """
    imag = float(imag)
    assert round(context.res['imag'] - imag, 1) == 0


@step("I get a magnitude squared (?P<m2>.+)")
def step_impl(context, m2):
    """
    :type context: behave.runner.Context
    :type m2: str
    """
    m2 = float(m2)
    assert round(context.res['m2'] - m2, -4) == 0


@step("a magnitude (?P<m>.+)\.")
def step_impl(context, m):
    """
    :type context: behave.runner.Context
    :type m: str
    """
    m = float(m)
    assert round(context.res['m'] - m, -1) == 0
