def round_price(x, d=4):
    try:
        return round(float(x), d)
    except:
        return x
