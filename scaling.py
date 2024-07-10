def scale(n):
    sq = int(n**0.5)
    rem = n - sq * (sec := n // sq)
    sq1, sec2, rem2 = sq + 1, n // (sq + 1), n - (sq + 1) * (n // (sq + 1))
    width, height, rem = (sq, sec, rem) if rem < rem2 else (sq1, sec2, rem2)
    print(f"{n}={width}x{height}+{rem}")
    

scale(45)