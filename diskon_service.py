# diskon_service.py
import pdb

class DiskonCalculator:
    """Menghitung harga akhir setelah diskon."""

    def hitung_diskon(self, harga_awal: float, persentase_diskon: int) -> float:
        
        # pdb.set_trace() # <-- Aktifkan ini saat menjalankan Langkah 2 (Debugging)
        
        # 1. Hitung diskon (Logika Benar)
        jumlah_diskon = harga_awal * persentase_diskon / 100
        
        # 2. Kurangi harga awal
        harga_akhir = harga_awal - jumlah_diskon

        # --- SIMULASI BUG (Langkah 1) ---
        # "Secara tidak sengaja" menambahkan PPN 10% ke harga akhir
        # Ini akan menyebabkan hasil menjadi 990.0 (seharusnya 900.0) untuk input 1000
        harga_akhir = harga_akhir + (harga_akhir * 0.10) 

        return harga_akhir

if __name__ == '__main__':
    calc = DiskonCalculator()
    # Input: 1000, Diskon 10%. Harapan: 900.0. Realitas (Bug): 990.0
    print(f"Hasil: {calc.hitung_diskon(1000, 10)}")