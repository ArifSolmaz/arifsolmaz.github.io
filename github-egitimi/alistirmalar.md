# Alıştırmalar

> 45 dakikalık derste sınıf içi alıştırma yoktur; o sürümde L1, Ö1 ve “ilk
> repo” (sunum, 33. slayt) isteyenlere önerilir. Bu sayfa 2 × 100 dakikalık
> uygulamalı sürüm içindir.

Eğitmen için süreli alıştırma listesi. Sıra ve süreler
[eğitmen rehberindeki](egitmen-rehberi.md) iki derslik planla aynıdır; öğrencinin
adım adım talimatları [katılımcı el kitabındadır](katilimci-el-kitabi.md).

| Kod | Alıştırma | Nerede? | Ne zaman? | Süre |
|---|---|---|---|---|
| N0 | Git gerekli mi? | Tartışma / örnek senaryolar | Ders 1 | 10 dk |
| R1 | Gerçek repo okuma | [Gerçek GitHub örnekleri](gercek-ornekler/) | Ders 1 ya da ödev | 10–20 dk |
| L1 | Commit ve branch | Learn Git Branching | Ders 1 | 15 dk |
| L2 | Merge | Learn Git Branching | Ders 1 | 10 dk |
| L3 | Revert (hızlılar için) | Learn Git Branching | Ders 1 | 5–10 dk |
| Ö1 | Introduction to GitHub | GitHub Skills | Ödev | ~1 saat |
| Ö2 | Push ve pull | Learn Git Branching | Ödev | 20 dk |
| A | Depoyu tanı | Takım deposu | Ders 2 | 5 dk |
| B | Profil dosyası, yeni branch | Takım deposu | Ders 2 | 10 dk |
| C | Pull request aç | Takım deposu | Ders 2 | 5 dk |
| D | Review ve merge | Takım deposu | Ders 2 | 10 dk |
| E | Çakışma çöz | Takım deposu | Ders 2 | 15 dk |
| F | Takımlar arası review | Takım depoları | Ders 2 | 10 dk |
| G | Mini takım görevi | Takım deposu | 3. ders ya da ödev | 30–45 dk |

---

## Ders 1 — Önce karar: GitHub ne için kullanılır?

### N0. Senaryo tartışması

**Amaç:** GitHub'ı “her şeyi yüklediğimiz depo” diye değil; proje hafızası,
web sitesi, portfolyo, görev takibi ve ekip çalışması aracı olarak görmek.

Sınıfa beş kısa senaryo verin ve her biri için “GitHub burada ne işe yarar,
ne işe yaramaz, neyi koymayız?” diye sorun:

1. Tek kişinin bir akşamlık hesaplama notu.
2. Dört kişilik robot projesi: Arduino kodu, devre şeması, rapor ve görev listesi.
3. İçinde kişisel veri olan ham anket dosyaları ve analiz kodu.
4. Bir öğrencinin kişisel portfolyo sitesi.
5. Okul kulübünün etkinlik web sitesi ve görev listesi.

Beklenen çıkarım:

- Birinci senaryoda Git şart olmayabilir.
- İkinci senaryoda Git ve GitHub güçlü biçimde faydalıdır.
- Üçüncü senaryoda analiz kodu Git'e girebilir; ham kişisel veri ve gizli dosyalar dikkatle ayrılmalıdır.
- Dördüncü ve beşinci senaryoda GitHub Pages, README, Issues ve proje panosu
  kod yazmayan işler için de anlamlı olabilir.

Başarı ölçütü:

- Öğrenci “GitHub burada ne işe yarar?” sorusuna sadece “repo açarız” değil,
  gerekçeli cevap verebiliyor.
- Öğrenci depoya girmemesi gereken dosya türlerine örnek verebiliyor.

### R1. Gerçek repo okuma

**Amaç:** GitHub'ın yalnızca “dosya yükleme sitesi” olmadığını, yaşayan bir proje
yönetim alanı olduğunu görmek.

Öğrenciler [Gerçek GitHub örnekleri](gercek-ornekler/) sayfasından bir repo seçer:
PX4, ArduPilot, OpenCV, ROS 2, Arduino IDE, VS Code, CPython ya da Home Assistant.

Önce beş soruya kısa cevap yazarlar:

1. README size projenin ne yaptığını 30 saniyede anlattı mı?
2. Issues sekmesinde en sık görünen etiketler ne?
3. Açık bir pull request'te hangi dosyalar değişmiş?
4. Son release notunda kullanıcıyı ilgilendiren bir değişiklik var mı?
5. Star sayısına bakmadan, bu repo sağlıklı görünüyor mu? Neden?

Sonra “bu repoyu gerçekten kullanacak olsam ne yaparım?” kararını eklerler:

- Sadece incelemek: Star ver, release notlarını ve README'yi oku.
- Denemek: Code → Download ZIP veya GitHub Desktop / `git clone` ile indir.
- Kendi projene uyarlamak: lisansı oku, kaynak göster, küçük bir örnek çalıştır.
- Katkı vermek: CONTRIBUTING dosyasını oku, fork al, branch aç, test et, pull request aç.

Başarı ölçütü:

- Öğrenci README, Issues, Pull requests ve Releases sekmelerini bulabiliyor.
- Öğrenci star sayısını tek başına kalite ölçütü sanmıyor.
- Öğrenci gerçek bir PR diff'ini okumayı denemiş oluyor.
- Öğrenci download, clone, fork ve pull request arasındaki farkı pratik bir senaryo üzerinden açıklayabiliyor.

## Ders 1 — Learn Git Branching (sınıfta, çiftler hâlinde)

