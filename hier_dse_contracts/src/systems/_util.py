def shrink(iv, α=0.9):
    lo, hi = iv
    mid = 0.5*(lo+hi)
    half = 0.5*(hi-lo)*α
    return (mid-half, mid+half)