# Code-X 🎭
**Developer:** Yoseph Alganeh

Code-X is a lightweight, terminal-based Unicode Steganography tool built specifically for **Termux**. It allows you to inject invisible text (zero-width characters) directly behind a cover emoji. When the target emoji is copied, the hidden payload comes with it.

It features a built-in terminal UI, start-up animation, and automatic clipboard integration via the Termux API.

## ⚙️ Installation (Termux)

To use the automatic copy-to-clipboard feature, you must install Python and the Termux API package. Run the following commands in your Termux terminal:

```bash
# Update packages
pkg update && pkg upgrade -y

# Install Python and Termux API
pkg install python -y
pkg install termux-api -y

# Clone the repository
git clone https://github.com/yosephalgnahe-cloud/Code-X.git
cd Code-X
python3 codex.py
