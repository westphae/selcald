from behave import *
from selcald.binsize import SelcalParams


use_step_matcher("re")


def before_all(context):
    context.params = SelcalParams()
    context.samprate = 8000
    context.n = 800
    context.freq = [0]
    context.dur = 1
    context.delays = (0.5, 0.5)
    context.rand = False
    context.noise_level = 0
