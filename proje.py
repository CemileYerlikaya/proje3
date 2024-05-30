import json
import os
import matplotlib.pyplot as plt
import nltk
import string
from tkinter import *
from tkinter.filedialog import *
from tkinter.scrolledtext import ScrolledText
from googletrans import Translator
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from collections import Counter
from tkinter import messagebox
from tkinter import filedialog

class Arama_yapma:
    def dosya_secme(self):
        selected_files = filedialog.askopenfilenames(title="Dosya Seç", filetypes=[("Metin Dosyaları", "*.txt")])
        if selected_files:
            self.kelime_sec(selected_files)

    def kelime_sec(self, dosyalar):
        kelime_penceresi = Toplevel(arayuz)
        kelime_penceresi.title("Kelime Seç")

        Label(kelime_penceresi, text="Bir kelime girin:", font=("Helvetica", 14)).pack(pady=10)

        kelime_entry = Entry(kelime_penceresi, font=("Helvetica", 12))
        kelime_entry.pack(pady=10)

        Button(kelime_penceresi, text="Ara",
               command=lambda: self.kelime_ara(kelime_entry.get(), kelime_penceresi, dosyalar)).pack(pady=5)

    def kelime_ara(self, kelime, pencere, dosyalar):
        pencere.destroy()
        self.ekrana_yazdirma(kelime, dosyalar)

    def kelime_sayisi_bulma(self, kelime, dosyalar):
        kelime_sayisi = 0
        for dosya_yolu in dosyalar:
            with open(dosya_yolu, 'r') as file:
                veri = file.read()
                kelimeler = word_tokenize(veri)
                kelime_sayisi += kelimeler.count(kelime)
        return kelime_sayisi

    def cumle_bulma(self, kelime, dosyalar):
        cumleler = []
        for dosya_yolu in dosyalar:
            with open(dosya_yolu, 'r') as file:
                veri = file.read()
                ayrilan_cumleler = sent_tokenize(veri)
                for cumle in ayrilan_cumleler:
                    if kelime in word_tokenize(cumle):
                        cumleler.append(cumle)
        return cumleler

    def ekrana_yazdirma(self, kelime, dosyalar):
        kelime_sayisi = self.kelime_sayisi_bulma(kelime, dosyalar)
        bulunan_cumleler = self.cumle_bulma(kelime, dosyalar)

        sonuc_penceresi = Toplevel(arayuz)
        sonuc_penceresi.title("Arama Sonuçları")

        sonuclar_label = Label(sonuc_penceresi, text="Arama Sonuçları:", font=("Helvetica", 14, 'bold'))
        sonuclar_label.pack(pady=5)
        sonuclar_text = ScrolledText(sonuc_penceresi, width=100, height=25, font=("Helvetica", 12))
        sonuclar_text.pack(pady=5)

        sonuclar_text.insert('end', f"'{kelime}' kelimesi toplam {kelime_sayisi} kez geçti.\n\n")
        sonuclar_text.insert('end', "Kelimenin geçtiği cümleler:\n")
        for cumle in bulunan_cumleler:
            sonuclar_text.insert('end', f"{cumle}\n")
        
        sonuclar_text.config(state='disabled')

        Button(sonuc_penceresi, text="Geri Dön", command=sonuc_penceresi.destroy).pack(pady=5)

