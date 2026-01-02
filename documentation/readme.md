# Challenge Test - Mid. Firmware Engineer
Repositori ini berisi solusi teknis untuk pengerjaan Challenge Test Firmware Engineer di PT Synapsis Sinergi Digital.

## Struktur Direktori
- `soal1/`: REST API menggunakan Flask dan MySQL.
- `soal2/`: Penjadwalan (Scheduling) pengambilan data dari OpenWeather API.
- `soal3/`: Komunikasi protokol Modbus TCP/IP (Master & Slave).
- `soal4/`: Implementasi MQTT Gateway (Publish & Subscribe).
- `soal5/`: Link simulasi ESP32-S3 pada platform Wokwi.
- `function/`: Library fungsi pendukung (Helper) yang digunakan secara reusable.
- `database/`: File SQL untuk import struktur tabel MySQL.
- `log/`: Penyimpanan log data dalam format JSON dan CSV.

## Persiapan dan Instalasi
1. Pastikan Anda telah menginstal Python 3.x.
2. Instal semua library yang dibutuhkan menggunakan pip:
   ```bash
   pip install -r requirement.txt
3. Siapkan database MySQL (XAMPP/Docker) dan import file database/project_db.sql.

## Cara Menjalankan Program
Setiap modul dijalankan melalui terminal dari direktori utama (root):
Soal 1: REST API Flask
- python -m soal1.main
Soal 2: Scheduling Weather API
- python -m soal2.main
Soal 3: Modbus TCP/IP
- Jalankan Slave: python -m soal3.slave_main
- lalu Jalankan Master : python -m soal3.master_main
Soal 4: 
- python -m soal4.main
Soal 5: ESP32-S3 (Wokwi)
- Buka link yang tertera pada file soal_wokwi/link.txt untuk melihat simulasi hardware.

## Aturan Penulisan
Seluruh kode mengikuti kriteria:
Variabel: snake_case 
Fungsi/Method: camelCase 
Class: PascalCase 
String: Kutip dua (") 
Jarak antar fungsi: 2 blank line