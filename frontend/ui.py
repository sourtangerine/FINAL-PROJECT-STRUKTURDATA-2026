# frontend/ui.py - 2EZ4U Food Delivery Tkinter UI
import tkinter as tk
from tkinter import messagebox
import time, sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# --- Theme Colors (matching screenshot reference) ---
NAVY_HEADER = '#1c344d'
BG_APP      = '#f4f5f7'
BG_SIDEBAR  = '#f4f5f7'
BG_WHITE    = '#ffffff'
BORDER_GRAY = '#cbd5e1'
BORDER_DARK = '#94a3b8'
TEXT_DARK   = '#0f172a'
TEXT_SUB    = '#64748b'
TEXT_MUTED  = '#94a3b8'
HDR_BG      = '#e2e8f0'
HDR_FG      = '#334155'
BTN_BG      = '#ffffff'
BTN_FG      = '#1e293b'
SEL_BG      = '#cfe2fe'
SEL_FG      = '#0f172a'
HINT_BG     = '#fef9c3'
HINT_BORDER = '#fef08a'
HINT_FG     = '#713f12'

FONT_TITLE  = ('Segoe UI', 11, 'bold')
FONT_SUB    = ('Segoe UI', 8)
FONT_LABEL  = ('Segoe UI', 8, 'bold')
FONT_ENTRY  = ('Segoe UI', 9)
FONT_BTN    = ('Segoe UI', 9, 'bold')
FONT_SB_HDR = ('Segoe UI', 8, 'bold')
FONT_SB_BTN = ('Segoe UI', 8)
FONT_MONO   = ('Consolas', 9)
FONT_CMD    = ('Consolas', 9)

state = {
    'raw': [],
    'arr': None,
    'lnk': None,
    'q_naif': None,
    'q_circ': None,
    'ur': None,
    'sorted_oid': None,
    'sorted_oid_time': None,
    'next_oid': 200001,
}

def _fmt_ribuan(n):
    if n is None: return '-'
    return f"{n:,}".replace(',', '.')

def _fmt_jam(detik):
    if detik is None or detik == '' or detik == '-': return '-'
    try:
        d = int(detik)
        return f"{d // 3600:02d}:{(d % 3600) // 60:02d}:{d % 60:02d}"
    except (ValueError, TypeError):
        return '-'

def _fmt_ms(t):
    return f"{t*1000:.2f} ms" if t < 1 else f"{t:.3f} s"

def _new_oid():
    oid = f"O-{state['next_oid']:06d}"
    state['next_oid'] += 1
    return oid

def _pesanan_baru(nama, prioritas=2):
    return {
        'oid': _new_oid(),
        'pelanggan': nama,
        'resto': 'kafe-teknik',
        'menu': 'roti-bakar',
        'harga': 12000,
        'prioritas': prioritas,
        't_masuk_detik': 28800,  # 08:00:00
        't_selesai_detik': None,
        'status': 'ANTRE'
    }

def _row_text(p):
    oid = str(p.get('oid') if hasattr(p, 'get') else p[0])
    pel = str(p.get('pelanggan') if hasattr(p, 'get') else p[1])
    res = str(p.get('resto') if hasattr(p, 'get') else p[2])
    men = str(p.get('menu') if hasattr(p, 'get') else p[3])
    hrg = p.get('harga') if hasattr(p, 'get') else p[4]
    pr  = p.get('prioritas') if hasattr(p, 'get') else p[5]
    st  = p.get('status') if hasattr(p, 'get') else p[8]
    return (f"{oid:<12} {pel[:22]:<23} {res[:15]:<16} "
            f"{men[:14]:<15} Rp{_fmt_ribuan(hrg):>8} P{pr} {st}")

def _header():
    return (f"{'OID':<12} {'PELANGGAN':<23} {'RESTO':<16} "
            f"{'MENU':<15} {'HARGA':>10} PR STATUS")


