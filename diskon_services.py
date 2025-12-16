# diskon_service.py
import pdb

class DiskonCalculator:
    """Menghitung harga akhir setelah diskon."""

    def hitung_diskon(self, harga_awal: float, persentase_diskon: int) -> float:
        
        # pdb.set_trace() 
        
        # --- CATATAN BUG LOGIKA ---
        # Kode yang salah (bug): 
        # jumlah_diskon = harga_awal * persentase_diskon 
        # (Salah karena tidak dibagi 100)

        # code perbaikan
        jumlah_diskon = harga_awal * persentase_diskon / 100

        harga_akhir = harga_awal - jumlah_diskon

        return harga_akhir

# --- UJI COBA ---
if __name__ == '__main__':
    calc = DiskonCalculator()
    # Input: 1000 dengan diskon 10%. Hasil yang diharapkan: 900.0
    hasil = calc.hitung_diskon(1000, 10)
    print(f"Hasil: {hasil}")