import tkinter as tk
from tkinter import filedialog
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
nltk.download('punkt')

class Istatistik:
    selected_files = []

    def en_sık_kullanılan_kelime(self):
        kelime_listesi = []
        kelime_kullanım_sayisi = {}

        with open("en_sık_kullanilan_kelime.txt", "w") as file:
            file.write("")
    
        if Dosyaverilerinidüzenleme.selected_files:
            for dosya in Dosyaverilerinidüzenleme.selected_files:
                with open(dosya, 'r') as file:
                    veri = file.read()
                    ayrilan_kelimeler = word_tokenize(veri)
                
                    for kelime in ayrilan_kelimeler:
                        if not kelime.isalnum():
                            continue
                        if kelime not in kelime_kullanım_sayisi:
                            kelime_kullanım_sayisi[kelime] = 1
                        else:
                            kelime_kullanım_sayisi[kelime] += 1
    
        en_sık_kelimeler = sorted(kelime_kullanım_sayisi.items(), key=lambda x: x[1], reverse=True)[:5]
    
        with open("en_sık_kullanilan_kelime.txt", "w") as file:
            for kelime, sayi in en_sık_kelimeler:
                file.write(f"{kelime}: {sayi}\n")

        

        secilen_dosya_yuzu.config(text=str(en_sık_kelimeler))

        return en_sık_kelimeler
                        
    
    def kelime_sayisi(self):
        dosya_uzunluklari = []
        for dosya_yolu in self.selected_files:
            with open(dosya_yolu, 'r') as file:
                
                veri = file.read()
                kelimeler = word_tokenize(veri)
                kelimeler = [kelime for kelime in kelimeler if kelime.isalnum()]
                uzunluk = len(kelimeler)
                dosya_uzunluklari.append(uzunluk)
        kelime_sayisi_text = "\n".join([f"{i+1}. Dosyanızda yer alan kelime sayısı: {uzunluk}" for i, uzunluk in enumerate(dosya_uzunluklari)])
        secilen_dosya_yuzu.config(text=kelime_sayisi_text)

class Dosyaverilerinidüzenleme:
    selected_files = []

    def cumle_ayırma(self):
        with open("ayrilan_cumleler.txt", "w") as file:
            file.write("")  
        if self.selected_files:
            dosya_sayisi = len(self.selected_files)
            for i in range(dosya_sayisi):
                with open(self.selected_files[i], 'r') as file:
                    veri = file.read()
                    ayrilan_cumleler = sent_tokenize(veri)
                    with open("ayrilan_cumleler.txt", "a") as file:
                        file.write(f"{i+1}. Dosyanın cümlelerine ayrılmış formu: {ayrilan_cumleler} \n \n")

            with open("ayrilan_cumleler.txt", "r") as file:
                    veri = file.readlines()
                    
            secilen_dosya_yuzu.config(text=veri)
                    

    def kelimelere_ayırma(self):
        with open("ayrilan_kelimeler.txt", "w") as file:
            file.write("")  
        if self.selected_files:
            dosya_sayisi = len(self.selected_files)
            for i in range(dosya_sayisi):
                with open(self.selected_files[i], 'r') as file:
                    veri = file.read()
                    ayrilan_kelimeler = word_tokenize(veri)
                    with open("ayrilan_kelimeler.txt", "a") as file:
                        file.write(f"{i+1}. Dosyanın kelimelerine ayrılmış formu: {ayrilan_kelimeler} \n")
            with open("ayrilan_kelimeler.txt", "r") as file:
                    veri = file.readlines()

            secilen_dosya_yuzu.config(text=veri)

    def noktalama_isareti_silme(self):
        noktalamasız_liste = []
        for dosya_yolu in self.selected_files:
            with open(dosya_yolu, 'r') as file:
                veri = file.read()
                kelimeler = word_tokenize(veri)
                dosya_noktalamasız_liste = []
                for kelime in kelimeler:
                    if kelime.isalnum():
                        dosya_noktalamasız_liste.append(kelime)
                noktalamasız_liste.append(dosya_noktalamasız_liste)

        secilen_dosya_yuzu.config(text=noktalamasız_liste)
        
