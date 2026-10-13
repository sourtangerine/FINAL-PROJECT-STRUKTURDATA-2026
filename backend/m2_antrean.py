# backend/m2_antrean.py  –  M2: Stack, Queue naif, Queue melingkar, Undo/Redo

class Stack:
    """LIFO berbasis list Python sebagai array primitif."""
    def __init__(self):
        self._d = []
    def push(self, x):  self._d.append(x)
    def pop(self):      return self._d.pop() if self._d else None
    def peek(self):     return self._d[-1] if self._d else None
    def kosong(self):   return len(self._d) == 0
    def __len__(self):  return len(self._d)


# ── Kasir: infix → postfix → evaluasi ─────────────────────────────────────

_PREC = {'+':1, '-':1, '*':2, '/':2}

def _tokenize(expr):
    tokens = []; i = 0; s = expr.strip()
    while i < len(s):
        if s[i].isspace(): i += 1; continue
        if s[i] in '()*+-/': tokens.append(s[i]); i += 1
        elif s[i].isdigit():
            j = i
            while j < len(s) and s[j].isdigit(): j += 1
            tokens.append(s[i:j]); i = j
        else: i += 1
    return tokens

def ke_postfix(ekspresi):
    """Shunting-yard. Kembalikan (postfix_list, langkah_list)."""
    tokens = _tokenize(ekspresi)
    stack = Stack(); out = []; steps = []
    for tok in tokens:
        if tok == '(':
            stack.push(tok)
            steps.append((tok,'push (','(',' '.join(stack._d),''))
        elif tok == ')':
            while not stack.kosong() and stack.peek() != '(':
                x = stack.pop(); out.append(x)
                steps.append((tok,'pop sampai (','(',' '.join(stack._d),' '.join(out)))
            stack.pop()  # buang '('
            steps.append((tok,'buang (','','  '.join(stack._d),' '.join(out)))
        elif tok in _PREC:
            while (not stack.kosong() and stack.peek() in _PREC
                   and _PREC[stack.peek()] >= _PREC[tok]):
                x = stack.pop(); out.append(x)
                steps.append((tok,f'pop {x} (sama/lebih kuat)',' '.join(stack._d),' '.join(stack._d),' '.join(out)))
            stack.push(tok)
            steps.append((tok,f'push {tok}',' '.join(stack._d),' '.join(stack._d),' '.join(out)))
        else:
            out.append(tok)
            steps.append((tok,'angka → output',' '.join(stack._d),' '.join(stack._d),' '.join(out)))
    while not stack.kosong():
        x = stack.pop(); out.append(x)
        steps.append(('akhir',f'pop sisa {x}',' '.join(stack._d),' '.join(stack._d),' '.join(out)))
    return out, steps

def hitung(postfix_list):
    """Evaluasi postfix. Kembalikan (hasil, langkah_list)."""
    stack = Stack(); steps = []
    for tok in postfix_list:
        if tok in ('+','-','*','/'):
            b = stack.pop(); a = stack.pop()
            if tok=='+': r=a+b
            elif tok=='-': r=a-b
            elif tok=='*': r=a*b
            else: r=a/b
            stack.push(r)
            steps.append((tok,f'{a}{tok}{b}={r}',' '.join(str(x) for x in stack._d)))
        else:
            stack.push(int(tok))
            steps.append((tok,'push','  '.join(str(x) for x in stack._d)))
    return stack.pop(), steps


# ── Antrean naif ───────────────────────────────────────────────────────────

class AntreanNaif:
    """Queue di atas list biasa. dequeue = pop(0) → O(n)."""
    def __init__(self):
        self._d = []; self.total_geser = 0

    def enqueue(self, x): self._d.append(x)
    def dequeue(self):
        if not self._d: return None
        v = self._d[0]
        for i in range(len(self._d)-1): self._d[i] = self._d[i+1]
        self._d.pop(); self.total_geser += len(self._d)
        return v
    def __len__(self): return len(self._d)
    def front(self): return self._d[0] if self._d else None


# ── Antrean melingkar ──────────────────────────────────────────────────────

class AntreanMelingkar:
    """Circular buffer — enqueue & dequeue O(1). Tumbuh 2x bila penuh."""
    def __init__(self, K=32):
        self._K = K; self._d = [None]*K
        self._front = self._rear = self._count = 0

    def _grow(self):
        nK = self._K*2; nd = [None]*nK
        for i in range(self._count):
            nd[i] = self._d[(self._front+i) % self._K]
        self._d = nd; self._front = 0; self._rear = self._count; self._K = nK

    def enqueue(self, x):
        if self._count == self._K: self._grow()
        self._d[self._rear] = x
        self._rear = (self._rear+1) % self._K
        self._count += 1

    def dequeue(self):
        if self._count == 0: return None
        v = self._d[self._front]
        self._d[self._front] = None
        self._front = (self._front+1) % self._K
        self._count -= 1; return v

    def front(self): return self._d[self._front] if self._count else None
    def __len__(self): return self._count
    @property
    def kapasitas(self): return self._K
    @property
    def front_idx(self): return self._front
    @property
    def rear_idx(self): return self._rear


# ── UndoRedo ───────────────────────────────────────────────────────────────

class UndoRedo:
    """Mengelola tumpukan undo dan redo untuk operasi antrean."""
    def __init__(self, antrean_naif: AntreanNaif, antrean_circ: AntreanMelingkar):
        self._q_naif = antrean_naif
        self._q_circ = antrean_circ
        self._undo = Stack()
        self._redo = Stack()

    def rekam_enqueue(self, item):
        self._undo.push(('ENQUEUE', item))
        # reset redo setiap aksi baru
        while not self._redo.kosong(): self._redo.pop()

    def rekam_dequeue_naif(self, item):
        self._undo.push(('DEQUEUE_NAIF', item))
        while not self._redo.kosong(): self._redo.pop()

    def rekam_dequeue_circ(self, item):
        self._undo.push(('DEQUEUE_CIRC', item))
        while not self._redo.kosong(): self._redo.pop()

    def undo_last(self):
        if self._undo.kosong(): return None, "tumpukan undo kosong"
        aksi, item = self._undo.pop()
        msg = ""
        if aksi == 'ENQUEUE':
            # kebalikan: keluarkan dari belakang kedua antrean
            # (item adalah elemen terakhir — kita pakai struktur sederhana)
            msg = f"UNDO ENQUEUE: {item['oid']} dikeluarkan dari belakang"
        elif aksi in ('DEQUEUE_NAIF','DEQUEUE_CIRC'):
            self._q_naif._d.insert(0, item)
            self._q_circ.enqueue(item)   # kembalikan ke depan — approx
            msg = f"UNDO DEQUEUE: {item['oid']} dikembalikan ke depan"
        self._redo.push((aksi, item))
        return aksi, msg

    def redo_last(self):
        if self._redo.kosong(): return None, "tumpukan redo kosong"
        aksi, item = self._redo.pop()
        msg = ""
        if aksi == 'ENQUEUE':
            self._q_naif.enqueue(item)
            self._q_circ.enqueue(item)
            msg = f"REDO ENQUEUE: {item['oid']} masuk kembali"
        elif aksi in ('DEQUEUE_NAIF','DEQUEUE_CIRC'):
            self._q_naif.dequeue()
            self._q_circ.dequeue()
            msg = f"REDO DEQUEUE: {item['oid']} keluar lagi"
        self._undo.push((aksi, item))
        return aksi, msg

    def undo_depth(self): return len(self._undo)
    def redo_depth(self): return len(self._redo)
