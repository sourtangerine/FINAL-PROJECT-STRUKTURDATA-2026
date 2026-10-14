# 2EZ4U Food Delivery Engine

**Proyek Akhir EC234303 — Struktur Data & Analisa Algoritma**  
Departemen Teknik Komputer, FTEIC-ITS

## Cara Menjalankan

```bash
python app.py
```

Pastikan Python 3.11+ dan Tkinter tersedia. Klik **Load** terlebih dahulu untuk memuat 200.000 data pesanan ke dalam memori.

---

## Struktur Repositori

```
2ez4u/
|-- README.md            <- LAPORANMU
|
|-- data/
|   |-- peta.csv
|   |-- pesanan.csv
|
|-- backend/
|   |-- m1_pesanan.py    M1: Larik (array) + Rantai (linked list)
|   |-- m2_antrean.py    M2: AntreanMelingkar + Tumpukan (undo)
|   |-- m3_laporan.py    M3: insertion sort + binary search
|   |-- m4_pencarian.py  M4: PetaHash + merge sort
|   |-- m5_katalog.py    M5: Katalog (BST) + MinHeap (prioritas)
|   `-- m6_peta.py       M6: Peta (graf) + BFS + Dijkstra
|
|-- frontend/            <- ANTARMUKA
|   |-- ui.py
|
|-- app.py               "python app.py" main application
```

---

## Status Milestone

| # | Milestone | Struktur Data / Algoritma | Status |
|---|---|---|---|
| M1 | Data Pesanan | Array dinamis (2x growth) vs Singly Linked List | **SELESAI** |
| M2 | Stack & Queue | Tumpukan (Array M1), Queue Naif, Circular Buffer, Undo/Redo | **SELESAI** |
| M3 | Sort & Search | Insertion Sort O(n²), Merge Sort O(n log n), Linear & Binary Search | **SELESAI** |
| M4 | Hash Table | Open addressing, Linear Probing | *Coming Soon* |
| M5 | BST & MinHeap | Binary Search Tree, Priority Queue | *Coming Soon* |
| M6 | Graf & Rute | Graf Berbobot, BFS, Algoritma Dijkstra | *Coming Soon* |

---

## Aturan Keras yang Dipatuhi

- **Tanpa struktur data bawaan tingkat tinggi**: Seluruh kode `backend/` tidak menggunakan `dict`, `set`, `sorted()`, `.sort()`, `heapq`, `bisect`, `collections.*`, literal `{}`, maupun comprehension dict/set.
- **Implementasi dari nol**: Menggunakan `list` Python semata-mata sebagai array primitif berkapasitas tetap `[None] * K` atau di atas `Array` dinamis buatan sendiri dari M1.
- **Deterministik**: Seluruh perbandingan dan pergeseran dihitung menggunakan objek `Pencacah` eksplisit.
- **Format Lokal**: Tampilan antarmuka mengikuti format Indonesia (pemisah ribuan titik `19.852`, desimal koma `0,09 ms`, mata uang `Rp 48.000`).

---

## Milestone 2: Stack & Queue

### 1. Diagram Antrean Melingkar (Circular Buffer)

```
        front = 2                      rear = 5
           │                              │
           ▼                              ▼
 ┌──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┐
 │ None │ None │ P_03 │ P_04 │ P_05 │ None │ None │ None │  (Kapasitas K = 8, count = 3)
 └──────┴──────┴──────┴──────┴──────┴──────┴──────┴──────┘
    0      1      2      3      4      5      6      7
                  ▲                    │
                  └────── dequeue ◄────┘ (elemen masuk di rear, keluar di front)
