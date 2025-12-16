# Laporan Debugging (DEBUG_REPORT.md)

**Masalah:** Unit test gagal atau hasil perhitungan salah (Output: 990.0, Seharusnya: 900.0).

**Langkah Penelusuran:**
1. Mengaktifkan `pdb.set_trace()` di dalam `diskon_service.py`.
2. Menjalankan script: `python diskon_service.py`.
3. Menggunakan perintah `n` (next) untuk baris per baris.

**Log Terminal:**
(Pdb) n
> .../diskon_service.py(15)hitung_diskon()
-> harga_akhir = harga_awal - jumlah_diskon

(Pdb) p harga_akhir
900.0  <-- (Sampai sini nilai masih BENAR)

(Pdb) n
> .../diskon_service.py(19)hitung_diskon()
-> harga_akhir = harga_akhir + (harga_akhir * 0.10)

(Pdb) n
> .../diskon_service.py(21)hitung_diskon()
-> return harga_akhir

(Pdb) p harga_akhir
990.0  <-- (BUG DITEMUKAN: Nilai berubah menjadi salah setelah baris 19)

**Akar Masalah:**
Terdapat baris kode tambahan `harga_akhir = harga_akhir + (harga_akhir * 0.10)` yang secara tidak sengaja menambahkan pajak 10% setelah diskon dihitung.

**Perbaikan:**
Menghapus baris perhitungan PPN tersebut agar fungsi hanya menghitung diskon murni.