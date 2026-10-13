# frontend/ui.py - 2EZ4U Food Delivery Tkinter UI
import tkinter as tk
from tkinter import messagebox
import time, sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# --- Theme Colors (matching Image 1) ---
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
SEL_BORDER  = '#3b82f6'

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
    'next_oid': 200001,
}

def _fmt_ms(t):
    return f"{t*1000:.2f} ms" if t < 1 else f"{t:.3f} s"

def _new_oid():
    oid = f"O-{state['next_oid']:06d}"
    state['next_oid'] += 1
    return oid

def _pesanan_baru(nama, prioritas=3):
    t = int(time.time()) % 86400
    return {
        'oid': _new_oid(),
        'pelanggan': nama,
        'resto': 'manual',
        'menu': '-',
        'harga': 0,
        'prioritas': prioritas,
        't_masuk_detik': t,
        't_selesai_detik': None,
        'status': 'ANTRE'
    }

def _row_text(p):
    return (f"{p['oid']:<12} {str(p['pelanggan'])[:22]:<23} "
            f"{str(p['resto'])[:15]:<16} {str(p['menu'])[:14]:<15} "
            f"Rp{p['harga']:>7,} P{p['prioritas']} {p['status']}")

def _header():
    return (f"{'OID':<12} {'PELANGGAN':<23} {'RESTO':<16} "
            f"{'MENU':<15} {'HARGA':>9} PR STATUS")


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
    ('M2 - ANTREAN DAN UNDO', [
        ('Isi antrean FIFO', 'm2_fifo'),
        ('Layani berikutnya', 'm2_layani'),
        ('Undo', 'm2_undo'),
    ]),
    ('M3 DAN M4 - LAPORAN DAN PENCARIAN', [
        ('Laporan harian', 'm3_laporan'),
        ('Cari di laporan', 'm3_cari'),
        ('Bangun indeks hash', 'm4_hash'),
        ('Cari pesanan (oid)', 'm4_cari_oid'),
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
        self.geometry('1050x700')
        self.minsize(850, 550)
        self.configure(bg=BG_APP)

        self.current_key = None
        self.sidebar_buttons = {}

        self._build_header()
        self._build_body()
        self._build_statusbar()

        # Default selected view matching screenshot
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
        sb_container = tk.Frame(body, bg=BG_SIDEBAR, width=260)
        sb_container.pack(side='left', fill='y')
        sb_container.pack_propagate(False)

        # Right divider line
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

        # Mousewheel scroll support on sidebar
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
        res_container.pack(fill='both', expand=True, padx=14, pady=(0, 6))

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

        # Bottom Command Log Area
        cmd_container = tk.Frame(self.right_panel, bg=BG_WHITE)
        cmd_container.pack(fill='x', side='bottom', padx=14, pady=(0, 6))

        tk.Label(cmd_container, text='COMMAND', font=FONT_LABEL, fg='#334155',
                 bg=BG_WHITE, anchor='w').pack(fill='x', pady=(0, 2))

        cmd_border = tk.Frame(cmd_container, bg=BORDER_DARK, bd=1, relief='solid')
        cmd_border.pack(fill='x')

        cmd_ys = tk.Scrollbar(cmd_border, orient='vertical')
        self.cmd_text = tk.Text(cmd_border, height=4, bg=BG_WHITE, fg=TEXT_DARK,
                                font=FONT_CMD, relief='flat', bd=0,
                                highlightthickness=0, wrap='none', state='disabled',
                                yscrollcommand=cmd_ys.set)
        cmd_ys.config(command=self.cmd_text.yview)
        cmd_ys.pack(side='right', fill='y')
        self.cmd_text.pack(side='left', fill='both', expand=True)

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
            # Section Header
            hdr = tk.Label(self.sb_frame, text=header_title, font=FONT_SB_HDR,
                           fg=HDR_FG, bg=HDR_BG, anchor='w', padx=6, pady=2,
                           relief='solid', bd=1)
            hdr.pack(fill='x', padx=6, pady=(6, 2))

            # Items under Section
            for label, key in items:
                btn = tk.Button(self.sb_frame, text=label, font=FONT_SB_BTN,
                                bg=BTN_BG, fg=BTN_FG, activebackground='#e2e8f0',
                                anchor='w', padx=6, pady=2, relief='solid', bd=1,
                                cursor='hand2', command=lambda k=key, l=label: self._on_sidebar_click(k, l))
                btn.pack(fill='x', padx=6, pady=1)
                self.sidebar_buttons[key] = btn

    def _on_sidebar_click(self, key, label):
        # M2 through M6 trigger "Fitur sedang dikerjakan" popup
        if key.startswith(('m2_', 'm3_', 'm4_', 'm5_', 'm6_')):
            messagebox.showinfo('Fitur Sedang Dikerjakan', 'Fitur sedang dikerjakan.')
            return

        self._select_action(key)

    def _select_action(self, key):
        self.current_key = key
        # Update sidebar visual selection
        for k, btn in self.sidebar_buttons.items():
            if k == key:
                btn.config(bg=SEL_BG, fg=SEL_FG)
            else:
                btn.config(bg=BTN_BG, fg=BTN_FG)

        # Route to appropriate action form
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
        }
        fn = ROUTES.get(key)
        if fn:
            fn()

    def _log(self, cmd, modul, elapsed_s):
        ms_str = _fmt_ms(elapsed_s)
        line = f"{cmd:<21} -> {modul:<15} {ms_str:>10}\n"
        self.cmd_text.config(state='normal')
        self.cmd_text.insert('end', line)
        self.cmd_text.see('end')
        self.cmd_text.config(state='disabled')
        self.status_badge.config(text='siap')

    def _render_form(self, title, subtitle, fields, btn_text, btn_cmd):
        for w in self.form_frame.winfo_children():
            w.destroy()

        # Header Titles
        tk.Label(self.form_frame, text=title, font=FONT_TITLE, fg=TEXT_DARK,
                 bg=BG_WHITE, anchor='w').pack(fill='x', padx=14, pady=(10, 1))
        if subtitle:
            tk.Label(self.form_frame, text=subtitle, font=FONT_SUB, fg=TEXT_SUB,
                     bg=BG_WHITE, anchor='w').pack(fill='x', padx=14, pady=(0, 8))

        # Form Row
        row_frame = tk.Frame(self.form_frame, bg=BG_WHITE)
        row_frame.pack(fill='x', padx=14, pady=(0, 8))

        entries = {}
        for lbl_text, default_val, helper_text, field_id in fields:
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

        # Divider line below form
        tk.Frame(self.form_frame, height=1, bg=BORDER_GRAY).pack(fill='x', padx=14, pady=(4, 6))

    # --- M1 Forms & Handlers ---
    def _form_load(self):
        def do_load(_):
            from loader import baca_pesanan
            from backend.m1_pesanan import Array, LinkList
            t0 = time.perf_counter()
            rows = baca_pesanan()
            state['raw'] = rows
            arr = Array()
            lnk = LinkList()
            for r in rows:
                arr.tambah_reguler(r)
                lnk.tambah_reguler(r)
            state['arr'] = arr
            state['lnk'] = lnk
            elapsed = time.perf_counter() - t0

            self.result_text.config(state='normal')
            self.result_text.delete('1.0', 'end')
            self.result_text.insert('end', f"Loaded {len(rows):,} pesanan\n"
                                           f"Array: {len(arr):,}  LinkList: {len(lnk):,}\n"
                                           f"Waktu: {_fmt_ms(elapsed)}\n")
            self.result_text.config(state='disabled')
            self._log('load', 'M1 - larik', elapsed)

        self._render_form(
            title='Load data CSV',
            subtitle='Membaca pesanan.csv ke memori untuk Array dan LinkedList',
            fields=[],
            btn_text='LOAD',
            btn_cmd=do_load
        )

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

            try:
                i = int(entries['idx'].get())
            except ValueError:
                i = 0
            try:
                n = int(entries['n'].get())
            except ValueError:
                n = 20

            t0 = time.perf_counter()
            rows = ds.to_list()
            elapsed = time.perf_counter() - t0

            self.result_text.config(state='normal')
            self.result_text.delete('1.0', 'end')
            self.result_text.insert('end', _header() + '\n' + '-' * 90 + '\n')
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

            t0 = time.perf_counter()
            if prioritas == 3:
                ds.tambah_reguler(p)
            elif prioritas == 2:
                ds.tambah_prioritas(p)
            else:
                ds.tambah_vip(p)
            elapsed = time.perf_counter() - t0

            self.result_text.config(state='normal')
            self.result_text.delete('1.0', 'end')
            self.result_text.insert('end', f"Ditambahkan: {_row_text(p)}\n"
                                           f"Panjang {name}: {len(ds):,}\n"
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

            try:
                i = int(entries['idx'].get())
            except ValueError:
                i = 0

            t0 = time.perf_counter()
            try:
                v = ds.hapus(i)
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
                                           f"Sisa {name}: {len(ds):,}\n"
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


if __name__ == '__main__':
    app = App()
    app.mainloop()
