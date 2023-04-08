from DBConnect import checkduplicate, addlaptop
from bs4 import BeautifulSoup
import requests

url = "http://127.0.0.1:8000/"
page = requests.get(url)


def laptopcum():
    print(page.status_code)
    text = page.text
    gridSoup = BeautifulSoup(text, 'html.parser')
    grid = gridSoup.find_all('a', class_='products')
    print('---------------------------------------------')
    for i in grid:
        producturl = "http://127.0.0.1:8000" + i.get('href')
        productPage = requests.get(producturl)
        if not productPage.status_code == 200:
            print("Error: ", productPage.status_code)
            continue
        pageSoup = BeautifulSoup(productPage.text, 'html.parser')
        technicalDetails = pageSoup.find_all('p')
        if not technicalDetails:
            print("Error: No technical details found in the product page ")
            continue
        productname = technicalDetails[0].get_text()
        if checkduplicate('laptopcum', producturl):
            print("duplicate")
            continue
        productscreen = None
        productram = None
        productcpu = None
        productgpu = None
        productspace = None
        productos = None
        productmodel = None
        productdisk = None
        productbrand = None
        productprice = None
        productrating = None
        for j in technicalDetails[1:]:
            specname = j.get_text().split(":")[0].replace('İ', 'i').lower()
            specvalue = j.get_text().split(":")[1]
            print(specname, specvalue)
            if 'marka' in specname:
                productbrand = specvalue.strip()
            if 'model' in specname:
                productmodel = specvalue.strip()
            if 'puan' in specname:
                if specvalue.strip().lower() == 'none':
                    continue
                productrating = float(specvalue)
            if 'fiyat' in specname:
                productprice = float(specvalue)
            if 'işletim sistemi' in specname:
                productos = specvalue.strip()
            if 'işlemci' in specname:
                productcpu = specvalue.strip()
            if 'ekran kartı' in specname:
                productgpu = specvalue.strip()
            if 'ram' in specname:
                productram = int(specvalue)
            if 'disk kapasitesi' in specname:
                productspace = int(specvalue)
            if 'disk türü' in specname:
                productdisk = specvalue.strip()
            if 'ekran boyutu' in specname:
                productscreen = float(specvalue)
        addlaptop(productname, productbrand, productmodel, productos, productram, productdisk, productspace,
                  productscreen, productcpu, productgpu, 'laptopcum', producturl, productprice, productrating)
        print('---------------------------------------------')


laptopcum()
