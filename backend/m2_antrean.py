# backend/m2_antrean.py  –  M2: Stack, Queue naif, Queue melingkar, Undo/Redo
from backend.m1_pesanan import Array

def _get_val(p, key):
    """Ambil nilai field baik dari dict maupun tuple/list dengan konstanta indeks."""
    if hasattr(p, 'get'):
        return p.get(key)
    # (OID, PELANGGAN, RESTO, MENU, HARGA, PRIORITAS, T_MASUK, T_SELESAI, STATUS)
    keys = ('oid', 'pelanggan', 'resto', 'menu', 'harga', 'prioritas',
            't_masuk_detik', 't_selesai_detik', 'status')
    for i in range(len(keys)):
        if keys[i] == key and i < len(p):
            return p[i]
    return None

def _get_oid(p):
    val = _get_val(p, 'oid')
    return str(val) if val is not None else ''


class Tumpukan:
    """Tumpukan (LIFO) berbasis Array dinamis dari M1."""
    def __init__(self):
        self._arr = Array()

    def push(self, x):
        self._arr.append(x)

    def pop(self):
        if self._arr._n == 0:
            return None
        return self._arr.delete(self._arr._n - 1)

    def peek(self):
        if self._arr._n == 0:
            return None
        return self._arr.get(self._arr._n - 1)

    def kosong(self):
        return self._arr._n == 0

    def panjang(self):
        return self._arr._n

    def __len__(self):
        return self._arr._n

    def to_list(self):
        return self._arr.to_list()


# Alias Stack untuk kompatibilitas
Stack = Tumpukan


# ── Kasir: pemecah token, infix → postfix → evaluasi ───────────────────────

def _prec(op):
    if op in ('+', '-'):
        return 1
    if op in ('*', '/'):
        return 2
    return 0


def _tokenize(expr):
    tokens = []
    i = 0
    s = expr.strip()
    n = len(s)
    prev_tok_type = 'start'  # 'start', 'op', 'num', 'lparen', 'rparen'
    
    while i < n:
        ch = s[i]
        if ch.isspace():
            i += 1
            continue
        if ch in '()*+-/':
            if ch == '-':
                # Periksa apakah minus unary (di awal atau setelah operator/kurung buka)
                if prev_tok_type in ('start', 'op', 'lparen'):
                    raise ValueError("Minus unary tidak didukung, gunakan nilai positif saja.")
            tokens.append(ch)
            if ch == '(':
                prev_tok_type = 'lparen'
            elif ch == ')':
                prev_tok_type = 'rparen'
            else:
                prev_tok_type = 'op'
            i += 1
        elif ch.isdigit():
            j = i
            while j < n and s[j].isdigit():
                j += 1
            tokens.append(s[i:j])
            prev_tok_type = 'num'
            i = j
        else:
            raise ValueError(f"Karakter tidak valid: '{ch}'")

    # Validasi kurung seimbang
    kurung = 0
    for t in tokens:
        if t == '(':
            kurung += 1
        elif t == ')':
            kurung -= 1
            if kurung < 0:
                raise ValueError("Kurung tidak seimbang: tanda ')' berlebih.")
    if kurung != 0:
        raise ValueError("Kurung tidak seimbang: tanda '(' belum ditutup.")

    return tokens


def ke_postfix(ekspresi):
    """
    Shunting-yard algorithm.
    Kembalikan (postfix_list, langkah_list).
    langkah_list berisi tuple: (langkah_str, token, tindakan, stack_str, output_str)
    """
    tokens = _tokenize(ekspresi)
    stack = Tumpukan()
    out = []
    steps = []
    step_num = 1

    for tok in tokens:
        l_str = f"1.{step_num}"
        step_num += 1
        if tok == '(':
            stack.push(tok)
            steps.append((l_str, tok, 'push (', ' '.join(stack.to_list()), ' '.join(out)))
        elif tok == ')':
            while not stack.kosong() and stack.peek() != '(':
                x = stack.pop()
                out.append(x)
                steps.append((l_str, tok, f'pop {x} sampai (', ' '.join(stack.to_list()), ' '.join(out)))
            stack.pop()  # buang '('
            steps.append((l_str, tok, 'buang (', ' '.join(stack.to_list()), ' '.join(out)))
        elif tok in ('+', '-', '*', '/'):
            p_tok = _prec(tok)
            while (not stack.kosong() and stack.peek() in ('+', '-', '*', '/')
                   and _prec(stack.peek()) >= p_tok):
                x = stack.pop()
                out.append(x)
                steps.append((l_str, tok, f'pop {x} (sama/lebih kuat)', ' '.join(stack.to_list()), ' '.join(out)))
            stack.push(tok)
            steps.append((l_str, tok, f'push {tok}', ' '.join(stack.to_list()), ' '.join(out)))
        else:
            out.append(tok)
            steps.append((l_str, tok, 'angka -> output', ' '.join(stack.to_list()), ' '.join(out)))

    while not stack.kosong():
        x = stack.pop()
        out.append(x)
        steps.append(('1.akhir', x, f'pop sisa {x}', ' '.join(stack.to_list()), ' '.join(out)))

    return out, steps


