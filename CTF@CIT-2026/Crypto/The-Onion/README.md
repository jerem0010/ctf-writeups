# The Onion

## Challenge information

* **CTF:** CTF@CIT 2026
* **Category:** Crypto
* **Challenge:** The Onion
* **Difficulty:** Elemental
* **Flag format:** `CIT{string}`

## Description

We are given a file named `challenge.txt`.

The challenge description says:

```txt
Can you peel back the layers?
```

There is also an important note:

```txt
The answer you get will not have the CIT{} wrapper, make sure you add it to the final answer.
```

The content of the file is a very long string starting with:

```txt
Vm0wd2QyUXlVWGxWV0d4V1YwZDRWMVl3WkRSWFJteFZVMjA1...
```

## Analysis

The string looked like Base64 because it only contained characters from the Base64 alphabet:

```txt
ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=
```

It also ended with padding characters:

```txt
==
```

At first, decoding it once only produced another similar-looking Base64 string.
Because of the challenge name, **The Onion**, and the hint about peeling back layers, the idea was to repeatedly decode the string.

## Solution

I used CyberChef with the `From Base64` operation several times.

After decoding the content repeatedly, each layer produced another Base64-encoded string.

After enough Base64 decodings, you should find the flag.
