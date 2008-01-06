from mpmath import *

def test_special():
    assert inf == inf
    assert inf != -inf
    assert -inf == -inf
    assert inf != nan
    assert nan != nan
    assert isnan(nan)
    assert --inf == inf
    assert abs(inf) == inf
    assert abs(-inf) == inf
    assert abs(nan) != abs(nan)

    assert isnan(inf - inf)
    assert isnan(inf + (-inf))
    assert isnan(-inf - (-inf))

    assert isnan(inf + nan)
    assert isnan(-inf + nan)

    assert mpf(2) + inf == inf
    assert 2 + inf == inf
    assert mpf(2) - inf == -inf
    assert 2 - inf == -inf

    assert inf > 3
    assert 3 < inf

    assert 3 > -inf
    assert -inf < 3

    assert isnan(inf * 0)
    assert isnan(-inf * 0)
    assert inf * 3 == inf
    assert inf * -3 == -inf
    assert -inf * 3 == -inf
    assert -inf * -3 == inf
    assert inf * inf == inf
    assert -inf * -inf == inf

    assert isnan(nan / 3)
    assert inf / -3 == -inf
    assert inf / 3 == inf
    assert 3 / inf == 0
    assert -3 / inf == 0
    assert 0 / inf == 0
    assert isnan(inf / inf)
    assert isnan(inf / -inf)
    assert isnan(inf / nan)

    assert mpf('inf') == mpf('+inf') == inf
    assert mpf('-inf') == -inf
    assert isnan(mpf('nan'))
