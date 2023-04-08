//200201012 Baris Kakilli
//200201032 Muhammed Sina Cimen
//Programlama Laboratuvari I - 3. proje

#include <stdio.h>
#include <stdlib.h>

typedef struct kayit
{
    int oncelik_id;
    int ucak_id;
    int talep_edilen_inis_saati;
    int ceza;
} kayit;

typedef struct output
{
    int oncelik_id;
    int ucak_id;
    int talep_edilen_inis_saati;
    int inis_saati;
    int gecikme_suresi;
    int kalkis_saati;
} output;

int dosyaoku(kayit izin[100])
{
    FILE *file = fopen("input.txt","r");
    if(file == NULL)
        return 1;
    int sayi = 0;
    while (!feof(file))
    {
        fscanf(file,"%d %d %d",&izin[sayi].oncelik_id, &izin[sayi].ucak_id, &izin[sayi].talep_edilen_inis_saati);
        sayi++;
    }
    fclose(file);
    return 0;
}

int veriDosyasiniGoster(kayit izin[100], int eleman_sayisi)
{
    int sayi = 0;
    while (sayi < eleman_sayisi)
    {
        printf("Oncelik: %d Ucak ID'si: %d Talep edilen inis saati: %d\n", izin[sayi].oncelik_id, izin[sayi].ucak_id, izin[sayi].talep_edilen_inis_saati);
        sayi++;
    }
    return 0;
}

int veriDosyasiniGoster2(output izin[100], int eleman_sayisi)
{
    int sayi = 0;
    while (sayi < eleman_sayisi)
    {
        printf("Oncelik: %d Ucak ID'si: %d Talep edilen inis saati: %d ", izin[sayi].oncelik_id, izin[sayi].ucak_id, izin[sayi].talep_edilen_inis_saati);
        printf("Inis saati: %d(%d) ", izin[sayi].inis_saati%24, izin[sayi].inis_saati);
        printf("Gecikme suresi: %d Kalkis saati: %d(%d)\n", izin[sayi].gecikme_suresi, izin[sayi].kalkis_saati%24, izin[sayi].kalkis_saati);
        sayi++;
    }
    return 0;
}

int sirala(kayit izin[100])
{
    FILE *file = fopen("input.txt","r");
    if (file == NULL)
        return 1;
    char tmp[20];
    int counter = 0;
    while (!feof(file))
    {
        fscanf(file,"%s",tmp);
        counter++;
    }
    counter = counter/3;
    fclose(file);
    int swap[3];
    for(int i=0; i<counter; i++)
    {
        for(int j=i; j<counter; j++)
        {
            if (izin[i].talep_edilen_inis_saati > izin[j].talep_edilen_inis_saati)
            {
                swap[0] = izin[i].talep_edilen_inis_saati;
                swap[1] = izin[i].ucak_id;
                swap[2] = izin[i].oncelik_id;

                izin[i].talep_edilen_inis_saati = izin[j].talep_edilen_inis_saati;
                izin[i].ucak_id = izin[j].ucak_id;
                izin[i].oncelik_id = izin[j].oncelik_id;

                izin[j].talep_edilen_inis_saati = swap[0];
                izin[j].ucak_id = swap[1];
                izin[j].oncelik_id = swap[2];

                j = i;
            }
        }
    }


    FILE *dosya = fopen("sirali.txt","w");


    if (file == NULL)
        return 1;

    for(int i=0; i<counter; i++)
    {
        fprintf(dosya,"%d %d %d\n",izin[i].oncelik_id,izin[i].ucak_id,izin[i].talep_edilen_inis_saati);
    }

    fclose(dosya);
    return counter;
}

