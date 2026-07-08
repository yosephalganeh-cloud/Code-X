"
Code-X — zero-width Unicode steganography tool
Encodes/decodes hidden text inside an emoji (or any string) using
invisible zero-width characters (U+200B / U+200C).

Works on Termux, Kali Linux, and generic Linux/macOS/Windows.
Clipboard support auto-detects whatever tool is available on the
system instead of hard-depending on termux-api.
"""
import os
import sys
import time
import shutil
import subprocess

# --- Animation & UI ---
def animate_text(text, delay=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def show_banner():
    os.system('clear' if os.name == 'posix' else 'cls')
    banner = """\033[92m
     ██████╗ ██████╗ ██████╗ ███████╗    ██╗  ██╗
    ██╔════╝██╔═══██╗██╔══██╗██╔════╝    ╚██╗██╔╝
    ██║     ██║   ██║██║  ██║█████╗       ╚███╔╝ 
    ██║     ██║   ██║██║  ██║██╔══╝       ██╔██╗ 
    ╚██████╗╚██████╔╝██████╔╝███████╗    ██╔╝ ██╗
     ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝    ╚═╝  ╚═╝
    \033[0m"""
    print(banner)
    print("\033[96m" + " " * 12 + "Code-X — by Yoseph Alganeh\033[0m\n")
    animate_text("\033[93m[+] Booting Code-X Engine...\033[0m", 0.04)
    animate_text("\033[93m[+] Initializing Zero-Width Subroutines...\033[0m", 0.02)
    time.sleep(0.3)
    print()

# --- Steganography Core ---
def encode_message(cover, hidden_text):
    """Hide `hidden_text` inside `cover` using zero-width chars.
    Works with an emoji, a word, or a whole sentence as the cover."""
    if not hidden_text:
        return cover
    binary = ''.join(format(ord(c), '08b') for c in hidden_text.encode('utf-8').decode('utf-8'))
    zero_width_mapping = {'0': '\u200b', '1': '\u200c'}
    hidden_unicode = ''.join(zero_width_mapping[bit] for bit in binary)
    return cover + hidden_unicode

def decode_message(encoded_text):
    """Extract any hidden zero-width-encoded text from a string."""
    if not encoded_text:
        return ""
    zero_width_chars = [c for c in encoded_text if c in ('\u200b', '\u200c')]
    if not zero_width_chars:
        return "No hidden message detected."

    reverse_mapping = {'\u200b': '0', '\u200c': '1'}
    binary = ''.join(reverse_mapping[c] for c in zero_width_chars)

    # Decode as UTF-8 bytes so multi-byte characters (emoji, accents, etc.) work
    byte_chunks = [binary[i:i+8] for i in range(0, len(binary), 8)]
    try:
        raw_bytes = bytes(int(b, 2) for b in byte_chunks if len(b) == 8)
        return raw_bytes.decode('utf-8')
    except (ValueError, UnicodeDecodeError):
        return "[!] Corrupted or non-text payload detected."

# --- Cross-platform clipboard handling ---
def copy_to_clipboard(text):
    """
    Try, in order:
      1. termux-clipboard-set (if present, e.g. Termux with termux-api installed)
      2. wl-copy (Wayland, common on some Kali/Linux desktops)
      3. xclip (X11, common on Kali Linux)
      4. xsel (X11 fallback)
      5. pbcopy (macOS, just in case)
      6. pyperclip (cross-platform python lib, if installed)
    Falls back to printing the payload for manual copy.
    """
    candidates = [
        (['termux-clipboard-set'], None),
        (['wl-copy'], None),
        (['xclip', '-selection', 'clipboard'], None),
        (['xsel', '--clipboard', '--input'], None),
        (['pbcopy'], None),
    ]

    for cmd, _ in candidates:
        exe = shutil.which(cmd[0])
        if exe:
            try:
                proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
                proc.communicate(input=text.encode('utf-8'))
                if proc.returncode == 0:
                    print(f"\n\033[92m[✓] Copied to clipboard using '{cmd[0]}'.\033[0m")
                    return
            except Exception:
                continue

    # Try pyperclip as a last automated option
    try:
        import pyperclip
        pyperclip.copy(text)
        print("\n\033[92m[✓] Copied to clipboard using pyperclip.\033[0m")
        return
    except Exception:
        pass

    # Nothing worked — manual fallback
    print("\n\033[91m[!] No clipboard tool found on this system.\033[0m")
    print("\033[93m[!] Install one of the following for auto-copy:\033[0m")
    print("    Termux:      pkg install termux-api")
    print("    Kali/Linux:  sudo apt install xclip   (or xsel / wl-clipboard)")
    print("    Any OS:      pip install pyperclip")
    print("\033[93m[!] Payload (copy manually):\033[0m\n")
    print(f"> {text} <")

# --- Main Interface ---
def main():
    show_banner()

    while True:
        print("\033[94m[1] Encode Message into Emoji/Text")
        print("[2] Decode Message from Emoji/Text")
        print("[0] Exit\033[0m")
        choice = input("\033[97mCode-X > \033[0m").strip()

        if choice == '1':
            print("\n\033[95m--- ENCODER ---\033[0m")
            secret_msg = input("\033[97mEnter the secret message: \033[0m")
            emoji_cover = input("\033[97mEnter your cover text/emoji (e.g. 😀): \033[0m")

            result = encode_message(emoji_cover, secret_msg)
            animate_text("\n\033[93m[+] Injecting payload...\033[0m", 0.05)
            copy_to_clipboard(result)
            print()

        elif choice == '2':
            print("\n\033[95m--- DECODER ---\033[0m")
            target_emoji = input("\033[97mPaste the emoji/text payload here: \033[0m")

            animate_text("\n\033[93m[+] Extracting zero-width characters...\033[0m", 0.05)
            result = decode_message(target_emoji)

            print("\n\033[92m[✓] Decoded Message:\033[0m")
            print(f"\033[97m{result}\033[0m\n")

        elif choice == '0':
            print("\n\033[91mShutting down Code-X... Goodbye!\033[0m")
            break
        else:
            print("\n\033[91m[!] Invalid choice. Try again.\033[0m\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n\033[91m[!] Process interrupted. Exiting Code-X...\033[0m")
        sys.exit()
