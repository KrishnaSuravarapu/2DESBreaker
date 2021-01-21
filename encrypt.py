from BitVector import *
permu=[7,6,4,0,2,5,1,3]
invpermu=[3,6,4,7,2,5,1,0]
expa = [3,0,1,2,1,2,3,0]
per4 = [1, 0, 3, 2]
sboxstr = [[[1, 0, 2, 3], [3, 1, 0, 2], [2, 0, 3, 1], [1, 3, 2, 0]],
        [[0, 3, 1, 2], [3, 2, 0, 1], [1, 0, 3, 2], [2, 1, 3, 0]]]

def per4bit(smallsize):
    permsmallsize = []
    if (smallsize.length() != 4):
        return None
    else:
        for i in range(0, len(per4)):
            permsmallsize.append(smallsize[per4[i]])
    return BitVector(bitlist=permsmallsize)


def expansion(smallsize, perm):
    bigsiz = []
    if (smallsize.length() != 4):
        return None
    else:
        for i in range(0, len(perm)):
            bigsiz.append(smallsize[perm[i]])
    return BitVector(bitlist=bigsiz)


def sbox(bigsize):
    half1 = bigsize[0:4]
    half2 = bigsize[4:8]
    p1 = BitVector(size=2)
    p2 = BitVector(size=2)
    p1 = half1[1:3]
    p2[0] = half1[0]
    p2[1] = half1[3]
    val1 = p1.int_val()
    val2 = p2.int_val()
    store1 = sboxstr[0][val2][val1]
    p1 = half2[1:3]
    p2[0] = half2[0]
    p2[1] = half2[3]
    val1 = p1.int_val()
    val2 = p2.int_val()
    store2 = sboxstr[1][val2][val1]
    new1 = BitVector(intVal=store1, size=2)
    new2 = BitVector(intVal=store2, size=2)
    new2+= new1
    new2 = per4bit(new2)
    print("sboxout",new2)
    return new2


def rounding(vaduko, key):
    part1 = BitVector(size=0)
    part2 = BitVector(size=0)
    part1 = vaduko[0:4]
    part2 = vaduko[4:8]
    exp = BitVector(size=0)
    exp += expansion(part2, expa)
    exp ^= key
    newval = sbox(exp)
    #print("Number in Rounding is ",number)
    newval ^= part1
    part2+=newval
    return part2

def permute8msg(msg,permu):
    lperm=[]
    for i in range(0,8):
        lperm.append(msg[permu[i]])
    #print(str(lperm))
    return BitVector(bitlist=lperm)

def invpermute8msg(msg,invpermu):
    lperm=[]
    for i in range(0,8):
        lperm.append(msg[invpermu[i]])
    return BitVector(bitlist=lperm)

def keyexp(key):
    key_bv = key
    C0 = BitVector(size=5)
    D0 = BitVector(size=5)
    C1 = BitVector(size=5)
    D1 = BitVector(size=5)
    key1 = BitVector(size=8)
    key2 = BitVector(size=8)
    PC1 = [[9, 7, 3, 8, 0], [2, 6, 5, 1, 4]]
    PC2 = [3, 1, 7, 5, 0, 6, 4, 2]
    for i in range(0, 5):
        C0[i] = key_bv[PC1[0][i]]
        D0[i] = key_bv[PC1[1][i]]
    C0 = C0 << 1
    D0 = D0 << 1
    C1 = C1 | C0
    D1 = D1 | D0
    C1 = C1 << 2
    D1 = D1 << 2
    temp_bv1 = BitVector(size=0)
    temp_bv2 = BitVector(size=0)
    temp_bv1 += C0
    temp_bv1 += D0
    temp_bv2 += C1
    temp_bv2 += D1
    key1=temp_bv1
    key2=temp_bv2
    key1=permute8msg(key1,PC2)
    key2=permute8msg(key2,PC2)
    key1+=key2
    return key1
def swap(msg):
    temp= BitVector(size=0)
    temp+=msg[0:4]
    msg[0:4]=msg[4:8]
    msg[4:8]=temp
    return msg

inputkey=input("Enter the 10-bit key :  ")
key=BitVector(bitstring = inputkey)
smthing=keyexp(key)
key1=smthing[0:8]
key2=smthing[8:16]

def encrypt(msg,key1,key2):
    msg=permute8msg(msg,permu)
    beachme = rounding(msg, key1)
    final = rounding(beachme, key2)
    final=swap(final)
    final=invpermute8msg(final,invpermu)
    return final

if len(sys.argv) is not 3:                                                    #(B)
    sys.exit('''Needs two command-line arguments, one for '''
             '''the message file and the other for the '''
             '''encrypted output file''')
finalout=BitVector(size=0)
bv = BitVector( filename = sys.argv[1] )                                      #(T)
while (bv.more_to_read):                                                      #(U)
    bv_read = bv.read_bits_from_file(8)                                          #(X)
    finalout+=encrypt(bv_read,key1,key2)
FILEOUT = open(sys.argv[2], 'w')                                              #(d)
FILEOUT.write(str(finalout))                                                  #(e)
FILEOUT.close()
