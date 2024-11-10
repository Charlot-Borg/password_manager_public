#This project is proprietary and cannot be modified or distributed without explicit permission.

# Python Password Manager

A simple password manager application with encryption, developed in Python using `tkinter` for the GUI and `cryptography` for data security. Users can create and save unique encryption keys, store passwords securely in encrypted files, and retrieve them.

## Features

- **Create User Key**: Generate a unique key for encrypting passwords.
- **Login with Key**: Access saved passwords with the generated key.
- **Save and Retrieve Passwords**: Securely save passwords with encryption, retrieve them by browsing saved files.

## Requirements

- Python 3.x
- Libraries:
  - `tkinter` (built into Python)
  - `cryptography`
  - `json`

Install the required libraries with:
```bash
pip install cryptography
