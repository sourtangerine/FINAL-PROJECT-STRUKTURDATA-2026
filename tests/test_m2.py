# tests/test_m2.py – Pengujian Milestone 2: Stack, Queue naif & circular, Undo/Redo
import unittest
from backend.m2_antrean import (
    Tumpukan, Stack, ke_postfix, hitung, AntreanNaif, AntreanMelingkar, UndoRedo
)

class TestM2Stack(unittest.TestCase):
    def test_stack_basic(self):
        s = Tumpukan()
        self.assertTrue(s.kosong())
        self.assertEqual(len(s), 0)
        self.assertIsNone(s.pop())
        self.assertIsNone(s.peek())

        s.push(10)
        s.push(20)
        self.assertFalse(s.kosong())
        self.assertEqual(len(s), 2)
        self.assertEqual(s.peek(), 20)
        self.assertEqual(s.pop(), 20)
        self.assertEqual(s.pop(), 10)
        self.assertIsNone(s.pop())
        self.assertTrue(s.kosong())


class TestM2Postfix(unittest.TestCase):
    def test_empat_ekspresi(self):
        # 1. Tanpa kurung
        p1, _ = ke_postfix("3 * 1000 + 500")
        self.assertEqual(' '.join(p1), "3 1000 * 500 +")
        r1, _ = hitung(p1)
        self.assertEqual(r1, 3500)

        # 2. Berkurung (Contoh Wajib)
        p2, steps2 = ke_postfix("( 3 * 12000 ) + ( 2 * 8500 ) - 5000")
        self.assertEqual(' '.join(p2), "3 12000 * 2 8500 * + 5000 -")
        r2, _ = hitung(p2)
        self.assertEqual(r2, 48000)
        # Pastikan tidak ada kurung di output postfix
        self.assertNotIn('(', p2)
        self.assertNotIn(')', p2)

        # 3. Ada '-' beruntun
        p3, _ = ke_postfix("10 - 2 - 3")
        self.assertEqual(' '.join(p3), "10 2 - 3 -")
        r3, _ = hitung(p3)
        self.assertEqual(r3, 5)

        # 4. Kurung bersarang
        p4, _ = ke_postfix("8 - ( 3 - 1 )")
        self.assertEqual(' '.join(p4), "8 3 1 - -")
        r4, _ = hitung(p4)
        self.assertEqual(r4, 6)

    def test_evaluasi_khusus(self):
        # Pembagian beruntun
        p, _ = ke_postfix("100 / 5 / 2")
        r, _ = hitung(p)
        self.assertEqual(r, 10)

        # Ekspresi tanpa spasi
        p_nospc, _ = ke_postfix("(3*12000)+(2*8500)-5000")
        self.assertEqual(' '.join(p_nospc), "3 12000 * 2 8500 * + 5000 -")
        r_nospc, _ = hitung(p_nospc)
        self.assertEqual(r_nospc, 48000)

        # Pembagian dengan nol
        p_divzero, _ = ke_postfix("10 / 0")
        with self.assertRaises(ZeroDivisionError):
            hitung(p_divzero)

        # Minus unary ditolak ramah
        with self.assertRaises(ValueError):
            ke_postfix("-5000 + 1000")

        # Kurung tidak seimbang
        with self.assertRaises(ValueError):
            ke_postfix("( 3 * 1000")
        with self.assertRaises(ValueError):
            ke_postfix("3 * 1000 )")


