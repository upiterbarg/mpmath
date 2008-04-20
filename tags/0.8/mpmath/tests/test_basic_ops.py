from mpmath import *

def test_type_compare():
    assert mpf(2) == mpc(2,0)
    assert mpf(0) == mpc(0)
    assert mpf(2) != mpc(2, 0.00001)
    assert mpf(2) == 2.0
    assert mpf(2) != 3.0
    assert mpf(2) == 2
    assert mpf(2) != '2.0'
    assert mpc(2) != '2.0'

def test_add():
    assert mpf(2.5) + mpf(3) == 5.5
    assert mpf(2.5) + 3 == 5.5
    assert mpf(2.5) + 3.0 == 5.5
    assert 3 + mpf(2.5) == 5.5
    assert 3.0 + mpf(2.5) == 5.5
    assert (3+0j) + mpf(2.5) == 5.5
    assert mpc(2.5) + mpf(3) == 5.5
    assert mpc(2.5) + 3 == 5.5
    assert mpc(2.5) + 3.0 == 5.5
    assert mpc(2.5) + (3+0j) == 5.5
    assert 3 + mpc(2.5) == 5.5
    assert 3.0 + mpc(2.5) == 5.5
    assert (3+0j) + mpc(2.5) == 5.5

def test_sub():
    assert mpf(2.5) - mpf(3) == -0.5
    assert mpf(2.5) - 3 == -0.5
    assert mpf(2.5) - 3.0 == -0.5
    assert 3 - mpf(2.5) == 0.5
    assert 3.0 - mpf(2.5) == 0.5
    assert (3+0j) - mpf(2.5) == 0.5
    assert mpc(2.5) - mpf(3) == -0.5
    assert mpc(2.5) - 3 == -0.5
    assert mpc(2.5) - 3.0 == -0.5
    assert mpc(2.5) - (3+0j) == -0.5
    assert 3 - mpc(2.5) == 0.5
    assert 3.0 - mpc(2.5) == 0.5
    assert (3+0j) - mpc(2.5) == 0.5

def test_mul():
    assert mpf(2.5) * mpf(3) == 7.5
    assert mpf(2.5) * 3 == 7.5
    assert mpf(2.5) * 3.0 == 7.5
    assert 3 * mpf(2.5) == 7.5
    assert 3.0 * mpf(2.5) == 7.5
    assert (3+0j) * mpf(2.5) == 7.5
    assert mpc(2.5) * mpf(3) == 7.5
    assert mpc(2.5) * 3 == 7.5
    assert mpc(2.5) * 3.0 == 7.5
    assert mpc(2.5) * (3+0j) == 7.5
    assert 3 * mpc(2.5) == 7.5
    assert 3.0 * mpc(2.5) == 7.5
    assert (3+0j) * mpc(2.5) == 7.5

def test_div():
    assert mpf(6) / mpf(3) == 2.0
    assert mpf(6) / 3 == 2.0
    assert mpf(6) / 3.0 == 2.0
    assert 6 / mpf(3) == 2.0
    assert 6.0 / mpf(3) == 2.0
    assert (6+0j) / mpf(3.0) == 2.0
    assert mpc(6) / mpf(3) == 2.0
    assert mpc(6) / 3 == 2.0
    assert mpc(6) / 3.0 == 2.0
    assert mpc(6) / (3+0j) == 2.0
    assert 6 / mpc(3) == 2.0
    assert 6.0 / mpc(3) == 2.0
    assert (6+0j) / mpc(3) == 2.0

def test_pow():
    assert mpf(6) ** mpf(3) == 216.0
    assert mpf(6) ** 3 == 216.0
    assert mpf(6) ** 3.0 == 216.0
    assert 6 ** mpf(3) == 216.0
    assert 6.0 ** mpf(3) == 216.0
    assert (6+0j) ** mpf(3.0) == 216.0
    assert mpc(6) ** mpf(3) == 216.0
    assert mpc(6) ** 3 == 216.0
    assert mpc(6) ** 3.0 == 216.0
    assert mpc(6) ** (3+0j) == 216.0
    assert 6 ** mpc(3) == 216.0
    assert 6.0 ** mpc(3) == 216.0
    assert (6+0j) ** mpc(3) == 216.0

def test_mixed_misc():
    assert 1 + mpf(3) == mpf(3) + 1 == 4
    assert 1 - mpf(3) == -(mpf(3) - 1) == -2
    assert 3 * mpf(2) == mpf(2) * 3 == 6
    assert 6 / mpf(2) == mpf(6) / 2 == 3
    assert 1.0 + mpf(3) == mpf(3) + 1.0 == 4
    assert 1.0 - mpf(3) == -(mpf(3) - 1.0) == -2
    assert 3.0 * mpf(2) == mpf(2) * 3.0 == 6
    assert 6.0 / mpf(2) == mpf(6) / 2.0 == 3

def test_add_misc():
    mp.dps = 15
    assert mpf(4) + mpf(-70) == -66
    assert mpf(1) + mpf(1.1)/80 == 1 + 1.1/80
    assert mpf((1, 10000000000)) + mpf(3) == mpf((1, 10000000000))
    assert mpf(3) + mpf((1, 10000000000)) == mpf((1, 10000000000))
    assert mpf((1, -10000000000)) + mpf(3) == mpf(3)
    assert mpf(3) + mpf((1, -10000000000)) == mpf(3)
    assert mpf(1) + 1e-15 != 1
    assert mpf(1) + 1e-20 == 1
    assert mpf(1.07e-22) + 0 == mpf(1.07e-22)
    assert mpf(0) + mpf(1.07e-22) == mpf(1.07e-22)

def test_complex_misc():
    # many more tests needed
    assert 1 + mpc(2) == 3
    assert not mpc(2).ae(2 + 1e-13)
    assert mpc(2+1e-15j).ae(2)

def test_complex_zeros():
    for a in [0,2]:
      for b in [0,3]:
        for c in [0,4]:
          for d in [0,5]:
            assert mpc(a,b)*mpc(c,d) == complex(a,b)*complex(c,d)