class Metin_islemleri:
    def dosya_secme(self):
        selected_files = filedialog.askopenfilenames(title="Dosya Seç", filetypes=[("Metin Dosyaları", "*.txt")])
        if selected_files:
            self.secim(selected_files)

    def secim(self, dosyalar):
        analiz_penceresi = Toplevel(arayuz)
        analiz_penceresi.title("Analiz Seçenekleri")

        Label(analiz_penceresi, text="Lütfen bir seçenek seçin", font=("Helvetica", 14)).pack(pady=10)

        Button(analiz_penceresi, text="Metni Cümlelerine Ayır",
               command=lambda: [analiz_penceresi.destroy(), self.ekrana_yazdirma("ayir", dosyalar)]).pack(pady=5)
        Button(analiz_penceresi, text="Gereksiz Kelimeleri Sil",
               command=lambda: [analiz_penceresi.destroy(), self.ekrana_yazdirma("gereksiz", dosyalar)]).pack(pady=5)
        Button(analiz_penceresi, text="Noklama İşaretlerini Kaldır",
               command=lambda: [analiz_penceresi.destroy(), self.ekrana_yazdirma("noktalama", dosyalar)]).pack(pady=5)

    def noktalama_isareti_silme(self, selected_files):
        noktalamasız_liste = []
        for dosya_yolu in selected_files:
            with open(dosya_yolu, 'r') as file:
                veri = file.read()
                kelimeler = word_tokenize(veri)
                dosya_noktalamasız_liste = []
                for kelime in kelimeler:
                    if kelime.isalnum():
                        dosya_noktalamasız_liste.append(kelime)
                noktalamasız_liste.append(" ".join(dosya_noktalamasız_liste))
        return noktalamasız_liste

    def cumle_ayirma(self, selected_files):
        ayrilan_cumleler_listesi = []
        for i, dosya_yolu in enumerate(selected_files):
            with open(dosya_yolu, 'r') as file:
                veri = file.read()
                ayrilan_cumleler = sent_tokenize(veri)
                ayrilan_cumleler_listesi.append(f"{i + 1}. Dosyanın cümlelerine ayrılmış formu: \n {'\n'.join(ayrilan_cumleler)} \n")
        return ayrilan_cumleler_listesi

    def etkisiz_kelime_silme(self, selected_files):
        etkisiz_kelime_turkce = ["yani", "işte", "hani", "şey", "tabii ki", "well", "actually", "just", "şöyle", "basically", "and", "ve"]
        etkisiz_kelime_olmaksizin_olusan_yapi = []
        for dosya in selected_files:
            with open(dosya, 'r') as file:
                veri = file.read()
                ayrilan_kelimeler = word_tokenize(veri)
                for kelime in ayrilan_kelimeler:
                    if kelime not in etkisiz_kelime_turkce:
                        etkisiz_kelime_olmaksizin_olusan_yapi.append(kelime)
                etkisiz_kelime_olmaksizin_olusan_yapi.append("\n")
        return [" ".join(etkisiz_kelime_olmaksizin_olusan_yapi)]

    def ekrana_yazdirma(self, analiz_turu, selected_files):
        if analiz_turu == "gereksiz":
            analiz_sonuclari = self.etkisiz_kelime_silme(selected_files)
        elif analiz_turu == "ayir":
            analiz_sonuclari = self.cumle_ayirma(selected_files)
        elif analiz_turu == "noktalama":
            analiz_sonuclari = self.noktalama_isareti_silme(selected_files)

        sonuc_penceresi = Toplevel(arayuz)
        sonuc_penceresi.title("Analiz Sonuçları")

        sonuclar_label = Label(sonuc_penceresi, text="Analiz Sonuçları:", font=("Helvetica", 14, 'bold'))
        sonuclar_label.pack(pady=5)
        sonuclar_text = ScrolledText(sonuc_penceresi, width=100, height=25, font=("Helvetica", 12))
        sonuclar_text.pack(pady=5)

        Button(sonuc_penceresi, text="Geri Dön", command=sonuc_penceresi.destroy).pack(pady=5)

        for sonuc in analiz_sonuclari:
            sonuclar_text.insert('end', f"{sonuc}\n")
        sonuclar_text.config(state='disabled')
