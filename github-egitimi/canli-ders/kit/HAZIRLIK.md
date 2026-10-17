# GitHub Ne İşime Yarar? · Ders kiti

45 dakikalık, başlangıç seviyesinde ders. Terminal, branch ya da pull request yok; her şey tarayıcıda ve telefonda.

## Kitte ne var?

- `ornek-proje/`: canlı gösterimde GitHub'a yükleyeceğiniz örnek proje (README, Arduino kodu, devre şeması, rapor, görsel)
- `example-project/`: aynı projenin İngilizcesi
- `qr-sinif-sayfasi.png`: sınıf sayfasının QR kodu → github.com/arifsolmaz/sinif-duvari/issues/1
- Animasyonlar ayrı zip dosyalarında: GIF (slaytlar için) ve MP4

## Dersten önce (5 dakika)

1. **Sınıf sayfası için depo:** github.com/new → ad: `sinif-duvari` → Public → Create repository. Bu depo daha önceden varsa onu kullanın.
2. **Sınıf sayfası:** Issues → New issue → aşağıdaki başlığı ve metni yapıştırın → Create. Sağdaki menüden **Pin issue** ile sabitleyebilirsiniz.
3. **QR kontrolü:** Issue'nun numarasına bakın. #1 ise slayttaki QR doğru. Değilse yeni bir QR yapın: Chrome'da issue sayfasındayken sayfaya sağ tıklayın → "Bu sayfa için QR kodu oluştur" (İngilizce Chrome'da: "Create QR Code for this page") ve slayttaki QR yerine onu gösterin.
4. **Örnek proje:** `ornek-proje` klasörünü masaüstüne koyun. `robot.ino` içinde `ESIK = 500` yazdığını kontrol edin; zaman makinesi gösteriminde bunu 900 yapacaksınız.
5. **Arduino IDE** açık olsun (hazır kod gösterimi için).
6. **Telefonla bir deneme:** QR'ı okutun; sayfa açılıyor mu, yorum yazılabiliyor mu? Deneme yorumunuzu silebilir ya da örnek olarak bırakabilirsiniz.
7. **Öğrencilere mesaj:** Dersten bir iki gün önce aşağıdaki mesajı gönderin.

## Sınıf sayfası: issue metni

**Başlık:** Sınıfımızın depoları

**Metin:**

```
İlk deponu aç ve linkini aşağıya yorum olarak yaz.

1. github.com/new → ad: ilk-projem → Add README: On → Create repository
2. README'deki kaleme dokun → kendini 2 satırda yaz → Commit changes
3. Bu sayfaya dön → deponun linkini yorum olarak yaz → Comment

Örnek yorum: github.com/kullanici-adin/ilk-projem
```

## Canlı gösterimler

Ayrıntılar slaytların konuşmacı notlarında.

| Slayt | Ne yapılacak? |
|---|---|
| Fayda 1 · Projen kaybolmaz | Telefonda kendi GitHub profilinizi gösterin. |
| Projeni GitHub'a koy | github.com/new → `ornek-proje` → Add README: On → Create repository → Add file → Upload files → klasördeki dosyaları sürükleyin → Commit changes |
| Fayda 2 · Zaman makinesi | `robot.ino` → kalem → `ESIK = 500` → `900` → Commit changes → History → kayda tıklayın |
| Fayda 3 · Takımın listesi | Issues → New issue → "Robotun fotoğrafını çek" → Assignees: siz → Create → Close issue |
| Fayda 4 · Hazır kod | "DHT sensor library" arayın → adafruit/DHT-sensor-library → Code → Download ZIP → Arduino IDE: Eskiz → Kütüphane Ekle → .ZIP Kütüphanesi Ekle... |
| Fayda 5 · Portfolyo | github.com/arifsolmaz → sabitlenmiş depolar → iyi bir README |
| Fayda 6 · Öğrenciye ücretsiz | education.github.com/pack |

## Öğrencilere mesajlar

**Dersten bir iki gün önce:**

> Merhaba! [Gün] dersinde GitHub'ı kullanacağız. Lütfen derse gelmeden github.com/signup adresinden ücretsiz bir hesap açın; iki üç dakika sürüyor ve e-postanıza gelen kodu girmeniz gerekiyor. Kullanıcı adınızı kolay hatırlanır seçin; ileride CV'nizde de kullanacaksınız. Derse telefonunuzu şarjlı getirin.

**Dersten sonra:**

> Bugünün slaytları ve animasyonları: [link]. Bu haftanın görevi: bir projenizi GitHub'a koyun (kod, şema, bir fotoğraf ve README) ve linkini sınıf sayfasına yorum olarak yazın: github.com/arifsolmaz/sinif-duvari/issues/1. Öğrenci paketi için: education.github.com/pack

## Bir şey ters giderse

- **İnternet yok:** Animasyonlar her adımı gösteriyor; GIF ve MP4 dosyaları internetsiz de oynar.
- **Öğrencinin hesabı yok:** Yanındakiyle eşleşsin; görevi evde yapar.
- **Kalem bulunamıyor:** README kutusunun sağ üst köşesinde; olmazsa README.md dosyasına dokunup oradaki kalem.
- **"already exists" uyarısı:** Başka bir ad: `ilk-projem-2`.

## Gizlilik

Sınıf sayfası herkese açık bir depoda. Öğrenciler yoruma yalnızca depo linkini yazsın; telefon ya da öğrenci numarası gibi bilgileri paylaşmasınlar.
