import requests
from bs4 import BeautifulSoup
from DBConnect import checkduplicate, addlaptop, checkmodel, addModelFromExistingModel

url = "https://www.n11.com/bilgisayar/dizustu-bilgisayar"
page = requests.get(url)


def n11():
    text = page.text
    gridSoup = BeautifulSoup(text, 'html.parser')
    # print(gridSoup.prettify())
    grid = gridSoup.find_all('li', class_='column')
    # print(grid[0].prettify())
    # n11 starts from page 1
    pagenum = 1

    while 1:
        print("Page: ", pagenum)
        print(page.status_code)
        pagenum += 1

        for i in grid:
            producturl = i.find('a', class_='plink').get('href')
            print(producturl)
            if checkduplicate('n11', producturl):
                print("duplicate")
                continue
            # get product name
            productname = i.find('a', class_='plink').get('title')
            print(productname)
            # get product brand(we can get this from technical details)
            productbrand = productname.split()[0]
            # get product price
            productprice = i.find('div', class_='priceContainer')
            productprice = productprice.find('ins').get_text().strip()
            productprice = float(productprice.replace('TL', '').replace('.', '').replace(',', '.'))
            print(productprice)
            # get product rating
            productrating = i.find('div', class_='ratingCont')
            productrating = float(productrating.find('span')['class'][1][1:])
            if productrating == 0 and int(i.find('span', class_='ratingText').get_text().strip("()")) == 0:
                productrating = None
            print(productrating)
            # request product page
            productPage = requests.get(producturl)
            if not productPage.status_code == 200:
                print("Error: ", productPage.status_code)
                continue
            pageSoup = BeautifulSoup(productPage.text, 'html.parser')
            technicalDetails = pageSoup.find_all('li', class_="unf-prop-list-item")
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

            # get product specs
            for j in technicalDetails:
                specname.append(j.find('p', class_='unf-prop-list-title').text.strip())
                specvalue.append(j.find('p', class_='unf-prop-list-prop').text.strip())
            # print('specname: ', specname)
            # print('specvalue: ', specvalue)
            for j in specname:
                text = j.replace('İ', 'i').lower()
                # print(text)
                if 'bellek kapasitesi' in text:
                    productram = specvalue[specname.index(j)]
                    productram = int(productram.split()[0])
                    print(productram)
                if 'işlemci modeli' == text:
                    productcpu = specvalue[specname.index(j)]
                    print(productcpu)
                if 'boyut' in text:
                    productscreen = specvalue[specname.index(j)]
                    productscreen = float(productscreen.replace('"', ''))
                    print(productscreen)
                if 'disk kapasitesi' in text:
                    productspace = specvalue[specname.index(j)]
                    if 'TB' in productspace:
                        productspace = int(productspace.split()[0]) * 1024
                    else:
                        productspace = int(productspace.split()[0])
                    print(productspace)
                if 'disk türü' in text:
                    productdisk = specvalue[specname.index(j)]
                    print(productdisk)
                if 'ekran kartı modeli' in text:
                    productgpu = specvalue[specname.index(j)]
                    print(productgpu)
                if 'işletim sistemi' in text:
                    productos = specvalue[specname.index(j)]
                    if 'dos' in productos.lower():
                        productos = 'FreeDOS'
                    print(productos)
                if 'model' == text:
                    productmodel = specvalue[specname.index(j)]
                    print(productmodel)
                if 'marka' in text:
                    productbrand = specvalue[specname.index(j)]
                    print(productbrand)

            if not productmodel:
                productmodel = addModelFromExistingModel(productname)
                print('model eklendi: ', productmodel)
            if productmodel:
                if checkmodel('n11', productmodel):
                    print("duplicate")
                    continue
            # addlaptop
            addlaptop(productname, productbrand, productmodel, productos, productram, productdisk, productspace,
                      productscreen, productcpu, productgpu, 'n11', producturl, productprice, productrating)
            print("laptop added")
            print("")

        print("next page")
        nextpage = url + "?ipg=5&pg=" + str(pagenum)
        gridSoup = BeautifulSoup(requests.get(nextpage).text, 'html.parser')
        grid = gridSoup.find_all('li', class_='column')
        if not grid:
            print("No more pages")
            break


def startn11():
    n11()

startn11()