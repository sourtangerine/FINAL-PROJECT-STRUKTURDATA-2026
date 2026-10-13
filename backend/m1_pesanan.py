# backend/m1_pesanan.py  –  M1: Array dinamis + Linked list berrantai

class Array:
    """Array dinamis: append O(1) amortized, akses O(1)."""
    def __init__(self):
        self._cap = 8
        self._data = [None] * self._cap
        self._n = 0

    def __len__(self): return self._n

    def _grow(self):
        nc = self._cap * 2
        nd = [None] * nc
        for i in range(self._n): nd[i] = self._data[i]
        self._data, self._cap = nd, nc

    def get(self, i):
        if i < 0 or i >= self._n: raise IndexError(i)
        return self._data[i]

    def append(self, v):
        if self._n == self._cap: self._grow()
        self._data[self._n] = v; self._n += 1

    def insert(self, i, v):
        if self._n == self._cap: self._grow()
        for j in range(self._n, i, -1): self._data[j] = self._data[j-1]
        self._data[i] = v; self._n += 1

    def delete(self, i):
        if i < 0 or i >= self._n: raise IndexError(i)
        v = self._data[i]
        for j in range(i, self._n-1): self._data[j] = self._data[j+1]
        self._data[self._n-1] = None; self._n -= 1
        return v

    def tambah_reguler(self, p):   self.append(p)
    def tambah_prioritas(self, p): self.insert(self._n // 2, p)
    def tambah_vip(self, p):       self.insert(0, p)
    def hapus(self, i):            return self.delete(i)
    def to_list(self): return [self._data[i] for i in range(self._n)]


class _Node:
    __slots__ = ('val','next')
    def __init__(self, v): self.val=v; self.next=None

class LinkList:
    """Linked list berantai: VIP O(1), Reguler O(1), Prioritas O(n)."""
    def __init__(self):
        self.head = self.tail = None; self._n = 0

    def __len__(self): return self._n

    def get(self, i):
        if i < 0 or i >= self._n: raise IndexError(i)
        cur = self.head
        for _ in range(i): cur = cur.next
        return cur.val

    def _insert_at(self, i, v):
        node = _Node(v)
        if i == 0:
            node.next = self.head; self.head = node
            if self._n == 0: self.tail = node
        else:
            cur = self.head
            for _ in range(i-1): cur = cur.next
            node.next = cur.next
            if cur.next is None: self.tail = node
            cur.next = node
        self._n += 1

    def delete(self, i):
        if i < 0 or i >= self._n: raise IndexError(i)
        if i == 0:
            v = self.head.val; self.head = self.head.next
            if self.head is None: self.tail = None
        else:
            cur = self.head
            for _ in range(i-1): cur = cur.next
            v = cur.next.val; cur.next = cur.next.next
            if cur.next is None: self.tail = cur
        self._n -= 1; return v

    def tambah_reguler(self, p):
        node = _Node(p)
        if self.tail is None: self.head = self.tail = node
        else: self.tail.next = node; self.tail = node
        self._n += 1

    def tambah_prioritas(self, p): self._insert_at(self._n // 2, p)
    def tambah_vip(self, p):       self._insert_at(0, p)
    def hapus(self, i):            return self.delete(i)
    def to_list(self):
        r=[]; cur=self.head
        while cur: r.append(cur.val); cur=cur.next
        return r
