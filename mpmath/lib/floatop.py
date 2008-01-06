"""
Functions for basic operations on raw mpfs: normalization, comparison,
addition, subtraction, multiplication, division, integer powers.
"""

from util import *
import random as _random

# Some commonly needed raw mpfs
fzero = (0, 0, 0)
fone = (1, 0, 1)
ftwo = (1, 1, 1)
ften = (5, 1, 3)
fhalf = (1, -1, 1)

# Special numbers. The choice of representation is fairly arbitrary.
# Any code that works with raw tuples can look for them by checking
# whether the bitcount is None. These objects should always have
# unique instances to permit identification via the 'is' operator.
finf = ('+inf', None, None)
fninf = ('-inf', None, None)
fnan = ('nan', None, None)
#fnzero = ('-0', None, None)


#-----------------------------------------------------------------------------
#
# normalize() is the workhorse function in mpmath. All floating-point
# operations are implemented according to the pattern
#
#  1) convert floating-point problem to an equivalent integer problem
#  2) solve integer problem using Python integer arithmetic
#  3) use normalize() to convert the integer solution to a canonical
#     floating-point number
#
# A number of hacks are used in normalize() to reduce the overhead of step
# (3) as far as possible.
#

# Pre-computing and avoiding calls to trailing_zeros() in
# normalize improves performance at 15-digit precision by ~15%
shift_table = map(trailing_zeros, range(256))

# The general method for counting bits is to use the bitcount() function,
# which calls math.log. However, for prec ~< 200 bits, converting to a 
# hex string and using table lookup for the last four bits is slightly
# faster. This idea was taken from decimal.py
correction = {
        '0': 4, '1': 3, '2': 2, '3': 2,
        '4': 1, '5': 1, '6': 1, '7': 1,
        '8': 0, '9': 0, 'a': 0, 'b': 0,
        'c': 0, 'd': 0, 'e': 0, 'f': 0}

def normalize(man, exp, prec, rounding, CO1=-(1<<600), CO2=(1<<600)):
    """
    normalize(man, exp, prec, rounding) -> return tuple representing
    a fully rounded and normalized raw mpf with value (man * 2**exp)

    The mantissa is rounded in the specified direction if the number of
    exceeds the precision. Trailing zero bits are also stripped from
    the mantissa to ensure that the representation is canonical.
    """

    # Count bits
    if CO1 < man < CO2:
        # Inlined for a small speed boost at low precision
        hex_n = "%x" % abs(man)
        bc = 4*len(hex_n) - correction[hex_n[0]]
    else:
        bc = bitcount(man)
    return normalize2(man, exp, bc, prec, rounding)


def normalize2(man, exp, bc, prec, rounding):
    """
    Does the same as normalize(), but uses a precomputed bitcount.
    """
    # The bit-level operations below assume a nonzero mantissa
    if not man:
        return fzero
    # Cut mantissa down to size
    if bc > prec:
        man = rshift(man, bc-prec, rounding)
        exp += (bc-prec)
        bc = prec
    # Strip trailing zeros
    if not man & 1:
        # To within the nearest byte
        while not man & 0xff:
            man >>= 8
            exp += 8
            bc -= 8
        t = shift_table[man & 0xff]
        man >>= t
        exp += t
        bc -= t
    # If result is +/- a power of two due to rounding up in rshift(),
    # bc may be wrong
    if man == 1 or man == -1:
        bc = 1
    return man, exp, bc


def fpos(s, prec, rounding):
    """Calculate 0+s for a raw mpf (i.e., just round s to the specified
    precision, or return s unchanged if its mantissa is smaller than
    the precision)."""
    man, exp, bc = s
    if bc is None:
        return s
    return normalize2(man, exp, bc, prec, rounding)


#-----------------------------------------------------------------------------
# Comparison operations
#

def feq(s, t):
    """Test equality of two raw mpfs. (This is simply tuple comparion
    unless either number is nan, in which case the result is False)."""
    if s is fnan or t is fnan:
        return False
    return s == t


def fcmp(s, t):
    """Compare the raw mpfs s and t. Return -1 if s < t, 0 if s == t,
    and 1 if s > t. (Same convention as Python's cmp() function.)"""

    # In principle, a comparison amounts to determining the sign of s-t.
    # A full subtraction is relatively slow, however, so we first try to
    # look at the components.
    sman, sexp, sbc = s
    tman, texp, tbc = t

    # Handle special numbers
    if sbc is None or tbc is None:
        if s is t: return 0
        # Follow same convention as Python's cmp for float nan
        if t is fnan: return 1
        if s is finf: return 1
        return -1

    # Very easy cases: check for zeros and opposite signs
    if not tman: return cmp(sman, 0)
    if not sman: return cmp(0, tman)
    if sman > 0 and tman < 0: return 1
    if sman < 0 and tman > 0: return -1

    # This reduces to direct integer comparison
    if sexp == texp: return cmp(sman, tman)

    # Check position of the highest set bit in each number. If
    # different, there is certainly an inequality.
    a = sbc + sexp
    b = tbc + texp
    if sman > 0:
        if a < b: return -1
        if a > b: return 1
    else:
        if a < b: return 1
        if a > b: return -1

    # Both numbers have the same highest bit. Subtract to find
    # how the lower bits compare.
    return cmp(fsub(s, t, 5, ROUND_FLOOR)[0], 0)


