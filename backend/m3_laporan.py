# backend/m3_laporan.py  –  M3: Insertion sort, Merge sort, Linear search, Binary search

def insertion_sort(larik, kunci):
    """
    Insertion sort in-place dan stabil. O(n^2).
    Kembalikan jumlah perbandingan dan pemindahan.
    """
    n = len(larik); cmp = 0; mv = 0
    for i in range(1, n):
        cur = larik[i]; j = i - 1
        while j >= 0:
            cmp += 1
            if larik[j][kunci] > cur[kunci]:   # > menjaga stabilitas
                larik[j+1] = larik[j]; j -= 1; mv += 1
            else:
                break
        larik[j+1] = cur; mv += 1
    return cmp, mv


def merge_sort(larik, kunci):
    """
    Merge sort rekursif dan stabil. O(n log n).
    Kembalikan (hasil_terurut, jumlah_perbandingan, jumlah_pemindahan).
    """
    cmp_box = [0]; mv_box = [0]

    def _merge(L, R):
        out = []; i = j = 0
        while i < len(L) and j < len(R):
            cmp_box[0] += 1
            if L[i][kunci] <= R[j][kunci]:   # <= menjaga stabilitas
                out.append(L[i]); i += 1
            else:
                out.append(R[j]); j += 1
            mv_box[0] += 1
        while i < len(L): out.append(L[i]); i += 1; mv_box[0] += 1
        while j < len(R): out.append(R[j]); j += 1; mv_box[0] += 1
        return out

    def _ms(a):
        if len(a) <= 1: return a
        mid = len(a)//2
        return _merge(_ms(a[:mid]), _ms(a[mid:]))

    hasil = _ms(larik)
    return hasil, cmp_box[0], mv_box[0]


def linear_search(larik, target, kunci='oid'):
    """Telusur satu per satu. O(n). Kembalikan (indeks|-1, perbandingan)."""
    cmp = 0
    for i, item in enumerate(larik):
        cmp += 1
        if item[kunci] == target:
            return i, cmp
    return -1, cmp


def binary_search(larik_terurut, target, kunci='oid'):
    """
    Binary search pada larik terurut menurut kunci.
    Kembalikan (indeks|-1, perbandingan).
    """
    lo, hi, cmp = 0, len(larik_terurut)-1, 0
    while lo <= hi:
        mid = (lo+hi)//2; cmp += 1
        val = larik_terurut[mid][kunci]
        if val == target:   return mid, cmp
        elif val < target:  lo = mid+1
        else:               hi = mid-1
    return -1, cmp
