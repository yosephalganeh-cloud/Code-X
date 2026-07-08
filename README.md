# Code-X 🎭
**Developer:** Yoseph Alganeh

Code-X is a lightweight, terminal-based Unicode Steganography tool built specifically for *Termux*linux*. It allows you to inject invisible text (zero-width characters) directly behind a cover emoji. When the target emoji is copied, the hidden payload comes with it.

It features a built-in terminal UI, start-up animation, and automatic clipboard integration via the Termux API.

## ⚙️ Installation (Termux/linux)
```bash
# Update packages
apt update && apt upgrade -y

# Clone the repository
git clone https://github.com/yosephalganeh-cloud/Code-X.git
cd Code-X
python3 codex.py
