def jaccard_benzerliği(self):
        dosya_sayisi = len(self.selected_files)
        for i in range(dosya_sayisi):
            for j in range(i + 1, dosya_sayisi):
                self.jaccard_benzerligi(self.selected_files[i], self.selected_files[j])


    def pdf_jaccard_benzerligi_hesaplama(self,secilen1, secilen2):
        with open(secilen1, 'rb') as dosya1, open(secilen2, 'rb') as dosya2:
            pdf1 = PyPDF2.PdfReader(dosya1)
            pdf2 = PyPDF2.PdfReader(dosya2)
            kelime_seti1 = set()
            kelime_seti2 = set()
            for sayfa in pdf1.pages:
                kelime_seti1.update(word_tokenize(sayfa.extract_text().lower()))
            for sayfa in pdf2.pages:
                kelime_seti2.update(word_tokenize(sayfa.extract_text().lower()))
            benzerlik = len(kelime_seti1.intersection(kelime_seti2)) / len(kelime_seti1.union(kelime_seti2))
            yazdirilacak=f"Jaccard Benzerliği ({secilen1}, {secilen2}): {benzerlik}"

            label=tk.Label(self.yeni_pencere, text=yazdirilacak)
            label.pack()