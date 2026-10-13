# backend/m5_katalog.py  –  M5: BST (Katalog per rentang harga) + MinHeap (prioritas)

class _BSTNode:
    __slots__ = ('harga','items','kiri','kanan')
    def __init__(self, harga, item):
        self.harga = harga; self.items = [item]
        self.kiri = self.kanan = None

class Katalog:
    """BST berdasarkan harga menu."""
    def __init__(self):
        self._root = None; self._n = 0

    def _insert(self, node, harga, item):
        if node is None: return _BSTNode(harga, item)
        if harga < node.harga:  node.kiri  = self._insert(node.kiri,  harga, item)
        elif harga > node.harga: node.kanan = self._insert(node.kanan, harga, item)
        else: node.items.append(item)
        return node

    def tambah(self, harga, item):
        self._root = self._insert(self._root, harga, item); self._n += 1

    def _range(self, node, lo, hi, out):
        if node is None: return
        if lo < node.harga:  self._range(node.kiri,  lo, hi, out)
        if lo <= node.harga <= hi: out.extend(node.items)
        if hi > node.harga:  self._range(node.kanan, lo, hi, out)

    def rentang(self, lo, hi):
        out = []; self._range(self._root, lo, hi, out); return out

    def _stats(self, node, depth, acc):
        if node is None: return
        acc.append((node.harga, len(node.items), depth))
        self._stats(node.kiri,  depth+1, acc)
        self._stats(node.kanan, depth+1, acc)

    def stats(self):
        acc = []; self._stats(self._root, 0, acc); return acc

    def __len__(self): return self._n


class MinHeap:
    """Min-heap berbasis list — prioritas terkecil di puncak."""
    def __init__(self):
        self._d = []   # setiap elemen: (kunci_int, nilai)

    def _swap(self, i, j): self._d[i], self._d[j] = self._d[j], self._d[i]

    def _up(self, i):
        while i > 0:
            p = (i-1)//2
            if self._d[p][0] > self._d[i][0]: self._swap(p, i); i = p
            else: break

    def _down(self, i):
        n = len(self._d)
        while True:
            smallest = i; l = 2*i+1; r = 2*i+2
            if l < n and self._d[l][0] < self._d[smallest][0]: smallest = l
            if r < n and self._d[r][0] < self._d[smallest][0]: smallest = r
            if smallest == i: break
            self._swap(i, smallest); i = smallest

    def push(self, kunci, nilai):
        self._d.append((kunci, nilai)); self._up(len(self._d)-1)

    def pop_min(self):
        if not self._d: return None
        self._swap(0, len(self._d)-1)
        v = self._d.pop(); self._down(0); return v

    def peek(self): return self._d[0] if self._d else None
    def __len__(self): return len(self._d)

    def stats(self):
        return {'panjang': len(self._d),
                'puncak': self._d[0] if self._d else None}
