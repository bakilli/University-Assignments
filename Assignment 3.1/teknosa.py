import requests
from bs4 import BeautifulSoup
from DBConnect import checkduplicate, addlaptop, checkmodel, addModelFromExistingModel

url = "https://www.teknosa.com/laptop-notebook-c-116004?sort=bestSellerPoint-desc&s=%3Arelevance"
page = requests.get(url)


def teknosa():
    text = page.text
    gridSoup = BeautifulSoup(text, 'html.parser')
    # print(soup.prettify())
    grid = gridSoup.find_all('div', id='product-item')
    # print(grid[0].prettify())
    print(page.status_code)
    pagenum = 0

    while 1:
        print("Page: ", pagenum)
        pagenum += 1

        for i in grid:
            producturl = "https://www.teknosa.com/" + i.find('a', class_='prd-link').get('href')
            print(producturl)
            productPage = requests.get(producturl)
            if not productPage.status_code == 200:
                print("Error: ", productPage.status_code)
                continue
            if checkduplicate('teknosa', producturl):
                print("duplicate")
                continue
            # get product name
            productname = i.find('a', class_='prd-link').get('title')
            print(productname)
            productbrand = productname.split()[0]
            # get product price
            productprice = i.find('div', class_='prd-prices').get_text().strip()
            productprice = float(productprice.replace('TL', '').replace('.', '').replace(',', '.'))
            print(productprice)
            pageSoup = BeautifulSoup(productPage.text, 'html.parser')
            technicalDetails = pageSoup.find_all('div', class_="ptf-body")
            if not technicalDetails:
                print("Error: No technical details found in the product page ")
                continue
            tables = (technicalDetails[0].find_all('table'))
            # assignements
            specname = []
            specvalue = []
            productscreen = None
            productram = None
            productcpu = None
            productgpu = None
            productspace = None
            productos = 'FreeDOS'
            productmodel = None
            productdisk = None
            productrating = None

            # get product specs
            for j in tables:
                specname.append(j.find_all('th'))
                specvalue.append(j.find_all('td'))
            for j in specname:
                for k in j:
                    text = k.text.replace('İ', 'i').lower()
                    if 'ram' in text:
                        productram = specvalue[specname.index(j)][j.index(k)].text
                        productram = int(productram.split()[0])
                        print(productram)
                    if 'işlemci' == text:
                        productcpu = specvalue[specname.index(j)][j.index(k)].text
                        print(productcpu)
                    if 'boyut' in text:
                        productscreen = specvalue[specname.index(j)][j.index(k)].text
                        productscreen = productscreen.replace('inç', '').replace('"', '')
                        productscreen = float(productscreen.replace(',', '.'))
                        print(productscreen)
                    if 'depolama' in text:
                        productspace = specvalue[specname.index(j)][j.index(k)].text
                        productspace = int(productspace.split()[0])
                        print(productspace)
                    if 'disk türü' in text:
                        productdisk = specvalue[specname.index(j)][j.index(k)].text
                        print(productdisk)
                    if 'ekran kartı model' in text:
                        productgpu = specvalue[specname.index(j)][j.index(k)].text
                        print(productgpu)
                    if 'işletim sistemi' in text:
                        productos = specvalue[specname.index(j)][j.index(k)].text
                        if 'dos' in productos.lower():
                            productos = 'FreeDOS'
                        print(productos)
                    if 'model kodu' in text:
                        productmodel = specvalue[specname.index(j)][j.index(k)].text
                        print(productmodel)
            if not productmodel:
                productmodel = addModelFromExistingModel(productname)
                if productmodel:
                    print("Model added from existing model: ", productmodel)
            if productmodel:
                if checkmodel('teknosa', productmodel):
                    print("duplicate")
                    continue
            # addlaptop
            addlaptop(productname, productbrand, productmodel, productos, productram, productdisk, productspace,
                      productscreen, productcpu, productgpu, 'teknosa', producturl, productprice, productrating)
            print("laptop added")

            # for j in technicalDetails.find('tr'):
            #     print("printing technical details: and j: ", j)
            #     print(j.find('th').text, j.find('td').text)
            #     for k in j.find('tr'):
            #         print(k.find_all('th').text, k.find_all('td').text)

            # print(i.find('span', class_='a-size-base a-color-price').get_text())
            # # print(i.find('span', class_='a-price-whole').get_text())
            # # print(i.find('span', class_='a-price-fraction').get_text())
            # # print(i.find('span', class_='a-icon-alt').get_text())
            # print("https://www.amazon.com.tr" + i.find('a', class_='a-link-normal a-text-normal').get('href'))
            print("")

        print("next page")
        nextpage = url + "&page=" + str(pagenum)
        gridSoup = BeautifulSoup(requests.get(nextpage).text, 'html.parser')
        grid = gridSoup.find_all('div', id='product-item')
        if not grid:
            print("No more pages")
            break


def startTeknosa():
    teknosa()

teknosa()