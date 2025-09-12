# 🔐 Zablos Secret Sharer V3 OTP

**Zablos Secret Sharer V3** is a Python-based secret-sharing tool that splits a message into multiple parts ("shares").
Only when **all shares are combined** can the original message be reconstructed.

This tool supports both:

- **One-Time Pad (OTP)-style encryption** (2 shares)
- **Multi-party secret sharing** (more than 2 shares)

---

## Features

- Custom symbol-to-number mapping (0–99)
- Split messages into multiple code shares
- Reconstruct messages from all shares
- Perfect secrecy with 2-share mode (OTP)
- Pseudo-random OTP code generation with python's secrets - modul
- Terminal-based interface

---

## How It Works

### Master Code Mapping

Characters (letters, digits, symbols) are converted into numbers using a fixed mapping (`mastercode`). This forms the basis for encryption and decryption.

### Encryption

- **2 Shares (OTP mode):**
  - You enter a secret key (`Code1`).
  - The tool calculates `Code2` such that:
    ```
    Message = (Code1 + Code2) mod 100
    ```
  - This mimics a One-Time Pad: perfectly secure if Code1 is random and used only once.

- **More than 2 Shares:**
  - Tool generates random shares (`Code2`, `Code3`, ..., `Code(N-1)`).
  - The final code is calculated so that all shares sum (mod 100) to the original message.

### Decryption

- Input **all shares**.
- The message is reconstructed by summing the numerical values of the shares (mod 100).
- Output is decoded back into readable characters.

---

## Example

### Encrypt (2-share mode)
create a One Time Pad with at least the message length:
(S)plit, (C)ombine, (M)astercode, (O)TP, (W)ipe, (Q)uit? o  
Code length: 20  
Code start#: 1  
Code last#: 1  
C1: i*S=#>Erbj8BYz<Eo:b"  

split message with OTP:  
(S)plit, (C)ombine, (M)astercode, (O)TP, (W)ipe, (Q)uit? s  
enter shares count 2 -> 99: 2  
Message: short secret message  
C1: i*S=#>Erbj8BYz<Eo:b"  
  
-> result:  
C1: i*S=#>Erbj8BYz<Eo:b"  
C2: A,Mß,]e<18WiX<re4k5ß
  
-> combine:  
Message: short secret message  
  
🎲 Why secrets?  
secrets uses system-level sources (/dev/urandom or CryptGenRandom) designed for crypto.
random is deterministic and predictable, even if seeded with time.
OTP security collapses if the pad isn’t truly random.


🛡️ Best Practices for OTP  
Pad length ≥ message length (never shorter).
Never reuse pads (once used, discard forever).
Distribute pads securely (sending them alongside ciphertext breaks the whole system).
Store pads safely (offline, or in encrypted vaults).


📦 Requirements

Python 3.6+

No external dependencies (secrets, os are standard)

▶️ Running the Tool
python zablos_secret_sharer.py


Use the interactive menu:

(S)plit, (C)ombine, (M)astercode, (O)TP, (W)ipe, Sa(V)e, (L)oad, (Q)uit?

Menu Options
Option	Description
S	Split (encrypt) a message
C	Combine (decrypt) shares
M	Show mastercode mapping
O	Generate random OTP-style codes
W	Clear screen
Q	Quit the program


📘 License

This project is free to use, modify, and distribute.
Credit appreciated but not required.

🧠 Author Notes

This tool is great for:

Teaching principles of information-theoretic encryption

Exploring modular arithmetic and secret splitting

If you find it useful or improve it, feel free to share or fork!
