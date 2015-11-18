from behave import *
from selcald.binsize import SelcalParams


use_step_matcher("re")


def before_all(context):
    context.params = SelcalParams()
    context.samprate = 48000
    context.n = 8096
    context.freq = [0]
    context.dur = 1
    context.rand = False
    context.noise_level = 0
