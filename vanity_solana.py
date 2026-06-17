import os
import sys
import time
import base58
import threading
from solders.keypair import Keypair
from flask import Flask

app = Flask(__name__)
TARGET_PREFIX = "GVyByL"
TARGET_SUFFIX = "Cpap"
MAX_ATTEMPTS = 1000000
FOUND = False
WALLET_DATA = {}

def generate_vanity():
    global FOUND, WALLET_DATA
    print(f"[*] Aranıyor: '{TARGET_PREFIX}' ile başlayıp '{TARGET_SUFFIX}' ile biten...")
    start_time = time.time()
    attempt = 0
    
    while attempt < MAX_ATTEMPTS and not FOUND:
        attempt += 1
        keypair = Keypair()
        address = str(keypair.pubkey())
        
        if address.startswith(TARGET_PREFIX) and address.endswith(TARGET_SUFFIX):
            elapsed = time.time() - start_time
            private_key = base58.b58encode(bytes(keypair.secret_key())).decode()
            FOUND = True
            WALLET_DATA = {
                "address": address,
                "private_key": private_key,
                "attempts": attempt,
                "time": f"{elapsed:.2f} saniye"
            }
            print("\n" + "="*50)
            print(f"[✓] BULUNDU! ({attempt} denemede, {elapsed:.2f}s)")
            print(f"[✓] Adres: {address}")
            print(f"[✓] Özel Anahtar: {private_key}")
            print("="*50)
            with open("found_wallet.txt", "w") as f:
                f.write(f"Adres: {address}\nÖzel Anahtar: {private_key}\nDeneme: {attempt}\nSüre: {elapsed:.2f}s\n")
            print("[+] found_wallet.txt kaydedildi.")
            return
            
        if attempt % 10000 == 0:
            print(f"[*] {attempt} deneme oldu, aranıyor...")
    
    if not FOUND:
        print(f"[!] {MAX_ATTEMPTS} denemede bulunamadı.")

@app.route('/')
def home():
    if FOUND:
        return f"""
        <h2>✅ Bulundu!</h2>
        <p><b>Adres:</b> {WALLET_DATA['address']}</p>
        <p><b>Özel Anahtar:</b> {WALLET_DATA['private_key']}</p>
        <p><b>Deneme:</b> {WALLET_DATA['attempts']}</p>
        <p><b>Süre:</b> {WALLET_DATA['time']}</p>
        """
    else:
        return "<h2>⏳ Aranıyor...</h2><p>Henüz uygun adres bulunamadı. Logları kontrol et.</p>"

if __name__ == "__main__":
    # Anahtar arayıcıyı arka planda başlat
    thread = threading.Thread(target=generate_vanity)
    thread.daemon = True
    thread.start()
    
    # Flask sunucusunu başlat (Render'ın beklediği şey bu)
    app.run(host='0.0.0.0', port=10000)
