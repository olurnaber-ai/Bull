import os
import sys
import time
import base58
from solana.keypair import Keypair  # Bu import bazı sürümlerde sorun çıkarıyor

# Alternatif import (daha yeni sürümler için)
try:
    from solana.keypair import Keypair
except ImportError:
    # Eğer yukarıdaki olmazsa, bu alternatifi dene
    from solders.keypair import Keypair

# Hedef kalıplar
TARGET_PREFIX = "GVyByL"
TARGET_SUFFIX = "Cpap"
MAX_ATTEMPTS = 500000

def generate_vanity():
    print(f"[*] Hedef: '{TARGET_PREFIX}' ile başlayıp '{TARGET_SUFFIX}' ile biten adres aranıyor...")
    print(f"[*] En fazla {MAX_ATTEMPTS} deneme yapılacak.")
    
    start_time = time.time()
    attempt = 0
    
    while attempt < MAX_ATTEMPTS:
        attempt += 1
        keypair = Keypair()
        address = str(keypair.pubkey())
        
        if address.startswith(TARGET_PREFIX) and address.endswith(TARGET_SUFFIX):
            elapsed = time.time() - start_time
            print("\n" + "="*50)
            print(f"[✓] BAŞARILI! ({attempt} denemede, {elapsed:.2f} saniye)")
            print(f"[✓] Adres: {address}")
            private_key = base58.b58encode(bytes(keypair.secret_key())).decode()
            print(f"[✓] Özel Anahtar: {private_key}")
            print("="*50)
            
            with open("found_wallet.txt", "w") as f:
                f.write(f"Adres: {address}\n")
                f.write(f"Özel Anahtar: {private_key}\n")
                f.write(f"Deneme: {attempt}\n")
                f.write(f"Süre: {elapsed:.2f} saniye\n")
            print("[+] found_wallet.txt kaydedildi.")
            return True
            
        if attempt % 10000 == 0:
            print(f"[*] {attempt} deneme oldu, aranıyor...")
    
    print(f"[!] {MAX_ATTEMPTS} deneme yapıldı, bulunamadı.")
    return False

if __name__ == "__main__":
    try:
        generate_vanity()
    except KeyboardInterrupt:
        print("\n[!] Durduruldu.")
    except Exception as e:
        print(f"[!] Hata: {e}")
        sys.exit(1)
