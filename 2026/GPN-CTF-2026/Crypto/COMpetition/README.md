# COMpetition

* Category: Crypto
* CTF: GPN CTF 2026
* Difficulty: Introduction
* Status: Solved

## Description

The goal is to beat the server 100 times in a row. Before each round, we must first send a commitment. Then the server reveals its move, and only after that we reveal our own move together with a proof opening the commitment.

At first glance, this looks fair: we should not be able to choose our move after seeing the server's move, because our move was supposedly committed before.

## Provided files

```txt
main.py
pyproject.toml
.python-version
uv.lock
```

The important file is `main.py`.

## Challenge summary

The server runs 100 rounds of rock-paper-scissors.

For each round:

1. We send a commitment as hexadecimal bytes.
2. The server randomly chooses `rock`, `paper`, or `scissors`.
3. The server prints its choice.
4. We send our choice.
5. We send a proof opening the commitment.
6. If our choice beats the server's choice, the round continues.

The commitment verification is:

```python
def verify(commitment: bytes, message: bytes, unveil_info: tuple[bytes, bytes]) -> bool:
    r1, r2 = unveil_info
    return commitment == sha256(r1 + message + r2).digest()
```

So to open a commitment to a message, we only need to provide two byte strings `r1` and `r2` such that:

```txt
commitment = sha256(r1 || message || r2)
```

## Vulnerability

The commitment scheme is not binding.

A proper commitment should force us to commit to exactly one message before seeing the server's choice. Here, the commitment is just the hash of:

```txt
r1 || message || r2
```

But since `r1` and `r2` are both fully controlled by us, we can create one large blob containing all possible messages:

```txt
round-0-AAArockBBBpaperCCCscissorsDDD
```

Then we compute:

```python
commitment = sha256(blob)
```

After the server reveals its move, we choose the winning response.

For example, if the server chooses `rock`, we answer `paper`.

Now we need to open the same commitment to `paper`.

Since `paper` is inside the blob, we split the blob around the substring `paper`:

```txt
r1 = b"round-0-AAArockBBB"
message = b"paper"
r2 = b"CCCscissorsDDD"
```

Then:

```txt
sha256(r1 || message || r2) = sha256(blob)
```

So the server accepts the commitment as valid.

This means the commitment can be opened as `rock`, `paper`, or `scissors`, depending on which substring we choose to reveal.

That breaks the whole purpose of the commitment.

## Why the anti-reuse check does not stop us

The server also stores commitments it has already seen:

```python
elif com in already_seen and already_seen[com] != your_choice:
    print("Something fishy is going on here. What are you doing?")
    return
```

This prevents reusing the same commitment and opening it to different messages.

But we can easily bypass this by using a different blob for every round:

```txt
round-0-AAArockBBBpaperCCCscissorsDDD
round-1-AAArockBBBpaperCCCscissorsDDD
round-2-AAArockBBBpaperCCCscissorsDDD
...
```

Each round has a different hash, so each commitment is unique.

## Exploit idea

For each round:

1. Create a blob containing all three possible moves.
2. Send `sha256(blob)` as the commitment.
3. Wait for the server's move.
4. Choose the winning move.
5. Find the position of that move inside the blob.
6. Split the blob into `r1`, `message`, and `r2`.
7. Send `r1.hex()` and `r2.hex()` as the proof.
8. Repeat 100 times.

The winning move table is:

| Server move | Our move |
| ----------- | -------- |
| rock        | paper    |
| paper       | scissors |
| scissors    | rock     |
