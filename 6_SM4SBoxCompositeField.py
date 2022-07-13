from pyfinite import ffield
from pyfinite import genericmatrix

gen = 0b111110101
F = ffield.FField(8, gen, useLUT=0) # 这里一定要写useLUT=0

#计算在F域上的平方
def field_pow2(x,F):
    return F.Multiply(x,x)

#计算在F域上的三次方
def field_pow3(x,F):
    return F.Multiply(x,field_pow2(x,F))

#计算在F域上的四次方
def field_pow4(x,F):
    return F.Multiply(field_pow2(x,F),F)

#搜索 w^2+w+1 = 0的根，得到正规基W=0x5d，W2=0x5c
for i in range(256):
    if field_pow2(i, F)^i^1 == 0:
        print(hex(i))

#然后，搜索GF(2^4)/GF(2^2)的正规基Z^4，求出其在GF(2^8)下的多项式基的表示，s(z)=z^2+z+N，N=W^2=0xbc
#得到Z=0x0c,Z4=0x0d
for i in range(256):
    if field_pow2(i, F)^i^0x5c == 0:                                  # 搜索 z^2+z+0x5c = 0的根
        print(hex(i))

#再搜索GF(2^8)/GF(2……4)的正规基{Y^16,Y}，我们求出其在GF(2^8)下多项式基的表示。r(y)=y^2+y+υ，υ=(N^2)Z
#得到Y=0xef,Y^16=0xee
u = F.Multiply(field_pow2(0x5c, F), 0x0c)
for i in range(256):
    if field_pow2(i, F)^i^0x76 == 0:                                  # 搜索 z^2+z+0x76 = 0的根
        print(hex(i))

#求多项式基在复合域基下表示
w = 0x5d
w_2 = 0x5c
z = 0x0c
z_4 = 0x0d
y = 0xef
y_16 = 0xee
w_2_z_4_y_16 = F.Multiply(F.Multiply(w_2, z_4), y_16)
w_z_4_y_16 = F.Multiply(F.Multiply(w, z_4), y_16)
w_2_z_y_16 = F.Multiply(F.Multiply(w_2, z), y_16)
w_z_y_16 = F.Multiply(F.Multiply(w, z), y_16)
w_2_z_4_y = F.Multiply(F.Multiply(w_2, z_4), y)
w_z_4_y = F.Multiply(F.Multiply(w, z_4), y)
w_2_z_y = F.Multiply(F.Multiply(w_2, z), y)
w_z_y = F.Multiply(F.Multiply(w, z), y)
 
print('w_2_z_4_y_16\t', hex(w_2_z_4_y_16))
print('w_z_4_y_16\t', hex(w_z_4_y_16))
print('w_2_z_y_16\t', hex(w_2_z_y_16))
print('w_z_y_16\t', hex(w_z_y_16))
print('w_2_z_4_y\t', hex(w_2_z_4_y))
print('w_z_4_y\t\t', hex(w_z_4_y))
print('w_2_z_y\t\t', hex(w_2_z_y))
print('w_z_y\t\t', hex(w_z_y))

#求X^(-1)
XOR = lambda x,y: x^y
AND = lambda x,y: x&y
DIV = lambda x,y: x
m = genericmatrix.GenericMatrix(size=(8, 8),zeroElement=0,identityElement=1,add=XOR,mul=AND,sub=XOR,div=DIV)
m.SetRow(0, [1, 1, 0, 1, 1, 1, 0, 1])
m.SetRow(1, [1, 1, 1, 0, 1, 1, 0, 1])
m.SetRow(2, [1, 1, 0, 1, 0, 0, 1, 0])
m.SetRow(3, [1, 0, 1, 0, 1, 0, 0, 1])
m.SetRow(4, [0, 1, 0, 0, 0, 0, 1, 0])
m.SetRow(5, [1, 1, 1, 0, 0, 1, 1, 1])
m.SetRow(6, [0, 0, 0, 1, 1, 1, 1, 0])
m.SetRow(7, [0, 0, 0, 0, 0, 1, 0, 0])
print(m)
print(m.Inverse())



