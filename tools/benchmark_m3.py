# tools/benchmark_m3.py – Benchmark pengurutan dan pencarian untuk Milestone 3
import time
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from loader import baca_pesanan
from backend.m3_laporan import insertion_sort, merge_sort, linear_search, binary_search

DOCS_DIR = os.path.join(os.path.dirname(__file__), '..', 'docs')
os.makedirs(DOCS_DIR, exist_ok=True)

def jalankan_benchmark():
    print("Memuat seluruh 200.000 data pesanan...")
    t0 = time.perf_counter()
    data = baca_pesanan()
    print(f"Data selesai dimuat dalam {time.perf_counter() - t0:.2f} detik ({len(data)} baris).")

    # ── 1. Benchmark Pengurutan (Insertion vs Merge Sort) ───────────────────
    n_list = [500, 1000, 2000, 4000, 8000, 16000]
    hasil_sort = []

    print("\n--- Menjalankan Benchmark Sort (Kunci: harga) ---")
    for n in n_list:
        sub_ins = [dict(x) for x in data[:n]]
        sub_mrg = [dict(x) for x in data[:n]]

        # Insertion Sort
        t_ins0 = time.perf_counter()
        cmp_ins, mv_ins = insertion_sort(sub_ins, 'harga')
        t_ins = (time.perf_counter() - t_ins0) * 1000

        # Merge Sort
        t_mrg0 = time.perf_counter()
        _, cmp_mrg, mv_mrg = merge_sort(sub_mrg, 'harga')
        t_mrg = (time.perf_counter() - t_mrg0) * 1000

        hasil_sort.append({
            'n': n,
            'cmp_ins': cmp_ins,
            'mv_ins': mv_ins,
            't_ins_ms': t_ins,
            'cmp_mrg': cmp_mrg,
            'mv_mrg': mv_mrg,
            't_mrg_ms': t_mrg
        })
        print(f"n = {n:5d} | Ins: {cmp_ins:10d} cmp, {t_ins:8.2f} ms | Mrg: {cmp_mrg:10d} cmp, {t_mrg:8.2f} ms")

    # Merge sort untuk 200.000 baris penuh
    print("Menjalankan Merge Sort untuk 200.000 baris penuh...")
    sub_full = [dict(x) for x in data]
    t_mrg200k0 = time.perf_counter()
    _, cmp_200k, mv_200k = merge_sort(sub_full, 'harga')
    t_200k = (time.perf_counter() - t_mrg200k0) * 1000

    hasil_sort.append({
        'n': 200000,
        'cmp_ins': "DITOLAK (>20k)",
        'mv_ins': "-",
        't_ins_ms': "-",
        'cmp_mrg': cmp_200k,
        'mv_mrg': mv_200k,
        't_mrg_ms': t_200k
    })
    print(f"n = 200.000 | Ins: DITOLAK (>20k) | Mrg: {cmp_200k:10d} cmp, {t_200k:8.2f} ms")

    # ── 2. Benchmark Pencarian (Linear vs Binary Search) ────────────────────
    print("\n--- Menjalankan Benchmark Search (Kunci: oid) ---")
    print("Membangun indeks terurut-oid dengan Merge Sort...")
    t_idx0 = time.perf_counter()
    data_sorted_oid, _, _ = merge_sort(data, 'oid')
    t_build_idx = (time.perf_counter() - t_idx0) * 1000
    print(f"Indeks terurut-oid selesai dibangun dalam {t_build_idx:.2f} ms.")

    target_oids = ['O-000001', 'O-100000', 'O-137442', 'O-199999', 'O-999999']
    hasil_search = []

    for target in target_oids:
        # Linear Search
        t_lin0 = time.perf_counter()
        idx_lin, cmp_lin = linear_search(data, target, 'oid')
        t_lin = (time.perf_counter() - t_lin0) * 1000

        # Binary Search
        t_bin0 = time.perf_counter()
        idx_bin, cmp_bin = binary_search(data_sorted_oid, target, 'oid')
        t_bin = (time.perf_counter() - t_bin0) * 1000

        hasil_search.append({
            'target': target,
            'posisi': 'Awal' if target == 'O-000001' else ('Tengah' if target == 'O-100000' else ('Spesifik' if target == 'O-137442' else ('Akhir' if target == 'O-199999' else 'Tidak Ada'))),
            'idx': idx_lin,
            'cmp_lin': cmp_lin,
            't_lin_ms': t_lin,
            'cmp_bin': cmp_bin,
            't_bin_ms': t_bin,
            't_build_idx_ms': t_build_idx
        })
        print(f"Target: {target:<8} | Linear: {cmp_lin:7d} cmp ({t_lin:6.2f} ms) | Binary: {cmp_bin:2d} cmp ({t_bin:6.4f} ms)")

    # ── 3. Tulis Hasil ke File CSV ──────────────────────────────────────────
    csv_sort_path = os.path.join(DOCS_DIR, 'benchmark_sort.csv')
    with open(csv_sort_path, 'w', encoding='utf-8') as f:
        f.write("n,cmp_insertion,mv_insertion,time_insertion_ms,cmp_merge,mv_merge,time_merge_ms\n")
        for row in hasil_sort:
            f.write(f"{row['n']},{row['cmp_ins']},{row['mv_ins']},{row['t_ins_ms']},{row['cmp_mrg']},{row['mv_mrg']},{row['t_mrg_ms']}\n")
    print(f"\nDisimpan ke {csv_sort_path}")

    csv_search_path = os.path.join(DOCS_DIR, 'benchmark_search.csv')
    with open(csv_search_path, 'w', encoding='utf-8') as f:
        f.write("target,posisi,indeks,cmp_linear,time_linear_ms,cmp_binary,time_binary_ms,time_build_index_ms\n")
        for row in hasil_search:
            f.write(f"{row['target']},{row['posisi']},{row['idx']},{row['cmp_lin']},{row['t_lin_ms']:.4f},{row['cmp_bin']},{row['t_bin_ms']:.4f},{row['t_build_idx_ms']:.2f}\n")
    print(f"Disimpan ke {csv_search_path}")

    # ── 4. Tampilkan Tabel Markdown untuk README ───────────────────────────
    print("\n" + "=" * 80)
    print("TABEL MARKDOWN BENCHMARK SORT (UNTUK README):")
    print("=" * 80)
    print("| n | Insertion Sort (Cmp) | Insertion Sort (Mv) | Waktu Ins (ms) | Merge Sort (Cmp) | Merge Sort (Mv) | Waktu Mrg (ms) |")
    print("|---|---|---|---|---|---|---|")
    for r in hasil_sort:
        c_i = f"{r['cmp_ins']:,}".replace(',', '.') if isinstance(r['cmp_ins'], int) else str(r['cmp_ins'])
        m_i = f"{r['mv_ins']:,}".replace(',', '.') if isinstance(r['mv_ins'], int) else str(r['mv_ins'])
        t_i = f"{r['t_ins_ms']:.2f}".replace('.', ',') if isinstance(r['t_ins_ms'], float) else str(r['t_ins_ms'])
        c_m = f"{r['cmp_mrg']:,}".replace(',', '.')
        m_m = f"{r['mv_mrg']:,}".replace(',', '.')
        t_m = f"{r['t_mrg_ms']:.2f}".replace('.', ',')
        n_str = f"{r['n']:,}".replace(',', '.')
        print(f"| {n_str} | {c_i} | {m_i} | {t_i} | {c_m} | {m_m} | {t_m} |")

    print("\n" + "=" * 80)
    print("TABEL MARKDOWN BENCHMARK SEARCH (UNTUK README):")
    print("=" * 80)
    print("| Target OID | Posisi Data | Linear Search (Cmp) | Waktu Linear | Binary Search (Cmp) | Waktu Binary | Ongkos Bangun Indeks |")
    print("|---|---|---|---|---|---|---|")
    for r in hasil_search:
        c_l = f"{r['cmp_lin']:,}".replace(',', '.')
        t_l = f"{r['t_lin_ms']:.2f} ms".replace('.', ',')
        c_b = f"{r['cmp_bin']}"
        t_b = f"{r['t_bin_ms']:.3f} ms".replace('.', ',')
        t_idx = f"{r['t_build_idx_ms']:.2f} ms".replace('.', ',')
        print(f"| {r['target']} | {r['posisi']} | {c_l} | {t_l} | {c_b} | {t_b} | {t_idx} |")

    # ── 5. Buat Diagram SVG untuk docs/grafik_sort.svg ──────────────────────
    svg_path = os.path.join(DOCS_DIR, 'grafik_sort.svg')
    _generate_sort_svg(hasil_sort[:-1], svg_path)
    print(f"Grafik visual SVG disimpan ke {svg_path}")

