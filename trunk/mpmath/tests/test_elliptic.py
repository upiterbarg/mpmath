"""
Limited tests of the elliptic functions module.  A full suite of
extensive testing can be found in elliptic_torture_tests.py

Author of the first version: M.T. Taschuk

References:

[1] Abramowitz & Stegun. 'Handbook of Mathematical Functions, 9th Ed.', 
    (Dover duplicate of 1972 edition)
[2] Whittaker 'A Course of Modern Analysis, 4th Ed.', 1946, 
    Cambridge Univeristy Press

"""

import mpmath
import random
from mpmath.mptypes import (mpc, mp, eps, j, zero, one)
from mpmath.elliptic import *
from mpmath.functions import ldexp

def mpc_ae(a, b, eps=eps):
    res = True
    res = res and a.real.ae(b.real, eps)
    res = res and a.imag.ae(b.imag, eps)
    return res

def test_calculate_nome():
    mp.dps = 100

    q = calculate_nome(zero)
    assert(q == zero)

    mp.dps = 25
    # used Mathematica's EllipticNomeQ[m]
    math1 = [(mpf(1)/10, mpf('0.006584651553858370274473060')),
             (mpf(2)/10, mpf('0.01394285727531826872146409')),
             (mpf(3)/10, mpf('0.02227743615715350822901627')),
             (mpf(4)/10, mpf('0.03188334731336317755064299')),
	     (mpf(5)/10, mpf('0.04321391826377224977441774')),
	     (mpf(6)/10, mpf('0.05702025781460967637754953')),
	     (mpf(7)/10, mpf('0.07468994353717944761143751')),
	     (mpf(8)/10, mpf('0.09927369733882489703607378')),
	     (mpf(9)/10, mpf('0.1401731269542615524091055')),
             (mpf(9)/10, mpf('0.1401731269542615524091055'))]

    for i in math1:
        m = i[0]
        q = calculate_nome(sqrt(m))
        assert q.ae(i[1])

