#!/usr/bin/env python3
import os
import sys
import time
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
    print("\033[96m" + " " * 12 + "Developer: Yoseph Alganeh\033[0m\n")
    animate_text("\033[93m[+] Booting Code-X Engine...\033[0m", 0.04)
    animate_text("\033[93m[+] Initializing Zero-Width Subroutines...\033[0m", 0.02)
    time.sleep(0.5)
    print("\n")

# --- Steganography Core ---
def encode_message(emoji, hidden_text):
    if not hidden_text:
        return emoji
    binary = ''.join(format(ord(c), '08b') for c in hidden_text)
    zero_width_mapping = {'0': '\u200b', '1': '\u200c'}
    hidden_unicode = ''.join(zero_width_mapping[bit] for bit in binary)
    return emoji + hidden_unicode

def decode_message(encoded_text):
    if not encoded_text:
        return ""
    zero_width_chars = [c for c in encoded_text if c in ('\u200b', '\u200c')]
    if not zero_width_chars:
        return "No hidden message detected."
    
    reverse_mapping = {'\u200b': '0', '\u200c': '1'}
    binary = ''.join(reverse_mapping[c] for c in zero_width_chars)
    
    decoded_text = ""
    for i in range(0, len(binary), 8):
        byte = binary[i:i+8]
        if len(byte) == 8:
            decoded_text += chr(int(byte, 2))
    return decoded_text

# --- Termux Clipboard Integration ---
def copy_to_clipboard(text):
    try:
        # Calls native termux-api to copy to Android clipboard
        process = subprocess.Popen(['termux-clipboard-set'], stdin=subprocess.PIPE)
        process.communicate(input=text.encode('utf-8'))
        print("\n\033[92m[✓] Success! The payload has been copied to your clipboard.\033[0m")
    except FileNotFoundError:
        print("\n\033[91m[!] Termux-API not found. Could not auto-copy.\033[0m")
        print("\033[93m[!] Please run: pkg install termux-api\033[0m")
        print("\033[93m[!] You can manually copy the output below:\033[0m\n")
        print(f"> {text} <")

# --- Main Interface ---
def main():
    show_banner()
    
    while True:
        print("\033[94m[1] Encode Message into Emoji")
        print("[2] Decode Message from Emoji")
        print("[0] Exit\033[0m")
        choice = input("\033[97mCode-X > \033[0m").strip()
        
        if choice == '1':
            print("\n\033[95m--- ENCODER ---\033[0m")
            secret_msg = input("\033[97mEnter the secret message: \033[0m")
            emoji_cover = input("\033[97mEnter your cover emoji (e.g. 😀): \033[0m")
            
            result = encode_message(emoji_cover, secret_msg)
            animate_text("\n\033[93m[+] Injecting payload...\033[0m", 0.05)
            copy_to_clipboard(result)
            print("\n")
            
        elif choice == '2':
            print("\n\033[95m--- DECODER ---\033[0m")
            target_emoji = input("\033[97mPaste the emoji payload here: \033[0m")
            
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
