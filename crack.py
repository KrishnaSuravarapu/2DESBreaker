from BitVector import *
permu=[7,6,4,0,2,5,1,3]
invpermu=[3,6,4,7,2,5,1,0]
expa = [3,0,1,2,1,2,3,0]
per4 = [1, 0, 3, 2]
s0delxy=[[16,0,0,0],[0,8,4,4],[0,4,12,0],[4,4,0,8],[0,4,0,12],[4,4,8,0],[0,8,4,4],[8,0,4,4],[2,2,10,2],[4,4,0,8],[10,2,2,2],[0,8,4,4],[2,10,2,2],[8,0,4,4],[2,2,2,10],[4,4,8,0]]
s1delxy=[[16,0,0,0],[2,8,2,4],[0,6,4,6],[4,2,8,2],[2,0,10,4],[2,4,2,8],[0,10,0,6],[8,2,4,2],[4,6,0,6],[8,2,4,2],[2,0,10,4],[0,6,4,6],[0,6,4,6],[6,0,6,4],[10,4,2,0],[2,8,2,4]]
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
    #print("Key is",key1)
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
    
    #print("before enc permu",msg)
    msg=permute8msg(msg,permu)
    beachme = rounding(msg, key1)
    #print("beachme is for msg ,",msg,beachme)
    #print("after enc beachme",beachme)
    final = rounding(beachme, key2)
    #print("beforeswap",final)
    final=swap(final)
    #print("afterswap",final)
    #print("after enc final",final)
    #print("before permutation",final)
    final=invpermute8msg(final,invpermu)
    #print("msg is ",msg," final is ",final)
    # print("-------------------------\n")
    return final
full=BitVector(bitstring="00001000")
acck2=[0 for i in range(0,256)]
for num in range(0,60):
    num=BitVector(intVal=num,size=8)
    num2=num^full
    in1=num
    in2=num2
    out1=encrypt(num,key1,key2)
    out2=encrypt(num2,key1,key2)
    inp1chng=permute8msg(in1,permu)
    inp2chng=permute8msg(in2,permu)
    #print(inp1chng,inp2chng,"sajdkjabjsahdhbdhsbjhdbjsk")
    #delim=im1^im2
    delinp=inp1chng^inp2chng
    #print(delinp)
    #print(delim,delinp)
    #first round
    def diffanal(inp1,inp2):
        rightpart1=inp1[4:8]
        rightpart2=inp2[4:8]
        rightdiffstr=rightpart1^rightpart2
        rightdiff=expansion(rightdiffstr,expa)
        sbox0indiff=rightdiff[0:4]
        sbox1indiff=rightdiff[4:8]
        sbox0indiffint=sbox0indiff.int_val()
        sbox1indiffint=sbox1indiff.int_val()
        #print("teesko ra bai",sbox0indiffint,sbox1indiffint)
        sbox0outdiffint=s0delxy[sbox0indiffint].index(max(s0delxy[sbox0indiffint]))
        sbox1outdiffint=s1delxy[sbox1indiffint].index(max(s1delxy[sbox1indiffint]))
        #print("icha ra babu",sbox0outdiffint,sbox1outdiffint)
        med1=BitVector(intVal=sbox0outdiffint,size=2)
        med2=BitVector(intVal=sbox1outdiffint,size=2)
        imdiffright=BitVector(size=0)
        imdiffright+=med1
        imdiffright+=med2
        imdiffright=per4bit(imdiffright)
        imdiff=BitVector(size=0)
        imdiff+=rightdiffstr
        imdiff+=imdiffright
        #print("imdiff",imdiff)
        return imdiff

    imdiffa=diffanal(inp1chng,inp2chng)
    acck1=[]
    for i in range(0,256):
        randkey=BitVector(intVal=i,size=8)
        im1=rounding(inp1chng,randkey)
        im2=rounding(inp2chng,randkey)
        new=im1^im2
        #print(randkey,imdiffa,new)
        if(new == imdiffa):
            acck1.append(str(randkey))
    #print(acck1)
    if(len(acck1))==0:
        continue
    for k in range(0,len(acck2)):
        findiff=out1^out2
        middle1=rounding(inp1chng,BitVector(bitstring=acck1[k]))
        middle2=rounding(inp2chng,BitVector(bitstring=acck1[k]))
            #print(imdiffa,findiff)
        for j in range(0,256):
            guesskey=BitVector(intVal=j,size=8)
            if(encrypt(in1,acck1[k],guesskey)==out1 and encrypt(in2,acck1[k],guesskey)==out2):
                acck2[j]+=1
print(acck2)
#for i in range(0,255):
 #  randomkey=BitVector(intVal=i)'''



