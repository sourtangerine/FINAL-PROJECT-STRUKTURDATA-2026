# loader.py  –  CSV reader tanpa modul csv (menangani field ber-quote)

import os

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

def _parse_line(line):
    """Pisahkan satu baris CSV yang mungkin mengandung koma di dalam quote."""
    fields = []; cur = ''; in_q = False
    for ch in line:
        if ch == '"':  in_q = not in_q
        elif ch == ',' and not in_q:
            fields.append(cur); cur = ''
        else:
            cur += ch
    fields.append(cur)
    return fields

def baca_pesanan(path=None):
    """Baca pesanan.csv dan kembalikan list of dict."""
    if path is None: path = os.path.join(DATA_DIR, 'pesanan.csv')
    rows = []
    with open(path, 'r', encoding='utf-8') as f:
        header = None
        for line in f:
            line = line.rstrip('\r\n')
            if not line: continue
            fields = _parse_line(line)
            if header is None: header = fields; continue
            row = {}
            for i, h in enumerate(header):
                v = fields[i] if i < len(fields) else ''
                if h in ('harga','prioritas'):
                    row[h] = int(v) if v else 0
                elif h in ('t_masuk_detik','t_selesai_detik'):
                    row[h] = int(v) if v else None
                else:
                    row[h] = v
            rows.append(row)
    return rows

def baca_peta(path=None):
    """Baca peta.csv, kembalikan list of (dari, ke, menit)."""
    if path is None: path = os.path.join(DATA_DIR, 'peta.csv')
    rows = []
    with open(path, 'r', encoding='utf-8') as f:
        first = True
        for line in f:
            line = line.rstrip('\r\n')
            if not line: continue
            if first: first=False; continue
            parts = line.split(',')
            if len(parts) < 3: continue
            rows.append((parts[0].strip(), parts[1].strip(), int(parts[2].strip())))
    return rows