def test_jtheta():
    mp.dps = 25

    z = q = zero
    for n in range(1,5):
        value = jtheta(n, z, q)
        assert(value == (n-1)//2)

    for q in [one, mpf(2)]:
        for n in range(1,5):
	    raised = True
	    try:
	        r = jtheta(n, z, q)
	    except:
	        pass
	    else:
	        raised = False
            assert(raised)

    z = one/10
    q = one/11

    # Mathematical N[EllipticTheta[1, 1/10, 1/11], 25]
    res = mpf('0.1069552990104042681962096')
    result = jtheta(1, z, q)
    assert(result.ae(res))

    # Mathematica N[EllipticTheta[2, 1/10, 1/11], 25]
    res = mpf('1.101385760258855791140606')
    result = jtheta(2, z, q)
    assert(result.ae(res))
   
    # Mathematica N[EllipticTheta[3, 1/10, 1/11], 25]
    res = mpf('1.178319743354331061795905')
    result = jtheta(3, z, q)
    assert(result.ae(res))

    # Mathematica N[EllipticTheta[4, 1/10, 1/11], 25]
    res = mpf('0.8219318954665153577314573')
    result = jtheta(4, z, q)
    assert(result.ae(res))

    # test for sin zeros for jtheta(1, z, q)
    # test for cos zeros for jtheta(2, z, q)
    z1 = pi
    z2 = pi/2
    for i in range(10):
        qstring = str(random.random())
        q = mpf(qstring)
	result = jtheta(1, z1, q)
	assert(result.ae(0))
	result = jtheta(2, z2, q)
        assert(result.ae(0))

def test_jtheta_boundary():
    # see issue 39
    mp.dps = 30
    mp.dps += 30
    q = mpf(6)/10 - one/10**6 - mpf(8)/10 * j
    mp.dps -= 30
    # Mathematica run first
    # N[EllipticTheta[3, 1, 6/10 - 10^-6 - 8/10*I], 2000]
    # then it works:
    # N[EllipticTheta[3, 1, 6/10 - 10^-6 - 8/10*I], 30]
    res = mpf('32.0031009628901652627099524264') + \
          mpf('16.6153027998236087899308935624') * j
    result = jtheta(3, 1, q)
    # check that for abs(q) > Q_LIM a ValueError exception is raised
    mp.dps += 30
    q = mpf(6)/10 - one/10**7 - mpf(8)/10 * j
    mp.dps -= 30
    try:
        result = jtheta(3, 1, q)
    except ValueError:
        pass
    else:
        assert(False)

def test_jtheta_identities():
    """
    Tests the some of the jacobi identidies found in Abramowitz,
    Sec. 16.28, Pg. 576.  The identies are tested to 1 part in 10^98.
    """
    mp.dps = 110
    eps1 = ldexp(eps, 30)

    for i in range(10):
        qstring = str(random.random())
	q = mpf(qstring)

	zstring = str(10*random.random())
	z = mpf(zstring)
        # Abramowitz 16.28.1
        # v_1(z, q)**2 * v_4(0, q)**2 =   v_3(z, q)**2 * v_2(0, q)**2
        #                               - v_2(z, q)**2 * v_3(0, q)**2
	term1 = (jtheta(1, z, q)**2) * (jtheta(4, zero, q)**2)
	term2 = (jtheta(3, z, q)**2) * (jtheta(2, zero, q)**2)
	term3 = (jtheta(2, z, q)**2) * (jtheta(3, zero, q)**2)
	equality = term1 - term2 + term3
	assert(equality.ae(0, eps1))
        
        zstring = str(100*random.random())
        z = mpf(zstring)
        # Abramowitz 16.28.2
        # v_2(z, q)**2 * v_4(0, q)**2 =   v_4(z, q)**2 * v_2(0, q)**2
        #                               - v_1(z, q)**2 * v_3(0, q)**2
        term1 = (jtheta(2, z, q)**2) * (jtheta(4, zero, q)**2)
        term2 = (jtheta(4, z, q)**2) * (jtheta(2, zero, q)**2)
        term3 = (jtheta(1, z, q)**2) * (jtheta(3, zero, q)**2)
        equality = term1 - term2 + term3
	assert(equality.ae(0, eps1))

        # Abramowitz 16.28.3
        # v_3(z, q)**2 * v_4(0, q)**2 =   v_4(z, q)**2 * v_3(0, q)**2
        #                               - v_1(z, q)**2 * v_2(0, q)**2
        term1 = (jtheta(3, z, q)**2) * (jtheta(4, zero, q)**2)
        term2 = (jtheta(4, z, q)**2) * (jtheta(3, zero, q)**2)
        term3 = (jtheta(1, z, q)**2) * (jtheta(2, zero, q)**2)
        equality = term1 - term2 + term3
	assert(equality.ae(0, eps1))

        # Abramowitz 16.28.4
        # v_4(z, q)**2 * v_4(0, q)**2 =   v_3(z, q)**2 * v_3(0, q)**2
        #                               - v_2(z, q)**2 * v_2(0, q)**2
        term1 = (jtheta(4, z, q)**2) * (jtheta(4, zero, q)**2)
        term2 = (jtheta(3, z, q)**2) * (jtheta(3, zero, q)**2)
        term3 = (jtheta(2, z, q)**2) * (jtheta(2, zero, q)**2)
        equality = term1 - term2 + term3
	assert(equality.ae(0, eps1))

        # Abramowitz 16.28.5
        # v_2(0, q)**4 + v_4(0, q)**4 == v_3(0, q)**4
        term1 = (jtheta(2, zero, q))**4
        term2 = (jtheta(4, zero, q))**4
        term3 = (jtheta(3, zero, q))**4
        equality = term1 + term2 - term3
	assert(equality.ae(0, eps1))

def test_jtheta_complex():
    mp.dps = 30
    z = mpf(1)/4 + j/8
    q = mpf(1)/3 + j/7
    # Mathematica N[EllipticTheta[1, 1/4 + I/8, 1/3 + I/7], 35]
    res = mpf('0.31618034835986160705729105731678285') + \
          mpf('0.07542013825835103435142515194358975') * j
    r = jtheta(1, z, q)
    assert(mpc_ae(r, res))

    # Mathematica N[EllipticTheta[2, 1/4 + I/8, 1/3 + I/7], 35]
    res = mpf('1.6530986428239765928634711417951828') + \
          mpf('0.2015344864707197230526742145361455') * j
    r = jtheta(2, z, q)
    assert(mpc_ae(r, res))

    # Mathematica N[EllipticTheta[3, 1/4 + I/8, 1/3 + I/7], 35]
    res = mpf('1.6520564411784228184326012700348340') + \
          mpf('0.1998129119671271328684690067401823') * j
    r = jtheta(3, z, q)
    assert(mpc_ae(r, res))

    # Mathematica N[EllipticTheta[4, 1/4 + I/8, 1/3 + I/7], 35]
    res = mpf('0.37619082382228348252047624089973824') - \
          mpf('0.15623022130983652972686227200681074') * j
    r = jtheta(4, z, q)
    assert(mpc_ae(r, res))

    # check some theta function identities
    mp.dos = 100
    z = mpf(1)/4 + j/8
    q = mpf(1)/3 + j/7
    mp.dps += 10
    a = [0,0, jtheta(2, 0, q), jtheta(3, 0, q), jtheta(4, 0, q)]
    t = [0, jtheta(1, z, q), jtheta(2, z, q), jtheta(3, z, q), jtheta(4, z, q)]
    r = [(t[2]*a[4])**2 - (t[4]*a[2])**2 + (t[1] *a[3])**2,
        (t[3]*a[4])**2 - (t[4]*a[3])**2 + (t[1] *a[2])**2,
        (t[1]*a[4])**2 - (t[3]*a[2])**2 + (t[2] *a[3])**2,
        (t[4]*a[4])**2 - (t[3]*a[3])**2 + (t[2] *a[2])**2,
        a[2]**4 + a[4]**4 - a[3]**4]
    mp.dps -= 10
    for x in r:
        assert(mpc_ae(x, mpc(0)))

def test_djtheta():
    mp.dps = 30

    z = one/7 + j/3
    q = one/8 + j/5
    # Mathematica N[EllipticThetaPrime[1, 1/7 + I/3, 1/8 + I/5], 35]
    res = mpf('1.5555195883277196036090928995803201') - \
	  mpf('0.02439761276895463494054149673076275') * j
    result = djtheta(1, z, q)
    assert(mpc_ae(result, res))

    # Mathematica N[EllipticThetaPrime[2, 1/7 + I/3, 1/8 + I/5], 35]
    res = mpf('0.19825296689470982332701283509685662') - \
	  mpf('0.46038135182282106983251742935250009') * j
    result = djtheta(2, z, q)
    assert(mpc_ae(result, res))

    # Mathematica N[EllipticThetaPrime[3, 1/7 + I/3, 1/8 + I/5], 35]
    res = mpf('0.36492498415476212680896699407390026') - \
          mpf('0.57743812698666990209897034525640369') * j
    result = djtheta(3, z, q)
    assert(mpc_ae(result, res))

    # Mathematica N[EllipticThetaPrime[4, 1/7 + I/3, 1/8 + I/5], 35]
    res = mpf('-0.38936892528126996010818803742007352') + \
          mpf('0.66549886179739128256269617407313625') * j
    result = djtheta(4, z, q)
    assert(mpc_ae(result, res))

    for i in range(10):
        q = (one*random.random() + j*random.random())/2
        # identity
        a = djtheta(1, 0, q)
        b = jtheta(2, 0, q)*jtheta(3, 0, q)*jtheta(4, 0, q)
        assert(a.ae(b))

def test_jsn():
    """
    Test some special cases of the sn(z, q) function.
    """
    mp.dps = 100

    # trival case
    result = jsn(zero, zero)
    assert(result == zero)

    # Abramowitz Table 16.5
    #
    # sn(0, m) = 0

    for i in range(10):
        qstring = str(random.random())
        q = mpf(qstring)

        equality = jsn(zero, q)
        assert(equality.ae(0))

    # Abramowitz Table 16.6.1
    #
    # sn(z, 0) = sin(z), m == 0
    #
    # sn(z, 1) = tanh(z), m == 1
    #
    # It would be nice to test these, but I find that they run
    # in to numerical trouble.  I'm currently treating as a boundary
    # case for sn function.
    
    mp.dps = 25
    arg = one/10
    #N[JacobiSN[1/10, 2^-100], 25]
    res = mpf('0.09983341664682815230681420')
    m = ldexp(one, -100)
    result = jsn(arg, m)
    assert(result.ae(res))

    # N[JacobiSN[1/10, 1/10], 25]
    res = mpf('0.09981686718599080096451168')
    result = jsn(arg, arg)
    assert(result.ae(res))

def test_jcn():
    """
    Test some special cases of the cn(z, q) function.
    """
    mp.dps = 100

    # Abramowitz Table 16.5
    # cn(0, q) = 1
    qstring = str(random.random())
    q = mpf(qstring)
    cn = jcn(zero, q)
    assert(cn.ae(one))

    # Abramowitz Table 16.6.2
    #
    # cn(u, 0) = cos(u), m == 0
    #
    # cn(u, 1) = sech(z), m == 1
    #
    # It would be nice to test these, but I find that they run
    # in to numerical trouble.  I'm currently treating as a boundary
    # case for cn function.

    mp.dps = 25
    arg = one/10
    m = ldexp(one, -100)
    #N[JacobiCN[1/10, 2^-100], 25]
    res = mpf('0.9950041652780257660955620')
    result = jcn(arg, m)
    assert(result.ae(res))

    # N[JacobiCN[1/10, 1/10], 25]
    res = mpf('0.9950058256237368748520459')
    result = jcn(arg, arg)
    assert(result.ae(res))

def test_jdn():
    """
    Test some special cases of the dn(z, q) function.
    """
    mp.dps = 100

    # Abramowitz Table 16.5
    # dn(0, q) = 1
    mstring = str(random.random())
    m = mpf(mstring)

    dn = jdn(zero, m)
    assert(dn.ae(one))

    mp.dps = 25
    # N[JacobiDN[1/10, 1/10], 25]
    res = mpf('0.9995017055025556219713297')
    arg = one/10
    result = jdn(arg, arg)
    assert(result.ae(res))

def test_sn_cn_dn_identities():
    """
    Tests the some of the jacobi elliptic function identidies found
    on Mathworld.  Havne't found in Abramowitz.  
    """
    mp.dps = 100
    for i in range(10):
        qstring = str(random.random())
        q = mpf(qstring)
        zstring = str(100*random.random())
        z = mpf(zstring)

        # MathWorld
	# sn(z, q)**2 + cn(z, q)**2 == 1 
        term1 = jsn(z, q)**2
        term2 = jcn(z, q)**2
        equality = one - term1 - term2
        assert(equality.ae(0))

    # MathWorld
    # k**2 * sn(z, m)**2 + dn(z, m)**2 == 1
    for i in range(10):
        mstring = str(random.random())
        m = mpf(qstring)
        k = m.sqrt()
        zstring = str(10*random.random())
        z = mpf(zstring)
        term1 = k**2 * jacobi_elliptic_sn(z, m)**2
        term2 = jdn(z, m)**2
        equality = one - term1 - term2
        assert(equality.ae(0))


    for i in range(10):
        mstring = str(random.random())
        m = mpf(mstring)
        k = m.sqrt()
        zstring = str(random.random())
        z = mpf(zstring)

        # MathWorld
        # k**2 * cn(z, m)**2 + (1 - k**2) = dn(z, m)**2
        term1 = k**2 * jcn(z, m)**2
        term2 = 1 - k**2
        term3 = jdn(z, m)**2
        equality = term3 - term1 - term2
        assert(equality.ae(0))

        K = ellipk(k**2)
	# Abramowitz Table 16.5
	# sn(K, m) = 1; K is K(k), first complete elliptic integral
	r = jsn(K, m)
	assert(r.ae(one))

        # Abramowitz Table 16.5
        # cn(K, q) = 0; K is K(k), first complete elliptic integral
        equality = jcn(K, m)
        assert(equality.ae(0))

        # Abramowitz Table 16.6.3
        # dn(z, 0) = 1, m == 0
	z = m
        value = jdn(z, zero)
        assert(value.ae(one))

def test_sn_cn_dn_complex():
    mp.dps = 30
    # N[JacobiSN[1/4 + I/8, 1/3 + I/7], 35] in Mathematica
    res = mpf('0.2495674401066275492326652143537') + \
          mpf('0.12017344422863833381301051702823') * j
    u = mpf(1)/4 + j/8
    m = mpf(1)/3 + j/7
    r = jsn(u, m)
    assert(mpc_ae(r, res))

    #N[JacobiCN[1/4 + I/8, 1/3 + I/7], 35]
    res = mpf('0.9762691700944007312693721148331') - \
          mpf('0.0307203994181623243583169154824')*j
    r = jcn(u, m)
    #assert r.real.ae(res.real)
    #assert r.imag.ae(res.imag)
    assert(mpc_ae(r, res))

    #N[JacobiDN[1/4 + I/8, 1/3 + I/7], 35]
    res = mpf('0.99639490163039577560547478589753039') - \
          mpf('0.01346296520008176393432491077244994')*j
    r = jdn(u, m)
    assert(mpc_ae(r, res))

