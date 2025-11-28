# TenParse – IP Range & CIDR Parser (Web UI)

TenParse adalah aplikasi web sederhana berbasis **Flask** untuk melakukan parsing dan ekspansi daftar IP Address.  
Aplikasi ini menerima input berupa:

- Single IP  
- IP range dengan tanda `-`  
- CIDR (contoh: `10.0.0.0/24`)  

Output berupa list IP yang sudah diekspansi, bisa dilihat di halaman web dan di-download sebagai file `.txt`.

---

## ✨ Fitur Utama

- ✅ Input lewat **textarea** atau **upload file `.txt`**
- ✅ Mendukung beberapa format:
  - `192.168.1.10` (single IP)
  - `192.168.1.10-192.168.1.20` (range)
  - `10.0.0.0/29` (CIDR)
- ✅ Multi-line & multi separator (spasi, koma, newline)
- ✅ Validasi input dengan feedback error yang jelas
- ✅ Hasil parsing:
  - ditampilkan di halaman
  - disimpan ke `uploads/output.txt`
  - bisa di-download via tombol **Download**

---

## 🧱 Teknologi yang Digunakan

- **Python 3.x**
- **Flask** – web framework
- **netaddr** – untuk operasi IP (`IPAddress`, `IPRange`, `IPNetwork`)
- **Jinja2** – templating engine bawaan Flask

---

## 📂 Struktur Project

Struktur minimal project:

```text
.
├── app.py
├── requirements.txt
├── uploads/
│   └── output.txt      # di-generate saat user proses IP
└── templates/
    └── index.html      # halaman utama web
