import os
import sys
import time
import base58
from solana.keypair import Keypair

# Hedef kalıplar (burayı değiştir!)
TARGET_PREFIX = "GVyByL"   # Başlangıç
TARGET_SUFFIX = "Cpap"     # Bitiş
MAX_ATTEMPTS = 1000000     # Kaç deneme yapacağını sınırla (1 milyon)

def generate_vanity():
    print(f"[*] Hedef: '{TARGET_PREFIX}' ile başlayıp '{TARGET_SUFFIX}' ile biten adres aranıyor...")
    print(f"[*] En fazla {MAX_ATTEMPTS} deneme yapılacak.")
    
    start_time = time.time()
    attempt = 0
    
    while attempt < MAX_ATTEMPTS:
        attempt += 1
        # Yeni anahtar çifti oluştur
        keypair = Keypair()
        address = str(keypair.pubkey)
        
        # Kontrol et
        if address.startswith(TARGET_PREFIX) and address.endswith(TARGET_SUFFIX):
            elapsed = time.time() - start_time
            print("\n" + "="*50)
            print(f"[✓] BAŞARILI! ({attempt} denemede, {elapsed:.2f} saniye)")
            print(f"[✓] Adres: {address}")
            private_key = base58.b58encode(keypair.secret_key).decode()
            print(f"[✓] Özel Anahtar (Base58): {private_key}")
            print("="*50)
            
            # Dosyaya kaydet
            with open("found_wallet.txt", "w") as f:
                f.write(f"Adres: {address}\n")
                f.write(f"Özel Anahtar: {private_key}\n")
                f.write(f"Deneme sayısı: {attempt}\n")
                f.write(f"Süre: {elapsed:.2f} saniye\n")
            print("[+] found_wallet.txt dosyasına kaydedildi.")
            return True
            
        # Her 10000 denemede bir durum göster
        if attempt % 10000 == 0:
            print(f"[*] {attempt} deneme oldu, aranıyor...")
    
    print(f"[!] {MAX_ATTEMPTS} deneme yapıldı ama uygun adres bulunamadı.")
    return False

if __name__ == "__main__":
    try:
        generate_vanity()
    except KeyboardInterrupt:
        print("\n[!] Kullanıcı tarafından durduruldu.")
    except Exception as e:
        print(f"[!] Hata oluştu: {e}")
        sys.exit(1)
