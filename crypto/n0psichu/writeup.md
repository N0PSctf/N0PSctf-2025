## n0psichu

### Description

In N0PSichu, polish a cryptosystem to reveal its hidden flaws and make it shine, or break.

**Author: factoreal**

Challenge designed by **[ASIS](https://asisctf.com/) team** 

### Solution

The challenge involves breaking RSA using an Approximate Common Divisor (ACD) attack. 

First, several approximate multiples of the RSA secret prime p were collected. These were passed into a polynomial-based ACD attack implemented using SageMath and a small_roots helper module. 

By exploiting the structure of these approximate values and using lattice techniques (specifically a Groebner basis method), the secret prime p was recovered. 

Once p was found, the full private key was reconstructed by computing $q = N // p$ and the private exponent $d = inverse(65537, (p-1)*(q-1))$. 

Finally, a custom decryption function was used to recover the flag from a specially structured ciphertext using this private key.

The full solution script can be found in the [`sol.py`](sol.py).


### Flag

The flag is `N0PS{RSA_P3lL_cRyp70_5YSTeM!}`