MAX_BITS = 8

X_AND_Y= dict(zx=0, nx=0, zy=0, ny=0, f=0, no=0)
X_PLUS_Y = dict(zx=0, nx=0, zy=0, ny=0, f=1, no=0)
Y_MINUS_X= dict(zx=0, nx=0, zy=0, ny=1, f=1, no=1)
X_PLUS_ONE= dict(zx=0, nx=1, zy=1, ny=1, f=1, no=1)
X_OR_Y= dict(zx=0, nx=1, zy=0, ny=1, f=0, no=1)
Y_MINUS_ONE= dict(zx=1, nx=1, zy=0, ny=0, f=1, no=0)


def ALU_sim(x, y, zx, nx, zy, ny, f, no):

    print()
    print()
    print("{:<10}{:^10}{:10}{:^10}{:10}\n".format('', 'x', '', 'y', ''))
    print("{:<10}{:<10}{:<10}{:<10}{:<10}".format("INPUT:", x, '=> ' + to_int(x), y, '=> ' + to_int(y)))
    print("{:<10}{:^10}{:10}{:^10}{:10}".format('', '|', '', '|', ''))
    
    if zx: x = zero_out(x)
    zxstr = "zx={}".format(zx)
    print("{:<10}{:<10}{:<10}{:^10}{:<10}".format(zxstr, x, '=> ' + to_int(x), '|', ''))
    print("{:<10}{:^10}{:10}{:^10}{:10}".format('', '|', '', '|', ''))
    
    if nx: x = negate(x)
    nxstr = "nx={}".format(nx)
    print("{:<10}{:<10}{:<10}{:^10}{:<10}".format(nxstr, x, '=> ' + to_int(x), '|', ''))
    print("{:<10}{:^10}{:10}{:^10}{:10}".format('', '|', '', '|', ''))
    
    if zy: y = zero_out(y)
    zystr = "zy={}".format(zy)
    print("{:<10}{:^10}{:<10}{:<10}{:<10}".format(zystr, '|', '', y, '=> ' + to_int(y)))
    print("{:<10}{:^10}{:10}{:^10}{:10}".format('', '|', '', '|', ''))
    
    if ny: y = negate(y)
    nystr = "ny={}".format(ny)
    print("{:<10}{:^10}{:<10}{:<10}{:<10}".format(nystr, '|', '', y, '=> ' + to_int(y)))
    print("{:<10}{:^10}{:10}{:^10}{:10}".format('', '|', '', '|', ''))
    
    print("{:<14}{}".format('', '---------------------'))
    print("{:<10}{:^30}".format('', '|'))
    print("{:<10}{:^30}".format('', '|'))
    
    if f:
        op = '+'
        out = adder8(x, y)
    else:
        op = '&'
        out = bitwise_and(x, y)


    fstr = "f: {}".format(op)
    print("{:<20}{:<10}{}".format(fstr, out, '=> ' + to_int(out)))
    print("{:<10}{:^30}".format('', '|'))

    if no: out = negate(out)
    nostr = "no={}".format(no)
    
    ng = out[0]
    zr = is_zero(out)
    
    print("{:<20}{:<10}{}".format(nostr, out, '=> ' + to_int(out)))
    print("{:<10}{:^30}".format('', '|'))
  
    print("{:<14}{}".format('', '---------------------'))
    print("{:<14}{:<10}{:<10}{:<10}".format('OUTPUT:', '|', '|', '|'))
    print("{:<14}{:<10}{:<10}{:<10}".format('ng', ng, '|', '|'))
    print("{:<14}{:<10}{:<10}{:<10}".format('', '', '|', '|'))
    print("{:<14}{:<10}{:<10}{:<10}".format('zr', '', zr, '|'))
    print("{:<14}{:<10}{:<10}{:<10}".format('', '', '', '|'))
    print("{:<14}{:<10}{:<6}{:<10}{}".format('f(x, y)', '', '', out, '=> ' + to_int(out)))
    print()
    print()

def to_int(binstr):
    if binstr[0] == '1': # negative number
        binstr = ''.join('1' if bit == '0' else '0' for bit in binstr)
        return str(-(int(binstr, 2) + 1))
    else:
        return str(int(binstr, 2))

def to_str(num):
    out = '1' if num < 0 else '0' 
    out += validate(bin(abs(num))[2:], MAX_BITS-1)
    return out

def adder(a, b, c):
    a, b, c = bool(a), bool(b), bool(c)
    s = a ^ b ^ c
    c = (c & (a | b)) | (a & b)
    return s, c

def adder8(x, y):
    c = 0
    out = list(zero_out(x))
    x, y = list(x), list(y)
    i = len(x) - 1
    while i >= 0:
        out[i], c = adder(int(x[i]), int(y[i]), c)
        i -= 1
    return ''.join([str(int(n)) for n in out])

def is_zero(binstr):
    for bit in binstr:
        if bit != '0':
            return False
    return True

def negate(binstr):
    return ''.join([str(int(not bool(int(n)))) for n in list(binstr)])

def zero_out(binstr):
    return '0' * len(binstr)

def validate(binstr, maxbits=MAX_BITS):
    zstr = '0' * maxbits
    return zstr[len(binstr[:maxbits]):] + binstr[:maxbits]

def bitwise_and(a, b):
    return ''.join([str(int(m) & int(n)) for m, n in zip(a, b)])
