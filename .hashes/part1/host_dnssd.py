from zeroconf import ServiceInfo, Zeroconf
import socket
import os
import time

def ipp_yazici_servisi_olustur():
    # TCP üzerinden IPP (standart IPP servisi)
    servis_turu = "_ipp._tcp.local."
    servis_adi = "Acme Laser Pro._ipp._tcp.local."
    
    ip_adresi = socket.inet_aton("10.0.0.3")  # Yazıcınızın IP'si (veya yerel için 127.0.0.1 kullanın)
    port = 631  # Standart IPP portu
    
    # IPP ve yerelleştirme öznitelikleri ile TXT kayıtları
    txt_kayitlari = {
        "txtvers": "1",                     # TXT kayıt sürümü
        "qtotal": "1",                      # Yazdırma kuyruğu sayısı
        "rp": "printers/acme_laser_pro",   # IPP için kaynak yolu (CUPS /printers/... kullanır)
        "ty-tr": "Acme Lazer Pro",          # Yerelleştirilmiş yazıcı türü (Türkçe)
        "note-tr": "Ofis yazıcısı, 3. Kat, Oda 301",  # Konum (Türkçe)
        "pdl": "application/postscript,application/pdf",  # Desteklenen PDL'ler (PostScript, PDF)
        "adminurl": "http://10.0.0.3:631",  # Yazıcı yönetici URL'si
        "UUID": "545253fb-1337-4d8d-98ed-ab6cd608cea9",  # Benzersiz tanımlayıcı
        "printer-type": "0x800683",  # IPP yazıcı türü (örn. 0x800683 renkli, çift taraflı vb. için)
    }

    servis_bilgisi = ServiceInfo(
        servis_turu,
        servis_adi,
        addresses=[ip_adresi],
        port=port,
        properties=txt_kayitlari,
        server="Acme-Lazer-Pro.local.",  # Yazıcının ana bilgisayar adı
    )
    
    return servis_bilgisi


def main():
    # DNS-SD duyurusu için Zeroconf'u başlat
    zeroconf = Zeroconf()
    servis_bilgisi = ipp_yazici_servisi_olustur()
    
    try:
        print("IPP yazıcı servisi kaydediliyor...")
        zeroconf.register_service(servis_bilgisi)
        print("IPP Yazıcı servisi kaydedildi. Çıkmak için Ctrl+C'ye basın.")

        input("Herhangi bir tuşa basın")
        
    except KeyboardInterrupt:
        print("Servis kaydı siliniyor...")
        zeroconf.unregister_service(servis_bilgisi)
        zeroconf.close()


if __name__ == "__main__":
    main()

