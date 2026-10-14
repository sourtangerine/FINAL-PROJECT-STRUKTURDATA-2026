# tests/test_m1.py – Pengujian Milestone 1: Array dinamis vs Linked List
import unittest
from backend.m1_pesanan import Array, LinkList

class TestM1Pesanan(unittest.TestCase):
    def test_array_basic(self):
        arr = Array()
        self.assertEqual(len(arr), 0)
        arr.append(10)
        arr.append(20)
        self.assertEqual(len(arr), 2)
        self.assertEqual(arr.get(0), 10)
        self.assertEqual(arr.get(1), 20)
        self.assertEqual(arr.to_list(), [10, 20])

    def test_array_grow(self):
        arr = Array()
        for i in range(20):
            arr.append(i)
        self.assertEqual(len(arr), 20)
        for i in range(20):
            self.assertEqual(arr.get(i), i)

    def test_array_prioritas_vip_reguler(self):
        arr = Array()
        # Reguler di belakang
        arr.tambah_reguler('R1')
        arr.tambah_reguler('R2')
        # VIP di paling depan (indeks 0)
        arr.tambah_vip('V1')
        # Prioritas di tengah (n // 2)
        arr.tambah_prioritas('P1')
        # [V1, R1, R2] -> len 3 -> n//2 = 1 -> [V1, P1, R1, R2]
        self.assertEqual(arr.to_list(), ['V1', 'P1', 'R1', 'R2'])

    def test_array_hapus(self):
        arr = Array()
        arr.append('A')
        arr.append('B')
        arr.append('C')
        val = arr.hapus(1)
        self.assertEqual(val, 'B')
        self.assertEqual(arr.to_list(), ['A', 'C'])
        self.assertEqual(len(arr), 2)
        with self.assertRaises(IndexError):
            arr.hapus(10)

    def test_linklist_basic(self):
        ll = LinkList()
        self.assertEqual(len(ll), 0)
        ll.tambah_reguler(100)
        ll.tambah_reguler(200)
        self.assertEqual(len(ll), 2)
        self.assertEqual(ll.get(0), 100)
        self.assertEqual(ll.get(1), 200)
        self.assertEqual(ll.to_list(), [100, 200])

    def test_linklist_prioritas_vip_reguler(self):
        ll = LinkList()
        ll.tambah_reguler('R1')
        ll.tambah_reguler('R2')
        ll.tambah_vip('V1')
        ll.tambah_prioritas('P1')
        self.assertEqual(ll.to_list(), ['V1', 'P1', 'R1', 'R2'])

    def test_linklist_hapus(self):
        ll = LinkList()
        ll.tambah_reguler('A')
        ll.tambah_reguler('B')
        ll.tambah_reguler('C')
        v = ll.hapus(1)
        self.assertEqual(v, 'B')
        self.assertEqual(ll.to_list(), ['A', 'C'])
        self.assertEqual(len(ll), 2)
        with self.assertRaises(IndexError):
            ll.hapus(5)

if __name__ == '__main__':
    unittest.main()
