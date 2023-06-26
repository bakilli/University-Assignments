from PyQt5.QtWidgets import QFileDialog, QApplication
import sys
import docx2txt  # docx dosyalarını okumak için gereken kütüphane
import networkx as nx
import pdfrw
from PIL import Image
import matplotlib.pyplot as plt
# Uygulama oluşturmapip
# Uygulama oluşturma
app = QApplication(sys.argv)
# Dosya seçiciyi açma
filename, _ = QFileDialog.getOpenFileName(None, "Dosya Seç", "", "Metin Dosyaları (*.txt);;Word Dosyaları (*.docx);;PDF Dosyaları (*.pdf);;Tüm Dosyalar (*.*)")

# Dosya açma işlemi
if filename.endswith(".txt"):
    # txt dosyası okuma işlemi
    with open(filename, "r") as f:
        content = f.readlines()
elif filename.endswith(".docx"):
    # docx dosyası okuma işlemi
    content = docx2txt.process(filename)
elif filename.endswith(".pdf"):
    # pdf dosyası okuma işlemi
    pdf_file = pdfrw.PdfReader(filename)
    content = ""
    for page in pdf_file.pages:
        # Sayfadaki her bir objeyi gezer
        for obj in page['/Resources']['/Font']:
            if isinstance(obj, pdfrw.objects.pdfname.PdfName) and str(obj) == '/TrueType':
                continue
            elif isinstance(obj, pdfrw.objects.pdfname.PdfName):
                continue
            elif isinstance(obj, pdfrw.objects.pdfdict.PdfDict) and obj.get('/Subtype') == '/TrueType':
                # Font objesi ise, içeriği al
                font = obj['/BaseFont']
                text = obj['/Encoding']['/Differences'][2:]
                # İçeriği ekle
                content += text.decode(font)

# İçeriği yazdırma
print(content)
print(content[1])
# Boş bir graf oluştur
G = nx.Graph()


# Düğümleri grafa ekle
for line in content:
    print(line) 
    nodes = line.split()
    G.add_node(str(nodes))


plt.figure(figsize=(100, 100))


# Grafi göster
nx.draw(G, with_labels=True)
plt.show()