from datetime import datetime, timedelta
import prettytable
import os


# Data akun
akun = [
    {
        "Nama": "ererki",
        "PIN": "1234",
        "Status": "Reguler",
        "Saldo": 20000,
        "kyocoin": 0,
        "Voucher": {},
        "Riwayat_Pembelian": []
    },
    {
        "Nama": "msix",
        "PIN": "1235",
        "Status": "Reguler",
        "Saldo": 20000,
        "kyocoin": 0,
        "Voucher": {},
        "Riwayat_Pembelian": []
    },
]

# Menu VIP
menu_vip = {
    "Pagi": {"SALAD BUAH": 12, "BUBUR AYAM": 10, "GADO-GADO": 15, "SALAD SALMON": 30, "AVOCADO TOAST": 20, "MIXED FRUIT SMOOTHIE": 20},
    "Siang": {"SALAD SAYUR MAKARONI": 20, "DADA AYAM PANGGANG": 25, "SUP AYAM": 15,"TUMIS TUNA BROKOLI": 45, "NASI MERAH & IKAN TUNA": 50, "NASI IKAN KEMBUNG": 45},
    "Malam": {"JUS ALPUKAT": 10, "MIXED FRUIT & VEGETABLE": 15, "MASHED POTATO": 15, "OMELETE": 10, "BANANA SMOOTHIE": 15, "SUSU & OMELETE TOAST": 20, "JUS BUAH BIT": 15},
}

# Menu reguler
menu = {
    "Pagi": {"SALAD BUAH": 12, "BUBUR AYAM": 10, "GADO-GADO": 15},
    "Siang": {"SALAD SAYUR MAKARONI": 20, "DADA AYAM PANGGANG": 25, "SUP AYAM": 15},
    "Malam": {"JUS ALPUKAT": 10, "MIXED FRUIT & VEGETABLE": 15, "MASHED POTATO": 15, "OMELETE": 10},
}

benefit_vip = {
    "Voucher 25%": 3,
    "Voucher 20%": 4,
    "Voucher 15%": 5,
    "Voucher 10%": 6,
}

def cek_status_vip(pelanggan):
    if pelanggan["Status"] == "VIP" and all(jumlah == 0 for jumlah in pelanggan["Voucher"].values()):
        pelanggan["Status"] = "Reguler"
        print("Semua voucher telah habis. Status Anda telah berubah menjadi *Reguler*.")

def tampilkan_menu(judul, daftar_menu):
    tabel = prettytable.PrettyTable()
    tabel.title = judul
    tabel.field_names = ["No", "Menu", "Harga"]
    for indeks, (item, harga) in enumerate(daftar_menu.items(), start=1):
        tabel.add_row([indeks, item, f"{harga:,} kyocoin"])
    print(tabel)

def daftar_vip(pelanggan):
    os.system("cls")
    print("=== Pendaftaran VIP ===")
    print("Biaya pendaftaran VIP: Rp30,000")
    table = prettytable.PrettyTable()
    table.title = ("BENEFIT BERLANGGANAN VIP KYOU CATERING")
    table.field_names = ["No", "Benefit"]
    for no, (benefit, jumlah) in enumerate(benefit_vip.items(), start=1):
        table.add_row([no, f"{benefit} ({jumlah} kali)"])
    print(table)

    if pelanggan["Saldo"] < 30000:
        print("Saldo Anda tidak mencukupi untuk menjadi pelanggan VIP.")
        input("Tekan Enter untuk kembali...")
        return
    konfirmasi = input("Apakah Anda yakin ingin mendaftar sebagai pelanggan VIP? (y/n): ").lower()
    if konfirmasi == 'y':
        pelanggan["Saldo"] -= 30000
        pelanggan["Status"] = "VIP"
        pelanggan["Tanggal VIP Aktif Hingga"] = datetime.now() + timedelta(days=7)  # Tambah masa aktif 7 hari
        pelanggan["Voucher"] = {  # Tambah voucher dengan jumlah
            "25%": {"jumlah": 3, "berlaku_hingga": datetime.now() + timedelta(days=7)},
            "20%": {"jumlah": 4, "berlaku_hingga": datetime.now() + timedelta(days=7)},
            "15%": {"jumlah": 5, "berlaku_hingga": datetime.now() + timedelta(days=7)},
            "10%": {"jumlah": 6, "berlaku_hingga": datetime.now() + timedelta(days=7)},
        }
        print("\n=== INVOICE PENDAFTARAN VIP ===")
        print(f"Nama Pelanggan : {pelanggan['Nama']}")
        print("Status         : VIP")
        print(f"Saldo Tersisa  : Rp{pelanggan['Saldo']:,}")
        print("Voucher Anda   :")
        for voucher, detail in pelanggan["Voucher"].items():
            print(f"- {voucher} (Tersisa: {detail['jumlah']}x, Berlaku Hingga: {detail['berlaku_hingga'].strftime('%Y-%m-%d')})")
        input("Selamat, Anda telah menjadi pelanggan VIP KYOU CATERING! Tekan Enter untuk melanjutkan...")
        menu_pengguna(pelanggan)
    else:
        print("Pendaftaran dibatalkan.")
        input("Tekan Enter untuk kembali...")