class TestM2Queue(unittest.TestCase):
    def test_antrean_naif(self):
        q = AntreanNaif()
        self.assertEqual(len(q), 0)
        self.assertIsNone(q.dequeue())

        q.enqueue('A')
        q.enqueue('B')
        q.enqueue('C')
        self.assertEqual(len(q), 3)

        # Dequeue 'A', geser 2 elemen (B dan C)
        v1 = q.dequeue()
        self.assertEqual(v1, 'A')
        self.assertEqual(q.last_geser, 2)
        self.assertEqual(q.total_geser, 2)

        # Dequeue 'B', geser 1 elemen (C)
        v2 = q.dequeue()
        self.assertEqual(v2, 'B')
        self.assertEqual(q.last_geser, 1)
        self.assertEqual(q.total_geser, 3)

        v3 = q.dequeue()
        self.assertEqual(v3, 'C')
        self.assertEqual(q.last_geser, 0)
        self.assertEqual(q.total_geser, 3)

        self.assertIsNone(q.dequeue())

    def test_antrean_melingkar_k4_wraparound(self):
        # Uji terpenting M2: K=4, masukkan 3, keluarkan 2, masukkan 3 lagi
        q = AntreanMelingkar(K=4)
        self.assertTrue(q.kosong())

        # Masukkan 3
        q.enqueue('P1')
        q.enqueue('P2')
        q.enqueue('P3')
        self.assertEqual(len(q), 3)
        self.assertEqual(q.front_idx, 0)
        self.assertEqual(q.rear_idx, 3)

        # Keluarkan 2
        self.assertEqual(q.dequeue(), 'P1')
        self.assertEqual(q.dequeue(), 'P2')
        self.assertEqual(len(q), 1)
        self.assertEqual(q.front_idx, 2)
        self.assertEqual(q.rear_idx, 3)

        # Masukkan 3 lagi (P4, P5, P6) - penunjuk berputar (wraparound)
        q.enqueue('P4')  # rear -> 0
        q.enqueue('P5')  # rear -> 1
        q.enqueue('P6')  # rear -> 2 (atau grow bila mencapai kapasitas)
        # Total ada 4 elemen: P3, P4, P5, P6
        self.assertEqual(len(q), 4)

        # Pastikan isi dan urutan keluar tetap FIFO
        self.assertEqual(q.dequeue(), 'P3')
        self.assertEqual(q.dequeue(), 'P4')
        self.assertEqual(q.dequeue(), 'P5')
        self.assertEqual(q.dequeue(), 'P6')
        self.assertTrue(q.kosong())

    def test_antrean_melingkar_grow(self):
        q = AntreanMelingkar(K=2)
        q.enqueue('A')
        q.enqueue('B')
        self.assertEqual(q.kapasitas, 2)
        self.assertEqual(len(q), 2)

        # Enqueue ke-3 memicu _grow()
        q.enqueue('C')
        self.assertEqual(q.kapasitas, 4)
        self.assertEqual(len(q), 3)
        self.assertEqual(q.to_list(), ['A', 'B', 'C'])

    def test_kesetaraan_naif_dan_circular(self):
        qn = AntreanNaif()
        qc = AntreanMelingkar(K=4)

        items = [f"O-{i:06d}" for i in range(1, 20)]
        for item in items:
            qn.enqueue(item)
            qc.enqueue(item)

        out_n = []
        out_c = []
        for _ in range(len(items)):
            out_n.append(qn.dequeue())
            out_c.append(qc.dequeue())

        self.assertEqual(out_n, out_c)
        self.assertEqual(out_n, items)


class TestM2UndoRedo(unittest.TestCase):
    def test_undo_redo_enqueue(self):
        qn = AntreanNaif()
        qc = AntreanMelingkar(K=16)
        ur = UndoRedo(qn, qc)

        p1 = {'oid': 'O-200001', 'pelanggan': 'Ami'}
        qn.enqueue(p1)
        qc.enqueue(p1)
        ur.rekam_enqueue(p1)

        self.assertEqual(len(qn), 1)
        self.assertEqual(len(qc), 1)
        self.assertEqual(ur.undo_depth(), 1)
        self.assertEqual(ur.redo_depth(), 0)

        # Undo enqueue -> pesanan dikeluarkan dari belakang kedua antrean
        aksi, items, msg = ur.undo_last()
        self.assertEqual(aksi, 'ENQUEUE')
        self.assertEqual(len(qn), 0)
        self.assertEqual(len(qc), 0)
        self.assertEqual(ur.undo_depth(), 0)
        self.assertEqual(ur.redo_depth(), 1)

        # Redo enqueue -> pesanan dimasukkan kembali ke belakang kedua antrean
        aksi2, items2, msg2 = ur.redo_last()
        self.assertEqual(aksi2, 'ENQUEUE')
        self.assertEqual(len(qn), 1)
        self.assertEqual(len(qc), 1)
        self.assertEqual(ur.undo_depth(), 1)
        self.assertEqual(ur.redo_depth(), 0)

    def test_undo_redo_dequeue_dan_aksi_baru_mengosongkan_redo(self):
        qn = AntreanNaif()
        qc = AntreanMelingkar(K=16)
        ur = UndoRedo(qn, qc)

        p1 = {'oid': 'O-000001'}
        p2 = {'oid': 'O-000002'}
        qn.enqueue(p1)
        qn.enqueue(p2)
        qc.enqueue(p1)
        qc.enqueue(p2)

        # Dequeue dari naif
        d1 = qn.dequeue()
        ur.rekam_dequeue_naif([d1])
        self.assertEqual(len(qn), 1)

        # Undo dequeue naif -> item dikembalikan ke DEPAN antrean naif
        aksi, items, msg = ur.undo_last()
        self.assertEqual(len(qn), 2)
        self.assertEqual(qn.front()['oid'], 'O-000001')
        self.assertEqual(ur.redo_depth(), 1)

        # Aksi baru harus mengosongkan redo!
        p3 = {'oid': 'O-000003'}
        qn.enqueue(p3)
        qc.enqueue(p3)
        ur.rekam_enqueue(p3)
        self.assertEqual(ur.redo_depth(), 0)

        # Undo kosong & redo kosong mengembalikan pesan ramah
        ur2 = UndoRedo(AntreanNaif(), AntreanMelingkar())
        a_u, _, msg_u = ur2.undo_last()
        self.assertIsNone(a_u)
        self.assertIn("kosong", msg_u.lower())

        a_r, _, msg_r = ur2.redo_last()
        self.assertIsNone(a_r)
        self.assertIn("kosong", msg_r.lower())

if __name__ == '__main__':
    unittest.main()
