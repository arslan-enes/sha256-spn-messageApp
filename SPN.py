import unittest
from unittest import result
import selenium
#sonunda ters yazan fonksiyonlar cozümlemede kullanılıyor.
class spnSifreleme:
    
    def __init__(self):
        self.sbox_degerleri = [11, 6, 1, 15, 13, 3, 0, 4, 9, 5, 2, 8, 7, 12, 14, 10]
        self.pbox_degerleri = [15, 7, 16, 5, 9, 10, 1, 4, 14, 2, 6, 3, 8, 13, 11, 12]
        self.binaryAl = ["0000","0001","0010","0011","0100","0101","0110","0111", "1000", "1001", "1010", "1011", "1100", "1101", "1110", "1111"]
        self.anahtar = "10010101110010100000011100001110"
        self.anahtar_parcali = [self.anahtar[:16],self.anahtar[12:28],self.anahtar[16:32]]
        self.inversePbox = self.inversePermutation(self.pbox_degerleri,16)
        pass
    
    
    def xor(self,a,b):
        # xor işlemi
        
        if a == "1" and b == "1":
            return 0
        elif a == "0" and b == "1":
            return 1
        elif a == "1" and b == "0":
            return 1
        else:
            return 0
        
        
    def xorUygula(self,temp,anahtarParcasi):
        sonuc = ""
        for x in range(len(anahtarParcasi)):
            sonuc += str(self.xor(anahtarParcasi[x],temp[x]))
        return sonuc
    
    
    def sbox(self,temp):
        try:
            bolunmus = [int(temp[0:4],2),int(temp[4:8],2),int(temp[8:12],2),int(temp[12:16],2)]
        except:
            print("Bolunme hatasi")
        #print(bolunmus)
        sonuc = ""
        for x in bolunmus:
            sonuc += self.binaryAl[self.sbox_degerleri[x]]
        return sonuc
    
    def sbox_ters(self,temp):
        try:
            bolunmus = [int(temp[0:4],2),int(temp[4:8],2),int(temp[8:12],2),int(temp[12:16],2)]
        except:
            print("Bolunme hatasi")
        #print(bolunmus)
        sonuc = ""
        for x in bolunmus:
            t = self.sbox_degerleri.index(x)
            sonuc += self.binaryAl[t]
        return sonuc
    
    def pbox(self,temp):
        sonuc = ""
        for x in range(16):
            sonuc += temp[self.pbox_degerleri[x]-1]
        return sonuc
    
    
    def pbox_ters(self,temp):
        sonuc =""
        for x in range(16):
            sonuc += temp[int(self.inversePbox[x])-1]
        return sonuc
    
    
    def inversePermutation(self,arr, size) :
        
        #permutasyon islemini terse ceviren fonksiyon
        #(ALINTIDIR.)
        arr2 = [0] *(size)
        sonuc = []  
        for i in range(0, size) :
            arr2[arr[i] - 1] = i + 1

        for i in range(0, size) :
            sonuc.append(str(arr2[i]))
        return sonuc
    

    def SPN(self,string):
        sonuc=string
        for x in range(3):
            xorSonra = self.xorUygula(sonuc,self.anahtar_parcali[x])
            sboxSonra = self.sbox(xorSonra)
            pboxSonra = self.pbox(sboxSonra)
            sonuc = pboxSonra
        return sonuc
    
    
    def SPN_DESIFRE(self,string):
        sonuc = string
        
        for x in range(2,-1,-1):
            pboxOnce = self.pbox_ters(sonuc)
            sboxOnce = self.sbox_ters(pboxOnce)
            xorOnce = self.xorUygula(sboxOnce,self.anahtar_parcali[x])
            sonuc = xorOnce
        return sonuc
        
        
class TestSPN(unittest.TestCase):

    def test_spn(self):
        spnObj=spnSifreleme()
        result = spnObj.SPN("1000100010101111")
        self.assertEqual(result,"1101001010010011")
    
    def test_spn_ters(self):
        spnObj=spnSifreleme()
        result = spnObj.SPN_DESIFRE("1101001010010011")
        self.assertEqual(result,"1000100010101111")

    def test_xor(self):
        spnObj=spnSifreleme()
        result = spnObj.xorUygula("001100","110011")
        self.assertEqual(result,"111111")
    
    def test_sbox(self):
        spnObj=spnSifreleme()
        result = spnObj.sbox("1001011000101000")
        self.assertEqual(result,"0101000000011001")

    def test_pbox(self):
        spnObj=spnSifreleme()
        result = spnObj.pbox("1001011000101000")
        self.assertEqual(result,"0100001100100110")

    

        