def cek_status_vip(pelanggan):
    """Periksa apakah status VIP pelanggan masih aktif berdasarkan tanggal."""
    if pelanggan["Status"] == "VIP":
        if datetime.now() > pelanggan.get("Tanggal VIP Aktif Hingga", datetime.now()):
            pelanggan["Status"] = "Reguler"
            pelanggan["Voucher"] = {}  
            print("Keanggotaan VIP Anda telah berakhir. Status Anda sekarang adalah *Reguler*.")
    elif pelanggan["Status"] == "Reguler" and "Tanggal VIP Aktif Hingga" in pelanggan:
        del pelanggan["Tanggal VIP Aktif Hingga"]

def beli_menu(pelanggan, waktu):
    os.system("cls")
    print(f"=== Menu {waktu} ===")
    
    if pelanggan["Status"] == "VIP":
        print("\nMenu VIP:")
        tampilkan_menu(f"Menu {waktu} (VIP)", menu_vip[waktu])
        daftar_menu_vip = list(menu_vip[waktu].items())
        daftar_menu = daftar_menu_vip
        batas_vip = len(daftar_menu_vip)  
    else:
        tampilkan_menu(f"Menu {waktu}", menu[waktu])
        daftar_menu = list(menu[waktu].items())
        batas_vip = 0  

    try:
        pilihan = int(input("\nPilih menu (masukkan angka): ")) - 1
        if 0 <= pilihan < len(daftar_menu):
            item, harga = daftar_menu[pilihan]

            if pilihan < batas_vip and pelanggan["Status"] != "VIP":
                print("Menu ini hanya tersedia untuk pelanggan VIP.")
                input("Tekan Enter untuk kembali...")
                return
            
            if pelanggan["kyocoin"] < harga:
                print("kyocoin Anda tidak mencukupi untuk membeli menu ini. Silakan top up kyocoin terlebih dahulu.")
                input("Tekan Enter untuk kembali...")
                return
            
            if pelanggan["Voucher"]:
                print("\nVoucher tersedia:")
                for indeks, (voucher, detail) in enumerate(pelanggan["Voucher"].items(), start=1):
                    print(f"{indeks}. {voucher} (Tersisa: {detail['jumlah']})")
                gunakan_voucher = input("Gunakan voucher? (y/n): ").lower()
                if gunakan_voucher == 'y':
                    try:
                        pilihan_voucher = int(input("Pilih voucher (masukkan angka): ")) - 1
                        daftar_voucher = list(pelanggan["Voucher"].items())
                        if 0 <= pilihan_voucher < len(daftar_voucher):
                            nama_voucher, detail = daftar_voucher[pilihan_voucher]
                            if detail['jumlah'] > 0:
                                diskon = int(nama_voucher.split('%')[0]) / 100
                                harga = int(harga - (harga * diskon))
                                pelanggan["Voucher"][nama_voucher]["jumlah"] -= 1  # Kurangi jumlah voucher
                                print(f"Voucher {nama_voucher} digunakan! Harga setelah diskon: {harga:,} kyocoin")
                            else:
                                print("Voucher tidak tersedia.")
                        else:
                            print("Pilihan tidak valid.")
                    except ValueError:
                        print("Input tidak valid.")
            
            pelanggan["kyocoin"] -= harga
            waktu_transaksi = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            pelanggan["Riwayat_Pembelian"].append({"Menu": item, "Harga": harga, "Waktu": waktu_transaksi})
            print("\n=== INVOICE PEMBELIAN ===")
            print(f"Nama Pelanggan : {pelanggan['Nama']}")
            print(f"Menu Dibeli    : {item}")
            print(f"Harga          : {harga:,} kyocoin")
            print(f"Waktu Transaksi: {waktu_transaksi}")
            print(f"Kyocoin Tersisa: {pelanggan['kyocoin']:,} kyocoin")
            cek_status_vip(pelanggan)
            input("Tekan Enter untuk kembali...")
        else:
            print("Pilihan menu tidak valid.")
            input("Tekan Enter untuk kembali...")
    except ValueError:
        print("Input tidak valid.")
        input("Tekan Enter untuk kembali...")

