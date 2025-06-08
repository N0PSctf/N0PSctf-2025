FLAG = b'N0PS{RSA_P3lL_cRyp70_5YSTeM!}'

from Crypto.Util.number import *
def decrypt(enc, skey):
	p, q = skey
	c, f = enc
	c1, c2 = c
	n = p * q
	d = inverse(65537, (p - 1) * (q - 1))
	a = pow(f, d, n)
	assert (c1**2 - a**2 * c2**2) % n == 1
	c = pow(c1 - a * c2, d, n)
	m = (inverse(c, n) - c) * inverse(2 * a, n) % n
	return m