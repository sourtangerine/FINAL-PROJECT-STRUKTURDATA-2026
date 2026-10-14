# tools/benchmark_m2.py – Benchmark antrean naif vs antrean melingkar untuk Milestone 2
import time
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from loader import baca_pesanan
from backend.m2_antrean import AntreanNaif, AntreanMelingkar

def jalankan_benchmark_m2():
    print("Memuat data pesanan...")
    data = baca_pesanan()
    antre = [r for r in data if r.get('status') == 'ANTRE']
    n_antre = len(antre)
    print(f"Data ANTRE: {n_antre} pesanan.")

    # ── 1. Benchmark Enqueue ───────────────────────────────────────────────
    qn = AntreanNaif()
    qc = AntreanMelingkar(K=32768)

    t0 = time.perf_counter()
    for r in antre:
        qn.enqueue(r)
    t_enq_naif = (time.perf_counter() - t0) * 1000

    t0 = time.perf_counter()
    for r in antre:
        qc.enqueue(r)
    t_enq_circ = (time.perf_counter() - t0) * 1000

    print(f"Enqueue {n_antre} pesanan:")
    print(f"  Naif     : {t_enq_naif:.2f} ms")
    print(f"  Circular : {t_enq_circ:.2f} ms")

    # ── 2. Benchmark Dequeue 1 kali ────────────────────────────────────────
    qn1 = AntreanNaif()
    qc1 = AntreanMelingkar(K=32768)
    for r in antre:
        qn1.enqueue(r)
        qc1.enqueue(r)

    t0 = time.perf_counter()
    qn1.dequeue()
    t_deq1_naif = (time.perf_counter() - t0) * 1000
    geser1_naif = qn1.total_geser

    t0 = time.perf_counter()
    qc1.dequeue()
    t_deq1_circ = (time.perf_counter() - t0) * 1000
    geser1_circ = qc1.total_geser

    print(f"\nDequeue 1 kali:")
    print(f"  Naif     : {t_deq1_naif:.4f} ms, {geser1_naif:,} geseran")
    print(f"  Circular : {t_deq1_circ:.4f} ms, {geser1_circ:,} geseran")

    # ── 3. Benchmark Dequeue 100 kali ──────────────────────────────────────
    qn100 = AntreanNaif()
    qc100 = AntreanMelingkar(K=32768)
    for r in antre:
        qn100.enqueue(r)
        qc100.enqueue(r)

    t0 = time.perf_counter()
    for _ in range(100):
        qn100.dequeue()
    t_deq100_naif = (time.perf_counter() - t0) * 1000
    geser100_naif = qn100.total_geser

    t0 = time.perf_counter()
    for _ in range(100):
        qc100.dequeue()
    t_deq100_circ = (time.perf_counter() - t0) * 1000
    geser100_circ = qc100.total_geser

    print(f"\nDequeue 100 kali:")
    print(f"  Naif     : {t_deq100_naif:.2f} ms, {geser100_naif:,} geseran")
    print(f"  Circular : {t_deq100_circ:.4f} ms, {geser100_circ:,} geseran")

    print("\n" + "=" * 80)
    print("TABEL MARKDOWN BENCHMARK QUEUE (UNTUK README):")
    print("=" * 80)
    print("| Operasi | Antrean Naif (Geseran) | Waktu Naif (ms) | Antrean Melingkar (Geseran) | Waktu Melingkar (ms) |")
    print("|---|---|---|---|---|")
    print(f"| Enqueue {n_antre:,} pesanan | 0 | {t_enq_naif:.2f}".replace(',', '.') + f" | 0 | {t_enq_circ:.2f} |".replace('.', ','))
    print(f"| Dequeue 1 pesanan | {geser1_naif:,}".replace(',', '.') + f" | {t_deq1_naif:.2f}".replace('.', ',') + f" | 0 | {t_deq1_circ:.4f} |".replace('.', ','))
    print(f"| Dequeue 100 pesanan | {geser100_naif:,}".replace(',', '.') + f" | {t_deq100_naif:.2f}".replace('.', ',') + f" | 0 | {t_deq100_circ:.4f} |".replace('.', ','))

if __name__ == '__main__':
    jalankan_benchmark_m2()
