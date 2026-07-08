#!/usr/bin/env python3
"""
Code-X — zero-width Unicode steganography tool (CLI + Web, one file)
Developer: Yoseph Alganeh

Encodes/decodes hidden text inside an emoji (or any string) using
invisible zero-width characters (U+200B / U+200C).

Two ways to use it, both in this one script:
  [1] Encode  - CLI, prints the payload directly (no clipboard dependency)
  [2] Decode  - CLI
  [3] Web UI  - starts a local server at http://127.0.0.1:5000 with a
                browser Copy button. Recommended on mobile/Termux, since
                terminal copy/paste often drops invisible characters.
"""
import os
import sys
import time

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
    time.sleep(0.3)
    print()

# --- Steganography Core (shared by both CLI and Web) ---
def encode_message(cover, hidden_text):
    """Hide `hidden_text` inside `cover` using zero-width chars."""
    if not hidden_text:
        return cover
    utf8_bytes = hidden_text.encode('utf-8')
    binary = ''.join(format(b, '08b') for b in utf8_bytes)
    mapping = {'0': '\u200b', '1': '\u200c'}
    return cover + ''.join(mapping[bit] for bit in binary)

def decode_message(encoded_text):
    """Extract any hidden zero-width-encoded text from a string."""
    if not encoded_text:
        return ""
    zero_width_chars = [c for c in encoded_text if c in ('\u200b', '\u200c')]
    if not zero_width_chars:
        return "No hidden message detected."
    reverse = {'\u200b': '0', '\u200c': '1'}
    binary = ''.join(reverse[c] for c in zero_width_chars)
    byte_chunks = [binary[i:i+8] for i in range(0, len(binary), 8)]
    try:
        raw = bytes(int(b, 2) for b in byte_chunks if len(b) == 8)
        return raw.decode('utf-8')
    except (ValueError, UnicodeDecodeError):
        return "[!] Corrupted or non-text payload detected."

# --- Web Interface ---
WEB_PAGE = """
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Code-X</title>
<style>
  body { background:#0d0d0d; color:#e6e6e6; font-family: monospace; padding:16px; }
  h1 { color:#39ff14; }
  .credit { color:#5ad1ff; margin-bottom:20px; }
  input[type=text] {
    width:100%; box-sizing:border-box; background:#111; color:#eee;
    border:1px solid #333; padding:8px; font-family:monospace; font-size:16px;
  }
  button {
    background:#1e90ff; color:#fff; border:none; padding:10px 16px;
    margin-top:8px; border-radius:4px; font-size:15px;
  }
  .copybtn { background:#39ff14; color:#000; }
  section { border:1px solid #333; border-radius:6px; padding:14px; margin-bottom:20px; }
  label { display:block; margin:10px 0 4px; color:#aaa; }
  .result { background:#111; border:1px solid #333; padding:10px; margin-top:10px;
            word-break:break-all; font-size:20px; }
  .msg { color:#39ff14; margin-top:8px; }
</style>
</head>
<body>
  <h1>Code-X</h1>
  <div class="credit">Developer: Yoseph Alganeh</div>

  <section>
    <h2>Encode</h2>
    <form method="post" action="/encode">
      <label>Secret message</label>
      <input type="text" name="secret" required>
      <label>Cover emoji / text</label>
      <input type="text" name="cover" placeholder="😀" required>
      <button type="submit">Encode</button>
    </form>
    {% if encoded is not none %}
      <div class="result" id="encoded-result">{{ encoded }}</div>
      <button class="copybtn" onclick="copyResult()">Copy to clipboard</button>
      <div class="msg" id="copy-msg"></div>
    {% endif %}
  </section>

  <section>
    <h2>Decode</h2>
    <form method="post" action="/decode">
      <label>Paste emoji / text payload</label>
      <input type="text" name="payload" required>
      <button type="submit">Decode</button>
    </form>
    {% if decoded is not none %}
      <div class="result">{{ decoded }}</div>
    {% endif %}
  </section>

<script>
function copyResult() {
  const text = document.getElementById('encoded-result').innerText;
  navigator.clipboard.writeText(text).then(function() {
    document.getElementById('copy-msg').innerText = "✓ Copied exactly, invisible characters included.";
  }, function() {
    document.getElementById('copy-msg').innerText = "Copy failed — long-press the box above and copy manually.";
  });
}
</script>
</body>
</html>
"""

def run_web_interface():
    try:
        from flask import Flask, request, render_template_string
    except ImportError:
        print("\n\033[91m[!] Flask is not installed.\033[0m")
        print("\033[93m[!] Install it with: pip install flask\033[0m\n")
        return

    app = Flask(__name__)

    @app.route("/", methods=["GET"])
    def index():
        return render_template_string(WEB_PAGE, encoded=None, decoded=None)

    @app.route("/encode", methods=["POST"])
    def encode_route():
        secret = request.form.get("secret", "")
        cover = request.form.get("cover", "")
        result = encode_message(cover, secret)
        return render_template_string(WEB_PAGE, encoded=result, decoded=None)

    @app.route("/decode", methods=["POST"])
    def decode_route():
        payload = request.form.get("payload", "")
        result = decode_message(payload)
        return render_template_string(WEB_PAGE, encoded=None, decoded=result)

    print("\n\033[92m[+] Code-X web server starting...\033[0m")
    print("\033[93m[+] Open this in your browser (keep this terminal open):\033[0m")
    print("    \033[96mhttp://127.0.0.1:5000\033[0m\n")
    print("\033[93m[!] Press CTRL+C here to stop the server and return to the menu.\033[0m\n")
    try:
        app.run(host="127.0.0.1", port=5000)
    except KeyboardInterrupt:
        pass

# --- Main Interface ---
def main():
    show_banner()

    while True:
        print("\033[94m[1] Encode Message into Emoji/Text (CLI)")
        print("[2] Decode Message from Emoji/Text (CLI)")
        print("[3] Launch Web Interface (recommended for copy/paste)")
        print("[0] Exit\033[0m")
        choice = input("\033[97mCode-X > \033[0m").strip()

        if choice == '1':
            print("\n\033[95m--- ENCODER ---\033[0m")
            secret_msg = input("\033[97mEnter the secret message: \033[0m")
            emoji_cover = input("\033[97mEnter your cover text/emoji (e.g. 😀): \033[0m")

            result = encode_message(emoji_cover, secret_msg)
            animate_text("\n\033[93m[+] Injecting payload...\033[0m", 0.05)
            print("\n\033[92m[✓] Encoded payload:\033[0m\n")
            print(f"> {result} <\n")
            print("\033[93m[i] Tip: if copying this from the terminal loses the hidden")
            print("    text, use option [3] Web Interface instead.\033[0m\n")

        elif choice == '2':
            print("\n\033[95m--- DECODER ---\033[0m")
            target_emoji = input("\033[97mPaste the emoji/text payload here: \033[0m")

            animate_text("\n\033[93m[+] Extracting zero-width characters...\033[0m", 0.05)
            result = decode_message(target_emoji)

            print("\n\033[92m[✓] Decoded Message:\033[0m")
            print(f"\033[97m{result}\033[0m\n")

        elif choice == '3':
            run_web_interface()
            print("\n\033[92m[+] Web server stopped. Back to main menu.\033[0m\n")

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
