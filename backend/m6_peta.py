# backend/m6_peta.py  –  M6: Graf (adjacency list manual) + BFS + Dijkstra

class Peta:
    """Graf berarah berbobot menggunakan adjacency list manual (no dict)."""

    class _AdjNode:
        __slots__ = ('ke','bobot','next')
        def __init__(self, ke, bobot):
            self.ke=ke; self.bobot=bobot; self.next=None

    def __init__(self):
        self._node_list = []    # list nama simpul
        self._heads     = []    # list kepala adjacency list (AdjNode|None)

    def _idx(self, nama):
        for i,n in enumerate(self._node_list):
            if n == nama: return i
        return -1

    def _get_or_add(self, nama):
        i = self._idx(nama)
        if i == -1:
            self._node_list.append(nama)
            self._heads.append(None)
            i = len(self._node_list)-1
        return i

    def tambah_sisi(self, dari, ke, bobot):
        u = self._get_or_add(dari); v = self._get_or_add(ke)
        node = self._AdjNode(v, bobot)
        node.next = self._heads[u]; self._heads[u] = node

    def simpul(self): return list(self._node_list)

    def tetangga(self, nama):
        i = self._idx(nama); r = []
        if i == -1: return r
        cur = self._heads[i]
        while cur:
            r.append((self._node_list[cur.ke], cur.bobot)); cur = cur.next
        return r

    # ── BFS: zona dalam hop ──────────────────────────────────────────────
    def zona(self, awal, max_hop):
        """Kembalikan list (simpul, hop) yang terjangkau dalam max_hop."""
        n = len(self._node_list); start = self._idx(awal)
        if start == -1: return []
        kunjung = [False]*n; jarak = [-1]*n
        # queue manual sederhana
        antri = [start]; kunjung[start]=True; jarak[start]=0; ptr=0
        while ptr < len(antri):
            u = antri[ptr]; ptr += 1
            cur = self._heads[u]
            while cur:
                v = cur.ke
                if not kunjung[v] and jarak[u]+1 <= max_hop:
                    kunjung[v]=True; jarak[v]=jarak[u]+1; antri.append(v)
                cur = cur.next
        return [(self._node_list[i], jarak[i]) for i in range(n)
                if kunjung[i] and i != start]

    # ── Dijkstra: rute terpendek ─────────────────────────────────────────
    def rute(self, awal, tujuan):
        """
        Dijkstra dengan MinHeap manual.
        Kembalikan (jarak, jalur_list, langkah_eksplorasi).
        """
        from backend.m5_katalog import MinHeap
        n = len(self._node_list)
        src = self._idx(awal); dst = self._idx(tujuan)
        if src==-1 or dst==-1: return -1, [], []

        INF = float('inf')
        dist   = [INF]*n; prev = [-1]*n
        dist[src] = 0
        heap = MinHeap(); heap.push(0, src)
        steps = []   # (simpul, dist_saat_ini, via)

        while len(heap):
            d, u = heap.pop_min()
            if d > dist[u]: continue
            steps.append((self._node_list[u], d,
                          self._node_list[prev[u]] if prev[u]!=-1 else '-'))
            if u == dst: break
            cur = self._heads[u]
            while cur:
                v = cur.ke; nd = dist[u] + cur.bobot
                if nd < dist[v]:
                    dist[v] = nd; prev[v] = u
                    heap.push(nd, v)
                cur = cur.next

        if dist[dst] == INF: return -1, [], steps
        jalur = []; cur = dst
        while cur != -1: jalur.append(self._node_list[cur]); cur = prev[cur]
        jalur.reverse()
        return dist[dst], jalur, steps