Hazırlık: projeksiyonda [Türkçe sayfayı](https://learngitbranching.js.org/?locale=tr_TR)
gizli pencerede açın ve 1. seviyeyi siz yapın.

### L1. Commit ve branch

**Seviye:** Main → Introduction Sequence 1–2
**Amaç:** commit'in geçmişe nokta eklediğini, branch'in yalnızca bir etiket
olduğunu görmek

Başarı ölçütü:

- Her iki seviye tamamlandı (menüde işaretli)
- Öğrenci “`git branch` yeni bir commit oluşturdu mu?” sorusuna “hayır, sadece
  etiket” diye cevap verebiliyor

### L2. Merge

**Seviye:** Main → Introduction Sequence 3
**Amaç:** iki hattın birleşmesini görmek

Başarı ölçütü:

- Seviye tamamlandı
- Merge commit'inin neden iki ebeveyni olduğunu açıklayabiliyor
- Bunu GitHub'daki “Merge pull request” butonuyla ilişkilendirebiliyor

### L3. Revert (hızlı bitirenler)

**Seviye:** Main → Ramping Up 4 (Reversing Changes)
**Amaç:** hatalı bir commit'i geçmişi silmeden geri almak

Başarı ölçütü: `revert` ile `reset` arasındaki farkı söyleyebiliyor; ortak
branch'te `revert`'in güvenli olduğunu biliyor.

---

## Ödev

### Ö1. GitHub Skills — Introduction to GitHub

**Bağlantı:** [github.com/skills/introduction-to-github](https://github.com/skills/introduction-to-github)
**Amaç:** branch → commit → PR → merge akışını gerçek GitHub'da tek başına yapmak

Öğrenci depoyu **Public** olarak kopyalar ve bitirince depo bağlantısını gönderir.

Başarı ölçütü:

- Depo bağlantısı gönderildi
- Depoda kursun son adımına ulaşıldığı görülüyor
- Depoda birleştirilmiş en az bir pull request var

### Ö2. Learn Git Branching — push ve pull

**Seviye:** Remote → Push & Pull 1–6
**Amaç:** yerel ve uzak depo farkını, `pull` ve `push`'un ne yaptığını görmek

Başarı ölçütü: seviye menüsünün ekran görüntüsünde 1–6 işaretli.

---

## Ders 2 — takım deposu

Hazırlık: şablondan takım depolarını oluşturun, üyeleri davet edin ve
[issue şablonlarındaki](ornek-depo/issue-sablonlari.md) issue'ları açıp her üyeye
birini atayın ([eğitmen rehberi, bölüm 6](egitmen-rehberi.md)).

### A. Depoyu tanı

**Amaç:** GitHub ekranındaki temel alanları bulmak

Öğrenci şunları bulur: README, commit geçmişi, Issues, kendisine atanan issue,
Pull requests, branch menüsü.

Mini soru: “Bu depoda son değişikliği kim, ne zaman yapmış?”

### B. Profil dosyası, yeni branch

**Amaç:** dosya oluşturmak, commit sırasında yeni branch açmak

Görev: `katilimcilar/ad-soyad.md` dosyası; commit penceresinde “Create a new
branch” seçeneği.

Başarı ölçütü:

- Dosya doğru klasörde ve adlandırmada
- Değişiklik `main`'de değil, yeni branch'te
- Commit mesajı anlaşılır

### C. Pull request aç

**Amaç:** değişiklik önermek ve issue'ya bağlamak

PR açıklaması:

```md
## Ne değişti?

Closes #<issue numarası>

## Kontrol
- [ ] Dosya adı doğru mu?
- [ ] İçerik anlaşılır mı?
```

Başarı ölçütü: PR açık, açıklama boş değil, `Closes #` ile issue bağlı.

### D. Review ve merge

**Amaç:** başkasının değişikliğini inceleme alışkanlığı

Her öğrenci bir takım arkadaşının PR'ında **Files changed**'e bakar, en az bir
satıra yorum bırakır ve Approve / Request changes seçer. İnceleyici rolündeki
öğrenci onaylanan PR'ları birleştirir ve branch'i siler.

Başarı ölçütü:

- Yorum kibar, somut, satıra bağlı ve gerekçeli
- PR birleşince bağlı issue kendiliğinden kapandı

### E. Çakışma çöz

**Amaç:** merge conflict korkusunu azaltmak

`cakisma-alani.md`'deki şu satırı takımın dört üyesi de kendi önerisiyle
değiştirir ve PR açar:

```md
Atölyeden sonra GitHub’ı şu iş için kullanabiliriz: ...
```

İlk PR birleşince diğer üçünde çakışma çıkar. Takım **Resolve conflicts**
ekranında birlikte karar verir.

Başarı ölçütü:

- Çakışma ekranı görüldü
- İşaret satırları silinip temiz metin bırakıldı
- Çözüm commit edildi ve PR birleştirildi

### F. Takımlar arası review

**Amaç:** tanımadığı bir değişikliği okumak

Eşleşme: takım 1 → 2, 2 → 3 … 11 → 1. Her takım diğer takımın açık bir PR'ına en
az bir yorum bırakır.

---

## G. Mini takım görevi (3. ders ya da ödev)

**Amaç:** gerçek iş akışını baştan sona canlandırmak

Takım içinde roller dönüşümlüdür:

- Biri issue açar ve işi tarif eder
- Biri değişikliği yapar ve `Closes #` ile PR açar
- Biri review yapar ve merge eder

Örnek görevler:

- README'ye pin tablosu ekle (Markdown tablosu)
- README'ye kısa bir Git sözlüğü ekle
- `proje-notlari.md`'deki kaynak listesine bağlantılar ekle
- Bir yazım hatasını düzelt

Başarı ölçütü: her takım üyesinin en az bir birleştirilmiş PR'ı ve en az bir
review yorumu var.