def hitung(postfix_list):
    """
    Evaluasi ekspresi postfix.
    Kembalikan (total_angka, langkah_list).
    langkah_list berisi tuple: (langkah_str, token, tindakan, stack_str)
    """
    stack = Tumpukan()
    steps = []
    step_num = 1

    for tok in postfix_list:
        l_str = f"2.{step_num}"
        step_num += 1
        if tok in ('+', '-', '*', '/'):
            b = stack.pop()  # operand kanan
            a = stack.pop()  # operand kiri
            if a is None or b is None:
                raise ValueError(f"Ekspresi tidak valid: operand kurang untuk operator '{tok}'.")
            
            if tok == '+':
                r = a + b
            elif tok == '-':
                r = a - b
            elif tok == '*':
                r = a * b
            else:
                if b == 0:
                    raise ZeroDivisionError("Pembagian dengan nol!")
                r = a / b
                if isinstance(r, float) and r.is_integer():
                    r = int(r)
            stack.push(r)
            stack_str = ' '.join(str(v) for v in stack.to_list())
            steps.append((l_str, tok, f"{a} {tok} {b} = {r}", stack_str))
        else:
            val = int(tok)
            stack.push(val)
            stack_str = ' '.join(str(v) for v in stack.to_list())
            steps.append((l_str, tok, f"push {val}", stack_str))

    hasil = stack.pop()
    if isinstance(hasil, float) and hasil.is_integer():
        hasil = int(hasil)
    return hasil, steps


# ── Antrean Naif ───────────────────────────────────────────────────────────

class AntreanNaif:
    """Antrean naif berbasis Array dinamis M1. Dequeue menggeser seluruh elemen: O(n)."""
    def __init__(self):
        self._arr = Array()
        self.total_geser = 0
        self.last_geser = 0

    def enqueue(self, x):
        self._arr.append(x)

    def dequeue(self):
        if self._arr._n == 0:
            return None
        v = self._arr.get(0)
        geser = self._arr._n - 1
        for i in range(geser):
            self._arr._data[i] = self._arr._data[i + 1]
        self._arr._data[self._arr._n - 1] = None
        self._arr._n -= 1
        self.total_geser += geser
        self.last_geser = geser
        return v

    def pop_rear(self):
        if self._arr._n == 0:
            return None
        return self._arr.delete(self._arr._n - 1)

    def push_front_many(self, daftar):
        for i in range(len(daftar) - 1, -1, -1):
            self._arr.insert(0, daftar[i])

    def front(self):
        return self._arr.get(0) if self._arr._n > 0 else None

    def panjang(self):
        return self._arr._n

    def __len__(self):
        return self._arr._n

    def to_list(self):
        return self._arr.to_list()


# ── Antrean Melingkar (Circular Buffer) ────────────────────────────────────

class AntreanMelingkar:
    """
    Circular buffer dengan kapasitas K, front, rear, dan count.
    Enqueue & dequeue O(1).
    Wajib memakai count untuk membedakan kondisi kosong (count == 0)
    dan penuh (count == K) karena pada kedua kondisi tersebut front == rear.
    """
    def __init__(self, K=32768):
        self._K = K
        self._d = [None] * K
        self._front = 0
        self._rear = 0
        self._count = 0
        self.total_geser = 0
        self.last_geser = 0

    def _grow(self):
        nK = self._K * 2
        nd = [None] * nK
        for i in range(self._count):
            nd[i] = self._d[(self._front + i) % self._K]
        self._d = nd
        self._front = 0
        self._rear = self._count
        self._K = nK

    def enqueue(self, x):
        if self._count == self._K:
            self._grow()
        self._d[self._rear] = x
        self._rear = (self._rear + 1) % self._K
        self._count += 1

    def dequeue(self):
        if self._count == 0:
            return None
        v = self._d[self._front]
        self._d[self._front] = None
        self._front = (self._front + 1) % self._K
        self._count -= 1
        self.last_geser = 0
        return v

    def pop_rear(self):
        if self._count == 0:
            return None
        self._rear = (self._rear - 1 + self._K) % self._K
        v = self._d[self._rear]
        self._d[self._rear] = None
        self._count -= 1
        return v

    def push_front_many(self, daftar):
        m = len(daftar)
        while self._count + m > self._K:
            self._grow()
        for i in range(m - 1, -1, -1):
            self._front = (self._front - 1 + self._K) % self._K
            self._d[self._front] = daftar[i]
            self._count += 1

    def front(self):
        return self._d[self._front] if self._count > 0 else None

    def kosong(self):
        return self._count == 0

    def is_empty(self):
        return self._count == 0

    def panjang(self):
        return self._count

    def __len__(self):
        return self._count

    @property
    def kapasitas(self):
        return self._K

    @property
    def front_idx(self):
        return self._front

    @property
    def rear_idx(self):
        return self._rear

    def to_list(self):
        r = [None] * self._count
        for i in range(self._count):
            r[i] = self._d[(self._front + i) % self._K]
        return r


