# CUPSHax

Son CUPS güvenlik açığı için hızlı bir kavram kanıtı. Bunu çok daha fazla temizlemeyi planlıyordum, ancak ambargo beklenenden çok daha erken kaldırıldı, bu yüzden kod biraz aceleye geldi.

[Tüm teknik detaylar için aslında Evilsocket'in yazısını okumalısınız](https://www.evilsocket.net/2024/09/26/Attacking-UNIX-systems-via-CUPS-Part-I/).

Bu exploit, [OpenPrinting CUPS deposundaki bu commit'i](https://github.com/OpenPrinting/cups/commit/8361420cbbfa2e729545c4c537c49fc6322c9631) fark ettikten sonra yazıldı. Muhtemelen daha temiz enjeksiyon noktaları vardır.

Bu PoC, dns-sd yazıcı keşfini kullanır, bu nedenle hedefin yayın mesajını alabilmesi, yani aynı ağda olması gerekir.

## Kullanım

Exploit, `zeroconf` ve `ippserver` kullanır, ikisi de pip ile kurulabilir.

```
kullanım: cupshax.py [-h] [--name AD] --ip IP [--command KOMUT] [--port PORT] [--base64 | --no-base64]

Bir CUPS PPD enjeksiyon PoC'si

seçenekler:
  -h, --help            yardım mesajını göster ve çık
  --name AD             Kullanılacak ad (varsayılan: RCE Printer)
  --ip IP               Bu betiği çalıştıran makinenin IP adresi
  --command KOMUT       Çalıştırılacak komut (varsayılan: 'touch /tmp/pwn')
  --port PORT           Bağlanılacak port (varsayılan: 8631)
  --base64, --no-base64
                        Komutu base64 ile sarmalayın (varsayılan: etkin)
```

Örneğin:
```bash
python cupshax.py --name "PDF'ye Yazdır (Renkli)" \
                  --command "id>/tmp/pwn" \
                  --ip 10.0.0.3
```

## Güvenlik Açığının Kullanımı

Bu güvenlik açığı, CUPS (Common UNIX Printing System) sistemindeki bir zafiyeti kullanarak uzaktan kod çalıştırmayı mümkün kılar. İşte adım adım nasıl kullanılacağı:

1. **Gerekli Bağımlılıkları Yükleme:**
   Öncelikle, gerekli Python kütüphanelerini yükleyin:
   ```
   pip install zeroconf ippserver
   ```

2. **Saldırı Makinesini Hazırlama:**
   - Saldırı makinenizin IP adresini öğrenin (örneğin, `ifconfig` veya `ip addr` komutlarıyla).
   - Hedef ağda olduğunuzdan emin olun.

3. **Exploit Kodunu Çalıştırma:**
   `cupshax.py` dosyasını aşağıdaki gibi çalıştırın:
   ```
   python cupshax.py --name "Sahte Yazıcı" --ip SALDIRGAN_IP --command "ÇALIŞTIRMAK_İSTEDİĞİNİZ_KOMUT"
   ```
   Örnek:
   ```
   python cupshax.py --name "PDF Yazıcı" --ip 192.168.1.100 --command "whoami > /tmp/hacked.txt"
   ```

4. **Saldırının İşleyişi:**
   - Betik, belirtilen IP ve port üzerinde sahte bir IPP (Internet Printing Protocol) sunucusu başlatır.
   - Aynı zamanda, bu sahte yazıcıyı ağda duyurmak için DNS-SD (DNS Service Discovery) kullanır.
   - Hedef sistemdeki CUPS servisi, bu sahte yazıcıyı otomatik olarak keşfeder ve yapılandırmaya çalışır.
   - Yapılandırma sırasında, CUPS bizim sağladığımız kötü amaçlı PPD (PostScript Printer Description) dosyasını işler.
   - PPD dosyasındaki enjekte edilmiş komut, hedef sistemde çalıştırılır.

5. **Saldırının Sonuçları:**
   - Çalıştırılan komut, hedef sistemde CUPS servisinin yetkileriyle işletilir (genellikle root).
   - Komutun çıktısı veya etkisi, hedef sistemde görülebilir (örneğin, `/tmp` dizininde oluşturulan dosyalar).

6. **Güvenlik ve Etik Uyarılar:**
   - Bu aracı yalnızca yasal ve etik sınırlar içerisinde, izin verilen sistemlerde kullanın.
   - Gerçek dünya senaryolarında bu tür açıkları kullanmak yasadışı olabilir ve ciddi sonuçlar doğurabilir.
   - Bu PoC, güvenlik araştırmacıları ve sistem yöneticileri için eğitim ve savunma amaçlı tasarlanmıştır.

7. **Korunma Yöntemleri:**
   - CUPS sistemini en son sürüme güncelleyin.
   - Güvenilir olmayan ağlarda otomatik yazıcı keşfini devre dışı bırakın.
   - Ağ güvenlik duvarlarını ve segmentasyonunu güçlendirin.
   - CUPS servisini mümkün olan en düşük yetkilerle çalıştırın.

Bu güvenlik açığı, ağ güvenliğinin önemini ve güncel olmayan sistemlerin risklerini göstermektedir. Sistem yöneticileri, bu tür zafiyetlere karşı her zaman tetikte olmalı ve sistemlerini düzenli olarak güncellemelidir.