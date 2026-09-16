# Katılımcı el kitabı

Bu notlar, atölye sırasında adım adım takip etmek içindir. Komut satırı bilmeniz
gerekmiyor.

## GitHub’da ne yapacağız?

Bugün şunları öğreneceksiniz:

- Bir projedeki dosyaları bulmak
- Bir dosyayı düzenlemek
- Değişikliğinizi kaydetmek
- Kendi çalışma alanınızda branch açmak
- Pull request ile değişiklik önermek
- Başkasının değişikliğini incelemek
- Küçük bir çakışmayı çözmek

## Temel kavramlar

| Kavram | Kısa anlamı |
|---|---|
| Repository / Depo | Projenin ortak klasörü |
| Commit | Kaydedilmiş değişiklik noktası |
| Branch | Ana işi bozmadan çalışılan ayrı alan |
| Pull request | Değişikliği ekibe gösterme ve onay isteme |
| Merge | Onaylanan değişikliği ana çalışmaya alma |
| Issue | Yapılacak iş, soru veya hata kaydı |

## Alıştırma 1 — depoyu tanı

1. Eğitim deposunu açın.
2. `README.md` dosyasını bulun.
3. `Issues` sekmesini açın.
4. Size atanmış issue’yu bulun.
5. Issue’daki görevi okuyun.

## Alıştırma 2 — kendi dosyanı ekle

1. Depoda `katilimcilar/` klasörünü açın.
2. **Add file → Create new file** seçin.
3. Dosya adını kendi adınızla yazın:

```text
katilimcilar/ad-soyad.md
```

4. İçeriği şu şablonla doldurun:

```md
# Ad Soyad

- İlgi alanım:
- GitHub’dan beklentim:
- Bugün öğrendiğim ilk kavram:
```

5. Sayfanın altında commit mesajı yazın:

```text
Profil dosyamı ekle
```

6. Ana branch yerine yeni branch oluşturmayı seçin.
7. Değişikliği kaydedin.

## Alıştırma 3 — pull request aç

1. GitHub sizi pull request açmaya yönlendirirse **Compare & pull request** seçin.
2. Başlığa kısa bir açıklama yazın:

```text
Ad Soyad profilini ekle
```

3. Açıklamaya şunu yazın:

```md
## Ne değişti?
Katilimcilar klasörüne kendi profil dosyamı ekledim.

## Kontrol
- [ ] Dosya adı doğru mu?
- [ ] İçerik anlaşılır mı?
```

4. **Create pull request** düğmesine basın.

## Alıştırma 4 — bir arkadaşının pull request’ini incele

1. `Pull requests` sekmesini açın.
2. Size verilen PR’ı seçin.
3. `Files changed` sekmesine geçin.
4. Bir satıra yorum bırakın.
5. Uygunsa approve edin.

Yorum örnekleri:

```text
Dosya adı ve içerik iyi görünüyor.
```

```text
Bu cümleyi biraz daha açık yazabilir misin?
```

```text
Buraya ilgi alanını da eklemek ister misin?
```

## Alıştırma 5 — çakışma çöz

Eğitmeniniz yönlendirdiğinde `cakisma-alani.md` dosyasında aynı satırı
düzenleyeceksiniz. Çakışma oluşursa GitHub size iki değişikliği gösterir.

Yapmanız gereken:

1. Hangi metnin kalacağına karar verin.
2. Gereksiz işaretleri silin.
3. Dosyanın son halini okuyun.
4. Çözümü commit edin.

Çakışma bir hata değildir; aynı yere gelen iki iyi niyetli değişikliğin
birleştirilmesi gerekir.

## Dersten sonra yapabilecekleriniz

- Kendi notlarınız için küçük bir depo açın.
- Bir arkadaşınızla deneme pull request’i yapın.
- Bir kurum belgesindeki değişiklikleri issue ve PR ile takip etmeyi deneyin.
- GitHub Desktop kurup aynı akışı bilgisayarınızdan yapın.