MENU_SECTIONS = [
    ('DATA', [
        ('Load', 'load'),
    ]),
    ('M1 - DATA PESANAN', [
        ('ARRAY - LIHAT PESANAN', 'arr_lihat'),
        ('ARRAY - TAMBAH PESANAN REGULER', 'arr_reguler'),
        ('ARRAY - TAMBAH PESANAN PRIORITAS', 'arr_prioritas'),
        ('ARRAY - TAMBAH PESANAN VIP', 'arr_vip'),
        ('ARRAY - HAPUS PESANAN', 'arr_hapus'),
        ('LINKEDLIST - LIHAT PESANAN', 'll_lihat'),
        ('LINKEDLIST - TAMBAH PESANAN REGULER', 'll_reguler'),
        ('LINKEDLIST - TAMBAH PESANAN PRIORITAS', 'll_prioritas'),
        ('LINKEDLIST - TAMBAH PESANAN VIP', 'll_vip'),
        ('LINKEDLIST - HAPUS PESANAN', 'll_hapus'),
    ]),
    ('M2 - STACK DAN QUEUE', [
        ('STACK - POSTFIX (MESIN KASIR)', 'm2_postfix'),
        ('STACK - UNDO', 'm2_undo'),
        ('STACK - REDO', 'm2_redo'),
        ('QUEUE - ENQUEUE', 'm2_enqueue'),
        ('QUEUE - DEQUEUE NAIF', 'm2_dequeue_naif'),
        ('QUEUE - DEQUEUE CIRCULAR', 'm2_dequeue_circ'),
    ]),
    ('M3 - SORT DAN SEARCH', [
        ('SORT - INSERTION SORT', 'm3_insertion'),
        ('SORT - MERGE SORT', 'm3_merge'),
        ('SEARCH - LINEAR SEARCH', 'm3_linear'),
        ('SEARCH - BINARY SEARCH', 'm3_binary'),
    ]),
    ('M4 - HASH TABLE', [
        ('Bangun indeks hash', 'm4_hash'),
        ('Cari pesanan (oid)', 'm4_cari'),
    ]),
    ('M5 - KATALOG DAN PRIORITAS', [
        ('Menu per rentang harga', 'm5_rentang'),
        ('Isi antrean prioritas', 'm5_prioritas'),
    ]),
    ('M6 - PETA DAN RUTE', [
        ('Muat peta', 'm6_peta'),
    ]),
]


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('2EZ4U Food Delivery')
        self.geometry('1060x720')
        self.minsize(880, 560)
        self.configure(bg=BG_APP)

        self.current_key = None
        self.sidebar_buttons = {}

        self._build_header()
        self._build_body()
        self._build_statusbar()

        self._select_action('arr_reguler')

    def _build_header(self):
        header = tk.Frame(self, bg=NAVY_HEADER, height=44)
        header.pack(fill='x', side='top')
        header.pack_propagate(False)

        lbl = tk.Label(header, text='2EZ4U Food Delivery', bg=NAVY_HEADER, fg='#ffffff',
                       font=('Segoe UI', 12, 'bold'), anchor='w')
        lbl.pack(side='left', padx=14, fill='y')

    def _build_body(self):
        body = tk.Frame(self, bg=BG_APP)
        body.pack(fill='both', expand=True)

        # Left Sidebar container
        sb_container = tk.Frame(body, bg=BG_SIDEBAR, width=265)
        sb_container.pack(side='left', fill='y')
        sb_container.pack_propagate(False)

        divider = tk.Frame(body, bg=BORDER_GRAY, width=1)
        divider.pack(side='left', fill='y')

        # Sidebar canvas + scrollbar
        self.sb_canvas = tk.Canvas(sb_container, bg=BG_SIDEBAR, highlightthickness=0, bd=0)
        self.sb_scrollbar = tk.Scrollbar(sb_container, orient='vertical', command=self.sb_canvas.yview)
        self.sb_canvas.configure(yscrollcommand=self.sb_scrollbar.set)

        self.sb_frame = tk.Frame(self.sb_canvas, bg=BG_SIDEBAR)
        self.sb_canvas_window = self.sb_canvas.create_window((0, 0), window=self.sb_frame, anchor='nw')

        self.sb_canvas.pack(side='left', fill='both', expand=True)
        self.sb_scrollbar.pack(side='right', fill='y')

        self.sb_frame.bind('<Configure>', lambda e: self.sb_canvas.configure(scrollregion=self.sb_canvas.bbox('all')))
        self.sb_canvas.bind('<Configure>', lambda e: self.sb_canvas.itemconfig(self.sb_canvas_window, width=e.width))

        def _on_mousewheel(event):
            self.sb_canvas.yview_scroll(int(-1 * (event.delta / 120)), 'units')
        sb_container.bind('<Enter>', lambda e: sb_container.bind_all('<MouseWheel>', _on_mousewheel))
        sb_container.bind('<Leave>', lambda e: sb_container.unbind_all('<MouseWheel>'))

        self._populate_sidebar()

        # Right Content Area
        self.right_panel = tk.Frame(body, bg=BG_WHITE)
        self.right_panel.pack(side='right', fill='both', expand=True)

        # Top Action/Form Area
        self.form_frame = tk.Frame(self.right_panel, bg=BG_WHITE)
        self.form_frame.pack(fill='x', side='top')

        # Middle Result Display Area
        res_container = tk.Frame(self.right_panel, bg=BG_WHITE)
        res_container.pack(fill='both', expand=True, padx=14, pady=(0, 4))

        res_border = tk.Frame(res_container, bg=BORDER_DARK, bd=1, relief='solid')
        res_border.pack(fill='both', expand=True)

        ys = tk.Scrollbar(res_border, orient='vertical')
        xs = tk.Scrollbar(res_border, orient='horizontal')
        self.result_text = tk.Text(res_border, bg=BG_WHITE, fg=TEXT_DARK,
                                   font=FONT_MONO, relief='flat', bd=0,
                                   highlightthickness=0, wrap='none',
                                   yscrollcommand=ys.set, xscrollcommand=xs.set)
        ys.config(command=self.result_text.yview)
        xs.config(command=self.result_text.xview)
        ys.pack(side='right', fill='y')
        xs.pack(side='bottom', fill='x')
        self.result_text.pack(side='left', fill='both', expand=True)

        # Bottom Area: Hint bar + Command Log
        bottom_box = tk.Frame(self.right_panel, bg=BG_WHITE)
        bottom_box.pack(fill='x', side='bottom', padx=14, pady=(0, 6))

        # Command Log Box
        tk.Label(bottom_box, text='COMMAND', font=FONT_LABEL, fg='#334155',
                 bg=BG_WHITE, anchor='w').pack(fill='x', pady=(0, 2))

        cmd_border = tk.Frame(bottom_box, bg=BORDER_DARK, bd=1, relief='solid')
        cmd_border.pack(fill='x')

        cmd_ys = tk.Scrollbar(cmd_border, orient='vertical')
        self.cmd_text = tk.Text(cmd_border, height=4, bg=BG_WHITE, fg=TEXT_DARK,
                                font=FONT_CMD, relief='flat', bd=0,
                                highlightthickness=0, wrap='none', state='disabled',
                                yscrollcommand=cmd_ys.set)
        cmd_ys.config(command=self.cmd_text.yview)
        cmd_ys.pack(side='right', fill='y')
        self.cmd_text.pack(side='left', fill='both', expand=True)

        # Hint Bar (light yellow box matching screenshot)
        self.hint_frame = tk.Frame(bottom_box, bg=HINT_BG, relief='solid', bd=1)
        self.hint_frame.pack(fill='x', pady=(6, 0))
        self.hint_label = tk.Label(self.hint_frame, text='', font=('Segoe UI', 8),
                                   bg=HINT_BG, fg=HINT_FG, anchor='w', justify='left',
                                   wraplength=720, padx=8, pady=6)
        self.hint_label.pack(fill='x')

    def _build_statusbar(self):
        bottom_bar = tk.Frame(self, bg=BG_APP, height=30)
        bottom_bar.pack(fill='x', side='bottom')
        bottom_bar.pack_propagate(False)

        top_line = tk.Frame(bottom_bar, bg=BORDER_GRAY, height=1)
        top_line.pack(fill='x', side='top')

        content_bar = tk.Frame(bottom_bar, bg=BG_APP)
        content_bar.pack(fill='both', expand=True, padx=8, pady=2)

        self.status_badge = tk.Label(content_bar, text='siap', bg=NAVY_HEADER, fg='#ffffff',
                                     font=('Consolas', 9, 'bold'), padx=10, pady=1)
        self.status_badge.pack(side='left')

    def _populate_sidebar(self):
        for header_title, items in MENU_SECTIONS:
            hdr = tk.Label(self.sb_frame, text=header_title, font=FONT_SB_HDR,
                           fg=HDR_FG, bg=HDR_BG, anchor='w', padx=6, pady=2,
                           relief='solid', bd=1)
            hdr.pack(fill='x', padx=6, pady=(6, 2))

            for label, key in items:
                btn = tk.Button(self.sb_frame, text=label, font=FONT_SB_BTN,
                                bg=BTN_BG, fg=BTN_FG, activebackground='#e2e8f0',
                                anchor='w', padx=6, pady=2, relief='solid', bd=1,
                                cursor='hand2', command=lambda k=key, l=label: self._on_sidebar_click(k, l))
                btn.pack(fill='x', padx=6, pady=1)
                self.sidebar_buttons[key] = btn

    def _on_sidebar_click(self, key, label):
        # M4 through M6 trigger "Fitur sedang dikerjakan" popup
        if key.startswith(('m4_', 'm5_', 'm6_')):
            messagebox.showinfo('Fitur Sedang Dikerjakan', 'Fitur sedang dikerjakan.')
            return
        self._select_action(key)

    def _select_action(self, key):
        self.current_key = key
        for k, btn in self.sidebar_buttons.items():
            if k == key:
                btn.config(bg=SEL_BG, fg=SEL_FG)
            else:
                btn.config(bg=BTN_BG, fg=BTN_FG)

        ROUTES = {
            'load': self._form_load,
            'arr_lihat': lambda: self._form_lihat('array'),
            'arr_reguler': lambda: self._form_tambah('array', 3),
            'arr_prioritas': lambda: self._form_tambah('array', 2),
            'arr_vip': lambda: self._form_tambah('array', 1),
            'arr_hapus': lambda: self._form_hapus('array'),
            'll_lihat': lambda: self._form_lihat('ll'),
            'll_reguler': lambda: self._form_tambah('ll', 3),
            'll_prioritas': lambda: self._form_tambah('ll', 2),
            'll_vip': lambda: self._form_tambah('ll', 1),
            'll_hapus': lambda: self._form_hapus('ll'),
            # M2 Routes
            'm2_postfix': self._form_postfix,
            'm2_undo': self._form_undo,
            'm2_redo': self._form_redo,
            'm2_enqueue': self._form_enqueue,
            'm2_dequeue_naif': self._form_dequeue_naif,
            'm2_dequeue_circ': self._form_dequeue_circ,
            # M3 Routes
            'm3_insertion': self._form_insertion_sort,
            'm3_merge': self._form_merge_sort,
            'm3_linear': self._form_linear_search,
            'm3_binary': self._form_binary_search,
        }
        fn = ROUTES.get(key)
        if fn:
            fn()

    def _log(self, cmd, modul, elapsed_s):
        ms_str = _fmt_ms(elapsed_s)
        line = f"{cmd:<23} -> {modul:<18} {ms_str:>10}\n"
        self.cmd_text.config(state='normal')
        self.cmd_text.insert('end', line)
        self.cmd_text.see('end')
        self.cmd_text.config(state='disabled')
        self.status_badge.config(text=f"[{modul}] {ms_str}")

    def _set_hint(self, text):
        self.hint_label.config(text=text)

    def _render_form(self, title, subtitle, fields, btn_text, btn_cmd, dropdowns=None):
        for w in self.form_frame.winfo_children():
            w.destroy()

        tk.Label(self.form_frame, text=title, font=FONT_TITLE, fg=TEXT_DARK,
                 bg=BG_WHITE, anchor='w').pack(fill='x', padx=14, pady=(10, 1))
        if subtitle:
            tk.Label(self.form_frame, text=subtitle, font=FONT_SUB, fg=TEXT_SUB,
                     bg=BG_WHITE, anchor='w').pack(fill='x', padx=14, pady=(0, 8))

        row_frame = tk.Frame(self.form_frame, bg=BG_WHITE)
        row_frame.pack(fill='x', padx=14, pady=(0, 8))

        entries = {}
        for lbl_text, default_val, helper_text, field_id in (fields or []):
            field_col = tk.Frame(row_frame, bg=BG_WHITE)
            field_col.pack(side='left', padx=(0, 16))

            tk.Label(field_col, text=lbl_text, font=FONT_LABEL, fg='#1e293b',
                     bg=BG_WHITE, anchor='w').pack(fill='x')

            entry = tk.Entry(field_col, font=FONT_ENTRY, relief='solid', bd=1,
                             width=22, bg=BG_WHITE, fg='#000000', highlightthickness=0)
            entry.insert(0, default_val)
            entry.pack(pady=2)
            entries[field_id] = entry

            if helper_text:
                tk.Label(field_col, text=helper_text, font=FONT_SUB, fg=TEXT_MUTED,
                         bg=BG_WHITE, anchor='w').pack(fill='x')

        if dropdowns:
            for lbl_text, default_val, options, helper_text, field_id in dropdowns:
                dd_col = tk.Frame(row_frame, bg=BG_WHITE)
                dd_col.pack(side='left', padx=(0, 16))

                tk.Label(dd_col, text=lbl_text, font=FONT_LABEL, fg='#1e293b',
                         bg=BG_WHITE, anchor='w').pack(fill='x')

                var = tk.StringVar(value=default_val)
                opt = tk.OptionMenu(dd_col, var, *options)
                opt.config(bg='#52525b', fg='#ffffff', activebackground='#3f3f46',
                           activeforeground='#ffffff', font=FONT_ENTRY, relief='flat',
                           highlightthickness=0, bd=0, padx=8, pady=2)
                opt['menu'].config(bg='#3f3f46', fg='#ffffff', font=FONT_ENTRY)
                opt.pack(pady=2, fill='x')
                entries[field_id] = var

                if helper_text:
                    tk.Label(dd_col, text=helper_text, font=FONT_SUB, fg=TEXT_MUTED,
                             bg=BG_WHITE, anchor='w').pack(fill='x')

        if btn_text:
            btn_col = tk.Frame(row_frame, bg=BG_WHITE)
            btn_col.pack(side='left', padx=(4, 0), anchor='center')

            def wrapped_cmd():
                btn_cmd(entries)

            b = tk.Button(btn_col, text=btn_text, bg=NAVY_HEADER, fg='#ffffff',
                          activebackground='#2a4d70', activeforeground='#ffffff',
                          font=FONT_BTN, relief='flat', padx=22, pady=4,
                          cursor='hand2', command=wrapped_cmd)
            b.pack(pady=(12, 0))

        tk.Frame(self.form_frame, height=1, bg=BORDER_GRAY).pack(fill='x', padx=14, pady=(4, 6))

    def _ensure_queues(self):
        from backend.m2_antrean import AntreanNaif, AntreanMelingkar, UndoRedo
        if state['q_naif'] is None or state['q_circ'] is None:
            qn = AntreanNaif()
            qc = AntreanMelingkar(K=32768)
            if state['raw']:
                for r in state['raw']:
                    st = r.get('status') if hasattr(r, 'get') else r[8]
                    if st == 'ANTRE':
                        qn.enqueue(r)
                        qc.enqueue(r)
            state['q_naif'] = qn
            state['q_circ'] = qc
            state['ur'] = UndoRedo(qn, qc)

    # ── M1 Handlers ──────────────────────────────────────────────────────────
    def _form_load(self):
        def do_load(_):
            from loader import baca_pesanan
            from backend.m1_pesanan import Array, LinkList
            from backend.m2_antrean import AntreanNaif, AntreanMelingkar, UndoRedo
            t0 = time.perf_counter()
            rows = baca_pesanan()
            state['raw'] = rows
            arr = Array()
            lnk = LinkList()
            qn = AntreanNaif()
            qc = AntreanMelingkar(K=32768)

            for r in rows:
                arr.tambah_reguler(r)
                lnk.tambah_reguler(r)
                st = r.get('status') if hasattr(r, 'get') else r[8]
                if st == 'ANTRE':
                    qn.enqueue(r)
                    qc.enqueue(r)

            state['arr'] = arr
            state['lnk'] = lnk
            state['q_naif'] = qn
            state['q_circ'] = qc
            state['ur'] = UndoRedo(qn, qc)
            state['sorted_oid'] = None
            elapsed = time.perf_counter() - t0

            self.result_text.config(state='normal')
            self.result_text.delete('1.0', 'end')
            self.result_text.insert('end', f"Loaded {_fmt_ribuan(len(rows))} pesanan\n"
                                           f"Array: {_fmt_ribuan(len(arr))}  LinkList: {_fmt_ribuan(len(lnk))}\n"
                                           f"Antrean ANTRE: {_fmt_ribuan(len(qn))} pesanan pada naif & circular\n"
                                           f"Waktu: {_fmt_ms(elapsed)}\n")
            self.result_text.config(state='disabled')
            self._log('load', 'M1 - larik', elapsed)
            self._set_hint("Data berhasil dimuat. Kedua antrean M2 telah diisi dengan semua pesanan berstatus ANTRE.")

        self._render_form(
            title='Load data CSV',
            subtitle='Membaca pesanan.csv ke memori untuk Array, LinkedList, dan Antrean M2',
            fields=[],
            btn_text='LOAD',
            btn_cmd=do_load
        )
        self._set_hint("Klik LOAD untuk memuat 200.000 data pesanan dari file CSV.")

    def _form_lihat(self, mode):
        name = 'Array' if mode == 'array' else 'LinkedList'
        modul = 'M1 - array' if mode == 'array' else 'M1 - ll'
        cmd_name = f'{mode}_get'

        def do_lihat(entries):
            ds = state['arr'] if mode == 'array' else state['lnk']
            if ds is None or len(ds) == 0:
                self.result_text.config(state='normal')
                self.result_text.delete('1.0', 'end')
                self.result_text.insert('end', 'Data belum dimuat! Silakan klik Load terlebih dahulu.\n')
                self.result_text.config(state='disabled')
                return

            try: i = int(entries['idx'].get())
            except ValueError: i = 0
            try: n = int(entries['n'].get())
            except ValueError: n = 20

            t0 = time.perf_counter()
            rows = ds.to_list()
            elapsed = time.perf_counter() - t0

            self.result_text.config(state='normal')
            self.result_text.delete('1.0', 'end')
            self.result_text.insert('end', _header() + '\n' + '-' * 94 + '\n')
            for j, r in enumerate(rows[:n]):
                prefix = '>> ' if j == i else '   '
                self.result_text.insert('end', prefix + _row_text(r) + '\n')
            if 0 <= i < len(rows):
                self.result_text.insert('end', f'\n[indeks {i}] {_row_text(rows[i])}\n')
            self.result_text.config(state='disabled')
            self._log(cmd_name, modul, elapsed)

        self._render_form(
            title=f'{name}: Lihat pesanan',
            subtitle='Akses indeks tunggal dan tampilkan n teratas',
            fields=[
                ('Indeks ke-:', '0', 'indeks data yang ingin disorot', 'idx'),
                ('Tampil n teratas:', '20', 'jumlah baris yang ditampilkan', 'n'),
            ],
            btn_text='LIHAT',
            btn_cmd=do_lihat
        )
        self._set_hint(f"Melihat pesanan pada {name}. Akses indeks Array adalah O(1), sedangkan LinkedList adalah O(n).")

    def _form_tambah(self, mode, prioritas):
        name = 'Array' if mode == 'array' else 'LinkedList'
        modul = 'M1 - array' if mode == 'array' else 'M1 - ll'
        cmd_name = f'{mode}_tambah'

        jenis_map = {1: 'VIP', 2: 'PRIORITAS', 3: 'REGULER'}
        desc_map = {
            3: 'append: pesanan biasa mengantre di barisan paling belakang.',
            2: 'insert(mid): menyerobok ke tengah.',
            1: 'insert(0): langsung ke urutan pertama.'
        }
        jenis = jenis_map[prioritas]
        desc = desc_map[prioritas]

        def do_tambah(entries):
            ds = state['arr'] if mode == 'array' else state['lnk']
            if ds is None:
                self.result_text.config(state='normal')
                self.result_text.delete('1.0', 'end')
                self.result_text.insert('end', 'Data belum dimuat! Silakan klik Load terlebih dahulu.\n')
                self.result_text.config(state='disabled')
                return

            nama = entries['nama'].get().strip() or 'Pelanggan Baru'
            p = _pesanan_baru(nama, prioritas)
            state['sorted_oid'] = None

            t0 = time.perf_counter()
            if prioritas == 3: ds.tambah_reguler(p)
            elif prioritas == 2: ds.tambah_prioritas(p)
            else: ds.tambah_vip(p)
            elapsed = time.perf_counter() - t0

            self.result_text.config(state='normal')
            self.result_text.delete('1.0', 'end')
            self.result_text.insert('end', f"Ditambahkan: {_row_text(p)}\n"
                                           f"Panjang {name}: {_fmt_ribuan(len(ds))}\n"
                                           f"Waktu: {_fmt_ms(elapsed)}\n")
            self.result_text.config(state='disabled')
            self._log(cmd_name, modul, elapsed)

        self._render_form(
            title=f'{name}: pesanan {jenis}, {"masuk paling belakang" if prioritas==3 else "menyerobok ke tengah" if prioritas==2 else "langsung ke urutan pertama"}',
            subtitle=desc,
            fields=[
                ('Nama pelanggan', 'Pelanggan Baru', 'nama untuk pesanan yang akan dibuat', 'nama'),
            ],
            btn_text='TAMBAH',
            btn_cmd=do_tambah
        )
        self._set_hint(f"Penambahan {jenis}: Array vs LinkedList memiliki kompleksitas berbeda tergantung posisi sisip.")

    def _form_hapus(self, mode):
        name = 'Array' if mode == 'array' else 'LinkedList'
        modul = 'M1 - array' if mode == 'array' else 'M1 - ll'
        cmd_name = f'{mode}_hapus'

        def do_hapus(entries):
            ds = state['arr'] if mode == 'array' else state['lnk']
            if ds is None or len(ds) == 0:
                self.result_text.config(state='normal')
                self.result_text.delete('1.0', 'end')
                self.result_text.insert('end', 'Tidak ada data untuk dihapus!\n')
                self.result_text.config(state='disabled')
                return

            try: i = int(entries['idx'].get())
            except ValueError: i = 0

            state['sorted_oid'] = None
            t0 = time.perf_counter()
            try: v = ds.hapus(i)
            except IndexError:
                self.result_text.config(state='normal')
                self.result_text.delete('1.0', 'end')
                self.result_text.insert('end', f'Indeks {i} di luar batas!\n')
                self.result_text.config(state='disabled')
                return
            elapsed = time.perf_counter() - t0

            self.result_text.config(state='normal')
            self.result_text.delete('1.0', 'end')
            self.result_text.insert('end', f"Dihapus: {_row_text(v)}\n"
                                           f"Sisa {name}: {_fmt_ribuan(len(ds))}\n"
                                           f"Waktu: {_fmt_ms(elapsed)}\n")
            self.result_text.config(state='disabled')
            self._log(cmd_name, modul, elapsed)

        self._render_form(
            title=f'{name}: Hapus pesanan ke-i',
            subtitle='Menghapus pesanan pada indeks tertentu dan menggeser sisa elemen',
            fields=[
                ('Indeks ke-:', '0', 'indeks pesanan yang ingin dihapus', 'idx'),
            ],
            btn_text='HAPUS',
            btn_cmd=do_hapus
        )
        self._set_hint(f"Menghapus elemen dari {name}. Array butuh menggeser O(n), LinkedList menelusuri O(n).")

    # ── M2 Handlers: Stack & Queue ───────────────────────────────────────────
    def _form_postfix(self):
        from backend.m2_antrean import ke_postfix, hitung

        def do_hitung(entries):
            expr = entries['expr'].get().strip()
            if not expr:
                expr = "( 3 * 12000 ) + ( 2 * 8500 ) - 5000"

            t0 = time.perf_counter()
            try:
                postfix, steps1 = ke_postfix(expr)
                total, steps2 = hitung(postfix)
                elapsed = time.perf_counter() - t0
            except Exception as e:
                self.result_text.config(state='normal')
                self.result_text.delete('1.0', 'end')
                self.result_text.insert('end', f"GALAT: {str(e)}\n")
                self.result_text.config(state='disabled')
                return

            postfix_str = ' '.join(postfix)
            self.result_text.config(state='normal')
            self.result_text.delete('1.0', 'end')
            self.result_text.insert('end', f"Struk   : {expr}\n")
            self.result_text.insert('end', f"Postfix : {postfix_str}\n")
            self.result_text.insert('end', f"TOTAL   : Rp {_fmt_ribuan(total)}\n\n")

            # Tabel langkah Shunting-Yard & Evaluasi
            self.result_text.insert('end', f"{'langkah':<10} {'token':<12} {'tindakan':<32} {'stack':<28} {'output'}\n")
            self.result_text.insert('end', '-' * 96 + '\n')
            for l_str, tok, act, stk, out in steps1:
                self.result_text.insert('end', f"{l_str:<10} {tok:<12} {act[:30]:<32} {stk[:26]:<28} {out}\n")
            for l_str, tok, act, stk in steps2:
                self.result_text.insert('end', f"{l_str:<10} {tok:<12} {act[:30]:<32} {stk[:26]:<28} -\n")

            self.result_text.config(state='disabled')
            self._log('postfix_eval', 'M2 - stack', elapsed)

        self._render_form(
            title='Stack: konversi infix ke postfix & evaluasi kasir',
            subtitle='Operator dimasukkan ke stack; tanda kurung menentukan urutan hitung. Evaluasi membaca postfix dari kiri.',
            fields=[
                ('Struk belanja (ekspresi)', '( 3 * 12000 ) + ( 2 * 8500 ) - 5000', 'contoh: ( 3 * 12000 ) + ( 2 * 8500 ) - 5000', 'expr'),
            ],
            btn_text='HITUNG',
            btn_cmd=do_hitung
        )
        self._set_hint("Operator dengan prioritas lebih tinggi (*, /) didahulukan daripada (+, -). Evaluasi postfix menggunakan stack angka: operand kanan di-pop lebih dulu.")

    def _form_undo(self):
        self._ensure_queues()

        def do_undo(_):
            ur = state['ur']
            t0 = time.perf_counter()
            aksi, items, msg = ur.undo_last()
            elapsed = time.perf_counter() - t0

            qn_len = len(state['q_naif'])
            qc_len = len(state['q_circ'])
            u_depth = ur.undo_depth()

            self.result_text.config(state='normal')
            self.result_text.delete('1.0', 'end')
            if aksi is None:
                self.result_text.insert('end', f"{msg}\n")
                self.result_text.insert('end', f"Panjang antrean sekarang: naif {_fmt_ribuan(qn_len)}, circular {_fmt_ribuan(qc_len)}. tumpukan undo tersisa {u_depth} catatan.\n")
            else:
                self.result_text.insert('end', f"{msg}\n")
                self.result_text.insert('end', f"Panjang antrean sekarang: naif {_fmt_ribuan(qn_len)}, circular {_fmt_ribuan(qc_len)}. tumpukan undo tersisa {u_depth} catatan.\n\n")
                if items:
                    self.result_text.insert('end', f"{'#':<6} {'oid':<14} {'pelanggan':<22} {'resto':<20} {'menu'}\n")
                    self.result_text.insert('end', '-' * 80 + '\n')
                    for j, it in enumerate(items, 1):
                        oid = it.get('oid') if hasattr(it, 'get') else it[0]
                        pel = it.get('pelanggan') if hasattr(it, 'get') else it[1]
                        res = it.get('resto') if hasattr(it, 'get') else it[2]
                        men = it.get('menu') if hasattr(it, 'get') else it[3]
                        self.result_text.insert('end', f"{j:<6} {str(oid):<14} {str(pel)[:20]:<22} {str(res)[:18]:<20} {str(men)}\n")

            self.result_text.config(state='disabled')
            self._log('stack_undo', 'M2 - stack', elapsed)

        self._render_form(
            title='Stack: batalkan aksi antrean terakhir',
            subtitle='Mengambil catatan teratas tumpukan undo, lalu menjalankan kebalikannya. Aksi terakhirlah yang dibatalkan lebih dulu.',
            fields=[],
            btn_text='UNDO',
            btn_cmd=do_undo
        )
        self._set_hint("Kebalikan dari enqueue adalah membuang elemen paling belakang, dan itu murah pada kedua antrean.")

    def _form_redo(self):
        self._ensure_queues()

        def do_redo(_):
            ur = state['ur']
            t0 = time.perf_counter()
            aksi, items, msg = ur.redo_last()
            elapsed = time.perf_counter() - t0

            qn_len = len(state['q_naif'])
            qc_len = len(state['q_circ'])
            u_depth = ur.undo_depth()
            r_depth = ur.redo_depth()

            self.result_text.config(state='normal')
            self.result_text.delete('1.0', 'end')
            if aksi is None:
                self.result_text.insert('end', f"{msg}\n")
                self.result_text.insert('end', f"Panjang antrean sekarang: naif {_fmt_ribuan(qn_len)}, circular {_fmt_ribuan(qc_len)}. Tumpukan undo {u_depth}, redo {r_depth}.\n")
            else:
                self.result_text.insert('end', f"{msg}\n")
                self.result_text.insert('end', f"Panjang antrean sekarang: naif {_fmt_ribuan(qn_len)}, circular {_fmt_ribuan(qc_len)}. Tumpukan undo {u_depth}, redo {r_depth}.\n\n")
                if items:
                    self.result_text.insert('end', f"{'#':<6} {'oid':<14} {'pelanggan':<22} {'resto':<20} {'menu'}\n")
                    self.result_text.insert('end', '-' * 80 + '\n')
                    for j, it in enumerate(items, 1):
                        oid = it.get('oid') if hasattr(it, 'get') else it[0]
                        pel = it.get('pelanggan') if hasattr(it, 'get') else it[1]
                        res = it.get('resto') if hasattr(it, 'get') else it[2]
                        men = it.get('menu') if hasattr(it, 'get') else it[3]
                        self.result_text.insert('end', f"{j:<6} {str(oid):<14} {str(pel)[:20]:<22} {str(res)[:18]:<20} {str(men)}\n")

            self.result_text.config(state='disabled')
            self._log('stack_redo', 'M2 - stack', elapsed)

        self._render_form(
            title='Stack: kerjakan lagi aksi yang dibatalkan',
            subtitle='Mengambil catatan teratas tumpukan redo, lalu mengerjakan ulang aksi aslinya. Aksi baru apa pun mengosongkan tumpukan ini.',
            fields=[],
            btn_text='REDO',
            btn_cmd=do_redo
        )
        self._set_hint("Redo mengerjakan ULANG aksi aslinya, bukan kebalikannya, lalu mengembalikan catatannya ke tumpukan undo supaya bisa dibatalkan lagi.")

    def _form_enqueue(self):
        self._ensure_queues()

        def do_enqueue(entries):
            nama = entries['nama'].get().strip() or 'X2'
            p = _pesanan_baru(nama, 2)
            state['sorted_oid'] = None

            t0 = time.perf_counter()
            state['q_naif'].enqueue(p)
            state['q_circ'].enqueue(p)
            state['ur'].rekam_enqueue(p)
            elapsed = time.perf_counter() - t0

            qn_len = len(state['q_naif'])
            qc_len = len(state['q_circ'])

            self.result_text.config(state='normal')
            self.result_text.delete('1.0', 'end')
            self.result_text.insert('end', f"{p['oid']} masuk ke barisan paling belakang pada KEDUA antrean.\n")
            self.result_text.insert('end', f"Panjang sekarang: naif {_fmt_ribuan(qn_len)}, circular {_fmt_ribuan(qc_len)}.\n\n")

            # Tabel format kolom | isi (Image 3)
            self.result_text.insert('end', f"{'kolom':<18} {'isi'}\n")
            self.result_text.insert('end', '-' * 48 + '\n')
            self.result_text.insert('end', f"{'oid':<18} {p['oid']}\n")
            self.result_text.insert('end', f"{'pelanggan':<18} {p['pelanggan']}\n")
            self.result_text.insert('end', f"{'resto':<18} {p['resto']}\n")
            self.result_text.insert('end', f"{'menu':<18} {p['menu']}\n")
            self.result_text.insert('end', f"{'harga':<18} {_fmt_ribuan(p['harga'])}\n")
            self.result_text.insert('end', f"{'prioritas':<18} {p['prioritas']}\n")
            self.result_text.insert('end', f"{'masuk':<18} {_fmt_jam(p['t_masuk_detik'])}\n")
            self.result_text.insert('end', f"{'selesai':<18} -\n")
            self.result_text.insert('end', f"{'status':<18} {p['status']}\n")

            self.result_text.config(state='disabled')
            self._log('queue_enqueue', 'M2 - queue', elapsed)

        self._render_form(
            title='Queue: pesanan baru masuk ke belakang',
            subtitle='Menambah pesanan di ujung belakang kedua antrean sekaligus, yang naif maupun yang circular.',
            fields=[
                ('Nama pelanggan', 'X2', 'untuk pesanan yang akan dibuat', 'nama'),
            ],
            btn_text='ENQUEUE',
            btn_cmd=do_enqueue
        )
        self._set_hint("enqueue selalu menempel di belakang, jadi O(1) pada kedua versi. Perbedaannya baru muncul saat dequeue.")

    def _form_dequeue_naif(self):
        self._ensure_queues()

        def do_dequeue(entries):
            try: count = int(entries['count'].get())
            except ValueError: count = 1
            if count <= 0: count = 1

            qn = state['q_naif']
            available = len(qn)
            if available == 0:
                self.result_text.config(state='normal')
                self.result_text.delete('1.0', 'end')
                self.result_text.insert('end', 'Antrean naif kosong!\n')
                self.result_text.config(state='disabled')
                return

            if count > available:
                count = available

            t0 = time.perf_counter()
            items = []
            geser_sebelum = qn.total_geser
            for _ in range(count):
                v = qn.dequeue()
                if v is not None:
                    items.append(v)
            geser_terjadi = qn.total_geser - geser_sebelum
            elapsed = time.perf_counter() - t0

            state['ur'].rekam_dequeue_naif(items)
            rata_geser = geser_terjadi // count if count else 0

            self.result_text.config(state='normal')
            self.result_text.delete('1.0', 'end')
            self.result_text.insert('end', f"{len(items)} pesanan keluar dari depan antrean naif.\n")
            self.result_text.insert('end', f"Total {_fmt_ribuan(geser_terjadi)} elemen digeser, rata-rata {_fmt_ribuan(rata_geser)} geseran per dequeue.\n")
            self.result_text.insert('end', f"Sisa antrean naif {_fmt_ribuan(len(qn))}.\n\n")

            self.result_text.insert('end', f"{'#':<6} {'oid':<14} {'pelanggan':<22} {'resto':<18} {'menu':<16} {'masuk'}\n")
            self.result_text.insert('end', '-' * 86 + '\n')
            for j, p in enumerate(items, 1):
                oid = p.get('oid') if hasattr(p, 'get') else p[0]
                pel = p.get('pelanggan') if hasattr(p, 'get') else p[1]
                res = p.get('resto') if hasattr(p, 'get') else p[2]
                men = p.get('menu') if hasattr(p, 'get') else p[3]
                t_m = p.get('t_masuk_detik') if hasattr(p, 'get') else p[6]
                self.result_text.insert('end', f"{j:<6} {str(oid):<14} {str(pel)[:20]:<22} {str(res)[:16]:<18} {str(men)[:14]:<16} {_fmt_jam(t_m)}\n")

            self.result_text.config(state='disabled')
            self._log('queue_dequeue_naive', 'M2 - queue naif', elapsed)

        self._render_form(
            title='Queue naif: ambil dari depan dengan menggeser isi',
            subtitle='Mengambil indeks 0 lalu menggeser seluruh sisa isi satu petak ke kiri. Biayanya O(n) setiap kali.',
            fields=[
                ('Berapa kali dequeue', '2', 'sampai panjang antrean; coba 1 lalu 100 untuk melihat bedanya', 'count'),
            ],
            btn_text='DEQUEUE',
            btn_cmd=do_dequeue
        )
        self._set_hint("Mengambil indeks 0 memaksa seluruh sisa isi bergeser satu petak ke kiri, jadi O(n) per dequeue. Panjang antrean saat itu 19.852, dan segitu pula kira-kira geseran yang terjadi. Bandingkan waktunya dengan menu DEQUEUE CIRCULAR.")

    def _form_dequeue_circ(self):
        self._ensure_queues()

        def do_dequeue(entries):
            try: count = int(entries['count'].get())
            except ValueError: count = 1
            if count <= 0: count = 1

            qc = state['q_circ']
            available = len(qc)
            if available == 0:
                self.result_text.config(state='normal')
                self.result_text.delete('1.0', 'end')
                self.result_text.insert('end', 'Antrean circular kosong!\n')
                self.result_text.config(state='disabled')
                return

            if count > available:
                count = available

            t0 = time.perf_counter()
            items = []
            for _ in range(count):
                v = qc.dequeue()
                if v is not None:
                    items.append(v)
            elapsed = time.perf_counter() - t0

            state['ur'].rekam_dequeue_circ(items)

            self.result_text.config(state='normal')
            self.result_text.delete('1.0', 'end')
            self.result_text.insert('end', f"{len(items)} pesanan keluar dari depan antrean circular.\n")
            self.result_text.insert('end', f"Tidak ada elemen yang digeser (0 pergeseran).\n")
            self.result_text.insert('end', f"front: {qc.front_idx}, rear: {qc.rear_idx}, kapasitas: {_fmt_ribuan(qc.kapasitas)}, sisa antrean circular: {_fmt_ribuan(len(qc))}.\n\n")

            self.result_text.insert('end', f"{'#':<6} {'oid':<14} {'pelanggan':<22} {'resto':<18} {'menu':<16} {'masuk'}\n")
            self.result_text.insert('end', '-' * 86 + '\n')
            for j, p in enumerate(items, 1):
                oid = p.get('oid') if hasattr(p, 'get') else p[0]
                pel = p.get('pelanggan') if hasattr(p, 'get') else p[1]
                res = p.get('resto') if hasattr(p, 'get') else p[2]
                men = p.get('menu') if hasattr(p, 'get') else p[3]
                t_m = p.get('t_masuk_detik') if hasattr(p, 'get') else p[6]
                self.result_text.insert('end', f"{j:<6} {str(oid):<14} {str(pel)[:20]:<22} {str(res)[:16]:<18} {str(men)[:14]:<16} {_fmt_jam(t_m)}\n")

            self.result_text.config(state='disabled')
            self._log('queue_dequeue_circular', 'M2 - queue circular', elapsed)

        self._render_form(
            title='Queue circular: ambil dari depan tanpa menggeser isi',
            subtitle='Mengambil elemen pada indeks front lalu memajukan front. Biayanya O(1) setiap kali.',
            fields=[
                ('Berapa kali dequeue', '2', 'sampai panjang antrean; coba 1 lalu 100 untuk melihat bedanya', 'count'),
            ],
            btn_text='DEQUEUE',
            btn_cmd=do_dequeue
        )
        self._set_hint("Circular buffer hanya memajukan penunjuk front: front = (front + 1) % K. Tidak ada elemen yang digeser, sehingga biayanya O(1) konstan.")

    # ── M3 Handlers: Sort & Search ───────────────────────────────────────────
    def _form_insertion_sort(self):
        from backend.m3_laporan import insertion_sort

        def do_sort(entries):
            if not state['raw']:
                self.result_text.config(state='normal')
                self.result_text.delete('1.0', 'end')
                self.result_text.insert('end', 'Data belum dimuat! Silakan klik Load terlebih dahulu.\n')
                self.result_text.config(state='disabled')
                return

            try: n = int(entries['n'].get())
            except ValueError: n = 10
            kunci = entries['kunci'].get()

            if n > 20000:
                self.result_text.config(state='normal')
                self.result_text.delete('1.0', 'end')
                self.result_text.insert('end', "DITOLAK: batasnya 20.000 baris, pakai merge sort untuk data penuh.\n")
                self.result_text.config(state='disabled')
                return

            sub = [r for r in state['raw'][:n]]

            t0 = time.perf_counter()
            cmp_cnt, mv_cnt = insertion_sort(sub, kunci)
            elapsed = time.perf_counter() - t0

            self.result_text.config(state='normal')
            self.result_text.delete('1.0', 'end')
            self.result_text.insert('end', f"{len(sub)} pesanan diurutkan menurut {kunci}.\n")
            self.result_text.insert('end', f"{_fmt_ribuan(cmp_cnt)} perbandingan, {_fmt_ribuan(mv_cnt)} pemindahan.\n\n")

            self.result_text.insert('end', f"{'#':<6} {'oid':<14} {'harga':<12} {'selesai':<12} {'resto':<18} {'menu'}\n")
            self.result_text.insert('end', '-' * 80 + '\n')
            for j, p in enumerate(sub[:50], 1):
                oid = p.get('oid') if hasattr(p, 'get') else p[0]
                hrg = p.get('harga') if hasattr(p, 'get') else p[4]
                t_s = p.get('t_selesai_detik') if hasattr(p, 'get') else p[7]
                res = p.get('resto') if hasattr(p, 'get') else p[2]
                men = p.get('menu') if hasattr(p, 'get') else p[3]
                self.result_text.insert('end', f"{j:<6} {str(oid):<14} {_fmt_ribuan(hrg):<12} {_fmt_jam(t_s):<12} {str(res)[:16]:<18} {str(men)}\n")
            if len(sub) > 50:
                self.result_text.insert('end', f"... ({len(sub) - 50} baris lainnya disembunyikan)\n")

            self.result_text.config(state='disabled')
            self._log('insertion_sort', 'M3 - insertion sort', elapsed)

        self._render_form(
            title='Sort: insertion sort, O(n²)',
            subtitle='Setiap elemen digeser mundur sampai menemukan tempatnya. Sederhana, tetapi kerjanya tumbuh kuadratik.',
            fields=[
                ('Jumlah baris diurutkan', '10', 'diambil dari awal data; coba 1.000 lalu 2.000 lalu 4.000', 'n'),
            ],
            dropdowns=[
                ('Diurutkan menurut', 'harga', ['harga', 'oid', 'selesai'], 'ka), selesai (waktu selesai)', 'kunci')
            ],
            btn_text='URUTKAN',
            btn_cmd=do_sort
        )
        self._set_hint("Setiap elemen digeser mundur sampai menemukan tempatnya, jadi biayanya tumbuh kuadratik: melipatduakan jumlah baris membuat kerjanya kira-kira empat kali lipat. Jalankan SORT - MERGE SORT pada jumlah dan kunci yang sama, lalu bandingkan angka perbandingannya.")

    def _form_merge_sort(self):
        from backend.m3_laporan import merge_sort

        def do_sort(entries):
            if not state['raw']:
                self.result_text.config(state='normal')
                self.result_text.delete('1.0', 'end')
                self.result_text.insert('end', 'Data belum dimuat! Silakan klik Load terlebih dahulu.\n')
                self.result_text.config(state='disabled')
                return

            try: n = int(entries['n'].get())
            except ValueError: n = 4000
            kunci = entries['kunci'].get()

            sub = state['raw'][:n]
            self.status_badge.config(text="[M3 - merge sort] Memproses...")
            self.update_idletasks()

            t0 = time.perf_counter()
            sorted_res, cmp_cnt, mv_cnt = merge_sort(sub, kunci)
            elapsed = time.perf_counter() - t0

            self.result_text.config(state='normal')
            self.result_text.delete('1.0', 'end')
            self.result_text.insert('end', f"{_fmt_ribuan(len(sorted_res))} pesanan diurutkan menurut {kunci}.\n")
            self.result_text.insert('end', f"{_fmt_ribuan(cmp_cnt)} perbandingan, {_fmt_ribuan(mv_cnt)} pemindahan.\n\n")

            self.result_text.insert('end', f"{'#':<6} {'oid':<14} {'harga':<12} {'selesai':<12} {'resto':<18} {'menu'}\n")
            self.result_text.insert('end', '-' * 80 + '\n')
            for j, p in enumerate(sorted_res[:50], 1):
                oid = p.get('oid') if hasattr(p, 'get') else p[0]
                hrg = p.get('harga') if hasattr(p, 'get') else p[4]
                t_s = p.get('t_selesai_detik') if hasattr(p, 'get') else p[7]
                res = p.get('resto') if hasattr(p, 'get') else p[2]
                men = p.get('menu') if hasattr(p, 'get') else p[3]
                self.result_text.insert('end', f"{j:<6} {str(oid):<14} {_fmt_ribuan(hrg):<12} {_fmt_jam(t_s):<12} {str(res)[:16]:<18} {str(men)}\n")
            if len(sorted_res) > 50:
                self.result_text.insert('end', f"... ({len(sorted_res) - 50} baris lainnya disembunyikan)\n")

            self.result_text.config(state='disabled')
            self._log('merge_sort', 'M3 - merge sort', elapsed)

        self._render_form(
            title='Sort: merge sort, O(n log n)',
            subtitle='Bagi data sampai satu elemen, lalu gabung berpasangan. Stabil dan sanggup menangani seluruh 200.000 baris.',
            fields=[
                ('Jumlah baris diurutkan', '4000', 'coba 1.000 lalu 2.000 lalu 4.000 untuk melihat pola 2x', 'n'),
            ],
            dropdowns=[
                ('Diurutkan menurut', 'oid', ['oid', 'harga', 'selesai'], 'kunci pengurutan', 'kunci')
            ],
            btn_text='URUTKAN',
            btn_cmd=do_sort
        )
        self._set_hint("Merge sort membagi data menjadi dua bagian rekursif dan menggabungkannya secara stabil (<=). Pertumbuhan kerjanya n log n: melipatduakan n hanya menaikkan perbandingan kira-kira dua kali lipat.")

    def _form_linear_search(self):
        from backend.m3_laporan import linear_search

        def do_search(entries):
            if not state['raw']:
                self.result_text.config(state='normal')
                self.result_text.delete('1.0', 'end')
                self.result_text.insert('end', 'Data belum dimuat! Silakan klik Load terlebih dahulu.\n')
                self.result_text.config(state='disabled')
                return

            target = entries['oid'].get().strip()

            t0 = time.perf_counter()
            idx, cmp_cnt = linear_search(state['raw'], target, 'oid')
            elapsed = time.perf_counter() - t0

            self.result_text.config(state='normal')
            self.result_text.delete('1.0', 'end')
            if idx != -1:
                p = state['raw'][idx]
                self.result_text.insert('end', f"Ditemukan pada indeks {_fmt_ribuan(idx)}.\n")
                self.result_text.insert('end', f"{_fmt_ribuan(cmp_cnt)} perbandingan.\n\n")

                self.result_text.insert('end', f"{'kolom':<18} {'isi'}\n")
                self.result_text.insert('end', '-' * 48 + '\n')
                oid = p.get('oid') if hasattr(p, 'get') else p[0]
                pel = p.get('pelanggan') if hasattr(p, 'get') else p[1]
                res = p.get('resto') if hasattr(p, 'get') else p[2]
                men = p.get('menu') if hasattr(p, 'get') else p[3]
                hrg = p.get('harga') if hasattr(p, 'get') else p[4]
                pr  = p.get('prioritas') if hasattr(p, 'get') else p[5]
                t_m = p.get('t_masuk_detik') if hasattr(p, 'get') else p[6]
                t_s = p.get('t_selesai_detik') if hasattr(p, 'get') else p[7]
                st  = p.get('status') if hasattr(p, 'get') else p[8]

                self.result_text.insert('end', f"{'oid':<18} {oid}\n")
                self.result_text.insert('end', f"{'pelanggan':<18} {pel}\n")
                self.result_text.insert('end', f"{'resto':<18} {res}\n")
                self.result_text.insert('end', f"{'menu':<18} {men}\n")
                self.result_text.insert('end', f"{'harga':<18} {_fmt_ribuan(hrg)}\n")
                self.result_text.insert('end', f"{'prioritas':<18} {pr}\n")
                self.result_text.insert('end', f"{'masuk':<18} {_fmt_jam(t_m)}\n")
                self.result_text.insert('end', f"{'selesai':<18} {_fmt_jam(t_s)}\n")
                self.result_text.insert('end', f"{'status':<18} {st}\n")
            else:
                self.result_text.insert('end', f"Pesanan {target} TIDAK DITEMUKAN.\n")
                self.result_text.insert('end', f"{_fmt_ribuan(cmp_cnt)} perbandingan.\n")

            self.result_text.config(state='disabled')
            self._log('linear_search', 'M3 - linear', elapsed)

        self._render_form(
            title='Search: linear search, O(n)',
            subtitle='Mencari dari elemen pertama sampai target ditemukan. Sederhana dan tidak butuh data terurut.',
            fields=[
                ('Nomor pesanan (oid)', 'O-137442', 'format O-000001 sampai O-200000', 'oid'),
            ],
            btn_text='CARI',
            btn_cmd=do_search
        )
        self._set_hint("Linear search menelusuri data dari depan satu per satu. Pada data 200.000 baris, mencari pesanan di belakang membutuhkan ratusan ribu perbandingan.")

    def _form_binary_search(self):
        from backend.m3_laporan import merge_sort, binary_search

        def do_search(entries):
            if not state['raw']:
                self.result_text.config(state='normal')
                self.result_text.delete('1.0', 'end')
                self.result_text.insert('end', 'Data belum dimuat! Silakan klik Load terlebih dahulu.\n')
                self.result_text.config(state='disabled')
                return

            target = entries['oid'].get().strip()
            total_n = len(state['raw'])

            # Pembangunan daftar terurut-oid (hanya sekali jika belum ada)
            build_msg = ""
            if state['sorted_oid'] is None:
                self.status_badge.config(text="[M3 - binary] Membangun indeks terurut-oid...")
                self.update_idletasks()
                t_b0 = time.perf_counter()
                sorted_list, _, _ = merge_sort(state['raw'], 'oid')
                state['sorted_oid_time'] = time.perf_counter() - t_b0
                state['sorted_oid'] = sorted_list
                build_msg = f"Membangun daftar terurut-oid dengan merge sort: {_fmt_ms(state['sorted_oid_time'])}."
            else:
                build_msg = "Memakai daftar terurut yang sudah dibangun."

            t0 = time.perf_counter()
            idx, cmp_cnt = binary_search(state['sorted_oid'], target, 'oid')
            elapsed = time.perf_counter() - t0

            # Hitung perbandingan jika dicari dengan linear search
            # (Jika ada format O-XXXXXX, indeks target kira-kira integer nomor - 1)
            lin_cmp_est = total_n
            try:
                num = int(target.replace('O-', ''))
                if 1 <= num <= total_n:
                    lin_cmp_est = num
            except ValueError:
                pass

            self.result_text.config(state='normal')
            self.result_text.delete('1.0', 'end')
            self.result_text.insert('end', f"{build_msg}\n")
            if idx != -1:
                p = state['sorted_oid'][idx]
                self.result_text.insert('end', f"Ditemukan pada baris ke-{_fmt_ribuan(idx + 1)} dari {_fmt_ribuan(total_n)}.\n")
                self.result_text.insert('end', f"{cmp_cnt} perbandingan, bandingkan dengan linear search ({_fmt_ribuan(lin_cmp_est)} perbandingan).\n\n")

                self.result_text.insert('end', f"{'kolom':<18} {'isi'}\n")
                self.result_text.insert('end', '-' * 48 + '\n')
                oid = p.get('oid') if hasattr(p, 'get') else p[0]
                pel = p.get('pelanggan') if hasattr(p, 'get') else p[1]
                res = p.get('resto') if hasattr(p, 'get') else p[2]
                men = p.get('menu') if hasattr(p, 'get') else p[3]
                hrg = p.get('harga') if hasattr(p, 'get') else p[4]
                pr  = p.get('prioritas') if hasattr(p, 'get') else p[5]
                t_m = p.get('t_masuk_detik') if hasattr(p, 'get') else p[6]
                t_s = p.get('t_selesai_detik') if hasattr(p, 'get') else p[7]
                st  = p.get('status') if hasattr(p, 'get') else p[8]

                self.result_text.insert('end', f"{'oid':<18} {oid}\n")
                self.result_text.insert('end', f"{'pelanggan':<18} {pel}\n")
                self.result_text.insert('end', f"{'resto':<18} {res}\n")
                self.result_text.insert('end', f"{'menu':<18} {men}\n")
                self.result_text.insert('end', f"{'harga':<18} {_fmt_ribuan(hrg)}\n")
                self.result_text.insert('end', f"{'prioritas':<18} {pr}\n")
                self.result_text.insert('end', f"{'masuk':<18} {_fmt_jam(t_m)}\n")
                self.result_text.insert('end', f"{'selesai':<18} {_fmt_jam(t_s)}\n")
                self.result_text.insert('end', f"{'status':<18} {st}\n")
            else:
                self.result_text.insert('end', f"Pesanan {target} TIDAK DITEMUKAN.\n")
                self.result_text.insert('end', f"{cmp_cnt} perbandingan, bandingkan dengan linear search ({_fmt_ribuan(total_n)} perbandingan).\n")

            self.result_text.config(state='disabled')
            self._log('binary_search', 'M3 - binary', elapsed)

        self._render_form(
            title='Search: binary search, O(log n)',
            subtitle='Membagi ruang pencarian menjadi separuh di setiap langkah. Hanya sah bila data sudah terurut.',
            fields=[
                ('Nomor pesanan (oid)', 'O-137442', 'format O-000001 sampai O-200000', 'oid'),
            ],
            btn_text='CARI',
            btn_cmd=do_search
        )
        self._set_hint("Binary search hanya membutuhkan belasan perbandingan (log2 n) untuk menemukan pesanan di antara 200.000 data, namun membutuhkan data yang sudah terurut menurut kuncinya.")


if __name__ == '__main__':
    app = App()
    app.mainloop()