```

### 2. Alasan Wajib Menggunakan `count`
Pada circular buffer, kondisi `front == rear` terjadi pada **dua keadaan yang berlawanan**:
1. Saat antrean **kosong**: `front == rear` dan `count == 0`.
2. Saat antrean **penuh**: `front == rear` dan `count == K`.

Jika hanya mengandalkan penunjuk `front == rear` tanpa variabel `count`, buffer tidak dapat membedakan apakah antrean kosong atau penuh tanpa mengorbankan satu slot penyimpanan (`K - 1`). Dengan atribut `count`, seluruh slot array dapat dimanfaatkan 100% dan kondisi `is_empty()` didefinisikan secara tegas melalui `count == 0`.

### 3. Keputusan Desain: Enqueue Saat Penuh Tumbuh 2x
Alih-alih menolak pesanan atau menimpa data lama (yang berbahaya bagi pesanan makanan), `AntreanMelingkar` dirancang dengan kemampuan tumbuh dinamis 2 kali lipat saat `count == K`. Elemen disalin secara terurut mulai dari indeks `front` ke array baru berukuran `2 * K`, lalu `front` diatur ulang ke `0` dan `rear` ke `count`. Keputusan ini menjamin operasi `enqueue` tetap memiliki kompleksitas teramortisasi $O(1)$.

### 4. Desain Manajer Riwayat (Undo/Redo)
- Menggunakan dua `Tumpukan` mandiri: tumpukan `undo` dan tumpukan `redo`.
- **Aksi baru mengosongkan redo**: Setiap pemanggilan `enqueue` atau `dequeue` baru membersihkan tumpukan `redo`.
- **Menyimpan data utuh**: Saat `dequeue` dilakukan, seluruh daftar pesanan yang keluar disimpan ke tumpukan undo (bukan hanya hitungan angka).
- **Inversi Presisi**:
  - `UNDO ENQUEUE`: Menghapus kembali pesanan dari ujung belakang kedua antrean via `pop_rear()`.
  - `UNDO DEQUEUE`: Mengembalikan seluruh pesanan ke posisi **DEPAN** antrean via `push_front_many(daftar)` dengan urutan asli terjaga.
  - `REDO`: Menjalankan kembali aksi aslinya (bukan membalik kebalikan).

### 5. Hasil Benchmark Antrean (19.850 Pesanan ANTRE)

| Operasi | Antrean Naif (Geseran) | Waktu Naif (ms) | Antrean Melingkar (Geseran) | Waktu Melingkar (ms) |
|---|---|---|---|---|
| **Enqueue 19.850 pesanan** | 0 | 6,58 ms | 0 | 3,28 ms |
| **Dequeue 1 pesanan** | 19.849 | 3,97 ms | 0 | 0,0121 ms |
| **Dequeue 100 pesanan** | 1.979.950 | 238,91 ms | 0 | 0,0330 ms |

> **Analisis:** Pada `enqueue`, kedua antrean sama-sama murah ($O(1)$). Namun pada `dequeue`, antrean naif memaksa seluruh sisa elemen bergeser satu langkah ke kiri ($O(n)$), menghasilkan hampir 2 juta geseran untuk 100 dequeue. Antrean melingkar hanya memajukan penunjuk `front` ($O(1)$) tanpa pergeseran elemen sama sekali (7.000x lebih cepat).

### Dokumentasi Visual M2
- Screenshot UI M2: `docs/screenshots/m2_demo.png` *(placeholder)*
- Rekaman Video M2: `docs/videos/m2_walkthrough.mp4` *(placeholder)*

---

## Milestone 3: Sort & Search

### 1. Hasil Benchmark Pengurutan (Kunci: `harga`)

Diuji pada variasi $n = 500$ hingga $16.000$ baris, serta pengujian $200.000$ baris penuh untuk Merge Sort:

| n | Insertion Sort (Cmp) | Insertion Sort (Mv) | Waktu Ins (ms) | Merge Sort (Cmp) | Merge Sort (Mv) | Waktu Mrg (ms) |
|---|---|---|---|---|---|---|
| **500** | 55.847 | 55.849 | 20,39 ms | 3.829 | 4.488 | 2,77 ms |
| **1.000** | 233.802 | 233.804 | 86,77 ms | 8.650 | 9.976 | 6,11 ms |
| **2.000** | 962.430 | 962.432 | 361,61 ms | 19.240 | 21.952 | 14,38 ms |
| **4.000** | 3.831.520 | 3.831.522 | 1.983,36 ms | 42.355 | 47.904 | 49,06 ms |
| **8.000** | 15.058.881 | 15.058.883 | 13.535,80 ms | 92.616 | 103.808 | 108,44 ms |
| **16.000** | 60.049.240 | 60.049.242 | 43.798,36 ms | 200.936 | 223.616 | 239,71 ms |
| **200.000** | *DITOLAK (>20k)* | - | - | 3.226.139 | 3.537.856 | 3.913,52 ms |

> Grafik visual perbandingan dapat dilihat pada berkas [docs/grafik_sort.svg](docs/grafik_sort.svg).

### 2. Pola Pertumbuhan Kompleksitas
- **Insertion Sort ($O(n^2)$)**: Setiap kali $n$ dilipatduakan ($500 \to 1.000 \to 2.000 \to 4.000$), jumlah perbandingan meningkat sekitar **4 kali lipat** ($4{,}18\times \to 4{,}11\times \to 3{,}98\times \to 3{,}93\times$).
- **Merge Sort ($O(n \log n)$)**: Setiap kali $n$ dilipatduakan, jumlah perbandingan hanya meningkat sekitar **2,2 kali lipat** ($2{,}25\times \to 2{,}22\times \to 2{,}20\times \to 2{,}18\times$).

### 3. Hasil Benchmark Pencarian (Data Penuh: 200.000 Baris)

| Target OID | Posisi Data | Linear Search (Cmp) | Waktu Linear | Binary Search (Cmp) | Waktu Binary | Ongkos Bangun Indeks |
|---|---|---|---|---|---|---|
| `O-000001` | Paling Awal | 1 | 0,02 ms | 17 | 0,027 ms | 2.200,72 ms |
| `O-100000` | Tengah | 100.000 | 43,61 ms | 1 | 0,010 ms | 2.200,72 ms |
| `O-137442` | Acuan Spec | 137.442 | 63,90 ms | 17 | 0,031 ms | 2.200,72 ms |
| `O-199999` | Paling Akhir | 199.999 | 87,68 ms | 17 | 0,029 ms | 2.200,72 ms |
| `O-999999` | Tidak Ada | 200.000 | 85,60 ms | 18 | 0,029 ms | 2.200,72 ms |

### 4. Alasan Pemilihan Algoritma
1. **Insertion Sort**:
   - *Kapan tepat digunakan*: Pada data berukuran kecil ($n \le 50$) atau data yang sudah hampir terurut (nearly sorted). Sangat hemat memori karena bekerja langsung di tempat (*in-place*, $O(1)$ memori tambahan).
   - *Kapan ditolak*: Pada data besar ($n > 20.000$), biaya kuadratik $O(n^2)$ menyebabkan komputasi membutuhkan puluhan menit dan membekukan aplikasi. Oleh karena itu, form membatasi maksimal 20.000 baris.
2. **Merge Sort**:
   - *Kapan wajib digunakan*: Untuk pengurutan data dalam skala besar ($n = 200.000$). Memiliki jaminan batas atas performa terbaik $O(n \log n)$ dalam semua skenario (best, average, worst case) dan menjaga stabilitas data.
3. **Linear Search vs Binary Search**:
   - *Kapan Linear Search lebih masuk akal*: Jika pencarian hanya dilakukan **satu atau dua kali saja** pada data yang belum terurut. Membangun indeks terurut dengan Merge Sort membutuhkan waktu sekitar ~2.200 ms, sedangkan satu kali Linear Search rata-rata hanya butuh ~43 ms.
   - *Kapan Binary Search wajib*: Jika pencarian dilakukan berulang kali (*frequent queries*). Sekali indeks terurut dibangun, setiap pencarian berikutnya hanya membutuhkan maksimal $\lfloor \log_2(200.000) \rfloor + 1 = 18$ perbandingan ($< 0{,}03$ ms).

### 5. Pembuktian Stabilitas Pengurutan
Kestabilan (*stability*) berarti dua pesanan yang memiliki nilai kunci sama akan tetap mempertahankan urutan kedatangan aslinya.
- **Insertion Sort**: Kondisi pergeseran menggunakan operator lebih besar tegas (`>`), bukan `>=`. Jika nilainya sama, pergeseran langsung berhenti, sehingga elemen pertama tidak dilewati oleh elemen kedua.
- **Merge Sort**: Kondisi penggabungan menggunakan operator lebih kecil sama dengan (`<=`), mendahulukan elemen dari sub-array kiri saat nilai kuncinya identik.
- **Verifikasi**: Pesanan `O-000002` dan `O-000009` sama-sama memiliki harga Rp 11.000. Kedua algoritma terbukti menghasilkan urutan yang identik baris per baris, di mana `O-000002` selalu mendahului `O-000009`.

### Dokumentasi Visual M3
- Screenshot UI M3: `docs/screenshots/m3_demo.png` *(placeholder)*
- Rekaman Video M3: `docs/videos/m3_walkthrough.mp4` *(placeholder)*
