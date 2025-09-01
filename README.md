# Cisco Switch Config Generator 🛠️

Bu proje, **Python GUI (tkinter)** kullanarak Cisco switch’ler için otomatik konfigürasyon dosyası üreten bir uygulamadır.  
Form üzerinden hostname, IP, VLAN ID, domain-name, banner motd ve enable secret şifresini girerek hızlıca config oluşturabilirsiniz.  

---

## ✨ Özellikler
- Hostname ayarlama
- Banner MOTD ekleme
- Enable secret şifre ayarlama
- Service password-encryption
- IP domain-name
- SSH (RSA key + SSH version 2)
- Kullanıcı hesabı (admin privilege 15)
- VLAN numarasını değiştirebilme
- Interface VLAN konfigürasyonu
- Default gateway ayarı
- Line VTY 0-4 (SSH) ve Line Console ayarları
- Hazır `write memory` komutu

---

## 🚀 Kurulum
1. Python 3.8+ kurulu olmalı  
2. Gerekli kütüphaneleri yükle:
   ```bash
   pip install -r requirements.txt