class Dosyakiyaslama():
    def dosya_secme(self):
        selected_files = filedialog.askopenfilenames(title="Dosya Seç", filetypes=[("Metin Dosyaları", "*.txt")])
        if selected_files:
            dosya_listesi = "\n".join(selected_files)
            print("Seçilen Dosyalar:\n" + dosya_listesi)
            dosya_sayisi = len(selected_files)
            print(f"{dosya_sayisi} dosya seçildi.")
            yazdirilacak = []

            if dosya_sayisi >= 2:
                for i in range(dosya_sayisi):
                   for j in range(i + 1, dosya_sayisi):
                        dosya_yolu1 = selected_files[i]
                        dosya_yolu2 = selected_files[j]
                        benzerlik = self.jaccard_benzerlik(dosya_yolu1, dosya_yolu2)
                        yazdirilacak.append(f"{dosya_yolu1} ve {dosya_yolu2} dosyaları arasındaki Jaccard Benzerliği: {benzerlik}")
                return yazdirilacak
            else:
                yazdirilacak = "Lütfen en az iki dosya seçin."
                return [yazdirilacak]


    def jaccard_benzerlik(self, dosya_yolu1, dosya_yolu2):
        with open(dosya_yolu1, 'r', encoding='utf-8') as file1, open(dosya_yolu2, 'r', encoding='utf-8') as file2:
            kiyaslanacak1 = set(file1.read().split())
            kiyaslanacak2 = set(file2.read().split())

        intersection = len(kiyaslanacak1.intersection(kiyaslanacak2))
        union = len(kiyaslanacak1.union(kiyaslanacak2))

        if union == 0 or intersection == 0:

            yazdirilacak="Dosyalardan biri ya da her ikisi de boş olduğu için benzerlik yoktur"
            return yazdirilacak
        
        benzerlik_degeri = intersection / union
        return benzerlik_degeri
    def benzerlik_ekrana_yazdirma(self, analiz_turu):
        if analiz_turu == "benzerlik":
            analiz_sonuclari = Dosyakiyaslama().dosya_secme()

        sonuc_penceresi = Toplevel(arayuz)
        sonuc_penceresi.title("Analiz Sonuçları")


        sonuclar_label = Label(sonuc_penceresi, text="Analiz Sonuçları:", font=("Helvetica", 14, 'bold'))
        sonuclar_label.pack(pady=5)
        sonuclar_text = ScrolledText(sonuc_penceresi, width=100, height=25, font=("Helvetica", 12))
        sonuclar_text.pack(pady=5)

        Button(sonuc_penceresi, text="Geri Dön", command=lambda: geri_don(sonuc_penceresi)).pack(pady=5)
        for sonuc in analiz_sonuclari:
            sonuclar_text.insert('end', f"{sonuc}\n")
        sonuclar_text.config(state='disabled')


def harf_sikligi(metin):
    harfler = 'abcçdefgğhıijklmnoöprsştuüvyzxwq'

    harf_sikliklari = {h: 0 for h in harfler}

    for char in metin.lower():
        if char in harfler:
            harf_sikliklari[char] += 1

    analiz_sonuclari = {}
    for harf, sayi in harf_sikliklari.items():
        analiz_sonuclari[harf] = sayi

    return analiz_sonuclari

def kelime_sikligi(metin):
    metin = metin.lower()
    kelimeler = word_tokenize(metin)

    gereksiz_kelime = set(stopwords.words('turkish'))
    noktalama_cikar = set(string.punctuation)

    son_metin = []

    for kelime in kelimeler :
        if kelime not in gereksiz_kelime and kelime not in noktalama_cikar:
            son_metin.append(kelime)

    son_metin = Counter(son_metin) #Burada hangi kelimenin kaç kez geçtiğini buluyoruz

    en_cok = son_metin.most_common(5)
    en_az = son_metin.most_common()[:-5:-1] #Listenin son elemanlarını bulur.

    en_cok_kelime = [word[0] for word in en_cok]
    en_cok_deger = [word[1] for word in en_cok]

    en_az_kelime = [word[0] for word in en_az]
    en_az_deger = [word[1] for word in en_az]

    plt.subplot(2,1,1) # 2 tane satır her satırda  1 grafik olsun
    plt.bar(en_cok_kelime, en_cok_deger)

    plt.xlabel("En Çok Kullanılan Kelimeler")
    plt.ylabel("Sıklık")
    plt.title("Kelime Sıklığı Grafikleri")
    plt.subplot(2,1,2)
    plt.bar(en_az_kelime, en_az_deger, color='red')

    plt.xlabel("En Az Kullanılan Kelimeler")
    plt.ylabel("Sıklık")

    plt.tight_layout()


    plt.show()
