def toLower(data) : 
    d = {}
    for k,v in data.items():
        if type(v) == int :
            d[k.lower()] = v
        else:
            d[k.lower()] = v.lower()
    return d