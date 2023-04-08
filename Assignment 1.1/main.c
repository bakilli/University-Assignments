#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>

struct kayit
{
    int ogrno;
    int derskodu;
    int puan;
} kayitlar;
void sil_guncelle(int sil_gunc)
{
    int verisayisi = 0, i, low, istenen;
    if(sil_gunc == 1)
        printf("kaydini silmek istediginiz ogrencinin numarasi:");
    else
        printf("kaydini degistirmek istediginiz ogrencinin numarasi:");
    scanf("%d", &istenen);
    FILE *fp, *fpv;
    fp = fopen("index.txt", "r");
    fpv = fopen("veri.bin", "r");
    while(fscanf(fp, "%d", &low) == 1)
        verisayisi++;
    verisayisi = verisayisi / 2;
    int veridegismez = verisayisi;
    rewind(fp);
    int arr[verisayisi+1], arrindex[verisayisi+1];
    int ogrno[verisayisi+1], derskodu[verisayisi+1], puan[verisayisi+1];
    for(i = 1; i < verisayisi+1; i++)
    {
        fscanf(fp, "%d", &arr[i]);
        fscanf(fp, "%d", &arrindex[i]);
        fscanf(fpv, "%d", &ogrno[i]);
        fscanf(fpv, "%d", &derskodu[i]);
        fscanf(fpv, "%d", &puan[i]);
    }
    low = 0;
    while(low < verisayisi+1)
    {
        int mid = low + (verisayisi - low) / 2;
        if(arr[mid] == istenen)
        {
            int veridosyasiyeri;
            int adet = 1, midtest;
            midtest = mid;
            if(midtest != verisayisi)
                while(arr[midtest] == arr[midtest+1])
                {
                    adet++;
                    midtest++;
                }
            midtest = mid;
            if(midtest > 0)
                while(arr[midtest] == arr[midtest-1])
                {
                    adet++;
                    midtest--;
                }
            mid = midtest;
            if(adet == 1)
            {
                for(i = 1; i < veridegismez+1; i++)
                {
                    if(ogrno[i] == arr[mid])
                        veridosyasiyeri  = i;
                }
                if(sil_gunc == 1)
                {
                    int eminmi;
                    printf("%d nolu ogrencinin kaydi silinicek emin misiniz?\n1-Evet\n2-Hayir\n", arr[mid]);
                    scanf("%d", &eminmi);
                    if(eminmi == 1)
                    {
                        FILE *fpvnew;
                        fpvnew = fopen("verinew.bin", "w");
                        for(veridosyasiyeri; veridosyasiyeri < veridegismez; veridosyasiyeri++)
                        {
                            ogrno[veridosyasiyeri] = ogrno[veridosyasiyeri+1];
                            derskodu[veridosyasiyeri] = derskodu[veridosyasiyeri+1];
                            puan[veridosyasiyeri] = puan[veridosyasiyeri+1];
                        }
                        for(i = 1; i < veridegismez; i++)
                        {
                            fprintf(fpvnew, "%d %d %d\n", ogrno[i], derskodu[i], puan[i]);
                        }
                        fclose(fpvnew);
                        printf("veri basariyla silindi.\n");
                    }
                    else
                    {
                        printf("veri silinmedi.\n");
                        fclose(fp);
                        fclose(fpv);
                        sleep(1);
                        return 0;
                    }
                }
                if(sil_gunc == 2)
                {
                    int yeniderskodu, yenipuan;
                    printf("%d nolu ogrencinin yeni ders kodunu giriniz:", arr[mid]);
                    scanf("%d", &yeniderskodu);
                    printf("%d nolu ogrencinin yeni puanini giriniz:", arr[mid]);
                    scanf("%d", &yenipuan);
                    FILE *fpvnew;
                    fpvnew = fopen("verinew.bin", "w");
                    derskodu[veridosyasiyeri] = yeniderskodu;
                    puan[veridosyasiyeri] = yenipuan;
                    for(i = 1; i <= veridegismez; i++)
                    {
                        fprintf(fpvnew, "%d %d %d\n", ogrno[i], derskodu[i], puan[i]);
                    }
                    fclose(fpvnew);
                    printf("veri basariyla degistirildi.\n");
                }
                fclose(fp);
                fclose(fpv);
                remove("veri.bin");
                rename("verinew.bin", "veri.bin");
                indexsil();
                indexdosyasiolustur();
                sorting();
                sleep(1);
                return 0;
            }
            else
                adet++;
            printf("ogrenciye ait birden fazla veri var.\n");
            int onbilgi = 1;
            for(adet; adet > 1; adet--)
            {
                int yazdirma;
                printf("%d-", onbilgi);
                fseek(fpv, arrindex[mid], SEEK_SET);
                for(int i = 0; i < 3; i++)
                {
                    fscanf(fpv, "%d", &yazdirma);
                    printf("%d ", yazdirma);
                }
                mid++;
                onbilgi++;
                printf("\n");
            }
            mid = midtest;
            if(sil_gunc == 1)
            {
                int kayitsecim, nolukayit;
                printf("ogrenciye ait hangi kaydi silmek istiyorsunuz:");
                scanf("%d", &kayitsecim);
                while(onbilgi <= kayitsecim)
                {
                    printf("Hatali girdi! Lutfen tekrardan seciniz\n");
                    scanf("%d", &kayitsecim);

                }
                nolukayit = kayitsecim;
                kayitsecim = kayitsecim - 1;
                for(i = 1; i < veridegismez+1; i++)
                {
                    if(ogrno[i] == arr[mid])
                    {
                        veridosyasiyeri  = i;
                        if(kayitsecim == 0)
                            break;
                        else
                            kayitsecim--;
                    }
                }
                int eminmi;
                printf("%d nolu kayit silinicek emin misiniz?\n1-Evet\n2-Hayir\n", nolukayit);
                scanf("%d", &eminmi);
                if(eminmi == 1)
                {
                    FILE *fpvnew;
                    fpvnew = fopen("verinew.bin", "w");
                    for(veridosyasiyeri; veridosyasiyeri < veridegismez; veridosyasiyeri++)
                    {
                        ogrno[veridosyasiyeri] = ogrno[veridosyasiyeri+1];
                        derskodu[veridosyasiyeri] = derskodu[veridosyasiyeri]+1;
                        puan[veridosyasiyeri] = puan[veridosyasiyeri+1];
                    }
                    for(i = 1; i < veridegismez; i++)
                    {
                        fprintf(fpvnew, "%d %d %d\n", ogrno[i], derskodu[i], puan[i]);
                    }
                    fclose(fpvnew);
                    printf("veri basariyla silindi.\n");
                }
                else
                {
                    printf("veri silinmedi.\n");
                    fclose(fp);
                    fclose(fpv);
                    sleep(1);
                    return 0;
                }
            }
            if(sil_gunc == 2)
            {
                int kayitsecim;
                printf("ogrenciye ait hangi kaydi guncellemek istiyorsunuz:");
                scanf("%d", &kayitsecim);
                while(onbilgi <= kayitsecim)
                {
                    printf("Hatali girdi! Lutfen tekrardan seciniz\n");
                    scanf("%d", &kayitsecim);

                }
                kayitsecim = kayitsecim - 1;
                for(i = 1; i < veridegismez+1; i++)
                {
                    if(ogrno[i] == arr[mid])
                    {
                        veridosyasiyeri  = i;
                        if(kayitsecim == 0)
                            break;
                        else
                            kayitsecim--;
                    }
                }
                int yeniderskodu, yenipuan;
                printf("%d nolu ogrencinin yeni ders kodunu giriniz:", arr[mid]);
                scanf("%d", &yeniderskodu);
                printf("%d nolu ogrencinin yeni puanini giriniz:", arr[mid]);
                scanf("%d", &yenipuan);
                FILE *fpvnew;
                fpvnew = fopen("verinew.bin", "w");
                derskodu[veridosyasiyeri] = yeniderskodu;
                puan[veridosyasiyeri] = yenipuan;
                for(i = 1; i <= veridegismez; i++)
                {
                    fprintf(fpvnew, "%d %d %d\n", ogrno[i], derskodu[i], puan[i]);
                }
                fclose(fpvnew);
                printf("veri basariyla degistirildi.\n");
            }
            fclose(fp);
            fclose(fpv);
            remove("veri.bin");
            rename("verinew.bin", "veri.bin");
            indexsil();
            indexdosyasiolustur();
            sorting();
            sleep(1);
            return 0;
        }
        if(arr[mid] < istenen)
            low = mid + 1;
        else
            verisayisi = mid - 1;
    }
    fclose(fpv);
    fclose(fp);
    printf("ogrencinin numarasi bulunamadi.\n");
    sleep(1);
    return 0;
}
int binarysearch(int istenen)
{
    int verisayisi = 0, i, low;
    FILE *fp, *fpv;
    fp = fopen("index.txt", "r");
    fpv = fopen("veri.bin", "r");
    while(fscanf(fp, "%d", &low) == 1)
        verisayisi++;
    verisayisi = verisayisi / 2;
    rewind(fp);
    int arr[verisayisi+1], arrindex[verisayisi+1];
    for(i = 1; i < verisayisi+1; i++)
    {
        fscanf(fp, "%d", &arr[i]);
        fscanf(fp, "%d", &arrindex[i]);
    }
    low = 0;
    while(low < verisayisi+1)
    {
        int mid = low + (verisayisi - low) / 2;
        if(arr[mid] == istenen)
        {
            int adet = 1, midtest;
            midtest = mid;
            if(midtest != verisayisi)
                while(arr[midtest] == arr[midtest+1])
                {
                    adet++;
                    midtest++;
                }
            midtest = mid;
            if(midtest > 0)
                while(arr[midtest] == arr[midtest-1])
                {
                    adet++;
                    midtest--;
                }
            mid = midtest;
            if(adet == 1)
            {
                fclose(fp);
                fclose(fpv);
                return arrindex[mid];
            }
            else
                adet++;
            printf("ogrenciye ait birden fazla veri var.\n");
            int onbilgi = 1;
            for(adet; adet > 1; adet--)
            {
                int yazdirma;
                printf("%d-", onbilgi);
                fseek(fpv, arrindex[mid], SEEK_SET);
                for(int i = 0; i < 3; i++)
                {
                    fscanf(fpv, "%d", &yazdirma);
                    printf("%d ", yazdirma);
                }
                mid++;
                onbilgi++;
                printf("\n");
            }
            fclose(fp);
            fclose(fpv);
            return -1;
        }
        if(arr[mid] < istenen)
            low = mid + 1;
        else
            verisayisi = mid - 1;
    }
    fclose(fpv);
    fclose(fp);
    printf("ogrencinin numarasi bulunamadi.\n");
    return -1;
}
void sorting()
{
    int test = 0, verisayisi = 0, i, j, min, minyer;
    FILE *fp, *fpnew;
    fp = fopen("index.txt", "r");
    while(fscanf(fp, "%d", &test) == 1)
        verisayisi++;
    verisayisi = verisayisi / 2;
    rewind(fp);
    int arr[verisayisi], arrindex[verisayisi];
    for(i = 0; i < verisayisi; i++)
    {
        fscanf(fp, "%d", &arr[i]);
        fscanf(fp, "%d", &arrindex[i]);
    }
    for (i = 0; i < (verisayisi)-1; i++)
    {
        for (j = 0; j < (verisayisi)-i-1; j++)
        {
            if (arr[j] > arr[j+1])
            {
                int temp = arr[j];
                arr[j] = arr[j+1];
                arr[j+1] = temp;
                temp = arrindex[j];
                arrindex[j] = arrindex[j+1];
                arrindex[j+1] = temp;
            }
        }
    }
    fpnew = fopen("indexnew.txt", "w");
    for(i = 0; i < verisayisi; i++)
    {
        fprintf(fpnew, "%d %d\n", arr[i], arrindex[i]);
    }
    fclose(fp);
    fclose(fpnew);
    if (remove("index.txt") == 0)
        printf("index dosyasi siralaniyor.\n");
    rename("indexnew.txt", "index.txt");

}
int indexdosyasiolustur()
{
    FILE *fp, *fpv;
    if(fp = fopen("index.txt","r"))
    {
        fclose(fp);
        return 0;
    }
    else
    {
        int yaz = 0, sira = 3, verisayisi = 0, test;
        fp = fopen("index.txt", "a");
        fpv = fopen("veri.bin", "r");
        while(fscanf(fpv, "%d", &test) == 1)
            verisayisi++;
        verisayisi = verisayisi/3;
        rewind(fpv);
        test = ftell(fpv);
        fscanf (fpv, "%d", &yaz);
        while(!feof(fpv))
        {
            while(sira%3==0)
            {
                fprintf(fp, "%d ", yaz);
                fprintf(fp, "%d\n", test);
                break;
            }
            test = ftell(fpv)+2;
            fscanf(fpv, "%d", &yaz);
            sira++;
        }
        fclose(fp);
        fclose(fpv);
        return 1;
    }
}
void kayitekle(struct kayit kayitlar)
{
    printf("\n------------------------------------------------------------------------\n\n");
    FILE *fp,*fpi;
    fp = fopen("veri.bin", "a");
    fseek(fp, 0, SEEK_END);
    fpi = fopen("index.txt", "a");
    int a = ftell(fp);
    printf("kaydi eklenecek ogrencinin numarasi: ");
    scanf("%d", &kayitlar.ogrno);
    fprintf(fpi, "%d %d\n", kayitlar.ogrno, a);
    printf("kaydi eklenecek ders kodu: ");
    scanf("%d", &kayitlar.derskodu);
    printf("kaydi eklenecek dersin puani: ");
    scanf("%d", &kayitlar.puan);
    fprintf(fp, "%d %d %d\n", kayitlar.ogrno, kayitlar.derskodu, kayitlar.puan);
    fclose(fp);
    fclose(fpi);
    sorting();
    printf("\n------------------------------------------------------------------------\n\n");
    sleep(1);

}
void kayitbul()
{
    printf("\n------------------------------------------------------------------------\n\n");
    int istenen, yer;
    printf("bulmak istediginiz ogrencinin numarasi:");
    scanf("%d", &istenen);
    yer = binarysearch(istenen);
    if(yer!=-1)
    {
        FILE *fp;
        fp = fopen("veri.bin", "r");
        fseek(fp, yer, SEEK_SET);
        for(int i = 0; i < 3; i++)
        {
            fscanf(fp, "%d", &yer);
            printf("%d ", yer);
        }
        fclose(fp);
        printf("\n");
    }
    printf("\n------------------------------------------------------------------------\n\n");
}
void kayitsil()
{
    printf("\n------------------------------------------------------------------------\n\n");
    sil_guncelle(1);
    printf("\n------------------------------------------------------------------------\n\n");
}
void kayitgunc()
{
    printf("\n------------------------------------------------------------------------\n\n");
    sil_guncelle(2);
    printf("\n------------------------------------------------------------------------\n\n");

}
void verigoster()
{
    printf("\n------------------------------------------------------------------------\n\n");
    FILE *fp;
    fp = fopen("veri.bin", "a");
    fclose(fp);
    fp = fopen ("veri.bin", "r");
    int yaz = 0;
    int sira = 3;
    int on  = 1;
    printf("veri dosyasi gosteriliyor:\nogrenci no - ders kodu - puan");
    fscanf(fp, "%d", &yaz);
    while (!feof(fp))
    {
        while(sira%3==0)
        {
            printf("\n");
            printf("%d-", on);
            on++;
            break;
        }
        printf("%d ", yaz);
        fscanf(fp, "%d", &yaz);
        sira++;
    }
    fclose(fp);
    printf("\n\n------------------------------------------------------------------------\n\n");
    sleep(1);
}
void indexgoster()
{
    printf("\n------------------------------------------------------------------------\n\n");
    printf("index dosyasi gosteriliyor:\n");
    int c;
    FILE *fp;
    fp = fopen("index.txt", "r");
    if (fp == NULL)
    {
        printf("Hata index dosyasi mevcut degil!\n");
        printf("\n------------------------------------------------------------------------\n\n");
        sleep(1);
        return 0;
    }
    else
        printf("ogrenci no - veri dosyasindaki adresi\n");
    c = fgetc(fp);
    while (c != EOF)
    {
        printf ("%c", c);
        c = fgetc(fp);
    }
    fclose(fp);
    printf("\n------------------------------------------------------------------------\n\n");
    sleep(1);
}
int indexsil()
{
    if (remove("index.txt") == 0)
        return 1;
    else
        return 0;
}
int main()
{
    bool dongu = true;
    int islem;
    while(dongu)
    {
        printf("hangi islemi yapmak istiyorsunuz?\n");
        printf("1-Index dosyasi olustur\n");
        printf("2-Kayit ekle\n");
        printf("3-Kayit bul\n");
        printf("4-Kayit sil\n");
        printf("5-Kayit guncelle\n");
        printf("6-Veri dosyasini goster\n");
        printf("7-Index dosyasini goster\n");
        printf("8-Index dosyasini sil\n");
        printf("0-Programi kapat\n");
        scanf("%d", &islem);
        switch(islem)
        {
        case 1:
            printf("\n------------------------------------------------------------------------\n\n");
            if(indexdosyasiolustur())
            {
                printf("index dosyasi olusturuldu.\n");
                sorting();
            }
            else
                printf("index dosyasi zaten mevcut.\n");
            printf("\n------------------------------------------------------------------------\n\n");
            sleep(1);
            break;
        case 2:
            kayitekle(kayitlar);
            break;
        case 3:
            kayitbul();
            break;
        case 4:
            kayitsil();
            break;
        case 5:
            kayitgunc();
            break;
        case 6:
            verigoster();
            break;
        case 7:
            indexgoster();
            break;
        case 8:
            printf("\n------------------------------------------------------------------------\n\n");
            if(indexsil())
                printf("Index dosyasi basariyla silindi.\n");
            else
                printf("Hata! Index dosyasi silinemedi\nIpucu: Index dosyasi olusturulmamis olabilir.\n");
            printf("\n------------------------------------------------------------------------\n\n");
            sleep(1);
            break;
        case 0:
            printf("program kapatiliyor...\n");
            dongu=false;
            break;
        default:
            printf("\nlutfen gecerli bir deger giriniz.\n\n");
        }
    }
    return 0;
}