def duygu_analiz(metin):
    translator = Translator()
    ing = translator.translate(metin)
    son = ing.text
    analiz = SentimentIntensityAnalyzer()
    skor = analiz.polarity_scores(son)

    olumlu = skor["pos"] * 100
    olumsuz = skor["neg"] * 100
    notr = skor["neu"] * 100

    analiz_sonuclari = {
        "Pozitif Yüzde": olumlu,
        "Negatif Yüzde": olumsuz,
        "Nötr Yüzde": notr
    }
    return analiz_sonuclari
def temel_analiz(metin):
    kelimeler = nltk.word_tokenize(metin)
    cumleler = nltk.sent_tokenize(metin)
    kelime_sayisi = len(kelimeler)
    cumle_sayisi = len(cumleler)
    kelime_sayisi = kelime_sayisi - cumle_sayisi
    noktalama_olmayan = ""
    noktalama = string.punctuation
    for char in metin:
        if char not in noktalama and not char.isspace():
            noktalama_olmayan = noktalama_olmayan + char

    karakter_sayisi = len(noktalama_olmayan)

    ortalama_cumle_uzunlugu = kelime_sayisi/cumle_sayisi
    ortalama_kelime_uzunlugu = karakter_sayisi/kelime_sayisi

    analiz_sonuclari = {
        "Kelime Sayısısı": kelime_sayisi,
        "Cümle Sayısı": cumle_sayisi,
        "Karakter Sayısı": karakter_sayisi,
        "Ortalama Cümle Uzunluğu": ortalama_cumle_uzunlugu,
        "Ortalama Kelime Uzunluğu": ortalama_kelime_uzunlugu
    }
    return analiz_sonuclari



arayuz = Tk()
arayuz.title("Metin Analiz Uygulaması")

canvas = Canvas(arayuz, height=800, width=1100)
canvas.pack()

frame_ust = Frame(arayuz, bg='light blue')
frame_ust.place(relx=0.1, rely=0.1, relwidth=0.75, relheight=0.1)

frame_sol = Frame(arayuz, bg='light blue')
frame_sol.place(relx=0.1, rely=0.21, relwidth=0.23, relheight=0.55)

frame_sag = Frame(arayuz, bg='light blue')
frame_sag.place(relx=0.34, rely=0.21, relwidth=0.51, relheight=0.55)

Label(frame_ust, text="Metin Analiz Uygulaması", font=("Helvetica", 22, 'bold'), bg='light blue').pack(pady=15, anchor='center')
Label(frame_sol, text="Seçenekler", font=("Helvetica", 16, 'bold'), bg='light blue').pack(pady=10, anchor='center')

Button(frame_sol, text="Temel Analiz", command=lambda: analiz_menu("temel"), width=20, font=("Helvetica", 12)).pack(pady=5)
Button(frame_sol, text="Kelime Sıklığı", command=lambda: analiz_menu2(), width=20, font=("Helvetica", 12)).pack(pady=5)
Button(frame_sol, text="Duygu Analizi", command=lambda: analiz_menu("duygu"), width=20, font=("Helvetica", 12)).pack(pady=5)
Button(frame_sol, text="Harf Sıklığı", command=lambda: analiz_menu("harf"), width=20, font=("Helvetica", 12)).pack(pady=5)
Button(frame_sol, text="Arama ve Filtreleme", command=lambda: Arama_yapma().dosya_secme(), width=20, font=("Helvetica", 12)).pack(pady=5)
Button(frame_sol, text="Metin Değiştirme İşlemleri",command=lambda:Metin_islemleri().dosya_secme(), width=20, font=("Helvetica", 12)).pack(pady=5)
Button(frame_sol, text="Benzerlik Analizi", command=lambda:Dosyakiyaslama().benzerlik_ekrana_yazdirma("benzerlik") , width=20, font=("Helvetica", 12)).pack(pady=5)
Button(frame_sol, text="Dosya Veritabanı", command=lambda: veritabani_goster(), width=20, font=("Helvetica", 12)).pack(pady=5)
Button(frame_sol, text="Kullanım Kılavuzu", command=lambda : analiz_menu(), width=20, font=("Helvetica", 12)).pack(pady=5)


