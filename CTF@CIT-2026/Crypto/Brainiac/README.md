# Brainiac

## Challenge information

- **CTF:** CTF@CIT 2026
- **Category:** Crypto
- **Challenge:** Brainiac
- **Difficulty:** Elemental
- **Flag format:** `CIT{string}`

## Description

We are given a file named `challenge.txt`.

Its content looks like this:

```txt
++++++++++[>+>+++>+++++++>++++++++++<<<<-]>>>---.++++++.+++++++++++...
```

At first glance, this does not look like a classical cipher such as Caesar, Vigenère, Base64, or hexadecimal.

The file is mostly composed of the following characters:

```txt
+ - < > [ ] .
```


## Solution

After doing some research on this unusual syntax, I found out that it was Brainfuck, an esoteric programming language. I then used the dCode Brainfuck interpreter:

```txt
https://www.dcode.fr/langage-brainfuck
```

After pasting the content of `challenge.txt` into the interpreter, it printed the flag directly

## Brainfuck

Brainfuck is a very small esoteric programming language based on only eight instructions.

| Instruction | Meaning |
|---|---|
| `>` | Move the memory pointer to the right |
| `<` | Move the memory pointer to the left |
| `+` | Increment the current memory cell |
| `-` | Decrement the current memory cell |
| `.` | Output the current memory cell as an ASCII character |
| `,` | Read one byte of input |
| `[` | Start a loop while the current cell is non-zero |
| `]` | End the loop |

Since the challenge contains several `.` instructions, the program probably prints something when executed.