# ── Manajer Riwayat Undo/Redo ──────────────────────────────────────────────

class UndoRedo:
    """
    Manajer riwayat undo/redo menggunakan dua Tumpukan (Stack).
    Setiap aksi baru mengosongkan tumpukan redo.
    """
    def __init__(self, antrean_naif: AntreanNaif, antrean_circ: AntreanMelingkar):
        self._q_naif = antrean_naif
        self._q_circ = antrean_circ
        self._undo = Tumpukan()
        self._redo = Tumpukan()

    def rekam_enqueue(self, item):
        self._undo.push(('ENQUEUE', item))
        while not self._redo.kosong():
            self._redo.pop()

    def rekam_dequeue_naif(self, items):
        # items bisa berupa list ataupun single item
        daftar = items if isinstance(items, list) else [items]
        self._undo.push(('DEQUEUE_NAIF', daftar))
        while not self._redo.kosong():
            self._redo.pop()

    def rekam_dequeue_circ(self, items):
        daftar = items if isinstance(items, list) else [items]
        self._undo.push(('DEQUEUE_CIRC', daftar))
        while not self._redo.kosong():
            self._redo.pop()

    def undo_last(self):
        if self._undo.kosong():
            return None, [], "Tumpukan undo kosong."
        aksi, data = self._undo.pop()
        items = []
        msg = ""

        if aksi == 'ENQUEUE':
            # Kebalikan enqueue: buang elemen terakhir dari kedua antrean
            if len(self._q_naif) > 0:
                self._q_naif.pop_rear()
            if len(self._q_circ) > 0:
                self._q_circ.pop_rear()
            oid = _get_oid(data)
            items = [data]
            msg = f"Pembatalan enqueue: {oid} dikeluarkan lagi dari belakang."
        elif aksi == 'DEQUEUE_NAIF':
            self._q_naif.push_front_many(data)
            items = data
            msg = f"Pembatalan dequeue naif: {len(data)} pesanan dikembalikan ke depan."
        elif aksi == 'DEQUEUE_CIRC':
            self._q_circ.push_front_many(data)
            items = data
            msg = f"Pembatalan dequeue circular: {len(data)} pesanan dikembalikan ke depan."

        self._redo.push((aksi, data))
        return aksi, items, msg

    def redo_last(self):
        if self._redo.kosong():
            return None, [], "Tumpukan redo kosong."
        aksi, data = self._redo.pop()
        items = []
        msg = ""

        if aksi == 'ENQUEUE':
            self._q_naif.enqueue(data)
            self._q_circ.enqueue(data)
            oid = _get_oid(data)
            items = [data]
            msg = f"Enqueue dikerjakan lagi: {oid} masuk kembali ke belakang."
        elif aksi == 'DEQUEUE_NAIF':
            keluar = []
            for _ in range(len(data)):
                v = self._q_naif.dequeue()
                if v is not None:
                    keluar.append(v)
            items = keluar
            msg = f"Dequeue naif dikerjakan lagi: {len(data)} pesanan keluar lagi."
        elif aksi == 'DEQUEUE_CIRC':
            keluar = []
            for _ in range(len(data)):
                v = self._q_circ.dequeue()
                if v is not None:
                    keluar.append(v)
            items = keluar
            msg = f"Dequeue circular dikerjakan lagi: {len(data)} pesanan keluar lagi."

        self._undo.push((aksi, data))
        return aksi, items, msg

    def undo_depth(self):
        return len(self._undo)

    def redo_depth(self):
        return len(self._redo)

    def history(self):
        return self._undo.to_list()

    def stats(self):
        return (len(self._q_naif), len(self._q_circ), self._q_circ.kapasitas,
                self._q_naif.total_geser, len(self._undo), len(self._redo))
