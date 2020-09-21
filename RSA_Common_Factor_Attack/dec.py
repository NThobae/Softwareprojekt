from Crypto.PublicKey import RSA
from Crypto.Util import number
from Crypto.Cipher import PKCS1_v1_5
def gcd(a,b):
        if b>a:
                r=a
                a=b
                b=r
                while((a%b)>0):
                        g= a%b
                        a=b
                        b=g
        return b



pathfiles=['./1.pem','./2.pem','./3.pem','./4.pem','./5.pem','./6.pem','./7.pem','./8.pem']
Cfiles=['./1.bin','./2.bin','./3.bin','./4.bin','./5.bin','./6.bin','./7.bin','./8.bin']
for i in range(8):
        for j in range(i+1,8):
                if(i!=j):
                        k1= RSA.importKey(open(pathfiles[i])) #import the public keys
                        k2= RSA.importKey(open(pathfiles[j]))
                        print(pathfiles[i],"vs",pathfiles[j])
                        pp=gcd(k1.n,k2.n)
                        p1=pp-1
                        if(pp!=1):#if there is some common factor between of two n
                                print("geklappt")
                                qq=k1.n//pp#put the common factor in qq
                                q1=qq-1
                                mod1=p1*q1
                                d1=number.inverse(k1.e,mod1)#try to calculate the private exponent
                                rsa_sk= RSA.construct((k1.n,k1.e,d1,pp,qq))#claculate the private key
                                ciphertext = open(Cfiles[i],"rb").read()#read the first encrypted message
                                cipher= PKCS1_v1_5.new(rsa_sk)
                                message= cipher.decrypt(ciphertext, None)#decrypt the first message
                                print(Cfiles[i])
                                print (message)
                                qq2=k2.n//pp
                                q2=qq2-1
                                mod2=p1*q2
                                d2=number.inverse(k2.e,mod2)#try to calculate the seccond private exponent
                                rsa_sk2= RSA.construct((k2.n,k2.e,d2,pp,qq2))
                                ciphertext2 = open(Cfiles[j],"rb").read()#read the seccond enc message
                                cipher2= PKCS1_v1_5.new(rsa_sk2)
                                message2= cipher2.decrypt(ciphertext2, None)
                                print(Cfiles[j])
                                print(message2)