# tests/test_m3.py – Pengujian Milestone 3: Insertion sort, Merge sort, Linear search, Binary search
import unittest
import math
from backend.m3_laporan import (
    Pencacah, insertion_sort, merge_sort, linear_search, binary_search
)
from loader import baca_pesanan

class TestM3Sort(unittest.TestCase):
    def test_stabilitas_dan_kesetaraan(self):
        # Dua pesanan dengan harga yang sama (11.000): O-000002 dan O-000009
        data = baca_pesanan()[:10]
        # Salin data untuk insertion sort dan merge sort
        data_ins = [dict(x) for x in data]
        data_merge = [dict(x) for x in data]

        cmp_ins, mv_ins = insertion_sort(data_ins, 'harga')
        res_merge, cmp_mrg, mv_mrg = merge_sort(data_merge, 'harga')

        # Acuan spec: 10 baris pertama kunci harga -> 24 perbandingan, 25 pemindahan
        self.assertEqual(cmp_ins, 24)
        self.assertEqual(mv_ins, 25)

        # Stabilitas: O-000002 tetap mendahului O-000009
        idx2_ins = [i for i, x in enumerate(data_ins) if x['oid'] == 'O-000002'][0]
        idx9_ins = [i for i, x in enumerate(data_ins) if x['oid'] == 'O-000009'][0]
        self.assertLess(idx2_ins, idx9_ins)

        idx2_mrg = [i for i, x in enumerate(res_merge) if x['oid'] == 'O-000002'][0]
        idx9_mrg = [i for i, x in enumerate(res_merge) if x['oid'] == 'O-000009'][0]
        self.assertLess(idx2_mrg, idx9_mrg)

        # Hasil insertion sort dan merge sort identik baris per baris
        self.assertEqual(len(data_ins), len(res_merge))
        for i in range(len(data_ins)):
            self.assertEqual(data_ins[i]['oid'], res_merge[i]['oid'])
            self.assertEqual(data_ins[i]['harga'], res_merge[i]['harga'])

    def test_kasus_ekstrem_sort(self):
        # Kosong
        cmp_i, mv_i = insertion_sort([])
        self.assertEqual(cmp_i, 0)
        self.assertEqual(mv_i, 0)

        res_m, cmp_m, mv_m = merge_sort([])
        self.assertEqual(res_m, [])
        self.assertEqual(cmp_m, 0)

        # Satu elemen (tidak ada pergeseran)
        one_ins = [{'oid': 'O-1', 'harga': 5000}]
        cmp_i, mv_i = insertion_sort(one_ins, 'harga')
        self.assertEqual(cmp_i, 0)
        self.assertEqual(mv_i, 0)

        one_mrg = [{'oid': 'O-1', 'harga': 5000}]
        res_m, cmp_m, mv_m = merge_sort(one_mrg, 'harga')
        self.assertEqual(len(res_m), 1)

        # Sudah terurut, terbalik, duplikat, ukuran ganjil
        rev_data = [{'oid': f'O-{i}', 'harga': 100 - i} for i in range(5)]
        res_rev, _, _ = merge_sort(rev_data, 'harga')
        self.assertEqual([x['harga'] for x in res_rev], [96, 97, 98, 99, 100])

        # Verifikasi tidak ada elemen yang hilang
        self.assertEqual(len(res_rev), 5)

    def test_penolakan_insertion_sort_terlalu_besar(self):
        big_data = [{'oid': 'O-1', 'harga': 1000}] * 20001
        with self.assertRaises(ValueError):
            insertion_sort(big_data, 'harga')

    def test_pola_pertumbuhan(self):
        data = baca_pesanan()
        d500 = [dict(x) for x in data[:500]]
        d1000 = [dict(x) for x in data[:1000]]

        # Insertion sort pada n=500 dan n=1000 -> rasio mendekati 4x
        c500_i, _ = insertion_sort(d500, 'harga')
        c1000_i, _ = insertion_sort(d1000, 'harga')
        ratio_i = c1000_i / c500_i
        self.assertTrue(3.2 <= ratio_i <= 4.8, f"Rasio insertion sort {ratio_i} tidak mendekati 4x")

        # Merge sort pada n=500 dan n=1000 -> rasio mendekati 2x
        d500_m = [dict(x) for x in data[:500]]
        d1000_m = [dict(x) for x in data[:1000]]
        _, c500_m, _ = merge_sort(d500_m, 'harga')
        _, c1000_m, _ = merge_sort(d1000_m, 'harga')
        ratio_m = c1000_m / c500_m
        self.assertTrue(1.7 <= ratio_m <= 2.5, f"Rasio merge sort {ratio_m} tidak mendekati 2x")


class TestM3Search(unittest.TestCase):
    def setUp(self):
        self.data = baca_pesanan()[:100]

    def test_linear_search(self):
        # Awal (indeks 0 -> 1 perbandingan)
        idx_0, cmp_0 = linear_search(self.data, 'O-000001')
        self.assertEqual(idx_0, 0)
        self.assertEqual(cmp_0, 1)

        # Tengah
        idx_50, cmp_50 = linear_search(self.data, 'O-000051')
        self.assertEqual(idx_50, 50)
        self.assertEqual(cmp_50, 51)

        # Akhir (indeks 99 -> 100 perbandingan)
        idx_99, cmp_99 = linear_search(self.data, 'O-000100')
        self.assertEqual(idx_99, 99)
        self.assertEqual(cmp_99, 100)

        # Tidak ada (perbandingan = len(A))
        idx_none, cmp_none = linear_search(self.data, 'O-999999')
        self.assertEqual(idx_none, -1)
        self.assertEqual(cmp_none, len(self.data))

    def test_binary_search(self):
        # Bangun data terurut
        sorted_data, _, _ = merge_sort(self.data, 'oid')

        # Larik kosong
        idx_empty, cmp_empty = binary_search([], 'O-000001')
        self.assertEqual(idx_empty, -1)
        self.assertEqual(cmp_empty, 0)

        # Cari target di tengah, kiri, kanan, tidak ada
        n = len(sorted_data)
        max_cmp = int(math.floor(math.log2(n))) + 1

        targets = ['O-000050', 'O-000001', 'O-000100', 'O-999999']
        for t in targets:
            idx, cmp_cnt = binary_search(sorted_data, t)
            self.assertLessEqual(cmp_cnt, max_cmp, f"Perbandingan {cmp_cnt} melebihi log2(n)+1 {max_cmp}")
            if t == 'O-999999':
                self.assertEqual(idx, -1)
            else:
                self.assertNotEqual(idx, -1)
                self.assertEqual(sorted_data[idx]['oid'], t)

if __name__ == '__main__':
    unittest.main()