int sirala2(kayit izin[100])
{
    FILE *file = fopen("sirali.txt","r");
    if (file == NULL)
        return 1;
    char tmp[20];
    int counter = 0;
    while (!feof(file))
    {
        fscanf(file,"%s",tmp);
        counter++;
    }
    counter = counter/3;

    fclose(file);
    int swap[3];

    for(int i=0; i<counter; i++)
    {
        for(int j=i; j<counter; j++)
        {
            if (izin[i].talep_edilen_inis_saati == izin[j].talep_edilen_inis_saati)
            {
                if(izin[i].oncelik_id > izin[j].oncelik_id)
                {
                    swap[0] = izin[i].talep_edilen_inis_saati;
                    swap[1] = izin[i].ucak_id;
                    swap[2] = izin[i].oncelik_id;

                    izin[i].talep_edilen_inis_saati = izin[j].talep_edilen_inis_saati;
                    izin[i].ucak_id = izin[j].ucak_id;
                    izin[i].oncelik_id = izin[j].oncelik_id;

                    izin[j].talep_edilen_inis_saati = swap[0];
                    izin[j].ucak_id = swap[1];
                    izin[j].oncelik_id = swap[2];

                    j = i;
                }
            }
        }
    }
    FILE *dosya = fopen("sirali2.txt","w");

    if (file == NULL)
        return 1;

    for(int i=0; i<counter; i++)
    {
        fprintf(dosya,"%d %d %d\n",izin[i].oncelik_id,izin[i].ucak_id,izin[i].talep_edilen_inis_saati);
    }

    fclose(dosya);
    return counter;
}

int sirala3(kayit izin[100])
{
    FILE *file = fopen("sirali2.txt","r");
    if (file == NULL)
        return 1;
    char tmp[20];
    int counter = 0;
    while (!feof(file))
    {
        fscanf(file,"%s",tmp);
        counter++;
    }
    counter = counter/3;

    fclose(file);
    int swap[3];

    for(int i=0; i<counter; i++)
    {
        for(int j=i; j<counter; j++)
        {
            if (izin[i].talep_edilen_inis_saati == izin[j].talep_edilen_inis_saati)
            {
                if(izin[i].oncelik_id == izin[j].oncelik_id)
                {
                    if(izin[i].ucak_id > izin[j].ucak_id)
                    {
                        swap[0] = izin[i].talep_edilen_inis_saati;
                        swap[1] = izin[i].ucak_id;
                        swap[2] = izin[i].oncelik_id;

                        izin[i].talep_edilen_inis_saati = izin[j].talep_edilen_inis_saati;
                        izin[i].ucak_id = izin[j].ucak_id;
                        izin[i].oncelik_id = izin[j].oncelik_id;

                        izin[j].talep_edilen_inis_saati = swap[0];
                        izin[j].ucak_id = swap[1];
                        izin[j].oncelik_id = swap[2];

                        j = i;
                    }
                }
            }
        }
    }
    FILE *dosya = fopen("sirali3.txt","w");

    if (file == NULL)
        return 1;

    for(int i=0; i<counter; i++)
    {
        fprintf(dosya,"%d %d %d\n",izin[i].oncelik_id,izin[i].ucak_id,izin[i].talep_edilen_inis_saati);
    }

    fclose(dosya);
    return counter;
}

int ucakindi(kayit izin[100], int silincek_index)
{
    for(int i = silincek_index; i < 27; i++)
    {
        izin[i] = izin[i+1];
    }
    return 1;
}

