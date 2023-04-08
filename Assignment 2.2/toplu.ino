//Dijital termometre
#include<LiquidCrystal.h>
LiquidCrystal lcd(8, 9, 10, 11, 12, 13);
#define sensor A0

//Kilit sistemi
#include <Keypad.h>

int yesil_led = 22;
int kirmizi_led = 23;

const int satir_say = 4;
const int sutun_say = 3;

char keys[satir_say][sutun_say] = {
  {'1', '2', '3'},
  {'4', '5', '6'},
  {'7', '8', '9'},
  {'*', '0', '#'}
};

byte pin_satir[satir_say] = {27, 28, 29, 30};
byte pin_sutun[sutun_say] = {26, 25, 24};

Keypad keypad = Keypad( makeKeymap(keys), pin_satir, pin_sutun, satir_say, sutun_say );

const String sifre = "1253";
String sifre_giris;

//Yangin alarmi
const int buzzerPin = 21;
int atesPin = 20;
int ates = LOW;

//Hareket sensoru
int led = 51;
int hareket = 50;
int test = LOW;

void sicaklik_setup()
{
  analogReference(INTERNAL1V1);
  lcd.begin(16, 2);
  lcd.setCursor(0, 0);
  lcd.print("   dijital ");
  lcd.setCursor(0, 1);
  lcd.print("  termometre ");
}
void sicaklik_loop()
{
  // sicaklik olcum
  float reading = analogRead(sensor);
  float temperature = reading * (5.0 / 1023.0) * 100;
  delay(10);

  // sicaklik gosterme
  lcd.clear();
  lcd.setCursor(0, 0);
  if (temperature > 30)
  {
    lcd.print("Sicaklik yuksek");
  }
  else if (temperature < 20)
  {
    lcd.setCursor(1, 0);
    lcd.print("Sicaklik dustu");
  }
  else
  {
    lcd.setCursor(3, 0);
    lcd.print("Sicaklik");
  }
  lcd.setCursor(4, 1);
  lcd.print(temperature);
  lcd.print((char)223);
  lcd.print("C");
  //delay(1000);
}
void kilit_setup()
{
  Serial.begin(9600);
  pinMode(22, OUTPUT);
  pinMode(23, OUTPUT);
  sifre_giris.reserve(32); // max 32
}
void kilit_loop()
{
  char key = keypad.getKey();
  if (key)
  {
    if (key == '*') // * = temizleme
    {
      sifre_giris = "";
    }
    else if (key == '#') // # = onaylama
    {
      if (sifre == sifre_giris)
      {
        digitalWrite(yesil_led, HIGH);
        delay(500);
        digitalWrite(yesil_led, LOW);
      }
      else
      {
        digitalWrite(kirmizi_led, HIGH);
        delay(500);
        digitalWrite(kirmizi_led, LOW);
      }
      sifre_giris = "";
    }
    else
    {
      sifre_giris += key;
    }
  }
}
void yangin_setup()
{
  pinMode(buzzerPin, OUTPUT);
  pinMode(atesPin, INPUT);
  Serial.begin(9600);
}
void yangin_loop()
{
  ates = digitalRead(atesPin);
  if (ates == HIGH)
  {
    digitalWrite(buzzerPin, HIGH);
  }
  else
  {
    digitalWrite(buzzerPin, LOW);
  }
}
void hareket_setup()
{
  pinMode(led, OUTPUT);
  pinMode(hareket, INPUT);
}
void hareket_loop()
{
  test = digitalRead(hareket);
  if (test == HIGH)
  {
    digitalWrite(led, HIGH);
  }
  else
  {
    digitalWrite(led, LOW);
  }
}
void setup()
{
  sicaklik_setup();
  kilit_setup();
  yangin_setup();
  hareket_setup();
  delay(500);
  lcd.clear(); //ekrani temizle
}
void loop()
{
  sicaklik_loop();
  kilit_loop();
  yangin_loop();
  hareket_loop();
}
