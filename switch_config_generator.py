import customtkinter as ctk
from tkinter import messagebox
import re

# ---------------- Tema Ayarları ----------------
ctk.set_appearance_mode("Dark")  # Başlangıç teması
ctk.set_default_color_theme("blue")

def degistir_tema():
    # Dark ↔ Light geçişi
    if ctk.get_appearance_mode() == "Dark":
        ctk.set_appearance_mode("Light")
    else:
        ctk.set_appearance_mode("Dark")

# ---------------- Config Oluşturma ----------------
def olustur_config():
    # Kullanıcı girişleri
    isim = entry_name.get()
    ip = entry_ip.get()
    mask = entry_mask.get()
    gw = entry_gw.get()
    sifre = entry_pass.get()
    domain = entry_domain.get()
    vlan = entry_vlan.get()
    banner = entry_banner.get()
    timeout = entry_timeout.get()
    ntp = entry_ntp.get()

    # Şifre kontrolü
    if len(sifre) < 8 or not re.search(r"[A-Z]", sifre) or not re.search(r"[a-z]", sifre) or not re.search(r"[0-9]", sifre):
        messagebox.showerror("Hata", "Şifre en az 8 karakter, 1 büyük, 1 küçük ve 1 rakam içermeli!")
        return

    if not timeout:
        timeout = "10"

    # Config oluşturma
    conf = f"""hostname {isim}
!
banner motd #{banner}#
enable secret {sifre}
service password-encryption
no ip domain-lookup
ip domain-name {domain}
crypto key generate rsa modulus 1024
ip ssh version 2
username admin privilege 15 secret {sifre}

interface vlan {vlan}
 ip address {ip} {mask}
 no shutdown

ip default-gateway {gw}
"""

    if ntp:
        conf += f"ntp server {ntp}\n"

    conf += f"""
line vty 0 4
 exec-timeout {timeout} 0
 login local
 transport input ssh
 logging synchronous

line con 0
 exec-timeout {timeout} 0
 login local
 logging synchronous

vlan {vlan}
 no shutdown
end
write memory
"""

    txt_output.delete("1.0", "end")
    txt_output.insert("1.0", conf)

# ---------------- Panoya Kopyalama ----------------
def kopyala():
    window.clipboard_clear()
    window.clipboard_append(txt_output.get("1.0", "end"))
    messagebox.showinfo("Başarılı", "Config panoya kopyalandı!")

# ---------------- Arayüz ----------------
window = ctk.CTk()
window.title("Cisco Switch Config Generator")
window.geometry("700x750")

# Tema değiştir butonu
ctk.CTkButton(window, text="Dark / Light Theme", command=degistir_tema).pack(pady=10)

frame = ctk.CTkFrame(window)
frame.pack(padx=20, pady=20, fill="both", expand=True)

# Giriş alanları
entry_name = ctk.CTkEntry(frame, placeholder_text="Switch Name")
entry_ip = ctk.CTkEntry(frame, placeholder_text="IP Address")
entry_mask = ctk.CTkEntry(frame, placeholder_text="Subnet Mask")
entry_gw = ctk.CTkEntry(frame, placeholder_text="Default Gateway")
entry_pass = ctk.CTkEntry(frame, placeholder_text="Enable Secret Password", show="*")
entry_domain = ctk.CTkEntry(frame, placeholder_text="Domain Name")
entry_vlan = ctk.CTkEntry(frame, placeholder_text="Management VLAN ID")
entry_banner = ctk.CTkEntry(frame, placeholder_text="Banner MOTD")
entry_timeout = ctk.CTkEntry(frame, placeholder_text="Exec Timeout (minutes)")
entry_ntp = ctk.CTkEntry(frame, placeholder_text="NTP Server (optional)")

for e in [entry_name, entry_ip, entry_mask, entry_gw, entry_pass, entry_domain, entry_vlan, entry_banner, entry_timeout, entry_ntp]:
    e.pack(pady=5, padx=10, fill="x")

# Butonlar
ctk.CTkButton(frame, text="Generate Config", command=olustur_config).pack(pady=10)
ctk.CTkButton(frame, text="Copy to Clipboard", command=kopyala).pack(pady=5)

# Config gösterim alanı
txt_output = ctk.CTkTextbox(frame, width=650, height=250)
txt_output.pack(pady=10)

window.mainloop()