#-----------------------------------------------------------------------------
# Arithmetic: +, -, *, /, and related operations
#

def fadd(s, t, prec, rounding):
    """Add two raw mpfs and round the result to the specified precision,
    in the specified direction."""

    # We will assume below that s has the higher exponent.
    if t[1] > s[1]:
        s, t = t, s
    sman, sexp, sbc = s
    tman, texp, tbc = t

    # Handle special numbers
    if sbc is None or tbc is None:
        either = s, t
        if fnan in either: return fnan
        if finf in either and fninf in either: return fnan
        if finf in either: return finf
        return fninf

    # Check if one operand is zero. Zero always has exp = 0; if the
    # other operand has a large exponent, its mantissa will unnecessarily
    # be shifted a huge number of bits if we don't check for this case.
    if not tman: return normalize(sman, sexp, prec, rounding)
    if not sman: return normalize(tman, texp, prec, rounding)

    #------------------------------------------------------------------------
    # More generally, if one number is huge and the other is small,
    # and in particular, if their mantissas don't overlap at all at
    # the current precision level, we can avoid work.
    #       precision
    #    |            |
    #     111111111
    #  +                 222222222
    #     ------------------------
    #  #  1111111110000...
    #
    delta = (sbc + sexp) - (tbc + texp)
    if delta > prec + 5:   # an arbitrary number ~> 3
        # The result may have to be rounded up or down. So we shift s
        # and add a dummy bit outside the precision range to force
        # rounding.
        offset = min(delta + 3, prec+3)
        sman <<= offset
        if tman > 0:
            sman += 1
        else:
            sman -= 1
        return normalize(sman, sexp-offset, prec, rounding)

    #------------------------------------------------------------------------
    #  General algorithm: we set min(s.exp, t.exp) = 0, perform exact integer
    #  addition, and then round the result.
    #                   exp = 0
    #                       |
    #                       v
    #          11111111100000   <-- s.man (padded with zeros from shifting)
    #      +        222222222   <-- t.man (no shifting necessary)
    #          --------------
    #      =   11111333333333
    #
    return normalize(tman+(sman<<(sexp-texp)), texp, prec, rounding)


def fsub(s, t, prec, rounding):
    """Return the difference of two raw mpfs, s-t. This function is
    simply a wrapper of fadd that changes the sign of t."""
    man, exp, bc = t
    if bc is None:
        return fadd(s, fneg(t, prec, rounding), prec, rounding)
    return fadd(s, (-man, exp, bc), prec, rounding)


def fneg(s, prec, rounding):
    """Negate a raw mpf (return -s), rounding the result to the
    specified precision."""
    man, exp, bc = s
    if bc is None:
        return fneg_exact(s)
    return normalize(-man, exp, prec, rounding)


def fneg_exact(s):
    """Negate a raw mpf (return -s), without performing any rounding."""
    man, exp, bc = s
    if bc is None:
        if s is finf: return fninf
        if s is fninf: return finf
        return fnan
    return (-man, exp, bc)


def fabs(s, prec, rounding):
    """Return abs(s) of the raw mpf s, rounded to the specified
    precision."""
    man, exp, bc = s
    if bc is None:
        if s is fninf: return finf
        return s
    if man < 0:
        return normalize(-man, exp, prec, rounding)
    return normalize(man, exp, prec, rounding)

def fsign(s):
    man, exp, bc = s
    if bc is None:
        if s is finf: return 1
        if s is fninf: return -1
        return 0
    return cmp(man, 0)

def fmul(s, t, prec, rounding, bct=bctable):
    """Return the product of two raw mpfs, s*t, rounded to the
    specified precision.
    """

    # This function could be implemented by simply calling
    # normalize(sman*tman, sexp+texp, prec, rounding), but
    # we can gain a significant increase in speed by utilizing
    # the fact that the bitcount is given approximately by sbc+tbc
    # (so no call to bitcount() is needed)
    sman, sexp, sbc = s
    tman, texp, tbc = t

    if sbc is None or tbc is None:
        either = s, t
        if fnan in either: return fnan
        if tbc is None: s, t = t, s
        if t == fzero: return fnan
        return {1:finf, -1:fninf}[fsign(s) * fsign(t)]

    man = sman * tman

    return normalize2(man, sexp+texp, bitcount3(man, sbc+tbc), prec, rounding)


