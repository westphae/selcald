from behave import *
from selcald.binsize import SelcalParams


use_step_matcher("re")


def before_all(context):
    context.params = SelcalParams()
