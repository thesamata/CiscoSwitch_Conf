# Cisco Switch Config Generator 🛠️

Bu proje, Python GUI (CustomTkinter) kullanarak Cisco switch’ler için otomatik konfigürasyon dosyası üreten bir uygulamadır. 
Form üzerinden hostname, IP, VLAN ID, domain-name, banner MOTD ve enable secret şifresini girerek hızlıca config oluşturabilirsiniz.

✨ Özellikler:
- Hostname ayarlama
- Banner MOTD ekleme
- Enable secret şifre oluşturma ve şifre karmaşıklığı kontrolü
- Service password-encryption
- IP domain-name ayarı
- SSH yapılandırması (RSA key + SSH version 2)
- Kullanıcı hesabı (admin privilege 15)
- VLAN numarasını değiştirebilme
- Interface VLAN konfigürasyonu
- Default gateway ayarı
- Line VTY 0-4 (SSH) ve Line Console ayarları
- Exec-timeout ayarı
- NTP server ekleyebilme (opsiyonel)
- Config’i panoya kopyalama
- Dark / Light tema desteği
- write memory komutu ile kaydetme

🚀 Kurulum:
1. Python 3.8+ yüklü olmalı
2. Gerekli kütüphaneleri yükleyin:
   pip install -r requirements.txt
3. switch_config_generator.py dosyasını çalıştırın:
   python switch_config_generator.py

🖥️ Kullanım:
1. Form alanlarını doldurun (Hostname, IP, VLAN, vs.)
2. "Generate Config" butonuna basın
3. Oluşturulan konfigürasyon altta görünecek
4. "Copy to Clipboard" ile config’i panoya kopyalayabilirsiniz
5. Dark / Light tema butonu ile arayüz görünümünü değiştirebilirsiniz
