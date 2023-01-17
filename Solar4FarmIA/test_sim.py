import pytest
from timer import Timer 
from const import *
from solar_activity import SolarActivity

def test_succesful_year_iteration():
    _last = (0, 0, 0)
    for _t in Timer():
        _last = _t
    assert (_last[1] == 365 and _last[0] == 23 and _last[2] == 12)

def test_hour_stays_reasonable():
    for _t in Timer():
        assert (0 <= _t[0] <= 23 and 1 <= _t[1] <= 365 and 1 <= _t[2] <= 12)