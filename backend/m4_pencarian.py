# backend/m4_pencarian.py  –  M4: Hash table terbuka (open addressing) + merge sort



class PetaHash:
    """
    Hash table dengan open addressing (linear probing).
    Tidak menggunakan dict/set built-in.
    """
    def __init__(self, kapasitas=512):
        self._cap = kapasitas
        self._keys   = [None] * self._cap
        self._values = [None] * self._cap
        self._count  = 0
        self._HAPUS  = object()   # sentinel untuk slot yang dihapus

    def _hash(self, k):
        # polynomial rolling hash
        h = 0
        for ch in str(k): h = (h * 31 + ord(ch)) % self._cap
        return h

    def _probe(self, k):
        """Kembalikan (indeks slot, ditemukan)."""
        idx = self._hash(k); first_del = -1
        for _ in range(self._cap):
            s = self._keys[idx]
            if s is None:
                return (first_del if first_del != -1 else idx), False
            if s is self._HAPUS:
                if first_del == -1: first_del = idx
            elif s == k:
                return idx, True
            idx = (idx+1) % self._cap
        return (first_del if first_del != -1 else -1), False

    def _grow(self):
        old_k, old_v = self._keys, self._values
        self._cap *= 2
        self._keys   = [None]*self._cap
        self._values = [None]*self._cap
        self._count  = 0
        for i in range(len(old_k)):
            if old_k[i] not in (None, self._HAPUS):
                self.put(old_k[i], old_v[i])

    def put(self, k, v):
        if self._count >= self._cap * 0.7: self._grow()
        idx, found = self._probe(k)
        if not found: self._count += 1
        self._keys[idx] = k; self._values[idx] = v

    def get(self, k):
        idx, found = self._probe(k)
        return self._values[idx] if found else None

    def __len__(self): return self._count
