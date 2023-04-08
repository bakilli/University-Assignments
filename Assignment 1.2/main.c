//200201012 Baris Kakilli
//200201032 Muhammed Sina Cimen
//Programlama Laboratuvari I - 2. proje

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
void yazdir(int i, int harfsayisi, char katar[20])
{
    for(int j = i; j < harfsayisi; j++)
        printf("%c", katar[j]);
    printf("    ");
}
void tabat(int a)
{
    for(int i = 0; i < a; i++)
        printf("\t");
}
int main()
{
    printf("Islem yapmak istediginiz dosya ismini giriniz: ");
    char katar[50];
    char dosyaismi[50];
    scanf("%s", dosyaismi);
    FILE *fp;
    fp = fopen(dosyaismi, "r");
    fscanf(fp, "%s", katar);
    fclose(fp);
    int harfsayisi = strlen(katar);
    int dizi[3][harfsayisi];
    //  dizi elemanlarinin hepsini -1 yapiyor ramdeki sacma sayilari göstermesin diye
    // dizi[0] harf index gosterme
    // dizi[1] tekrar varsa kacinci index yoksa -1
    // dizi[2] tekrar varsa kac karakter yoksa ana suffixse 0 degilse -1
    for(int i = 0; i < 3; i++)
    {
        for(int j = 0; j < harfsayisi; j++)
        {
            dizi[i][j] = -1;
            if(i == 0)
                dizi[0][j] = j;
        }
    }
    // iki dongu icinde kacinci index ve kac karaketeri hesapliyoruz
    for(int i = 0; i < harfsayisi; i++)
    {
        int j;
        /*for(j = i; j < harfsayisi; j++) //tum katarlari yazdirma
        {
            printf("%c", katar[j]);
        }*/
        j = i;
        int kackarakter = 0;
        int kacinci_index = 0;
        // ayni harf var mi kontrolu burada yapiliyor
        for(int s = 0; s < j; s++)
        {
            // onceki harflerden ayni sey var mi ona bakiyor
            while(katar[j+kackarakter] == katar[s+kackarakter])
                kackarakter++;
            if(kackarakter > 0) // bu if i yazmazsak en sona kadar gidicek. kacinci index  degeri hatali olucak. break ile cikmamiz gerekli
                break;
            kacinci_index++;
        }
        if(kackarakter > 0)
        {
            dizi[1][j] = kacinci_index;
            dizi[2][j] = kackarakter;
            dizi[1][kacinci_index] = kacinci_index;
            dizi[2][kacinci_index] = 0;
            /*printf("test : %d : %d : ", kacinci_index, kackarakter);  // kac degerlerini yazdirma
            for(j = i; j < harfsayisi; j++)
            {
                printf("%c", katar[j]);
            }
            printf("\n");*/
        }
    }
    printf("%s icerigi: %s\n", dosyaismi, katar);



    while(1)
    {
        int secim;
        printf("\n");
        printf("0 | Cikis Yap\n");
        printf("1 | s katari icin sonek agaci olusturulabilir mi kontrolu\n");
        printf("2 | s katarindaki p katarini bulma\n");
        printf("3 | s katari icinde tekrar eden en uzun altkatar\n");
        printf("4 | s katari icinde en cok tekrar eden altkatar\n");
        printf("5 | s katari icin agaci goster\n");


        printf("\nHangi Islemi Yapmak Istediginizi Seciniz: ");

        scanf("%d", &secim);

        if (secim==1)
        {
            char onden[harfsayisi];
            char tersten[harfsayisi];
            int dogru = 1;
            for(int i = 1; i < harfsayisi; i++)
            {
                strncpy_s(onden, harfsayisi, katar, harfsayisi-i);
                strcpy(tersten, katar+i);
                if(strcmp(onden, tersten) == 0)
                    dogru = 0;
            }
            if(dogru == 0)
                printf("%s icin sonek agaci olusturulamaz.", katar);
            else
                printf("%s icin sonek agaci olusturulabilir.", katar);
        }
        else if (secim==3)
        {
            int en_uzun = 0;
            int enuzun_i;
            int temp;
            for(int i = 0; i < harfsayisi; i++)
            {
                if(en_uzun  < dizi[2][i])
                {
                    en_uzun = dizi[2][i];
                }
            }
            if(en_uzun == 0)
            {
                printf("tekrar eden katar yok\n");
            }
            else
            {
                for(int i = 0; i < harfsayisi; i++)
                {
                    if(en_uzun == dizi[2][i])
                    {
                        enuzun_i = i;
                        temp = dizi[1][enuzun_i];
                    }
                }
                printf("tekrar eden en uzun alt katar: ");
                for(int i = 0; i < en_uzun; i++)
                {
                    printf("%c", katar[enuzun_i]);
                    enuzun_i++;
                }
                int sayi = 0;
                for(int i = 0; i < harfsayisi; i++)
                {
                    if(temp == dizi[1][i] &&(dizi[2][i] >= en_uzun || dizi[2][i] == 0))
                        sayi++;
                }
                printf("\n%d kez geciyor.", sayi);
                printf("\n");
            }
        }
        else if(secim==2)
        {
            char istenen[harfsayisi+1];
            printf("bulmak istediginiz katari giriniz: ");
            scanf("%s", istenen);
            char *pch;
            int istenen_uzunluk = strlen(istenen);
            int istenen_deneme = 0;
            int test = 0;
            pch = strstr(katar, istenen);
            if(pch != NULL)
            {
                printf("evet katar geciyor.\nkatarin baslangic indexi: %d\n", pch-katar);
                int sayi = 0;
                char *temp = katar;
                while(temp = strstr(temp, istenen))
                {
                    sayi++;
                    temp++;
                }
                printf("%d kez geciyor.\n", sayi);
            }
            else
                printf("hayir katar gecmiyor.\n");
        }
        else if(secim==4)
        {
            printf("en cok tekrar eden alt katar: ");
            int temp;
            int deger;
            int dizi1[harfsayisi];
            for(int i = 0; i < harfsayisi; i++)
            {
                dizi1[i] = dizi[1][i];
            }
            int maxelement;
            int sayisi;
            int maxsayi = 0;
            int jtest;
            for(int i = 0; i < harfsayisi; i++)
            {
                if(dizi1[i] == -1)
                    continue;
                sayisi = 1;
                for(int j = i+1; j < harfsayisi; j++)
                {
                    if(dizi1[j] == -1)
                        continue;
                    if(dizi1[j] == dizi1[i])
                    {
                        sayisi++;
                        if(sayisi > maxsayi)
                        {
                            maxsayi = sayisi;
                            maxelement = dizi1[j];
                            jtest = j;
                        }
                    }
                }
            }
            int minsayisi = 999;
            for(int i = 0; i < harfsayisi; i++)
            {
                sayisi = 1;
                if(maxelement == dizi1[i])
                {
                    for(int j = i; j < harfsayisi; j++)
                    {
                        if(dizi1[j+1] > dizi1[j])
                            sayisi++;
                        else
                            break;
                    }
                    if(minsayisi > sayisi)
                    {
                        minsayisi = sayisi;
                    }
                }
            }
            for(int i = 0; i < minsayisi; i++)
            {
                printf("%c",katar[jtest]);
                jtest++;
            }
            printf("\n%d kez geciyor.", maxsayi);
        }
        else if (secim==5)
        {

    int benzerlik_olmayan = 0;
    // hic benzerlik olmayanlari yazdirma kismi
    for(int i = 0; i < harfsayisi; i++)
    {
        if(dizi[1][i] == -1) // hic benzerlik olmayanlar
        {
            yazdir(i, harfsayisi, katar);
            benzerlik_olmayan++;
        }
    }

    for(int i = 0; i < harfsayisi; i++)
    {
        if(dizi[2][i] != -1 && dizi[2][i] != 0) // dizi[][] > 0 ile ayni sey
        {
            printf(" ");
            int kacinci_index_kopya = dizi[1][i];
            int kackarakter[harfsayisi];
            int kac_adet = 0;
            for(int j = 0; j < harfsayisi; j++) // kac adet ayni harfle baslayan var?
            {
                if(kacinci_index_kopya == dizi[1][j])
                {
                    kackarakter[kac_adet] = dizi[2][j];
                    kac_adet++;
                }
            }
            int siralikackarakter[kac_adet];
            for(int k = 0; k < kac_adet; k++) //sirali kac karakter = kac karakter
            {
                siralikackarakter[k] = kackarakter[k];
            }
            for(int k = 0; k < kac_adet-1; k++) //bubble sort
            {
                for (int j = 0; j < kac_adet-k-1; j++)
                    if (siralikackarakter[j] > siralikackarakter[j+1])
                    {
                        int swap = siralikackarakter[j];
                        siralikackarakter[j] = siralikackarakter[j+1];
                        siralikackarakter[j+1] = swap;
                    }
            }
            int kac_adetdegis = kac_adet;
            int yaz = i;
            int a = 1;
            int a_arttir = 1;
            kac_adetdegis--;
            printf("\n");
            tabat(benzerlik_olmayan);
            for(int j = 0; j < siralikackarakter[kac_adet-kac_adetdegis]; j++) //ilk kisim
            {
                printf("%c", katar[yaz]);
                yaz++;
            }
            for(kac_adetdegis; kac_adetdegis > 1;) // sonraki kisimlar
            {
                kac_adetdegis--;
                printf("\n");
                tabat(benzerlik_olmayan);
                for(int j = siralikackarakter[kac_adet-kac_adetdegis]; j < harfsayisi; j++)
                {
                    printf("%c", katar[yaz]);
                    yaz++;
                }
                printf("|");
                for(int k = 0; k < harfsayisi; k++)
                {
                    if(dizi[2][k] == siralikackarakter[kac_adet-kac_adetdegis] && dizi[1][k] == kacinci_index_kopya)
                    {
                        yaz = k+kac_adet-kac_adetdegis;
                    }
                }
                for(int j = siralikackarakter[a]; j < siralikackarakter[kac_adet-kac_adetdegis]; j++)
                {
                    printf("%c", katar[yaz]);
                    yaz++;
                }
            }
            // son kisim
            printf("\n");
            tabat(benzerlik_olmayan);
            printf("\t");
            int son;
            for(int k = 0; k < harfsayisi; k++)
            {
                if(dizi[2][k] == siralikackarakter[kac_adet-1] && dizi[1][k] == kacinci_index_kopya)
                {
                    son = dizi[0][k];
                    yaz = k;
                }
            }
            for(int j = son+kac_adet; j < harfsayisi; j++)
            {
                printf("%c", katar[yaz+kac_adet]);
                yaz++;
            }
            printf("|");
            for(int k = 0; k < harfsayisi; k++)
            {
                if(dizi[2][k] == siralikackarakter[0] && dizi[1][k] == kacinci_index_kopya)
                {
                    yaz = k;
                }
            }
            for(int j = kac_adet; j < harfsayisi; j++)
            {
                printf("%c", katar[yaz+kac_adet]);
                yaz++;
            }
            printf("\n");
            for(int k = 0; k < harfsayisi; k++)
            {
                if(dizi[1][k] == kacinci_index_kopya)
                {
                    dizi[1][k] = -2;
                }
            }
            break;
        }
    }
        }
        else if (secim==0)
            break;
    }

}