def veritabani_goster():
    global veritabani_penceresi
    veritabani_penceresi = Toplevel(arayuz)
    veritabani_penceresi.title("Dosya Veritabanı")

    with open("C:\\Users\\ENES\\Desktop\\Metin_Analiz_Uyg\\pythonProject\\veritabani.json", "r") as dosya:
        veritabani = json.load(dosya)

    dosyalar = veritabani["dosyalar"]

    dosya_adlari = [dosya["dosya_adi"] for dosya in dosyalar]

    Label(veritabani_penceresi, text="Dosya Adları:", font=("Helvetica", 14, 'bold')).pack(pady=10)

    for dosya_adi in dosya_adlari:
        Button(veritabani_penceresi, text=dosya_adi, command=lambda d=dosya_adi: dosya_goster(d)).pack(pady=5)

    def dosya_ekle():
        secim = askopenfilename(initialdir="C:\\Users\\ENES\\Desktop\\Metinler",
                                 title="Dosya Seç",
                                 filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
        if not secim:
            return

        dosya_adi = os.path.basename(secim)
        dosya_yolu = secim

        with open("C:\\Users\\ENES\\Desktop\\Metin_Analiz_Uyg\\pythonProject\\veritabani.json", "r+") as file:
            dosya_veritabani = json.load(file)

            for dosya in dosya_veritabani["dosyalar"]:
                if dosya["dosya_adi"] == dosya_adi:
                    messagebox.showerror("Hata", "Bu dosya zaten veritabanında mevcut!")
                    return

            dosya_veritabani["dosyalar"].append({"dosya_adi": dosya_adi, "yol": dosya_yolu})

            file.seek(0)
            json.dump(dosya_veritabani, file, indent=4)
            file.truncate()

        messagebox.showinfo("Başarılı", "Dosya başarıyla eklendi.")



    # Dosya ekleme butonu
    Button(veritabani_penceresi, text="Dosya Ekle", command=dosya_ekle).pack(pady=5)



def dosya_goster(dosya_adi):
    dosya_yolu = None
    with open("C:\\Users\\ENES\\Desktop\\Metin_Analiz_Uyg\\pythonProject\\veritabani.json", "r") as file:
        dosya_veritabani = json.load(file)

    for dosya in dosya_veritabani["dosyalar"]:
        if dosya["dosya_adi"] == dosya_adi:
            dosya_yolu = dosya["yol"]
            break

    if dosya_yolu:
        with open(dosya_yolu, "r", encoding="utf-8") as dosya:
            metin = dosya.read()
            metin_goster(metin)

def metin_goster(metin):
    metin_penceresi = Toplevel(arayuz)
    metin_penceresi.title("Metin Göster")

    metin_label = Label(metin_penceresi, text="Metin:", font=("Helvetica", 14, 'bold'))
    metin_label.pack(pady=5)
    metin_text = ScrolledText(metin_penceresi, width=60, height=10, font=("Helvetica", 12))
    metin_text.pack(pady=5)
    metin_text.insert('end', metin)

    Button(metin_penceresi, text="Kapat", command=metin_penceresi.destroy).pack(pady=5)

def analiz_menu2():
    analiz_penceresi = Toplevel(arayuz)
    analiz_penceresi.title("Analiz Seçenekleri")

    Label(analiz_penceresi, text="Lütfen bir seçenek seçin", font=("Helvetica", 14)).pack(pady=10)

    Button(analiz_penceresi, text="Bilgisayardan Dosya Seç",
           command=lambda: [analiz_penceresi.destroy(), dosya_sec2()]).pack(pady=5)
    Button(analiz_penceresi, text="Kendin Metin Gir",
           command=lambda: [analiz_penceresi.destroy(), metin_gir2()]).pack(pady=5)

def metin_gir2():
    metin_penceresi = Toplevel(arayuz)
    metin_penceresi.title("Metin Girin")

    metin_label = Label(metin_penceresi, text="Lütfen metni aşağıya giriniz: ",font=("Helvetica", 14, 'bold'))
    metin_label.pack(pady=10)
    metin_text = ScrolledText(metin_penceresi, width=60, height=10, font=("Helvetica", 12))
    metin_text.pack(pady=10)

    def analiz_et():
        metin = metin_text.get(1.0, 'end').strip()
        kelime_sikligi(metin)
        metin_penceresi.destroy()

    Button(metin_penceresi, text="Analiz Et", command=analiz_et).pack(pady=10)

def dosya_sec2():
    secim=askopenfilename(initialdir="C:\\Users\\ENES\\Desktop\\Metinler",
                          title="dosya aç",
                          filetypes=(("text files", "*.txt"),("all files", "*.*")))
    if secim:
        with open(secim, 'r', encoding='utf-8') as dosya:
            icerik = dosya.read()
            kelime_sikligi(icerik)

def analiz_menu(analiz_turu):
    analiz_penceresi = Toplevel(arayuz)
    analiz_penceresi.title("Analiz Seçenekleri")

    Label(analiz_penceresi, text="Lütfen bir seçenek seçin", font=("Helvetica", 14)).pack(pady=10)

    Button(analiz_penceresi, text="Bilgisayardan Dosya Seç", command=lambda: [analiz_penceresi.destroy(), dosya_sec(analiz_turu)]).pack(pady=5)
    Button(analiz_penceresi, text="Kendin Metin Gir", command=lambda: [analiz_penceresi.destroy(), metin_gir(analiz_turu)]).pack(pady=5)

def dosya_sec(analiz_turu):
    secim=askopenfilename(initialdir="C:\\Users\\ENES\\Desktop\\Metinler",
                          title="dosya aç",
                          filetypes=(("text files", "*.txt"),("all files", "*.*")))
    if secim:
        with open(secim, 'r', encoding='utf-8') as dosya:
            icerik = dosya.read()
            metin_ve_analiz_goster(icerik, analiz_turu)

def metin_ve_analiz_goster(metin, analiz_turu):

    if analiz_turu == "temel" :
        analiz_sonuclari = temel_analiz(metin)
    elif analiz_turu == "harf" :
        analiz_sonuclari = harf_sikligi(metin)
    elif analiz_turu == "duygu" :
        analiz_sonuclari = duygu_analiz(metin)
    

    sonuc_penceresi = Toplevel(arayuz)
    sonuc_penceresi.title("Analiz Sonuçları")

    metin_label = Label(sonuc_penceresi, text="Metin:", font=("Helvetica", 14, 'bold'))
    metin_label.pack(pady=5)
    metin_text = ScrolledText(sonuc_penceresi, width=60, height=10, font=("Helvetica", 12))
    metin_text.pack(pady=5)
    metin_text.insert('end', metin)

    sonuclar_label = Label(sonuc_penceresi, text="Analiz Sonuçları:", font=("Helvetica", 14, 'bold'))
    sonuclar_label.pack(pady=5)
    sonuclar_text = ScrolledText(sonuc_penceresi, width=60, height=10, font=("Helvetica", 12))
    sonuclar_text.pack(pady=5)

    Button(sonuc_penceresi, text="Geri Dön", command=lambda: geri_don(sonuc_penceresi)).pack(pady=5)
    for anahtar, deger in analiz_sonuclari.items():
        sonuclar_text.insert('end', f"{anahtar}: {deger}\n")
    sonuclar_text.config(state='disabled') #etkileşim yok

def geri_don(pencere):
    pencere.destroy()
def metin_gir(analiz_turu):
    metin_penceresi = Toplevel(arayuz)
    metin_penceresi.title("Metin Girin")

    metin_label = Label(metin_penceresi, text="Lütfen metni aşağıya giriniz: ",font=("Helvetica", 14, 'bold'))
    metin_label.pack(pady=10)
    metin_text = ScrolledText(metin_penceresi, width=60, height=10, font=("Helvetica", 12))
    metin_text.pack(pady=10)

    def analiz_et():
        metin = metin_text.get(1.0, 'end').strip()
        metin_ve_analiz_goster(metin, analiz_turu)
        metin_penceresi.destroy()

    Button(metin_penceresi, text="Analiz Et", command=analiz_et).pack(pady=10)


arayuz.mainloop()
