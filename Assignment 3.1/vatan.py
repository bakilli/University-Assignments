from DBConnect import checkduplicate, addlaptop, checkmodel, addModelFromExistingModel
from bs4 import BeautifulSoup
import requests

url = "https://www.vatanbilgisayar.com/notebook/"
page = requests.get(url)


def vatan():
    text = page.text
    gridSoup = BeautifulSoup(text, 'html.parser')
    # print(gridSoup.prettify())
    grid = gridSoup.find_all('div', class_='product-list product-list--list-page')
    # print(grid[0].prettify())
    pagenum = 1

    while 1:
        print("Page: ", pagenum)
        print(page.status_code)
        pagenum += 1
        for i in grid:
            producturl = "https://www.vatanbilgisayar.com" + i.find('a', class_='product-list__link').get('href')
            print(producturl)
            if checkduplicate('vatan', producturl):
                print("duplicate")
                continue
            # get product name
            productname = i.find('div', class_='product-list__product-name').get_text().strip()
            print(productname)
            # get product brand(we can get this from technical details)
            productbrand = productname.split()[0]
            print(productbrand)
            # get product price
            productprice = i.find('span', class_='product-list__price').get_text().strip()
            productprice = float(productprice.replace('TL', '').replace('.', '').replace(',', '.'))
            print(productprice)
            # get product rating
            productrating = i.find('span', class_='score')
            productrating = float(productrating['style'].split('width:')[1].split('%;')[0])
            if productrating == 0 and int(i.find('a', class_="comment-count").get_text().strip("()")) == 0:
                productrating = None
            print(productrating)
            # request product page
            productPage = requests.get(producturl)
            if not productPage.status_code == 200:
                print("Error: ", productPage.status_code)
                continue
            pageSoup = BeautifulSoup(productPage.text, 'html.parser')
            technicalDetails = pageSoup.find_all('div',
                                                 class_="col-lg-6 col-md-6 col-sm-12 col-xs-12 property-tab-item")
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
            prductcpubrand = ''
            productcpunum = ''
            productcputech = ''

            # get product specs
            for j in technicalDetails:
                jvalue = j.find_all('td')
                for k in jvalue[::2]:
                    # print(k.get_text().strip())
                    specname.append(k.get_text().strip())
                for k in jvalue[1::2]:
                    val = k.find('p')
                    specvalue.append(val.get_text().strip())
            for j in specname:
                text = j.replace('İ', 'i').lower()
                # print(text)
                if 'sistem belleği' in text:
                    productram = specvalue[specname.index(j)]
                    productram = int(productram.split()[0])
                    print(productram)
                if 'işlemci' in text:
                    if 'markası' in text:
                        prductcpubrand = specvalue[specname.index(j)]
                    elif 'teknolojisi' in text:
                        productcputech = specvalue[specname.index(j)]
                    elif 'numarası' in text:
                        productcpunum = specvalue[specname.index(j)]
                if 'ekran boyutu' in text:
                    productscreen = specvalue[specname.index(j)]
                    productscreen = productscreen.replace('inç', '').replace('"', '').replace('inch', '')
                    productscreen = float(productscreen.replace(',', '.'))
                    print(productscreen)
                if 'disk kapasitesi' in text:
                    productspace = specvalue[specname.index(j)]
                    if 'tb' in productspace:
                        productspace = int(productspace.split()[0]) * 1024
                    else:
                        productspace = int(productspace.split()[0])
                    print(productspace)
                if 'disk türü' in text:
                    productdisk = specvalue[specname.index(j)]
                    print(productdisk)
                if 'ekran kartı chipseti' in text:
                    productgpu = specvalue[specname.index(j)]
                    print(productgpu)
                if 'işletim sistemi' in text:
                    productos = specvalue[specname.index(j)]
                    if 'dos' in productos.lower():
                        productos = 'FreeDOS'
                    if 'win 10' in productos.lower():
                        productos = productos.replace('Win 10', 'Windows 10')
                    print(productos)
                if 'üretici part numarası' == text:
                    productmodel = specvalue[specname.index(j)]
                    print(productmodel)
                # if 'marka' in text:
                #     productbrand = specvalue[specname.index(j)]
                #     print(productbrand)
            productcpu = prductcpubrand + " " + productcputech + " " + productcpunum
            print(productcpu)
            if not productmodel:
                productmodel = pageSoup.find('div', class_='product-list__product-code pull-left product-id')
                if productmodel:
                    productmodel = productmodel.get_text().strip()
                    print(productmodel)
            if not productmodel:
                productmodel = addModelFromExistingModel(productname)
                print('model eklendi: ', productmodel)
            if productmodel:
                if checkmodel('vatan', productmodel):
                    print("duplicate")
                    continue
            # addlaptop
            addlaptop(productname, productbrand, productmodel, productos, productram, productdisk, productspace,
                      productscreen, productcpu, productgpu, 'vatan', producturl, productprice, productrating)
            print("laptop added")
            print("")

        # for i in grid:
        #     producturl = "https://www.vatanbilgisayar.com/" + i.find('a', class_='product-list__link').get('href')
        #     productPage = requests.get(producturl)
        #     if not productPage.status_code == 200:
        #         print("Error: ", productPage.status_code)
        #         continue
        #     pageSoup = BeautifulSoup(productPage.text, 'html.parser')
        #     technicalDetails = pageSoup.find_all('div', class_="col-lg-6 col-md-6 col-sm-12 col-xs-12 property-tab-item masonry-brick")

        print("next page")
        nextpage = url + "?page=" + str(pagenum)
        gridSoup = BeautifulSoup(requests.get(nextpage).text, 'html.parser')
        grid = gridSoup.find_all('div', class_='product-list product-list--list-page')
        if not grid:
            print("No more pages")
            break


def startVatan():
    vatan()

vatan()