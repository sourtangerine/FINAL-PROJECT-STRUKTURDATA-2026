# 2EZ4U Food Delivery Engine

**Proyek Akhir EC234303 — Struktur Data & Analisa Algoritma**
Departemen Teknik Komputer, FTEIC-ITS

## Cara Menjalankan

```bash
python app.py
```

Pastikan Python 3.11+ dan Tkinter tersedia. Klik **Load** terlebih dahulu.

## Struktur Repositori

```
2EZ4U/
├── app.py               # titik masuk
├── loader.py            # pembaca CSV (tanpa modul csv)
├── data/
│   ├── pesanan.csv      # 200.000 baris pesanan
│   └── peta.csv         # graf pengiriman
├── backend/
│   ├── m1_pesanan.py    # Array dinamis + Linked list
│   ├── m2_antrean.py    # Stack, Queue naif, Queue melingkar, Undo/Redo
│   ├── m3_laporan.py    # Insertion sort, Merge sort, Linear search, Binary search
│   ├── m4_pencarian.py  # Hash table (open addressing)
│   ├── m5_katalog.py    # BST (Katalog) + MinHeap
│   └── m6_peta.py       # Graf + BFS + Dijkstra
└── frontend/
    └── ui.py            # Tkinter UI
```

## Ringkasan Milestone

| # | Fitur | Struktur Data | Kompleksitas |
|---|---|---|---|
| M1 | Array vs Linked List | Array dinamis (2x growth), Singly Linked List | get O(1)/O(n), VIP O(n)/O(1) |
| M2 | Stack & Queue | LIFO stack, Queue naif, Circular buffer, Undo/Redo | enqueue O(1), dequeue O(n)/O(1) |
| M3 | Sort & Search | Insertion sort, Merge sort, Linear, Binary search | O(n²)/O(n log n), O(n)/O(log n) |
| M4 | Hash Table | Open addressing (linear probing), load factor 0.7 | put/get O(1) amortized |
| M5 | BST + MinHeap | Binary Search Tree (harga), Min-Heap (prioritas) | rentang O(k+log n), pop O(log n) |
| M6 | Graf + BFS + Dijkstra | Adjacency list manual, BFS, Dijkstra | O(V+E), O((V+E) log V) |

## Aturan yang Dipatuhi

- Tidak menggunakan `dict`, `set`, `sorted`, `.sort()`, `heapq`, `bisect`, `collections.*`
- Array dinamis dibangun dari `list` Python sebagai array primitif
- Semua struktur data diimplementasi dari nol

## Catatan Teknis

- **CSV parsing** dilakukan manual (menangani field ber-quote seperti `"Oskar Puspita, S.Sos"`)
- **Circular queue** menggunakan `count` untuk membedakan keadaan kosong dan penuh
- **Hash table** tumbuh 2x saat load factor > 0.7
- **Binary search** membutuhkan larik terurut — dibangun sekali dengan merge sort
