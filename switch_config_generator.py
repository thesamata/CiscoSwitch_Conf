import tkinter as tk
from tkinter import messagebox, scrolledtext

def generate_config():
    switch_name = entry_name.get()
    ip_address = entry_ip.get()
    password = entry_pass.get()
    domain_name = entry_domain.get()
    vlan_id = entry_vlan.get()
    banner = entry_banner.get()

    if not switch_name or not ip_address or not password or not domain_name or not vlan_id:
        messagebox.showerror("Hata", "Lütfen tüm alanları doldurun!")
        return

    config = f"""
!
hostname {switch_name}
!
banner motd #{banner}#
!
enable secret {password}
service password-encryption
no ip domain-lookup
!
ip domain-name {domain_name}
crypto key generate rsa modulus 1024
ip ssh version 2
!
username admin privilege 15 secret {password}
!
interface vlan {vlan_id}
 ip address {ip_address} 255.255.255.0
 no shutdown
!
ip default-gateway {ip_address.rsplit('.',1)[0]}.1
!
line vty 0 4
 login local
 transport input ssh
 logging synchronous
exit
!
line con 0
 login local
 logging synchronous
exit
!
conf t
vlan {vlan_id}
 no shutdown
exit
!
end
write memory
"""

    txt_output.delete(1.0, tk.END)
    txt_output.insert(tk.END, config)


# ---- ARAYUZ KISMI ----
root = tk.Tk()
root.title("Cisco Switch Config Generator")
root.geometry("700x600")

tk.Label(root, text="Switch Name:").pack()
entry_name = tk.Entry(root, width=50)
entry_name.pack()

tk.Label(root, text="IP Address (ör: 10.100.101.63):").pack()
entry_ip = tk.Entry(root, width=50)
entry_ip.pack()

tk.Label(root, text="Enable Secret Password:").pack()
entry_pass = tk.Entry(root, width=50, show="*")
entry_pass.pack()

tk.Label(root, text="IP Domain-Name:").pack()
entry_domain = tk.Entry(root, width=50)
entry_domain.pack()

tk.Label(root, text="Management VLAN ID:").pack()
entry_vlan = tk.Entry(root, width=50)
entry_vlan.pack()

tk.Label(root, text="Banner MOTD:").pack()
entry_banner = tk.Entry(root, width=50)
entry_banner.pack()

btn_generate = tk.Button(root, text="Generate Config", command=generate_config)
btn_generate.pack(pady=10)

txt_output = scrolledtext.ScrolledText(root, width=80, height=20)
txt_output.pack()

root.mainloop()