def lihat_riwayat_pembelian(pelanggan):
    os.system("cls")
    if not pelanggan["Riwayat_Pembelian"]:
        print("Anda belum melakukan pembelian apa pun.")
        input("Tekan Enter untuk kembali.")
        return
    table = prettytable.PrettyTable()
    table.field_names = ["No", "Menu", "Harga", "Waktu"]
    for idx, pembelian in enumerate(pelanggan["Riwayat_Pembelian"], start=1):
        table.add_row([idx, pembelian["Menu"], f"{pembelian['Harga']:,} kyocoin", pembelian["Waktu"]])
    print(table)
    input("Tekan Enter untuk kembali.")

def lihat_saldo_gold(pelanggan):
    os.system("cls")
    print("Berikut Saldo dan Kyocoin kamuu")
    print(f"Saldo Anda: {pelanggan['Saldo']:,} ")
    print(f"kyocoin Anda: {pelanggan['kyocoin']}")
    input("Tekan Enter untuk kembali.")

def top_up_saldo(pelanggan):
    os.system("cls")
    while True:
        print("=== Menu Top Up Saldo Kyou Catering ===")
        print("1. Rp10.000")
        print("2. Rp25.000")
        print("3. Rp50.000")
        print("4. Rp100.000")
        print("5. Rp150.000")
        print("6. Rp200.000")
        print("7. Kembali")
        
        try:
            pilihan = int(input("Pilih jumlah top up (1-7): "))
            
            if pilihan == 1:
                jumlah = 10000
            elif pilihan == 2:
                jumlah = 25000
            elif pilihan == 3:
                jumlah = 50000
            elif pilihan == 4:
                jumlah = 100000
            elif pilihan == 5:
                jumlah = 150000
            elif pilihan == 6:
                jumlah = 200000
            elif pilihan == 7:
                print("Kembali ke menu sebelumnya.")
                break
            else:
                print("Pilihan tidak valid. Silakan pilih antara 1 dan 7.")
                continue

            # Update saldo
            pelanggan["Saldo"] += jumlah
            print(f"Top Up berhasil! Saldo Anda sekarang: Rp{pelanggan['Saldo']:,}")
            break
            
        except ValueError:
            print("Input tidak valid. Harap pilih angka yang sesuai.")
            input("Tekan Enter untuk melanjutkan...")


def top_up_kyocoin(pelanggan):
    os.system("cls")
    if pelanggan["Saldo"] <= 0:
        print("Saldo Anda tidak mencukupi untuk top up kyocoin.")
        input("Tekan Enter untuk kembali.")
        return
    
    while True:
        print("=== Menu Top Up Kyocoin Kyou Catering ===")
        print("1. 10 kyocoin (Rp10,000)")
        print("2. 25 kyocoin (Rp25,000)")
        print("3. 50 kyocoin (Rp50,000)")
        print("4. 100 kyocoin (Rp100,000)")
        print("5. 150 kyocoin (Rp150,000)")
        print("6. 200 kyocoin (Rp200,000)")
        print("7. Kembali")
        
        try:
            pilihan = int(input("Pilih jumlah kyocoin yang ingin ditukar (1-7): "))
            if pilihan == 1:
                jumlah_kyocoin = 10
                biaya = 10000
            elif pilihan == 2:
                jumlah_kyocoin = 25
                biaya = 25000
            elif pilihan == 3:
                jumlah_kyocoin = 50
                biaya = 50000
            elif pilihan == 4:
                jumlah_kyocoin = 100
                biaya = 100000
            elif pilihan == 5:
                jumlah_kyocoin = 150
                biaya = 150000
            elif pilihan == 6:
                jumlah_kyocoin = 200
                biaya = 200000
            elif pilihan == 7:
                print("Kembali ke menu sebelumnya.")
                break
            else:
                print("Pilihan tidak valid. Silakan pilih antara 1 dan 7.")
                continue
            
            if pelanggan["Saldo"] < biaya:
                print("Saldo Anda tidak mencukupi untuk melakukan top up kyocoin.")
            else:
                pelanggan["Saldo"] -= biaya
                pelanggan["kyocoin"] += jumlah_kyocoin
                print(f"Top Up berhasil! Anda mendapatkan {jumlah_kyocoin} kyocoin.")
                print(f"Saldo Anda sekarang: Rp{pelanggan['Saldo']:,}, kyocoin Anda: {pelanggan['kyocoin']}")
            break
        except ValueError:
            print("Input tidak valid. Harap pilih angka yang sesuai.")
            input("Tekan Enter untuk melanjutkan...")

    
