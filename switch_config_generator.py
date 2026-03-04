import customtkinter as ctk
from tkinter import messagebox, filedialog
import re
import ipaddress

# ---------------- Tema Ayarları ----------------
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

def degistir_tema():
    if ctk.get_appearance_mode() == "Dark":
        ctk.set_appearance_mode("Light")
    else:
        ctk.set_appearance_mode("Dark")

# ---------------- Doğrulama Fonksiyonları ----------------
def ip_gecerli_mi(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

# ---------------- Config Oluşturma ----------------
def olustur_config():
    # Kullanıcı girişleri
    isim = entry_name.get().strip()
    ip = entry_ip.get().strip()
    mask = entry_mask.get().strip()
    gw = entry_gw.get().strip()
    sifre = entry_pass.get().strip()
    domain = entry_domain.get().strip()
    vlan = entry_vlan.get().strip()
    banner = entry_banner.get().strip()
    timeout = entry_timeout.get().strip()
    ntp = entry_ntp.get().strip()

    # Boş alan kontrolü
    if not all([isim, ip, mask, gw, sifre, domain, vlan]):
        messagebox.showerror("Hata", "Lütfen tüm zorunlu alanları doldurun!")
        return

    # IP ve Mask kontrolü
    if not ip_gecerli_mi(ip):
        messagebox.showerror("Hata", f"Geçersiz IP adresi: {ip}")
        return
    if not ip_gecerli_mi(mask) and not mask.isdigit(): # Subnet mask genelde IP formatındadır
         if not (mask.startswith("/") or ip_gecerli_mi(mask)):
            messagebox.showerror("Hata", f"Geçersiz Alt Ağ Maskesi: {mask}")
            return

    # VLAN kontrolü
    if not vlan.isdigit() or not (1 <= int(vlan) <= 4094):
        messagebox.showerror("Hata", "VLAN ID 1 ile 4094 arasında bir sayı olmalıdır!")
        return

    # Şifre kontrolü
    if len(sifre) < 8 or not re.search(r"[A-Z]", sifre) or not re.search(r"[a-z]", sifre) or not re.search(r"[0-9]", sifre):
        messagebox.showerror("Hata", "Şifre en az 8 karakter, 1 büyük, 1 küçük ve 1 rakam içermeli!")
        return

    if not timeout:
        timeout = "10"

    # Config oluşturma
    conf = f"""! --- Cisco Switch Configuration for {isim} ---
hostname {isim}
!
banner motd #{banner if banner else "Unauthorized Access Only!"}#
enable secret {sifre}
service password-encryption
no ip domain-lookup
ip domain-name {domain}
crypto key generate rsa modulus 1024
ip ssh version 2
username admin privilege 15 secret {sifre}
!
vlan {vlan}
 name Management_VLAN
 no shutdown
!
interface vlan {vlan}
 ip address {ip} {mask}
 no shutdown
!
ip default-gateway {gw}
"""

    if ntp:
        conf += f"ntp server {ntp}\n"

    conf += f"""!
line vty 0 4
 exec-timeout {timeout} 0
 login local
 transport input ssh
 logging synchronous
!
line con 0
 exec-timeout {timeout} 0
 login local
 logging synchronous
!
end
write memory
"""

    txt_output.delete("1.0", "end")
    txt_output.insert("1.0", conf)

# ---------------- Dosya ve İşlemler ----------------
def kopyala():
    window.clipboard_clear()
    window.clipboard_append(txt_output.get("1.0", "end-1c"))
    messagebox.showinfo("Başarılı", "Config panoya kopyalandı!")

def dosya_kaydet():
    config_text = txt_output.get("1.0", "end-1c")
    if not config_text.strip():
        messagebox.showwarning("Uyarı", "Önce config üretmelisiniz!")
        return
    
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt"), ("Config files", "*.cfg"), ("All files", "*.*")],
        initialfile=f"{entry_name.get()}_config.txt"
    )
    if file_path:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(config_text)
        messagebox.showinfo("Başarılı", "Dosya başarıyla kaydedildi!")

# ---------------- Arayüz ----------------
window = ctk.CTk()
window.title("Cisco Switch Config Generator Pro")
window.geometry("850x900")

# Üst Başlık ve Tema Butonu
header_frame = ctk.CTkFrame(window, fg_color="transparent")
header_frame.pack(pady=20, fill="x")

ctk.CTkLabel(header_frame, text="Cisco Switch Config Generator", font=("Arial", 24, "bold")).pack()
ctk.CTkButton(header_frame, text="Görünüm Modu Değiştir (Dark/Light)", command=degistir_tema, width=250).pack(pady=10)

input_frame = ctk.CTkFrame(window)
input_frame.pack(padx=40, pady=10, fill="x")

