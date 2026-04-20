import customtkinter as ctk
from tkinter import messagebox, filedialog
import re
import ipaddress
import secrets
import string

# ---------------- Tema ve Renkler ----------------
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class CiscoConfigApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Cisco Switch Config Generator")
        self.geometry("1100x780")

        # Değişkenler
        self.appearance_mode = "Dark"
        self.setup_variables()
        
        # UI Bileşenlerini Oluştur
        self.create_layout()
        
    def setup_variables(self):
        """Uygulama içinde kullanılan tüm kontrol değişkenlerini tanımlar."""
        self.check_ssh_only = ctk.BooleanVar(value=True)
        self.check_ssh_acl = ctk.BooleanVar()
        self.check_port_security = ctk.BooleanVar()
        self.check_bpdu_guard = ctk.BooleanVar()
        self.check_ntp_enable = ctk.BooleanVar()
        self.check_dhcp_snooping = ctk.BooleanVar()
        self.check_arp_inspection = ctk.BooleanVar()
        self.check_static_binding = ctk.BooleanVar()

    def create_layout(self):
        """Ana ekran düzenini oluşturur."""
        # Grid konfigürasyonu
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ---- Sidebar (Sol Menü) ----
        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="CISCO GEN", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.sidebar_button_gen = ctk.CTkButton(self.sidebar_frame, text="Config Üret", command=self.olustur_config, fg_color="#1f538d", hover_color="#1a4473")
        self.sidebar_button_gen.grid(row=1, column=0, padx=20, pady=10)

        self.sidebar_button_copy = ctk.CTkButton(self.sidebar_frame, text="Kopyala", command=self.kopyala)
        self.sidebar_button_copy.grid(row=2, column=0, padx=20, pady=10)

        self.sidebar_button_save = ctk.CTkButton(self.sidebar_frame, text="Dosyaya Kaydet", command=self.dosya_kaydet, fg_color="#27ae60", hover_color="#219150")
        self.sidebar_button_save.grid(row=3, column=0, padx=20, pady=10)

        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Görünüm Modu:", anchor="w")
        self.appearance_mode_label.grid(row=4, column=0, padx=20, pady=(30, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=5, column=0, padx=20, pady=(10, 20))
        self.appearance_mode_optionemenu.set("Dark")

        # Sidebar alt boşluk ayarı (Artık en alta itmek yerine doğal akışında bırakıyoruz)
        self.sidebar_frame.grid_rowconfigure(6, weight=1)
        self.main_content = ctk.CTkFrame(self, fg_color="transparent")
        self.main_content.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.main_content.grid_columnconfigure(0, weight=1)
        self.main_content.grid_rowconfigure(1, weight=1)

        # Tabview (Kart Yapısı)
        self.tabview = ctk.CTkTabview(self.main_content)
        self.tabview.grid(row=0, column=0, sticky="nsew")
        self.tabview.add("Temel Ayarlar")
        self.tabview.add("Güvenlik & Arayüz")
        self.tabview.add("Gelişmiş Servisler")

        self.setup_basic_tab()
        self.setup_security_tab()
        self.setup_advanced_tab()

        # Çıktı Alanı (Alt Kısım)
        self.output_frame = ctk.CTkFrame(self.main_content)
        self.output_frame.grid(row=1, column=0, pady=(20, 0), sticky="nsew")
        self.output_frame.grid_columnconfigure(0, weight=1)
        self.output_frame.grid_rowconfigure(1, weight=1)

        self.output_label = ctk.CTkLabel(self.output_frame, text="Oluşturulan Konfigürasyon", font=ctk.CTkFont(weight="bold"))
        self.output_label.grid(row=0, column=0, padx=20, pady=(10, 0), sticky="w")

        self.txt_output = ctk.CTkTextbox(self.output_frame, font=("Courier New", 13), border_width=1)
        self.txt_output.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

        # Status Bar
        self.status_bar = ctk.CTkLabel(self, text="Hazır", anchor="w", font=ctk.CTkFont(size=12))
        self.status_bar.grid(row=1, column=0, columnspan=2, padx=20, pady=2, sticky="we")

    def setup_basic_tab(self):
        """Temel Ayarlar sekmesini inşa eder."""
        tab = self.tabview.tab("Temel Ayarlar")
        tab.grid_columnconfigure((0, 1), weight=1)

        # Grid yerleşimi
        self.create_label_entry(tab, "Hostname:", "SW-01", 0, 0)
        self.entry_name = self.last_entry

        self.create_label_entry(tab, "Yönetim IP:", "192.168.1.2", 0, 1)
        self.entry_ip = self.last_entry

        self.create_label_entry(tab, "Subnet Mask:", "255.255.255.0", 1, 0)
        self.entry_mask = self.last_entry

        self.create_label_entry(tab, "Default Gateway:", "192.168.1.1", 1, 1)
        self.entry_gw = self.last_entry

        self.create_label_entry(tab, "Management VLAN ID:", "10", 2, 0)
        self.entry_vlan = self.last_entry

        self.create_label_entry(tab, "Domain Name:", "sirket.local", 2, 1)
        self.entry_domain = self.last_entry

        self.create_label_entry(tab, "Banner Mesajı:", "Unauthorized Access Only!", 3, 0)
        self.entry_banner = self.last_entry

        self.create_label_entry(tab, "Timeout (Dakika):", "10", 3, 1)
        self.entry_timeout = self.last_entry

        # Şifre Bölümü
        password_group = ctk.CTkFrame(tab, fg_color="transparent")
        password_group.grid(row=4, column=0, columnspan=2, padx=20, pady=10, sticky="we")
        password_group.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(password_group, text="Cihaz Şifresi (Enable & Admin):").grid(row=0, column=0, sticky="w")
        self.entry_pass = ctk.CTkEntry(password_group, placeholder_text="Güçlü bir şifre girin veya üretin", show="*")
        self.entry_pass.grid(row=1, column=0, sticky="we", padx=(0, 10))

        self.btn_gen_pass = ctk.CTkButton(password_group, text="Şifre Üret (12)", width=120, command=self.sifre_uret_event)
        self.btn_gen_pass.grid(row=1, column=1)

    def setup_security_tab(self):
        """Güvenlik ve Arayüz Ayarları sekmesini inşa eder."""
        tab = self.tabview.tab("Güvenlik & Arayüz")
        tab.grid_columnconfigure((0, 1), weight=1)

        # Checkboxlar
        cb_frame = ctk.CTkFrame(tab, fg_color="transparent")
        cb_frame.grid(row=0, column=0, columnspan=2, padx=20, pady=10, sticky="we")
        cb_frame.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkCheckBox(cb_frame, text="Sadece SSH Erişimi", variable=self.check_ssh_only).grid(row=0, column=0, pady=5, sticky="w")
        ctk.CTkCheckBox(cb_frame, text="SSH Access-List (ACL)", variable=self.check_ssh_acl).grid(row=0, column=1, pady=5, sticky="w")
        ctk.CTkCheckBox(cb_frame, text="Port Security (Sticky)", variable=self.check_port_security).grid(row=1, column=0, pady=5, sticky="w")
        ctk.CTkCheckBox(cb_frame, text="BPDU Guard & Portfast", variable=self.check_bpdu_guard).grid(row=1, column=1, pady=5, sticky="w")

        # Parametreler
        self.create_label_entry(tab, "ACL İzinli Subnet (veya CIDR):", "192.168.1.0/24", 2, 0)
        self.entry_acl_subnet = self.last_entry

        self.create_label_entry(tab, "Port Aralığı (Security/STP):", "fa0/1 - 24", 2, 1)
        self.entry_int_range = self.last_entry

    def setup_advanced_tab(self):
        """Gelişmiş Servisler sekmesini inşa eder."""
        tab = self.tabview.tab("Gelişmiş Servisler")
        tab.grid_columnconfigure((0, 1), weight=1)

        # Checkboxlar
        cb_frame = ctk.CTkFrame(tab, fg_color="transparent")
        cb_frame.grid(row=0, column=0, columnspan=2, padx=20, pady=10, sticky="we")
        cb_frame.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkCheckBox(cb_frame, text="DHCP Snooping", variable=self.check_dhcp_snooping).grid(row=0, column=0, pady=5, sticky="w")
        ctk.CTkCheckBox(cb_frame, text="ARP Inspection (DAI)", variable=self.check_arp_inspection).grid(row=0, column=1, pady=5, sticky="w")
        ctk.CTkCheckBox(cb_frame, text="Statik IP Source Guard", variable=self.check_static_binding).grid(row=1, column=0, pady=5, sticky="w")
        ctk.CTkCheckBox(cb_frame, text="NTP Sunucusu", variable=self.check_ntp_enable).grid(row=1, column=1, pady=5, sticky="w")

        # Parametreler
        self.create_label_entry(tab, "NTP Sunucu IP:", "time.google.com", 2, 0)
        self.entry_ntp = self.last_entry

        self.create_label_entry(tab, "Statik MAC Address:", "0011.2233.4455", 2, 1)
        self.entry_static_mac = self.last_entry

        self.create_label_entry(tab, "Statik Cihaz IP:", "192.168.1.100", 3, 0)
        self.entry_static_ip_bind = self.last_entry

        self.create_label_entry(tab, "Statik Port:", "fa0/1", 3, 1)
        self.entry_static_int = self.last_entry

    # ---- Yardımcı Araçlar ----
    def create_label_entry(self, master, label_text, placeholder, row, col):
        frame = ctk.CTkFrame(master, fg_color="transparent")
        frame.grid(row=row, column=col, padx=15, pady=2, sticky="we")
        frame.grid_columnconfigure(0, weight=1)
        
        lbl = ctk.CTkLabel(frame, text=label_text, font=ctk.CTkFont(size=11))
        lbl.grid(row=0, column=0, sticky="w")
        
        entry = ctk.CTkEntry(frame, placeholder_text=placeholder, height=30)
        entry.grid(row=1, column=0, sticky="we", pady=(0, 0))
        self.last_entry = entry

    def update_status(self, message, is_error=False):
        color = "#e74c3c" if is_error else "#2ecc71"
        self.status_bar.configure(text=f" STATUS: {message}", text_color=color)

    # ---- Mantıksal Fonksiyonlar ----
    def sifre_uret_event(self):
        alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
        password = ''.join(secrets.choice(alphabet) for i in range(12))
        self.entry_pass.delete(0, "end")
        self.entry_pass.insert(0, password)
        self.update_status("Güçlü şifre üretildi.")

    def ip_gecerli_mi(self, ip):
        try:
            ipaddress.ip_address(ip)
            return True
        except:
            return False

    def wildcard_yap(self, duyuru):
        if not duyuru: return ""
        try:
            if "/" in duyuru:
                net = ipaddress.IPv4Network(duyuru, strict=False)
                return f"{net.network_address} {net.hostmask}"
            elif self.ip_gecerli_mi(duyuru):
                return f"{duyuru} 0.0.0.255"
            return duyuru
        except: return duyuru

    def interface_normalize(self, range_str):
        if not range_str: return ""
        res = range_str.replace(" ", "").lower()
        match = re.match(r"([a-z]+)(\d+)(.*)", res)
        if match:
            prefix = match.group(1)
            nums = match.group(2)
            rest = match.group(3)
            if prefix in ["fa", "f", "gi", "g", "te", "t"] and "/" not in nums:
                if len(nums) >= 2: nums = nums[0] + "/" + nums[1:]
            final = prefix + nums + rest
            if "-" in final: return final.replace("-", " - ")
            return final
        return range_str

    def olustur_config(self):
        # Verileri Topla
        try:
            isim = self.entry_name.get().strip()
            ip = self.entry_ip.get().strip()
            mask = self.entry_mask.get().strip()
            gw = self.entry_gw.get().strip()
            sifre = self.entry_pass.get().strip()
            vlan = self.entry_vlan.get().strip()
            domain = self.entry_domain.get().strip()
            banner = self.entry_banner.get().strip()
            timeout = self.entry_timeout.get().strip() or "10"
            ntp = self.entry_ntp.get().strip()

            # Formatlamalar
            acl_subnet = self.wildcard_yap(self.entry_acl_subnet.get().strip())
            int_range = self.interface_normalize(self.entry_int_range.get().strip())
            smac = self.entry_static_mac.get().strip()
            sip_bind = self.entry_static_ip_bind.get().strip()
            sint = self.interface_normalize(self.entry_static_int.get().strip())

            # Validasyonlar
            if not all([isim, ip, mask, gw, sifre, vlan, domain]):
                self.update_status("Hata: Temel alanlar boş bırakılamaz!", True)
                messagebox.showerror("Eksik Veri", "Lütfen Temel Ayarlar sekmesindeki zorunlu alanları doldurun.")
                return

            if not self.ip_gecerli_mi(ip):
                self.update_status("Hata: Geçersiz Yönetim IP!", True)
                return

            conf = f"""! --- Cisco Configuration ---
hostname {isim}
!
banner motd #{banner if banner else "Unauthorized Access Only!"}#
enable secret {sifre}
service password-encryption
no ip domain-lookup
ip domain-name {domain}
"""
            
            if self.check_ssh_only.get():
                conf += f"crypto key generate rsa modulus 2048\nip ssh version 2\nusername admin privilege 15 secret {sifre}\n"

            conf += f"!\nvlan {vlan}\n name Management_VLAN\n!\ninterface vlan {vlan}\n ip address {ip} {mask}\n no shutdown\n!\nip default-gateway {gw}\n"

            if self.check_ntp_enable.get() and ntp:
                conf += f"ntp server {ntp}\n"

            vty_acl_line = ""
            if self.check_ssh_acl.get():
                conf += f"!\naccess-list 10 permit {acl_subnet if acl_subnet else 'any'}\naccess-list 10 deny any log\n"
                vty_acl_line = " access-class 10 in"

            if (self.check_port_security.get() or self.check_bpdu_guard.get()) and int_range:
                conf += f"!\ninterface range {int_range}\n switchport mode access\n"
                if self.check_port_security.get():
                    conf += " switchport port-security\n switchport port-security maximum 2\n switchport port-security violation restrict\n switchport port-security mac-address sticky\n"
                if self.check_bpdu_guard.get():
                    conf += " spanning-tree portfast\n spanning-tree bpduguard enable\n"

            if self.check_dhcp_snooping.get() or self.check_arp_inspection.get():
                conf += "!\n"
                if self.check_dhcp_snooping.get():
                    conf += f"ip dhcp snooping\nip dhcp snooping vlan {vlan}\nno ip dhcp snooping information option\n"
                if self.check_arp_inspection.get():
                    conf += f"ip arp inspection vlan {vlan}\n"

            if self.check_static_binding.get() and all([smac, sip_bind, sint]):
                conf += f"!\nip source binding {smac} vlan {vlan} {sip_bind} interface {sint}\ninterface {sint}\n ip verify source\n"

            conf += f"!\nline vty 0 4\n exec-timeout {timeout} 0\n login local\n transport input {'ssh' if self.check_ssh_only.get() else 'all'}\n{vty_acl_line}\n logging synchronous\n"
            conf += f"!\nline con 0\n exec-timeout {timeout} 0\n login local\n logging synchronous\n!\nend\nwrite memory\n"

            self.txt_output.delete("1.0", "end")
            self.txt_output.insert("1.0", conf)
            self.update_status("Konfigürasyon başarıyla oluşturuldu.")
            
        except Exception as e:
            self.update_status(f"Hata: {str(e)}", True)

    def kopyala(self):
        self.clipboard_clear()
        self.clipboard_append(self.txt_output.get("1.0", "end-1c"))
        self.update_status("Panoya kopyalandı.")

    def dosya_kaydet(self):
        config_text = self.txt_output.get("1.0", "end-1c")
        if not config_text.strip():
            self.update_status("Hata: Kaydedilecek veri yok!", True)
            return
        
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", initialfile=f"{self.entry_name.get()}_config.txt")
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(config_text)
            self.update_status("Dosya kaydedildi.")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

if __name__ == "__main__":
    app = CiscoConfigApp()
    app.mainloop()
