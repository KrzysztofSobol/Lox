# 🛡️ Password Manager

A free and open-source password manager — simple, yet powerful. Built with Python, SQLite, and Textual, it keeps your passwords safe and organized without unnecessary complexity.

## 🌟 Features

- 🔐 Secure encryption of credentials using a master key
- 🗂️ Organize credentials by websites
- 🛡️ Encryption and decryption of usernames and passwords
- 📝 Editable credentials
- 🗑️ Deletion of credentials
- 🖥️ CLI interface built with the Textual library
- 🖼️ GUI version (discontinued)

---

## 🛠️ Tech Stack

- **Backend**: Python
- **Database**: SQLite
- **Encryption Utility**: CryptoUtils
- **CLI Interface**: Textual

---

## 🖥️ Interface

- **CLI Version (Recommended)**: Built with the Textual library for smooth terminal-based interaction.
- **GUI Version (discontinued)**: Contains minor bugs and is currently unoptimized.

---

## 📸 Preview

![Alt Text](https://github.com/KrzysztofSobol/Lox/blob/master/viewsGUI/icons/preview.png)
---

## 🔑 Usage

1. Clone the repository:

```bash
git clone https://github.com/KrzysztofSobol/password-manager.git
```

2. Navigate to the project directory:

```bash
cd Lox
```

3. Install dependencies:

```bash
pip install [needed_libraries]
```

4. Run the application:

```bash
python main.py
```

---

## 🛡️ Security

- AES encryption with a user-defined master key
- Sensitive data encrypted before being stored in the database
- Decryption performed only in-memory

---
