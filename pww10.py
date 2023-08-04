import subprocess
import os
import re

os.system("cls")

try:
    from tabulate import tabulate
    tabulate_available = True
except ModuleNotFoundError:
    tabulate_available = False
    print("Error: Modul 'tabulate' tidak terpasang. Silakan pasang dengan menggunakan 'pip3 install tabulate'.")

if tabulate_available:
    command_output = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output=True).stdout.decode()
    profile_names = re.findall("Semua Nama Profil Pengguna : (.*)\r", command_output)

    daftar_wifi = []

    if len(profile_names) != 0:
        for name in profile_names:
            profil_wifi = {}  # Buat kamus kosong untuk menyimpan informasi profil Wi-Fi
            profile_info = subprocess.run(["netsh", "wlan", "show", "profile", name], capture_output=True).stdout.decode()

            # Periksa apakah profil Wi-Fi memiliki kunci keamanan atau tidak
            if re.search("Kunci Keamanan           : Tidak Ada", profile_info):
                continue  # Lanjut ke profil Wi-Fi berikutnya jika tidak memiliki kunci keamanan
            else:
                # Simpan nama SSID dari profil Wi-Fi dalam kamus profil_wifi
                profil_wifi["ssid"] = name

                # Dapatkan informasi lengkap profil Wi-Fi, termasuk kata sandi
                profile_info_pass = subprocess.run(["netsh", "wlan", "show", "profile", name, "key=clear"], capture_output=True).stdout.decode()

                # Cari kata sandi menggunakan ekspresi reguler
                password = re.search("Konten Kunci            : (.*)\r", profile_info_pass)

                # Simpan kata sandi dalam kamus profil_wifi, atau None jika tidak ada kata sandi yang ditemukan
                if password is None:
                    profil_wifi["password"] = None
                else:
                    profil_wifi["password"] = password[1]

                # Tambahkan kamus profil_wifi ke daftar_wifi
                daftar_wifi.append(profil_wifi)

    # Format informasi profil Wi-Fi yang diambil menjadi tabel
    header_tabel = ["SSID", "Kata Sandi"]
    data_tabel = []
    for profil_wifi in daftar_wifi:
        ssid = profil_wifi["ssid"]
        password = profil_wifi["password"]
        data_tabel.append([ssid, password])

    # Cetak tabel
    print(tabulate(data_tabel, headers=header_tabel, tablefmt="grid"))
    
