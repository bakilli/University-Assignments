//200201012 Baris Kakilli
//200201032 Muhammed Sina Cimen
//Programlama Laboratuvari II - 1. proje

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>


int dosyaOku()
{
    char *filename = "hello.txt";
    FILE *fp = fopen(filename, "r");

    if (fp == NULL)
    {
        printf("Dosya acilamiyor: %s", filename);
        return 1;
    }

    char ch;
    while ((ch = fgetc(fp)) != EOF)
        putchar(ch);

    fclose(fp);


    FILE *file = fopen(filename, "r");
    int c = fgetc(file);
    if (c == EOF)
    {
        printf("Dosya Bos!");
    }
    else
    {
        ungetc(c, file);
    }
    fclose(file);

    return 0;

}

int main()
{
    dosyaOku();
    printf("\n\n------------------------------------------------------------------------\n\n");
    FILE *fp = fopen("hello.txt","r");
    char kelime[50];
    int donguadet = 0, donguadetmax;
    int lineer = 0, logaritmik = 0;
    int lineermax = 0, logaritmikmax = 0;
    int linlogtest = 1;
    int tnkarmasiklik[10] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
    int yerkarmasiklik = 0;
    char yerkarmasiklikchar[10][10];
    int yerkarmasiklikcharadet = 0;
    while(!feof(fp))
    {
        fpos_t doyeri;
        fpos_t whileyeri;
        char whilesaklama[50];
        int dowhilekontrol = 0;
        fscanf(fp, "%s", kelime);

        ///ister 4
        if(strstr(kelime, ";") != 0)
        {
            tnkarmasiklik[donguadet]++;
        }

        ///ister 2
        if(strcmp(kelime, "for") == 0 || strcmp(kelime, "do") == 0 || strcmp(kelime, "while") == 0 || strcmp(kelime, "return") == 0)
        {
            donguadet++;
            char *test;
            /// for icin
            if(strcmp(kelime, "for") == 0)
            {
                fscanf(fp, "%s", kelime);
                if((test = strstr(kelime, "+") != 0) || (test = strstr(kelime, "-") != 0))
                {
                    lineer++;
                    linlogtest = linlogtest * 2;
                }
                if((test = strstr(kelime, "*") != 0) || (test = strstr(kelime, "/") != 0))
                {
                    logaritmik++;
                    linlogtest = linlogtest * 3;
                }
            }
            /// while icin
            if(strcmp(kelime, "while") == 0)
            {
                printf("whili ici");
                dowhilekontrol++;
                bool flag = true;
                char bironceki[50];
                fgetpos(fp, &whileyeri);
                fscanf(fp, "%s", whilesaklama);
                while(flag)
                {
                    strcpy(bironceki, kelime);
                    fscanf(fp, "%s", kelime);
                    if(strcmp(kelime, "}") == 0)
                    {
                        flag = false;
                    }
                }
                //if(test = strstr(whilesaklama, bironceki) != 0) bu testi yapamiyorum 2 string icinde karsilastirma
                if((test = strstr(bironceki, "+") != 0) || (test = strstr(bironceki, "-") != 0))
                {
                    lineer++;
                    linlogtest = linlogtest * 2;
                }
                if((test = strstr(bironceki, "*") != 0) || (test = strstr(bironceki, "/") != 0))
                {
                    logaritmik++;
                    linlogtest = linlogtest * 3;
                }
                fsetpos(fp, &whileyeri);
            }
            /// do icin
            if(strcmp(kelime, "do") == 0)
            {
                printf("do ici");
                dowhilekontrol++;
                bool flag = true;
                char bironceki[50];
                fgetpos(fp, &doyeri);
                fscanf(fp, "%s", whilesaklama);
                while(flag)
                {
                    strcpy(bironceki, kelime);
                    fscanf(fp, "%s", kelime);
                    if(test = strstr(kelime, "}") != 0)
                    {
                        flag = false;
                    }
                }
                if((test = strstr(bironceki, "+") != 0) || (test = strstr(bironceki, "-") != 0))
                {
                    lineer++;
                    linlogtest = linlogtest * 2;
                }
                if((test = strstr(bironceki, "*") != 0) || (test = strstr(bironceki, "/") != 0))
                {
                    logaritmik++;
                    linlogtest = linlogtest * 3;
                }
                fsetpos(fp, &doyeri);
            }
            /// recursive icin
            if(strcmp(kelime, "return") == 0)
            {
                dowhilekontrol++;
                bool flag = true;
                while(flag)
                {
                    fscanf(fp, "%s", kelime);
                    if(test = strstr(kelime, "(") != 0)
                    {
                        if((test = strstr(kelime, "+") != 0) || (test = strstr(kelime, "-") != 0))
                        {
                            lineer++;
                            linlogtest = linlogtest * 2;
                        }
                        if((test = strstr(kelime, "*") != 0) || (test = strstr(kelime, "/") != 0))
                        {
                            logaritmik++;
                            linlogtest = linlogtest * 3;
                        }
                        flag = false;
                    }
                    else if(test = strstr(kelime, ";") != 0)
                    {
                        donguadet--;
                        flag = false;
                    }

                }
            }
            ///son kisim
            if(donguadetmax<donguadet)
                donguadetmax = donguadet;
            if(lineermax<lineer)
                lineermax = lineer;
            if(logaritmikmax<logaritmik)
                logaritmikmax = logaritmik;
        }

        /// ister 3
        if(strcmp(kelime, "int") == 0 || strcmp(kelime, "char") == 0 || strcmp(kelime, "double") == 0 || strcmp(kelime, "float") == 0)
        {
            if(strcmp(kelime, "int") == 0)
            {
                while(strstr(kelime, ";") == 0)
                {
                    if(strstr(kelime, "(") != 0)
                    {
                        break;
                    }
                    else if(strstr(kelime, ",") != 0)
                    {
                        yerkarmasiklik = yerkarmasiklik + 4;
                    }
                    fscanf(fp, "%s", kelime);
                }
                if(strstr(kelime, "[") != 0)
                {
                    char* kelimeyer;
                    char parantezlikelime[20];
                    char aranan = '[';
                    char aranan2 = ']';
                    char aranan3 = ';';
                    kelimeyer = strstr(kelime, "[");
                    strcpy(parantezlikelime, kelimeyer);
                    int length;
                    length = strlen(parantezlikelime);
                    for(int i = 0; i < length; i++)
                    {
                        if((parantezlikelime[i] == aranan) || (parantezlikelime[i] == aranan2) || (parantezlikelime[i] == aranan3))
                        {
                            for(int j = i; j < length; j++)
                            {
                                parantezlikelime[j] = parantezlikelime[j + 1];
                            }
                            length--;
                            i--;
                        }
                    }
                    strcat(parantezlikelime, "*4");
                    strcpy(yerkarmasiklikchar[yerkarmasiklikcharadet], parantezlikelime);
                    yerkarmasiklikcharadet++;
                    tnkarmasiklik[donguadet]++;
                }
                else
                {
                    yerkarmasiklik = yerkarmasiklik + 4;
                    tnkarmasiklik[donguadet]++;
                }
            }

            if(strcmp(kelime, "float") == 0)
            {
                while(strstr(kelime, ";") == 0)
                {
                    if(strstr(kelime, "(") != 0)
                    {
                        break;
                    }
                    else if(strstr(kelime, ",") != 0)
                    {
                        yerkarmasiklik = yerkarmasiklik + 4;
                    }
                    fscanf(fp, "%s", kelime);
                }
                if(strstr(kelime, "[") != 0)
                {
                    char* kelimeyer;
                    char parantezlikelime[20];
                    char aranan = '[';
                    char aranan2 = ']';
                    char aranan3 = ';';
                    kelimeyer = strstr(kelime, "[");
                    strcpy(parantezlikelime, kelimeyer);
                    int length;
                    length = strlen(parantezlikelime);
                    for(int i = 0; i < length; i++)
                    {
                        if((parantezlikelime[i] == aranan) || (parantezlikelime[i] == aranan2) || (parantezlikelime[i] == aranan3))
                        {
                            for(int j = i; j < length; j++)
                            {
                                parantezlikelime[j] = parantezlikelime[j + 1];
                            }
                            length--;
                            i--;
                        }
                    }
                    strcat(parantezlikelime, "*4");
                    strcpy(yerkarmasiklikchar[yerkarmasiklikcharadet], parantezlikelime);
                    yerkarmasiklikcharadet++;
                    tnkarmasiklik[donguadet]++;
                }
                else
                {
                    yerkarmasiklik = yerkarmasiklik + 4;
                    tnkarmasiklik[donguadet]++;
                }
            }

            if(strcmp(kelime, "double") == 0)
            {
                while(strstr(kelime, ";") == 0)
                {
                    if(strstr(kelime, "(") != 0)
                    {
                        break;
                    }
                    else if(strstr(kelime, ",") != 0)
                    {
                        yerkarmasiklik = yerkarmasiklik + 8;
                    }
                    fscanf(fp, "%s", kelime);
                }
                if(strstr(kelime, "[") != 0)
                {
                    char* kelimeyer;
                    char parantezlikelime[20];
                    char aranan = '[';
                    char aranan2 = ']';
                    char aranan3 = ';';
                    kelimeyer = strstr(kelime, "[");
                    strcpy(parantezlikelime, kelimeyer);
                    int length;
                    length = strlen(parantezlikelime);
                    for(int i = 0; i < length; i++)
                    {
                        if((parantezlikelime[i] == aranan) || (parantezlikelime[i] == aranan2) || (parantezlikelime[i] == aranan3))
                        {
                            for(int j = i; j < length; j++)
                            {
                                parantezlikelime[j] = parantezlikelime[j + 1];
                            }
                            length--;
                            i--;
                        }
                    }
                    strcat(parantezlikelime, "*8");
                    strcpy(yerkarmasiklikchar[yerkarmasiklikcharadet], parantezlikelime);
                    yerkarmasiklikcharadet++;
                    tnkarmasiklik[donguadet]++;
                }
                else
                {
                    yerkarmasiklik = yerkarmasiklik + 8;
                    tnkarmasiklik[donguadet]++;
                }
            }

            if(strcmp(kelime, "char") == 0)
            {
                while(strstr(kelime, ";") == 0)
                {
                    if(strstr(kelime, "(") != 0)
                    {
                        printf("( li %s", kelime);
                        break;
                    }
                    else if(strstr(kelime, ",") != 0)
                    {
                        yerkarmasiklik = yerkarmasiklik + 1;
                        printf("virgullu %s", kelime);
                    }
                    fscanf(fp, "%s", kelime);
                }
                if(strstr(kelime, "[") != 0)
                {
                    char* kelimeyer;
                    char parantezlikelime[20];
                    char aranan = '[';
                    char aranan2 = ']';
                    char aranan3 = ';';
                    kelimeyer = strstr(kelime, "[");
                    strcpy(parantezlikelime, kelimeyer);
                    int length;
                    length = strlen(parantezlikelime);
                    for(int i = 0; i < length; i++)
                    {
                        if((parantezlikelime[i] == aranan) || (parantezlikelime[i] == aranan2) || (parantezlikelime[i] == aranan3))
                        {
                            for(int j = i; j < length; j++)
                            {
                                parantezlikelime[j] = parantezlikelime[j + 1];
                            }
                            length--;
                            i--;
                        }
                    }
                    strcat(parantezlikelime, "*1");
                    strcpy(yerkarmasiklikchar[yerkarmasiklikcharadet], parantezlikelime);
                    yerkarmasiklikcharadet++;
                    tnkarmasiklik[donguadet]++;
                }
                else
                {
                    yerkarmasiklik = yerkarmasiklik + 1;
                    tnkarmasiklik[donguadet]++;
                }
            }
        }
        /// 3le ve 2le çarp one gore bole bole lineer logu cikar
        if(dowhilekontrol != 0)
        {
            dowhilekontrol--;
        }
        else
        {
            if(strstr(kelime, "}") != 0)
            {
                donguadet--;
                if((linlogtest%2) == 0)
                {
                    lineer--;
                    linlogtest = linlogtest / 2;
                }
                if((linlogtest%3) == 0)
                {
                    linlogtest = linlogtest / 3;
                    logaritmik--;
                }
            }
        }
    }
    fclose(fp);
    printf("\n");
    /// zaman karmasiklik yazdirma
    printf("zaman karmasikligi: ");
    if(logaritmikmax > 0 && lineermax > 0)
        printf("O(logn^%d*n^%d)", logaritmikmax, lineermax);
    else if(logaritmikmax > 0)
        printf("O(logn^%d)", logaritmikmax);
    else if(lineermax > 0)
        printf("O(n^%d)", lineermax);
    else
        printf("O(1)");
    printf("\n");
    printf("Programin calismasi icin gecen zaman: T(");
    for(int i = 0; i<4; i++)
    {
        if(tnkarmasiklik[i] != 0)
        {
            printf(" %dn^%d +", tnkarmasiklik[i], i);
        }
    }
    printf(")\n\n");
    /// yer karmasiklik yazdirma
    yerkarmasiklikcharadet--;
    printf("yer karmasikligi: %d  ", yerkarmasiklik);
    for(yerkarmasiklikcharadet; yerkarmasiklikcharadet >= 0; yerkarmasiklikcharadet--)
    {
        printf("+ %s ", yerkarmasiklikchar[yerkarmasiklikcharadet]);
    }
    printf("\n\n");
}
