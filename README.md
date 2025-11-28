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

```

## 📦 Dependency Utama
Lihat daftar di **requirements.txt** berikut:

```
Flask>=3.0.0
netaddr>=1.3.0
```
---

## 🛠️ Menjalankan di Lokal (Development)

Gunakan command-command berikut di terminal atau command prompt:

1. Clone repository
```
git clone <URL_REPO_GITHUB_KAMU>.git
cd <nama-folder-repo>
```

2. Buat virtual environment (opsional tapi dianjurkan)
```
python3 -m venv .venv
source .venv/bin/activate          # Linux/macOS
# .venv\\Scripts\\activate         # Windows (PowerShell/CMD)
```

3. Install dependency
```
pip install --upgrade pip
pip install -r requirements.txt
```

4. Jalankan server development
```
python app.py
```

Akses aplikasi lewat browser:
```
http://127.0.0.1:8087
```
---

## 🐳 Deployment: Opsi Platform

### 1. Nginx Reverse Proxy
```
Install Nginx (Linux):
sudo apt update
sudo apt install nginx
```

Contoh konfigurasi di `/etc/nginx/sites-available/tenparse.conf`:
```
server {
  listen 80;
  server_name tenparse.domain.id;

  access_log /var/log/nginx/tenparse_access.log;
  error_log  /var/log/nginx/tenparse_error.log;

  location / {
    proxy_pass http://127.0.0.1:8087;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
  }
}
```

Aktifkan dan reload Nginx:
```
sudo ln -s /etc/nginx/sites-available/tenparse.conf /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```
---

### 2. Apache mod_wsgi

Install Apache + mod_wsgi (Linux):
```
sudo apt update
sudo apt install apache2 libapache2-mod-wsgi-py3
```

Buat entry point WSGI wsgi.py di root project:
```
from app import app as application
```

Contoh VirtualHost di `/etc/apache2/sites-available/tenparse.conf`:
```
<VirtualHost *:80>
  ServerName tenparse.domain.id
  WSGIDaemonProcess tenparse python-home=/opt/tenparse/.venv python-path=/opt/tenparse
  WSGIScriptAlias / /opt/tenparse/wsgi.py

  <Directory /opt/tenparse>
    Require all granted
  </Directory>

  ErrorLog ${APACHE_LOG_DIR}/tenparse_error.log
  CustomLog ${APACHE_LOG_DIR}/tenparse_access.log combined
</VirtualHost>
```

Aktifkan site dan reload Apache:
```
sudo a2enmod wsgi
sudo a2ensite tenparse
sudo systemctl reload apache2
```
---

### 3. Docker

Contoh Dockerfile:
```
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN mkdir -p uploads
EXPOSE 8087
CMD ["python", "app.py"]

Build dan jalankan container:
docker build -t tenparse:prod .
docker run -d -p 8087:8087 --name tenparse tenparse:prod

Jika ingin persist output:
docker run -d \
  --name tenparse \
  -p 8087:8087 \
  -v /opt/tenparse-uploads:/app/uploads \
  tenparse:prod
```
---

### 4. Proxmox (CT / VM)

Rekomendasi resource minimal:
- 1–2 Core CPU
- 1–2 GB RAM
- Storage secukupnya
- OS: Debian/Ubuntu minimal

Cara deploy:
- Jalankan aplikasi di dalam CT/VM Linux
- Gunakan salah satu skenario: Python, Nginx, Apache, atau Docker
- Aplikasi tidak membutuhkan konfigurasi khusus Proxmox di level kode

---

## 🧾 Format Input yang Didukung

### Contoh input valid:
```
192.168.0.1
10.0.0.5-10.0.0.10
172.16.1.0/30
10.1.1.1,10.2.2.2-10.2.2.5,192.168.3.7/29
```

### Contoh input invalid (akan error dan menghentikan parsing):
```
10.0.0.999
192.168.1.10-192.168.1.5 (jika range terbalik dan gagal di-parse)
ini-bukan-ip
256.256.256.256
```
---

## ⚠️ Hal Penting

- Output tidak mengecualikan network/broadcast (untuk raw parsing)
- Setiap proses parsing akan overwrite file uploads/output.txt
- Folder uploads/ dibuat otomatis saat berjalan
- Mode debug Flask tidak cocok untuk production
- Setiap proses parsing akan overwrite file uploads/output.txt
- Folder uploads/ dibuat otomatis saat berjalan
- File `app.py` tidak mengandung `app.secret_key` karena aplikasi saat ini tidak menggunakan
  Flask `session`, `flash`, atau CSRF, sehingga `SECRET_KEY` tidak diperlukan untuk alur ini.
  Jika nanti Anda menambahkan fitur yang memerlukan session atau perlindungan CSRF, tetapkan
  `SECRET_KEY` melalui environment variable (jangan commit ke repo). Contoh singkat untuk
  development/production:

  ```bash
  export SECRET_KEY="$(python3 -c 'import os,base64; print(base64.urlsafe_b64encode(os.urandom(32)).decode())')"
  ```

  Dan di kode Python gunakan:

  ```python
  import os
  app.secret_key = os.environ.get('SECRET_KEY')
  ```
- Mode debug Flask tidak cocok untuk production

---

## ❗ Error Handling

Jika terjadi error (misalnya format IP salah):
Aplikasi akan menampilkan pesan error di halaman:

Contoh:
```
Invalid input detected: 10.0.0.999. Error: address cannot be parsed, invalid IP format.
```
Pesan error selalu menampilkan IP yang gagal di-parse agar user bisa memperbaiki input.