def fdiv(s, t, prec, rounding, bct=bctable):
    """Floating-point division"""
    sman, sexp, sbc = s
    tman, texp, tbc = t

    if (sbc is None) or (tbc is None) or (not tman):
        if fnan in (s, t): return fnan
        if sbc == tbc == None: return fnan
        if tbc is not None:
            if t == fzero:
                return fnan
            return {1:finf, -1:fninf}[fsign(s) * fsign(t)]
        return fzero

    # Same strategy as for addition: if there is a remainder, perturb
    # the result a few bits outside the precision range before rounding
    extra = prec-sbc+tbc+5
    if extra < 5:
        extra = 5
    quot, rem = divmod(sman<<extra, tman)

    if rem:
        quot = (quot << 5) + 1
        extra += 5

    bc = bitcount3(quot, sbc+extra-tbc)
    return normalize2(quot, sexp-texp-extra, bc, prec, rounding)


def fmod(s, t, prec, rounding):
    sman, sexp, sbc = s
    tman, texp, tbc = t
    # Important special case: do nothing if t is larger
    if ((sman < 0) == (tman < 0)) and texp > sexp+sbc:
        return s
    # Another important special case: this allows us to do e.g. x % 1.0
    # to find the fractional part of x, and it'll work when x is huge.
    if tman == 1 and sexp > texp+tbc:
        return fzero
    base = min(sexp, texp)
    man = (sman << (sexp-base)) % (tman << (texp-base))
    return normalize(man, base, prec, rounding)

def fceil(s, prec, rounding):
    sman, sexp, sbc = s
    if sexp > 0:
        return fpos(s, prec, rounding)
    from convert import to_int, from_int
    return from_int(to_int(s, ROUND_CEILING), prec, rounding)

def ffloor(s, prec, rounding):
    sman, sexp, sbc = s
    if sexp > 0:
        return fpos(s, prec, rounding)
    from convert import to_int, from_int
    return from_int(to_int(s, ROUND_FLOOR), prec, rounding)

def fshift_exact(s, n):
    """Quickly multiply the raw mpf s by 2**n without rounding."""
    man, exp, bc = s
    if not man:
        return s
    return man, exp+n, bc

reciprocal_rounding = {
  ROUND_DOWN : ROUND_UP,
  ROUND_UP : ROUND_DOWN,
  ROUND_FLOOR : ROUND_CEILING,
  ROUND_CEILING : ROUND_FLOOR,
  ROUND_HALF_DOWN : ROUND_HALF_UP,
  ROUND_HALF_UP : ROUND_HALF_DOWN,
  ROUND_HALF_EVEN : ROUND_HALF_EVEN
}

negative_rounding = {
  ROUND_DOWN : ROUND_DOWN,
  ROUND_UP : ROUND_UP,
  ROUND_FLOOR : ROUND_CEILING,
  ROUND_CEILING : ROUND_FLOOR,
  ROUND_HALF_DOWN : ROUND_HALF_DOWN,
  ROUND_HALF_UP : ROUND_HALF_UP,
  ROUND_HALF_EVEN : ROUND_HALF_EVEN
}

def fpow(s, n, prec, rounding):
    """Compute s**n, where n is an integer"""
    n = int(n)
    if n == 0: return fone
    if n == 1: return fpos(s, prec, rounding)
    if n == 2: return fmul(s, s, prec, rounding)
    if n == -1: return fdiv(fone, s, prec, rounding)
    if n < 0:
        inverse = fpow(s, -n, prec+5, reciprocal_rounding[rounding])
        return fdiv(fone, inverse, prec, rounding)

    man, exp, bc = s

    # Use exact integer power when the exact mantissa is small
    if bc*n < 5000 or man in (1, -1):
        return normalize(man**n, exp*n, prec, rounding)

    # Use directed rounding all the way through to maintain rigorous
    # bounds for interval arithmetic
    sign = 1
    rounding2 = rounding
    if man < 0 and n % 2:
        sign = -1
        rounding2 = negative_rounding[rounding]
    man = abs(man)

    # Now we perform binary exponentiation. Need to estimate precision
    # to avoid rounding from temporary operations. Roughly log_2(n)
    # operations are performed.
    prec2 = prec + 4*bitcount2(n) + 4
    pm, pe, pbc = fone
    while n:
        if n & 1:
            pm, pe, pbc = normalize(pm*man, pe+exp, prec2, rounding2)
            n -= 1
        man, exp, bc = normalize(man*man, exp+exp, prec2, rounding2)
        n = n // 2

    return normalize(sign*pm, pe, prec, rounding)


def frand(prec):
    """Return a raw mpf chosen randomly from [0, 1), with prec bits
    in the mantissa."""
    return normalize(_random.randrange(0, 1<<prec), -prec, prec, ROUND_FLOOR)