int main()
{
    kayit izin[100];
    output kalkis[100];
    int eleman_sayisi;
    int inen_ucak_sayisi = 0;
    dosyaoku(izin);
    int kac_adet = sirala(izin);
    eleman_sayisi = kac_adet;
    sirala2(izin);
    sirala3(izin);
    veriDosyasiniGoster(izin, eleman_sayisi);
    printf("\n");
    int saat = 1;
    int kac_ucak_izin_istiyor = 0;
    for(int i = 0; i <= kac_adet; i++)
        izin[i].ceza = 0;
    for(int i = 0; i <= eleman_sayisi; i++)
    {
        printf("saat su an: %d ", saat);
        kac_ucak_izin_istiyor = 0;
        for(int j = 0; j <= kac_adet; j++) // kac adet ucak
        {
            if(izin[j].talep_edilen_inis_saati <= saat)
                kac_ucak_izin_istiyor++;
            else
                break;
        }
        printf("izin isteyen ucak sayisi: %d\n", kac_ucak_izin_istiyor);
        if(kac_ucak_izin_istiyor == 0)
        {
            saat++;
            printf("\n");
            continue;
        }
        int ceza_flag = 0;
        int cezali_sayisi = 0;
        int cezali_yer[10] = {-1, -1, -1, -1, -1, -1, -1, -1, -1, -1};

        for(int j = 0; j < kac_adet; j++) // cezali var mi
        {
            if(izin[j].ceza >= 3)
            {
                ceza_flag = 1;
                cezali_yer[cezali_sayisi] = j;
                cezali_sayisi++;

            }
        }
        int en_kucuk_sayisi = 0;
        int en_kucuk = 5;
        int en_kucuk_yer;
        int en_kucuk_id;
        for(int j = 0; j < kac_ucak_izin_istiyor; j++)  // ceza ++
        {
            izin[j].ceza++;
            //printf("ceza ++ [izin[j%d].ceza :%d : %d\n", j, izin[j].ceza, izin[j].ucak_id);
        }

        // ucak indirme
        if(ceza_flag == 0)  // cezali olmayan
        {
            for(int k = 0; k < kac_ucak_izin_istiyor; k++)
            {
                if(izin[k].oncelik_id < en_kucuk)
                {
                    en_kucuk = izin[k].oncelik_id;
                    en_kucuk_yer = k;
                    en_kucuk_id = izin[k].ucak_id;
                }
            }
            for(int k = 0; k < kac_ucak_izin_istiyor; k++)
            {
                if(izin[k].oncelik_id == en_kucuk)
                {
                    en_kucuk_sayisi++;
                }
            }
            if(en_kucuk_sayisi > 1)
            {
                for(int k = 0; k < kac_ucak_izin_istiyor; k++)
                {
                    if(izin[k].ucak_id < en_kucuk_id && izin[k].oncelik_id == en_kucuk)
                    {
                        en_kucuk_id = izin[k].ucak_id;
                        en_kucuk_yer = k;
                    }
                }
                printf("sirasi gelen %d id'li ucak inis yapiyor\n", izin[en_kucuk_yer].ucak_id);
                kalkis[inen_ucak_sayisi].talep_edilen_inis_saati = izin[en_kucuk_yer].talep_edilen_inis_saati;
                kalkis[inen_ucak_sayisi].oncelik_id = izin[en_kucuk_yer].oncelik_id;
                kalkis[inen_ucak_sayisi].ucak_id = izin[en_kucuk_yer].ucak_id;
                kalkis[inen_ucak_sayisi].inis_saati = saat;
                kalkis[inen_ucak_sayisi].gecikme_suresi = saat - izin[en_kucuk_yer].talep_edilen_inis_saati;
                kalkis[inen_ucak_sayisi].kalkis_saati = saat + 1;
                inen_ucak_sayisi += ucakindi(izin, en_kucuk_yer);
                izin[eleman_sayisi-inen_ucak_sayisi].talep_edilen_inis_saati = 999;
                izin[eleman_sayisi-inen_ucak_sayisi].oncelik_id = 999;
                izin[eleman_sayisi-inen_ucak_sayisi].ucak_id = 999;
                izin[eleman_sayisi-inen_ucak_sayisi].ceza = -999;
            }
            else
            {
                printf("sirasi gelen %d id'li ucak inis yapiyor\n", izin[en_kucuk_yer].ucak_id);
                kalkis[inen_ucak_sayisi].talep_edilen_inis_saati = izin[en_kucuk_yer].talep_edilen_inis_saati;
                kalkis[inen_ucak_sayisi].oncelik_id = izin[en_kucuk_yer].oncelik_id;
                kalkis[inen_ucak_sayisi].ucak_id = izin[en_kucuk_yer].ucak_id;
                kalkis[inen_ucak_sayisi].inis_saati = saat;
                kalkis[inen_ucak_sayisi].gecikme_suresi = saat - izin[en_kucuk_yer].talep_edilen_inis_saati;
                kalkis[inen_ucak_sayisi].kalkis_saati = saat + 1;
                inen_ucak_sayisi += ucakindi(izin, en_kucuk_yer);
                izin[eleman_sayisi-inen_ucak_sayisi].talep_edilen_inis_saati = 999;
                izin[eleman_sayisi-inen_ucak_sayisi].oncelik_id = 999;
                izin[eleman_sayisi-inen_ucak_sayisi].ucak_id = 999;
                izin[eleman_sayisi-inen_ucak_sayisi].ceza = -999;
            }
        }
        if(ceza_flag == 1) //cezali olan
        {
            if(cezali_sayisi == 1)
            {
                printf("bekleme yapan %d id'li ucak inis yapiyor\n", izin[cezali_yer[0]].ucak_id);
                kalkis[inen_ucak_sayisi].talep_edilen_inis_saati = izin[cezali_yer[0]].talep_edilen_inis_saati;
                kalkis[inen_ucak_sayisi].oncelik_id = izin[cezali_yer[0]].oncelik_id;
                kalkis[inen_ucak_sayisi].ucak_id = izin[cezali_yer[0]].ucak_id;
                kalkis[inen_ucak_sayisi].inis_saati = saat;
                kalkis[inen_ucak_sayisi].gecikme_suresi = saat - izin[cezali_yer[0]].talep_edilen_inis_saati;
                kalkis[inen_ucak_sayisi].kalkis_saati = saat + 1;
                inen_ucak_sayisi += ucakindi(izin, cezali_yer[0]);
                izin[eleman_sayisi-inen_ucak_sayisi].talep_edilen_inis_saati = 999;
                izin[eleman_sayisi-inen_ucak_sayisi].oncelik_id = 999;
                izin[eleman_sayisi-inen_ucak_sayisi].ucak_id = 999;
                izin[eleman_sayisi-inen_ucak_sayisi].ceza = -999;
            }
            else
            {
                for(int k = 0; k < kac_ucak_izin_istiyor; k++)
                {
                    if(izin[k].oncelik_id < en_kucuk && izin[k].ceza > 3)
                    {
                        en_kucuk = izin[k].oncelik_id;
                        en_kucuk_yer = k;
                        en_kucuk_id = izin[k].ucak_id;
                    }
                }
                for(int k = 0; k < kac_ucak_izin_istiyor; k++)
                {
                    if(izin[k].oncelik_id == en_kucuk && izin[k].ceza > 3)
                    {
                        en_kucuk_sayisi++;
                    }
                }
                if(en_kucuk_sayisi > 1)
                {
                    for(int k = 0; k < kac_ucak_izin_istiyor; k++)
                    {
                        if((izin[k].ucak_id < en_kucuk_id && izin[k].oncelik_id == en_kucuk) && izin[k].ceza > 3)
                        {
                            en_kucuk_id = izin[k].ucak_id;
                            en_kucuk_yer = k;
                        }
                    }
                    printf("bekleme yapan %d id'li ucak inis yapiyor\n", izin[en_kucuk_yer].ucak_id);
                    kalkis[inen_ucak_sayisi].talep_edilen_inis_saati = izin[en_kucuk_yer].talep_edilen_inis_saati;
                    kalkis[inen_ucak_sayisi].oncelik_id = izin[en_kucuk_yer].oncelik_id;
                    kalkis[inen_ucak_sayisi].ucak_id = izin[en_kucuk_yer].ucak_id;
                    kalkis[inen_ucak_sayisi].inis_saati = saat;
                    kalkis[inen_ucak_sayisi].gecikme_suresi = saat - izin[en_kucuk_yer].talep_edilen_inis_saati;
                    kalkis[inen_ucak_sayisi].kalkis_saati = saat + 1;
                    inen_ucak_sayisi += ucakindi(izin, en_kucuk_yer);
                    izin[eleman_sayisi-inen_ucak_sayisi].talep_edilen_inis_saati = 999;
                    izin[eleman_sayisi-inen_ucak_sayisi].oncelik_id = 999;
                    izin[eleman_sayisi-inen_ucak_sayisi].ucak_id = 999;
                    izin[eleman_sayisi-inen_ucak_sayisi].ceza = -999;

                    printf("birden fazla ucak beklemede oldugu icin bu ucaklar sabiha gokcene aktariliyor:\n");
                    int test = en_kucuk_yer;
                    for(int k = 0; k < cezali_sayisi; k++)
                    {
                        if(cezali_yer[k] != en_kucuk_yer)
                        {
                            if(cezali_yer[k] > test)
                            {
                                printf("%d idli ucak sabiha gokcene aktariliyor\n", izin[cezali_yer[k]-1].ucak_id);
                                eleman_sayisi -= ucakindi(izin, cezali_yer[k]-1);
                            }
                            else
                            {
                                printf("%d idli ucak sabiha gokcene aktariliyor\n", izin[k].ucak_id);
                                eleman_sayisi -= ucakindi(izin, cezali_yer[k]);
                                test = cezali_yer[k];
                            }
                        }
                    }
                }
                else
                {
                    printf("bekleme yapan %d id'li ucak inis yapiyor\n", izin[en_kucuk_yer].ucak_id);
                    kalkis[inen_ucak_sayisi].talep_edilen_inis_saati = izin[en_kucuk_yer].talep_edilen_inis_saati;
                    kalkis[inen_ucak_sayisi].oncelik_id = izin[en_kucuk_yer].oncelik_id;
                    kalkis[inen_ucak_sayisi].ucak_id = izin[en_kucuk_yer].ucak_id;
                    kalkis[inen_ucak_sayisi].inis_saati = saat;
                    kalkis[inen_ucak_sayisi].gecikme_suresi = saat - izin[en_kucuk_yer].talep_edilen_inis_saati;
                    kalkis[inen_ucak_sayisi].kalkis_saati = saat + 1;
                    inen_ucak_sayisi += ucakindi(izin, en_kucuk_yer);
                    izin[eleman_sayisi-inen_ucak_sayisi].talep_edilen_inis_saati = 999;
                    izin[eleman_sayisi-inen_ucak_sayisi].oncelik_id = 999;
                    izin[eleman_sayisi-inen_ucak_sayisi].ucak_id = 999;
                    izin[eleman_sayisi-inen_ucak_sayisi].ceza = -999;

                    printf("birden fazla ucak beklemede oldugu icin bu ucaklar sabiha gokcene aktariliyor:\n");
                    int test = en_kucuk_yer;
                    for(int k = 0; k < cezali_sayisi; k++)
                    {
                        if(cezali_yer[k] != en_kucuk_yer)
                        {
                            if(cezali_yer[k] > test)
                            {
                                printf("%d idli ucak sabiha gokcene aktariliyor\n", izin[cezali_yer[k]-1].ucak_id);
                                eleman_sayisi -= ucakindi(izin, cezali_yer[k]-1);
                            }
                            else
                            {
                                printf("%d idli ucak sabiha gokcene aktariliyor\n", izin[k].ucak_id);
                                eleman_sayisi -= ucakindi(izin, cezali_yer[k]);
                                test = cezali_yer[k];
                            }
                        }
                    }
                }
            }
            ceza_flag = 0;
        }
        // 24 ucak limiti yeri
        /*if(inen_ucak_sayisi >= 24)
        {
            printf("\ngunluk ucak limitine ulasildi.\n");
            break;
        }*/
        printf("\n");
        saat++;
    }
    printf("\n");
    veriDosyasiniGoster2(kalkis, inen_ucak_sayisi);
    FILE *dosya = fopen("output.txt","w");
    for(int i = 0; i < inen_ucak_sayisi; i++)
    {
        fprintf(dosya,"%d %d %d ", kalkis[i].oncelik_id, kalkis[i].ucak_id, kalkis[i].talep_edilen_inis_saati);
        fprintf(dosya, "%d %d %d\n", kalkis[i].inis_saati%24, kalkis[i].gecikme_suresi, kalkis[i].kalkis_saati%24);
    }
    fclose(dosya);

    return 0;
}