# Grid Sütunlarını Ortalama
input_frame.columnconfigure((0, 1), weight=1)

# Giriş alanları (Merkezi Hizalama için sticky="" yerine paddings kullanıyoruz)
# Sütun 0
ctk.CTkLabel(input_frame, text="Hostname:").grid(row=0, column=0, padx=20, pady=(15, 0))
entry_name = ctk.CTkEntry(input_frame, placeholder_text="Örn: Switch01", width=320)
entry_name.grid(row=1, column=0, padx=20, pady=5)

ctk.CTkLabel(input_frame, text="IP Adresi:").grid(row=2, column=0, padx=20, pady=(10, 0))
entry_ip = ctk.CTkEntry(input_frame, placeholder_text="Örn: 192.168.1.2", width=320)
entry_ip.grid(row=3, column=0, padx=20, pady=5)

ctk.CTkLabel(input_frame, text="Alt Ağ Maskesi:").grid(row=4, column=0, padx=20, pady=(10, 0))
entry_mask = ctk.CTkEntry(input_frame, placeholder_text="Örn: 255.255.255.0", width=320)
entry_mask.grid(row=5, column=0, padx=20, pady=5)

ctk.CTkLabel(input_frame, text="Default Gateway:").grid(row=6, column=0, padx=20, pady=(10, 0))
entry_gw = ctk.CTkEntry(input_frame, placeholder_text="Örn: 192.168.1.1", width=320)
entry_gw.grid(row=7, column=0, padx=20, pady=5)

ctk.CTkLabel(input_frame, text="Cihaz Şifresi:").grid(row=8, column=0, padx=20, pady=(10, 0))
entry_pass = ctk.CTkEntry(input_frame, placeholder_text="En az 8 karakter, A-a-1", show="*", width=320)
entry_pass.grid(row=9, column=0, padx=20, pady=(5, 20))

# Sütun 1
ctk.CTkLabel(input_frame, text="Domain Name:").grid(row=0, column=1, padx=20, pady=(15, 0))
entry_domain = ctk.CTkEntry(input_frame, placeholder_text="Örn: sirket.local", width=320)
entry_domain.grid(row=1, column=1, padx=20, pady=5)

ctk.CTkLabel(input_frame, text="Management VLAN ID:").grid(row=2, column=1, padx=20, pady=(10, 0))
entry_vlan = ctk.CTkEntry(input_frame, placeholder_text="Örn: 10", width=320)
entry_vlan.grid(row=3, column=1, padx=20, pady=5)

ctk.CTkLabel(input_frame, text="Banner MOTD:").grid(row=4, column=1, padx=20, pady=(10, 0))
entry_banner = ctk.CTkEntry(input_frame, placeholder_text="Giriş Mesajı", width=320)
entry_banner.grid(row=5, column=1, padx=20, pady=5)

ctk.CTkLabel(input_frame, text="Exec Timeout (dk):").grid(row=6, column=1, padx=20, pady=(10, 0))
entry_timeout = ctk.CTkEntry(input_frame, placeholder_text="Varsayılan: 10", width=320)
entry_timeout.grid(row=7, column=1, padx=20, pady=5)

ctk.CTkLabel(input_frame, text="NTP Server (Opsiyonel):").grid(row=8, column=1, padx=20, pady=(10, 0))
entry_ntp = ctk.CTkEntry(input_frame, placeholder_text="Örn: 1.1.1.1", width=320)
entry_ntp.grid(row=9, column=1, padx=20, pady=(5, 20))

# Butonlar Alanı
button_frame = ctk.CTkFrame(window, fg_color="transparent")
button_frame.pack(pady=15)

ctk.CTkButton(button_frame, text="Config Üret", command=olustur_config, width=160, height=40, font=("Arial", 13, "bold"), fg_color="#2c3e50", hover_color="#34495e").pack(side="left", padx=10)
ctk.CTkButton(button_frame, text="Kopyala", command=kopyala, width=160, height=40, font=("Arial", 13, "bold")).pack(side="left", padx=10)
ctk.CTkButton(button_frame, text="Dosyaya Kaydet", command=dosya_kaydet, width=160, height=40, font=("Arial", 13, "bold"), fg_color="#27ae60", hover_color="#2ecc71").pack(side="left", padx=10)

# Çıktı Alanı
output_label = ctk.CTkLabel(window, text="Oluşturulan Konfigürasyon:", font=("Arial", 14, "italic"))
output_label.pack(pady=(10, 0))

txt_output = ctk.CTkTextbox(window, width=780, height=300, font=("Courier New", 13), border_width=2)
txt_output.pack(padx=30, pady=(5, 30), fill="both", expand=True)

window.mainloop()
