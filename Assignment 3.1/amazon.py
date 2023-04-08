import time
import requests
from bs4 import BeautifulSoup
from DBConnect import checkduplicate, addlaptop, checkmodel, addModelFromExistingModel

url = "https://www.amazon.com.tr/gp/bestsellers/computers/12601898031"
# headers = {
#     'User-Agent':
#     'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
# }

page = requests.get(url)


def amazon():
    text = page.text
    gridSoup = BeautifulSoup(text, 'html.parser')
    # print(soup.prettify())
    grid = gridSoup.find_all('div', id='gridItemRoot')
    # print(grid[0].prettify())
    pagenum = 0
    while 1:
        print("Page: ", pagenum)
        print(page.status_code)
        pagenum += 1
        for i in grid:
            producturl = "https://www.amazon.com.tr" + i.find('a', class_='a-link-normal').get('href')
            productPage = requests.get(producturl)
            if not productPage.status_code == 200:
                print("Error: ", productPage.status_code)
                continue
            if checkduplicate('amazon', producturl):
                print("duplicate")
                continue
            print(producturl)
            pageSoup = BeautifulSoup(productPage.text, 'html.parser')
            # get product name
            productname = pageSoup.find('span', id='productTitle').get_text().strip()
            print(productname)
            # get product brand
            productbrand = productname.split()[0]
            print(productbrand)
            # get product price
            if pageSoup.find('span', class_='a-price aok-align-center reinventPricePriceToPayMargin priceToPay'):
                productprice = pageSoup.find('span',
                                             class_='a-price aok-align-center reinventPricePriceToPayMargin priceToPay')
                productprice = productprice.find('span', class_='').get_text().strip()
                productprice = float(productprice.replace('TL', '').replace('.', '').replace(',', '.'))
            else:
                print("Error: No price found in the product page")
                continue
            print(productprice)
            # get product rating
            productrating = pageSoup.find('span', id='acrPopover')
            if productrating:
                productrating = productrating.find('span', class_='a-icon-alt').get_text().strip()
                productrating = productrating.split()[3]
                productrating = float(productrating.replace(',', '.')) * 20
                print(productrating)
            # request product page
            technicalDetails = pageSoup.find_all('table', id="productDetails_techSpec_section_1")
            if not technicalDetails:
                print("Error: No technical details found in the product page ")
                continue
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

            # get product technical details
            for j in technicalDetails:
                for k in j.find_all('tr'):
                    specname.append(k.find('th').get_text().strip())
                    specvalue.append(k.find('td').get_text().strip())
            for j in specname:
                text = j.replace("İ", "i").lower()
                # print(text)
                if 'ram boyutu' in text:
                    productram = specvalue[specname.index(j)].replace('\u200e', '')
                    productram = productram.encode('ascii', 'ignore').decode('ascii')
                    productram = int(productram.split()[0])
                    print(productram)
                if 'işlemci türü' == text:
                    productcpu = specvalue[specname.index(j)].strip().replace('\u200e', '')
                    print(productcpu)
                if 'ekran boyutu' in text:
                    productscreen = specvalue[specname.index(j)].replace('\u200e', '')
                    productscreen = productscreen.encode('ascii', 'ignore').decode('ascii')
                    productscreen = float(productscreen.split()[0])
                    print(productscreen)
                if 'sabit sürücü boyutu' in text:
                    productspace = specvalue[specname.index(j)].replace('\u200e', '')
                    productspace = productspace.encode('ascii', 'ignore').decode('ascii')
                    productspace = int(productspace.split()[0])
                    print(productspace)
                if 'sabit sürücü' in text:
                    if 'arabirimi' in text:
                        productdisk = 'SSD'
                        print(productdisk)
                    elif 'açıklaması' in text and productdisk is None:
                        if 'yok' in text:
                            productdisk = None
                        else:
                            productspace = specvalue[specname.index(j)].strip().replace('\u200e', '')
                            print(productspace)
                if 'ekran kartı açıklaması' in text:
                    productgpu = specvalue[specname.index(j)].strip().replace('\u200e', '')
                    print(productgpu)
                if 'işletim sistemi' in text:
                    productos = specvalue[specname.index(j)].strip().replace('\u200e', '')
                    if 'dos' in productos.lower():
                        productos = 'FreeDOS'
                    print(productos)
                if 'ürün model numarası' in text:
                    productmodel = specvalue[specname.index(j)].strip().replace('\u200e', '')
                    print(productmodel)
                if 'seri' == text and productmodel is None:
                    productmodel = specvalue[specname.index(j)].strip().replace('\u200e', '')
                    print(productmodel)
                if 'marka' == text:
                    productbrand = specvalue[specname.index(j)].strip().replace('\u200e', '')
                    print(productbrand)
            if not productmodel:
                productmodel = addModelFromExistingModel(productname)
                print('model eklendi: ', productmodel)
            if productmodel:
                if checkmodel('amazon', productmodel):
                    print("duplicate")
                    continue
            # addlaptop
            addlaptop(productname, productbrand, productmodel, productos, productram, productdisk, productspace,
                      productscreen, productcpu, productgpu, 'amazon', producturl, productprice, productrating)
            print("Added to database")
            print("----------------------------------------------------------------------------------------------")
            # print(i.find('span', class_='a-size-base a-color-price').get_text())
            # # print(i.find('span', class_='a-price-whole').get_text())
            # # print(i.find('span', class_='a-price-fraction').get_text())
            # # print(i.find('span', class_='a-icon-alt').get_text())
            # print("https://www.amazon.com.tr" + i.find('a', class_='a-link-normal a-text-normal').get('href'))

        # next page button is disabled, so we can't go to next page
        if gridSoup.find('li', class_='a-disabled a-last'):
            print("No more pages")
            break
        print("next page")
        nextpage = "https://www.amazon.com.tr" + gridSoup.find('li', class_='a-last').find('a').get('href')
        gridSoup = BeautifulSoup(requests.get(nextpage).text, 'html.parser')
        grid = gridSoup.find_all('div', id='gridItemRoot')
        if not grid:
            print("No more pages")
            break


def startAmazon():
    amazon()


for i in range(10):
    print('iteration: ', i)
    print('----------------------------------------------------------------------------------------------')
    startAmazon()
    time.sleep(5)