def G4_mul(x, y):
    '''
    GF(2^2)的乘法运算，正规基{W^2, W}
    '''
    a = (x & 0x02)>>1
    b = x & 0x01
    c = (y & 0x02)>>1
    d = y & 0x01
    e = (a ^ b) & (c ^ d)
    return (((a & c) ^ e) << 1)|((b & d) ^ e)
 
def G4_mul_N(x):
    '''
    GF(2^2)的乘N操作，N = W^2
    '''
    a = (x & 0x02)>>1
    b = x & 0x01
    p = b
    q = a ^ b
    return (p<<1)|q
 
def G4_mul_N2(x):
    '''
    GF(2^2)的乘N^2操作，N = W^2
    '''
    a = (x & 0x02)>>1
    b = x & 0x01
    return ((a ^ b)<<1)|a
 
def G4_inv(x):
    '''
    GF(2^2)的求逆操作，该操作和GF(2^2)的平方操作等价
    '''
    a = (x & 0x02)>>1
    b = x & 0x01
    return (b<<1)|a
 
def G16_mul(x, y):
    '''
    GF(2^4)的乘法操作，正规基{Z^4, Z}
    '''
    a = (x & 0xc)>>2
    b = x & 0x03
    c = (y & 0xc)>>2
    d = y & 0x03
    e = G4_mul(a ^ b, c ^ d)
    e = G4_mul_N(e)
    p = G4_mul(a, c) ^ e
    q = G4_mul(b, d) ^ e
    return (p<<2) | q
 
def G16_sq_mul_u(x):
    '''
    GF(2^4)的平方后乘u操作, u = N^2Z, N = W^2
    '''
    a = (x & 0xc)>>2
    b = x & 0x03
    p = G4_inv(a ^ b) # G4平方和求逆等价
    q = G4_mul_N2(G4_inv(b))
    return (p<<2)|q
 
def G16_inv(x):
    '''
    GF(2^4)的求逆操作
    '''
    a = (x & 0xc)>>2
    b = x & 0x03
    c = G4_mul_N(G4_inv(a ^ b))
    d = G4_mul(a, b)
    e = G4_inv(c ^ d)
    p = G4_mul(e, b)
    q = G4_mul(e, a)
    return (p<<2)|q
 
def G256_inv(x):
    '''
    GF(2^8)的求逆操作
    '''
    a = (x & 0xF0)>>4
    b = x & 0x0F
    c = G16_sq_mul_u(a ^ b)
    d = G16_mul(a, b)
    e = G16_inv(c ^ d)
    p = G16_mul(e, b)
    q = G16_mul(e, a)
    return (p<<4)|q
 
def G256_new_basis(x, b):
    '''
    x在新基b下的表示
    '''
    y = 0
    for i in range(8):
        if x & (1<<(7-i)):
            y ^= b[i]
    return y

#计算输出SBox的值
g2b = [0b00100001, 0b11010011, 0b10000001, 0b01001010, 0b10001010, 0b10111001, 0b10110000, 0b11111111]
b2g = [0xf4, 0xec, 0x54, 0xa2, 0xd2, 0xc7, 0x2e, 0xd4]
A = [0b11100101, 0b11110010, 0b01111001, 0b10111100, 0b01011110, 0b00101111, 0b10010111, 0b11001011]
def SM4_SBOX(x):
    t = G256_new_basis(x, A)
    t ^= 0xd3
    t = G256_new_basis(t, g2b)
    t = G256_inv(t)
    t = G256_new_basis(t, b2g)
    t = G256_new_basis(t, A) #仿射变换乘
    return t ^ 0xd3
 
sbox = []
for i in range(256):
    sbox.append(SM4_SBOX(i))  # 生成sbox
 
for i,s in enumerate(sbox):
    print(f'%02x'%s,', ', end='')
    if (i+1)%16==0:
        print()

