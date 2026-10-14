# backend/m3_laporan.py  –  M3: Insertion sort, Merge sort, Linear search, Binary search

class Pencacah:
    """Objek pencacah operasi untuk mencatat perbandingan dan pemindahan secara deterministik."""
    def __init__(self):
        self.perbandingan = 0
        self.pemindahan = 0

    def tambah_perbandingan(self, n=1):
        self.perbandingan += n

    def tambah_pemindahan(self, n=1):
        self.pemindahan += n

    def reset(self):
        self.perbandingan = 0
        self.pemindahan = 0


def _get_val(p, key):
    """Ambil nilai field baik dari dict maupun tuple/list dengan konstanta indeks."""
    if hasattr(p, 'get'):
        return p.get(key)
    # (OID, PELANGGAN, RESTO, MENU, HARGA, PRIORITAS, T_MASUK, T_SELESAI, STATUS)
    keys = ('oid', 'pelanggan', 'resto', 'menu', 'harga', 'prioritas',
            't_masuk_detik', 't_selesai_detik', 'status')
    for i in range(len(keys)):
        if keys[i] == key and i < len(p):
            return p[i]
    return None


def _ambil_kunci(item, kunci):
    """Ekstraksi nilai kunci untuk perbandingan. Menangani nilai None/selesai kosong."""
    val = _get_val(item, kunci)
    if kunci in ('selesai', 't_selesai_detik'):
        # Pesanan belum selesai diletakkan di akhir urutan menaik
        if val is None or val == '' or val == '-':
            return float('inf')
        return int(val)
    if kunci == 'harga':
        return int(val) if val is not None else 0
    # Kunci teks (oid, resto, menu, status, dll.)
    return str(val) if val is not None else ''


def insertion_sort(larik, kunci='harga', pencacah=None):
    """
    Insertion sort in-place dan stabil. O(n^2).
    Menggunakan operator '>' agar stabil saat kunci bernilai sama.
    Tolak bila n > 20.000 dengan pesan jelas agar antarmuka tidak membeku.
    Kembalikan (jumlah_perbandingan, jumlah_pemindahan).
    """
    n = len(larik)
    if n > 20000:
        raise ValueError("DITOLAK: batasnya 20.000 baris, pakai merge sort untuk data penuh")

    if pencacah is None:
        pencacah = Pencacah()

    for i in range(1, n):
        cur = larik[i]
        cur_k = _ambil_kunci(cur, kunci)
        j = i - 1
        while j >= 0:
            pencacah.tambah_perbandingan(1)
            if _ambil_kunci(larik[j], kunci) > cur_k:  # '>' menjaga stabilitas
                larik[j + 1] = larik[j]
                pencacah.tambah_pemindahan(1)
                j -= 1
            else:
                break
        larik[j + 1] = cur
        pencacah.tambah_pemindahan(1)

    return pencacah.perbandingan, pencacah.pemindahan


def merge_sort(larik, kunci='oid', pencacah=None):
    """
    Merge sort rekursif dan stabil. O(n log n).
    Menggunakan operator '<=' agar elemen dari bagian kiri didahulukan saat kunci sama.
    Kembalikan (hasil_terurut, jumlah_perbandingan, jumlah_pemindahan).
    """
    if pencacah is None:
        pencacah = Pencacah()

    def _merge(L, R):
        total_len = len(L) + len(R)
        out = [None] * total_len
        i = 0
        j = 0
        k = 0
        while i < len(L) and j < len(R):
            pencacah.tambah_perbandingan(1)
            if _ambil_kunci(L[i], kunci) <= _ambil_kunci(R[j], kunci):  # '<=' menjaga stabilitas
                out[k] = L[i]
                i += 1
            else:
                out[k] = R[j]
                j += 1
            pencacah.tambah_pemindahan(1)
            k += 1

        # Salin sisa elemen yang belum habis
        while i < len(L):
            out[k] = L[i]
            i += 1
            k += 1
            pencacah.tambah_pemindahan(1)
        while j < len(R):
            out[k] = R[j]
            j += 1
            k += 1
            pencacah.tambah_pemindahan(1)
        return out

    def _ms(arr):
        if len(arr) <= 1:
            return arr
        mid = len(arr) // 2
        left_sorted = _ms(arr[:mid])
        right_sorted = _ms(arr[mid:])
        return _merge(left_sorted, right_sorted)

    hasil = _ms(larik)
    return hasil, pencacah.perbandingan, pencacah.pemindahan


def linear_search(larik, target, kunci='oid', pencacah=None):
    """
    Pencarian linear satu per satu dari awal sampai target ditemukan. O(n).
    Kembalikan (indeks|-1, jumlah_perbandingan).
    """
    if pencacah is None:
        pencacah = Pencacah()

    target_str = str(target)
    for i in range(len(larik)):
        pencacah.tambah_perbandingan(1)
        val = _ambil_kunci(larik[i], kunci)
        if str(val) == target_str:
            return i, pencacah.perbandingan
    return -1, pencacah.perbandingan


def binary_search(larik_terurut, target, kunci='oid', pencacah=None):
    """
    Binary search pada larik yang sudah terurut menurut kunci. O(log n).
    Kembalikan (indeks|-1, jumlah_perbandingan).
    """
    if pencacah is None:
        pencacah = Pencacah()

    lo = 0
    hi = len(larik_terurut) - 1
    target_str = str(target)

    while lo <= hi:
        mid = (lo + hi) // 2
        pencacah.tambah_perbandingan(1)
        val = str(_ambil_kunci(larik_terurut[mid], kunci))
        if val == target_str:
            return mid, pencacah.perbandingan
        elif val < target_str:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1, pencacah.perbandingan