def menu_pengguna(pelanggan):
    while True:
        os.system("cls")
        print("+====================================================+")
        print("          SELAMAT DATANG DI KYOU CATERING!!          ")
        print(f"      SAAT INI ANDA ADALAH PELANGGAN: {pelanggan['Status']}")
        print("+====================================================+")
        if pelanggan["Status"] == "VIP":
            if "Tanggal VIP Aktif Hingga" in pelanggan:
                waktu_aktif_hingga = pelanggan["Tanggal VIP Aktif Hingga"]
                sisa_waktu = waktu_aktif_hingga - datetime.now()
                if sisa_waktu.days > 0:
                    print(f"Sisa Waktu VIP: {sisa_waktu.days} hari, {sisa_waktu.seconds // 3600} jam")
                else:
                    print("Keanggotaan VIP Anda telah berakhir.")
                    pelanggan["Status"] = "Reguler"
                    pelanggan["Voucher"] = {}
        print("Ini Adalah Fitur Yang Tersedia Di Kyou Catering, Mau Ngapain Nih? ")
        print("1. Beli Menu")
        print("2. Lihat Riwayat Pembelian")
        print("3. Lihat Saldo dan kyocoin")
        print("4. Top Up Saldo")
        print("5. Top Up kyocoin")
        print("6. Daftar VIP")
        print("7. Keluar")
        try:
            pilih = int(input("Pilih menu: "))
            if pilih == 1:
                waktu = datetime.now().hour
                if 7.30 <= waktu < 11:
                    beli_menu(pelanggan, "Pagi")
                elif 12 <= waktu < 15:
                    beli_menu(pelanggan, "Siang")
                elif 16 <= waktu < 20:
                    beli_menu(pelanggan, "Malam")
                else:
                    print("Saat ini Kyou Catering lagi tutup nih, coba akses kembali saat jam operasional ya!!.")
                    input("Tekan Enter untuk kembali...")
            elif pilih == 2:
                lihat_riwayat_pembelian(pelanggan)
            elif pilih == 3:
                lihat_saldo_gold(pelanggan)
            elif pilih == 4:
                top_up_saldo(pelanggan)
            elif pilih == 5:
                top_up_kyocoin(pelanggan)
            elif pilih == 6:
                daftar_vip(pelanggan)
            elif pilih == 7:
                break
            else:
                print("Pilihan tidak valid.")
        except ValueError:
            print("Input tidak valid.")
        input("Tekan Enter untuk melanjutkan...")

# LOGIN
def login():
    os.system("cls")
    print("+=================================================================================+")
    print("|          SELAMAT DATANG DI KYOU CATERING, SILAHKAN LOGIN TERLEBIH DAHULU        |")
    print("| MASUKKAN NAMA DAN KATA SANDI ANDA DENGAN BENAR, MAKSIMAL PERCOBAAN ADALAH 3     |")
    print("+=================================================================================+")
    for i in range(3):
        nama = input("Masukkan Nama Anda: ")
        pin = input("Masukkan PIN Anda: ")
        for pelanggan in akun:
            if pelanggan["Nama"] == nama and pelanggan["PIN"] == pin:
                menu_pengguna(pelanggan)  
                return
        print("Nama atau PIN salah.")
    print("Anda salah memasukkan lebih dari 3 kali.")

# MENU AWAL
def menuawal():
    os.system("cls")
    print("--------------- HII!! SELAMAT DATANG DI KYOU CATERING  *_* ------------------")
    print("-- KYOU CATERING MENYEDIAKAN MENU DIET YANG SEHAT DAN BERGIZI UNTUK ANDA!! --")

    table = prettytable.PrettyTable()
    table.title = "KYOU CATERING (MENU DIET SEHAT)"
    table.field_names = ["NO", "MENU"]

    pilihanstatus = [
        ["1.", "LOGIN"],
        ["2.", "KELUAR"]
    ]

    for option in pilihanstatus:
        table.add_row(option)

    print(table)
    try:
        loginmenu = int(input("PILIH MENU YANG TERSEDIA (MASUKKAN ANGKA): "))
        if loginmenu == 1:
            login()
        elif loginmenu == 2:
            exit()
        else:
            print("Pilihan tidak valid!")
    except ValueError:
        print("Input tidak valid!")

menuawal()