class Dosyakiyaslama():
    def dosya_secme(self, label_widget):
        selected_files = filedialog.askopenfilenames(title="Dosya Seç", filetypes=[("Metin Dosyaları", "*.txt")])
        if selected_files:
            dosya_listesi = "\n".join(selected_files)  
            label_widget.config(text="Seçilen Dosyalar:\n" + dosya_listesi)
            Dosyaverilerinidüzenleme.selected_files = selected_files
            dosya_sayisi = len(selected_files)
            print(f"{dosya_sayisi} dosya seçildi.")
            return selected_files

    def jaccard_benzerlik(self, dosya_yolu1, dosya_yolu2, label_widget):
        with open(dosya_yolu1, 'r') as file1, open(dosya_yolu2, 'r') as file2:
            kıyaslanacak1 = set(file1.read().split())
            kıyaslanacak2 = set(file2.read().split())

        intersection = len(kıyaslanacak1.intersection(kıyaslanacak2))
        union = len(kıyaslanacak1.union(kıyaslanacak2))

        if union == 0 or intersection == 0:
            print("Dosyalardan biri ya da her ikisi de boş olduğu için benzerlik yoktur")
            return 0
        benzerlik_Degeri = str(intersection / union)
    
        secilen_dosya_yuzu.config(text="Jaccard Benzerliği:" + benzerlik_Degeri )

    def secilen_tum_dosyalarda_kiyas(self, label_widget):
        if Dosyaverilerinidüzenleme.selected_files:
            dosya_sayisi = len(Dosyaverilerinidüzenleme.selected_files)
            for i in range(dosya_sayisi):
                for j in range(i + 1, dosya_sayisi):
                    self.jaccard_benzerlik(Dosyaverilerinidüzenleme.selected_files[i], Dosyaverilerinidüzenleme.selected_files[j], label_widget)

    def secilen_iki_dosya_kiyasi(self, label_widget):
        selected_files = filedialog.askopenfilenames(title="Dosya Seç", filetypes=[("Tüm Dosyalar", ".")])
        if len(selected_files) == 2:  
            dosya_listesi = "\n".join(selected_files)  
            label_widget.config(text="Seçilen Dosyalar:\n" + dosya_listesi)
        
            dosya_sayisi = len(selected_files)
            print(f"{dosya_sayisi} dosya seçildi.")
            return selected_files
        else:
            print("Lütfen sadece iki dosya seçin.")
            return
    
    def benzerlik_kıyaslama_islemi(self, label_widget):
        dosyalar = self.secilen_iki_dosya_kiyasi(label_widget)
        if dosyalar:
            self.jaccard_benzerlik(*dosyalar, label_widget)
        else:
            print("Dosya seçme işlemi tamamlanmadı.")

    def benzerlik_kıyaslama(self, label_widget):
        acilacak_diger_pencere = tk.Tk()
        acilacak_diger_pencere.title("Metin Benzerlik Oranı")
        acilacak_diger_pencere.geometry('450x500')

        label = tk.Label(acilacak_diger_pencere, text="Benzerlik Kıyaslama", fg="magenta", font='Times 16 bold' )
        label.pack()

        buton = tk.Button(acilacak_diger_pencere, text="Secilen Tüm Dosyalar İçin Benzerlik Kıyaslaması", command=lambda: self.secilen_tum_dosyalarda_kiyas(label_widget), activebackground='pink')
        buton.place(x=80, y=50)

        buton2 = tk.Button(acilacak_diger_pencere, text="Secilen 2 Dosyanın Benzerliğini Kıyaslama", command=lambda: self.benzerlik_kıyaslama_islemi(label_widget), activebackground='pink')
        buton2.place(x=80, y=90)

def arayuz_olusturma():
    global secilen_dosya_yuzu
    pencere = tk.Tk()

    pencere.title("Metin Analiz Uygulaması")
    pencere.geometry('450x500')
    label = tk.Label(pencere, text="METİN ANALİZ UYGULAMASI", fg="green", font='Times 16 bold' )
    label.pack()

    secilen_dosya_yuzu = tk.Label(pencere, text="", wraplength=400)
    secilen_dosya_yuzu.pack()

    dosya_kiyaslama = Dosyakiyaslama()

    buton = tk.Button(pencere, text="Dosya Ekleme", command=lambda: dosya_kiyaslama.dosya_secme(secilen_dosya_yuzu), activebackground='light green')
    buton.pack()

    buton2 = tk.Button(pencere, text="Benzerlik Kıyaslama", command=lambda: dosya_kiyaslama.benzerlik_kıyaslama(secilen_dosya_yuzu), activebackground='light green')
    buton2.pack()

    buton3 = tk.Button(pencere, text="Dosya Verilerini Cümlelerine Ayrıma", command=lambda: Dosyaverilerinidüzenleme().cumle_ayırma(), activebackground='light green')
    buton3.pack()

    buton4 = tk.Button(pencere, text="Dosya Verilerini Kelimelerine Ayırma", command=lambda: Dosyaverilerinidüzenleme().kelimelere_ayırma(), activebackground='light green')
    buton4.pack()

    buton5 = tk.Button(pencere, text="Dosya Verilerinden Noktalama İşareti Silme", command=lambda: Dosyaverilerinidüzenleme().noktalama_isareti_silme(), activebackground='light green')
    buton5.pack()

    buton6 = tk.Button(pencere, text="Kod İstatistikleri", command=lambda: Istatistik().en_sık_kullanılan_kelime(), activebackground='light green')
    buton6.pack()
    
    pencere.mainloop()

arayuz_olusturma()
