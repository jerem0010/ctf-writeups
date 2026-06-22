# Baby Exponent

* **Category:** Crypto
* **CTF:** CTF@CIT 2026
* **Challenge:** Baby Exponent
* **Points:** 726
* **Status:** Solved

## Challenge

We are given an RSA public key and ciphertext:

```txt
n = 3975311104658158367804953186451876987828483822427305148759145730088615027289956528884778329789668637386484932183485546402292017850452360645365142100268336371204659887371551551598753305231985601246101574833959356250563521064956134365407699223

e = 3

c = 21208016443347524194488872231478291493949438339558450377152081476869432669496266457076405093626099218034592769060441274220970709748741037953818131469435699367735940032724483543045224740051080037
```

The public exponent is very small: `e = 3`.

## Vulnerability

In textbook RSA, encryption is done as:

```txt
c = m^e mod n
```

Here, since `e = 3`:

```txt
c = m^3 mod n
```

Normally, recovering `m` from `c` should be hard without the private key.

However, if the plaintext message `m` is small enough such that:

```txt
m^3 < n
```

then the modulo operation never wraps around.

So instead of having:

```txt
c = m^3 mod n
```

we simply have:

```txt
c = m^3
```

That means we can recover the plaintext by computing the integer cube root of the ciphertext.

No factorization of `n` is required.

## Exploit

We compute:

```txt
m = ∛c
```

Then we convert the integer `m` back into bytes.

It is important to compute an **integer** cube root, not a floating-point one, because the numbers are too large for normal floating-point precision.

## Output

```txt
[+] Exact cube root: True
[+] Plaintext: CIT{FLAG}
```
## Solver explanation

The `solve.py` script implements the attack described above.

First, it computes an integer cube root of the ciphertext `c`. Since the numbers involved are very large, the script avoids floating-point arithmetic and uses an integer-only binary search instead. The function returns both the candidate plaintext integer and a boolean indicating whether the cube root was exact.

If the cube root is exact, it confirms that:

```txt
c = m^3
```

and therefore that the RSA modulo did not wrap around during encryption.

Finally, the recovered integer `m` is converted back into bytes using Python's `to_bytes()` function, which reveals the plaintext flag.

The solver can be run with:

```bash
python3 solve.py
```
