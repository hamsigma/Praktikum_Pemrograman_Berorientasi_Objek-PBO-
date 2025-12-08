# Refactoring: Sistem Validasi Registrasi Mahasiswa (Satu-file Good + Bad terpisah)

Indetifikiasi
- SRP (Single Responsibility Principle)
- Pelanggaran: ValidatorManager melakukan banyak tugas sekaligus (cek SKS, cek prasyarat, cek jadwal, dan mencetak hasil) dalam satu kelas/method.
- Mengapa masalah: Sulit dipelihara & diuji; satu perubahan aturan memengaruhi banyak bagian.
- Perbaikan singkat: Pisahkan tiap aturan ke kelas tersendiri (mis. SksLimitRule, PrerequisiteRule, JadwalBentrokRule) dan buat koordinator yang hanya mengorkestrasikan.

- OCP (Open/Closed Principle)
- Pelanggaran: Kode memakai kontrol terpusat (if/else/loop) sehingga menambah aturan baru mengharuskan mengubah ValidatorManager.
- Mengapa masalah: Menambah fitur memicu modifikasi di kode yang sudah ada dan berisiko regresi.
- Perbaikan singkat: Definisikan interface rule (IValidationRule) dan inject rule baru tanpa mengubah koordinator.

- DIP (Dependency Inversion Principle)
- Pelanggaran: ValidatorManager bergantung pada implementasi konkret (logika validasi tertanam), bukan pada abstraksi.
- Mengapa masalah: Sulit mengganti/memock rule untuk testing dan mengikat kode pada detail.
- Perbaikan singkat: Buat abstraksi IValidationRule dan lakukan Dependency Injection ke RegistrationService sehingga service bergantung pada antarmuka, bukan implementasi.

Deskripsi:
- Refactoring_sistem_validasi_regestrasi_mahasiswa.py: Implementasi hasil refactor (semua kelas/abstraksi/koordinator dalam 1 file).
- validator_bad.py: Versi "sebelum refactor" yang menggabungkan banyak logika dalam satu kelas (digunakan untuk perbandingan).
- Tujuan: Memudahkan review — kode yang baik digabung agar mudah dipakai, sedangkan kode buruk dipisah untuk bukti sebelum/ sesudah.

Cara menjalankan:
1. Pastikan Python 3.8+ terpasang.
2. Jalankan versi good (refactor): (sesudah di refactor)
   python registration_good.py
3. Jalankan versi bad: (sebelum di refactor)
   python validator_bad.py

Output yang diharapkan:
-Refactoring_sistem_validasi_regestrasi_mahasiswa.py akan menampilkan hasil validasi yang memicu JadwalBentrokRule (contoh).
- validator_bad.py menampilkan cara kerja kode lama (juga akan mendeteksi bentrokan).

Mengapa struktur ini berguna:
- Menaruh kode refactor di satu file memudahkan pengajar/ reviewer menjalankan contoh dengan cepat.
- Memisahkan kode buruk membuat bukti "sebelum vs sesudah" jelas untuk laporan.
- Jika proyek berkembang, Anda bisa pecah registration_good.py ke package (models/, rules/, service/) nanti.

Refleksi singkat:
Dependency Injection (DI) vs if/else — penjelasan singkat:
    Decoupling: DI membuat service bergantung pada abstraksi (interface), bukan logika konkret; if/else mengikat semua logika di satu tempat.
    Mudah diperluas (OCP): Tambah aturan baru cukup buat kelas baru dan inject; if/else mengharuskan mengubah metode pusat.
    Single Responsibility (SRP): DI mendorong tiap rule punya satu tanggung jawab sehingga lebih mudah dipelihara; if/else cenderung menggabungkan banyak tanggung jawab.
    Testability: DI memudahkan mocking dan pengujian unit per-rule; if/else menyulitkan pengujian karena method jadi besar dan kompleks.
    Fleksibilitas runtime: Dengan DI, perilaku bisa diubah lewat konfigurasi/komposisi tanpa menyentuh kode koordinator.
    Intinya: DI mengurangi coupling dan risiko regresi, sementara if/else cenderung menimbun code smell saat fitur tumbuh.
    