def _generate_sort_svg(data_sort, path):
    """Membuat file SVG grafik perbandingan Insertion Sort vs Merge Sort."""
    width, height = 750, 420
    padding_left, padding_bottom, padding_top, padding_right = 90, 60, 40, 40
    plot_w = width - padding_left - padding_right
    plot_h = height - padding_top - padding_bottom

    max_x = max(d['n'] for d in data_sort)
    max_y = max(d['cmp_ins'] for d in data_sort)

    def to_svg_x(val):
        return padding_left + (val / max_x) * plot_w

    def to_svg_y(val):
        return height - padding_bottom - (val / max_y) * plot_h

    pts_ins = " ".join(f"{to_svg_x(d['n']):.1f},{to_svg_y(d['cmp_ins']):.1f}" for d in data_sort)
    pts_mrg = " ".join(f"{to_svg_x(d['n']):.1f},{to_svg_y(d['cmp_mrg']):.1f}" for d in data_sort)

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" style="background-color:#ffffff; font-family:Arial,sans-serif;">',
        f'  <text x="{width//2}" y="25" text-anchor="middle" font-size="14" font-weight="bold" fill="#1c344d">Jumlah Perbandingan: Insertion Sort O(n²) vs Merge Sort O(n log n)</text>',
        # Grid lines
        f'  <line x1="{padding_left}" y1="{height-padding_bottom}" x2="{width-padding_right}" y2="{height-padding_bottom}" stroke="#cbd5e1" stroke-width="2"/>',
        f'  <line x1="{padding_left}" y1="{padding_top}" x2="{padding_left}" y2="{height-padding_bottom}" stroke="#cbd5e1" stroke-width="2"/>',
    ]

    # Y-axis labels
    for step in range(5):
        y_val = max_y * (step / 4)
        y_coord = to_svg_y(y_val)
        lbl = f"{int(y_val):,}".replace(',', '.')
        svg.append(f'  <line x1="{padding_left-5}" y1="{y_coord:.1f}" x2="{width-padding_right}" y2="{y_coord:.1f}" stroke="#f1f5f9" stroke-width="1"/>')
        svg.append(f'  <text x="{padding_left-10}" y="{y_coord+4:.1f}" text-anchor="end" font-size="10" fill="#64748b">{lbl}</text>')

    # X-axis labels
    for d in data_sort:
        x_coord = to_svg_x(d['n'])
        svg.append(f'  <line x1="{x_coord:.1f}" y1="{height-padding_bottom}" x2="{x_coord:.1f}" y2="{height-padding_bottom+5}" stroke="#94a3b8" stroke-width="1"/>')
        svg.append(f'  <text x="{x_coord:.1f}" y="{height-padding_bottom+18}" text-anchor="middle" font-size="10" fill="#64748b">{d["n"]:,}</text>')

    # Lines & Points
    svg.append(f'  <polyline fill="none" stroke="#dc2626" stroke-width="3" points="{pts_ins}"/>')
    svg.append(f'  <polyline fill="none" stroke="#2563eb" stroke-width="3" points="{pts_mrg}"/>')

    for d in data_sort:
        svg.append(f'  <circle cx="{to_svg_x(d["n"]):.1f}" cy="{to_svg_y(d["cmp_ins"]):.1f}" r="4" fill="#dc2626"/>')
        svg.append(f'  <circle cx="{to_svg_x(d["n"]):.1f}" cy="{to_svg_y(d["cmp_mrg"]):.1f}" r="4" fill="#2563eb"/>')

    # Legend
    svg.append(f'  <rect x="{width-260}" y="{padding_top+10}" width="220" height="60" fill="#f8fafc" stroke="#e2e8f0" rx="4"/>')
    svg.append(f'  <line x1="{width-245}" y1="{padding_top+28}" x2="{width-220}" y2="{padding_top+28}" stroke="#dc2626" stroke-width="3"/>')
    svg.append(f'  <text x="{width-210}" y="{padding_top+32}" font-size="11" fill="#1e293b">Insertion Sort O(n²)</text>')
    svg.append(f'  <line x1="{width-245}" y1="{padding_top+50}" x2="{width-220}" y2="{padding_top+50}" stroke="#2563eb" stroke-width="3"/>')
    svg.append(f'  <text x="{width-210}" y="{padding_top+54}" font-size="11" fill="#1e293b">Merge Sort O(n log n)</text>')

    svg.append('</svg>')
    with open(path, 'w', encoding='utf-8') as f:
        f.write("\n".join(svg))

if __name__ == '__main__':
    jalankan_benchmark()
