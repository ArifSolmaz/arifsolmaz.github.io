# Hazır araçlar: Learn Git Branching, GitHub Skills ve repo keşfi

Kavramları denemek için kendi aracımızı yazmak yerine, milyonlarca kişinin
kullandığı iki ücretsiz araçla çalışıyoruz. İkisi de birbirini tamamlar:

Bu araçlar dersin kendisi değildir. Önce Git'in neden gerekli olabileceği ve iyi
çalışma alışkanlıkları konuşulur; araçlar bu fikirleri görünür ve denenebilir
hale getirir.

| | Learn Git Branching | GitHub Skills |
|---|---|---|
| Ne? | Branch ve commit'leri canlı bir ağaç olarak çizen Git oyunu | Kendi GitHub hesabınızda, bir botun adım adım yönlendirdiği gerçek kurslar |
| Nerede çalışır? | Tarayıcıda, hesap gerekmez | Gerçek GitHub'da, hesap gerekir |
| Ne öğretir? | Commit, branch, merge, revert, push/pull'un **Git tarafında** ne yaptığını | Branch, commit, pull request, review, conflict'in **GitHub arayüzünde** nasıl yapıldığını |
| Dil | Türkçe arayüz | İngilizce |
| Süre | Her seviye 3–10 dakika | Her kurs 30–60 dakika |
| Ne zaman? | Ders 1 ve ödev | Ders 1 ödevi, Ders 2 ve sonrası |

## 1. Learn Git Branching

**[Türkçe olarak aç →](https://learngitbranching.js.org/?locale=tr_TR)**

Sol tarafa `git commit`, `git branch` gibi komutlar yazılır, sağda commit ağacı
anında değişir. Her seviyede bir hedef ağaç vardır; öğrenci kendi ağacını ona
benzetmeye çalışır. Yanlış yapmak bedavadır: `reset` ile seviye baştan başlar,
`undo` son adımı geri alır.

> Komut yazmak gerekir ama ezberlemek gerekmez: her seviye önce ne
> yazılacağını gösteren kısa bir anlatımla başlar.

### Bu ders için seviyeler

Açılan sayfada **Seviyeler** menüsünden (ya da sola `levels` yazarak) seçilir.
Parantez içindeki adlar seviyelerin İngilizce adlarıdır.

| Sekme ve dizi | Seviye | Konu | Sunumdaki slayt |
|---|---|---|---|
| Main → Giriş (Introduction Sequence) | 1 | Commit | 12 Günlük döngü |
| | 2 | Branch | 17 Branch ve pull request |
| | 3 | Merge | 17, 20 |
| Main → Hızlanma (Ramping Up) | 4 | Değişiklikleri geri almak (Reversing Changes): `reset` ve `revert` | 23 Sık hatalar |
| Remote → Push & Pull | 1–2 | Clone, uzak branch'ler | 12 |
| | 4 | Pull | 23 |
| | 5–6 | Takım çalışması taklidi (Fake Teamwork), Push | 23 Reddedilen push |
| | 7 | Ayrışmış geçmiş (diverged history) | 23 |

Giriş dizisinin 4. seviyesi (rebase) ve Hızlanma dizisinin ilk üç seviyesi bu ders
için gerekli değildir; meraklılar yapabilir.

### Sınıfta nasıl kullanılır?

- Projeksiyonda 1. seviyeyi siz yapın: `git commit` yazın, ağacın nasıl uzadığını
  gösterin. Sonra öğrenciler devam etsin.
- İlerleme tarayıcıda saklanır; tamamlanan seviyeler menüde işaretlenir. Ortak
  bilgisayarlarda gizli pencere kullanılabilir.
- Sunucu yükü yoktur; 45 kişi aynı anda kullanabilir.

## 2. GitHub Skills

Her kurs, öğrencinin kendi hesabına kopyalanan gerçek bir depodur. Öğrenci bir
adımı yapınca (örneğin branch açınca) GitHub Actions ile çalışan bir bot bunu
kontrol eder ve sonraki adımın talimatını yazar. Hepsi ücretsizdir.

### Önerilen sıra

| Kurs | Süre | Ne yapılır? | Ne zaman? |
|---|---|---|---|
| [Introduction to GitHub](https://github.com/skills/introduction-to-github) | < 1 saat | Branch, commit, pull request, merge; sonunda profil README'si | Ders 1 ödevi |
| [Communicate using Markdown](https://github.com/skills/communicate-using-markdown) | < 1 saat | Başlık, görsel, kod bloğu, görev listesi | Ders 1 ödevi (isteğe bağlı) |
| [Review pull requests](https://github.com/skills/review-pull-requests) | < 30 dk | Review isteme, yorum, değişiklik önerme, onaylama | Ders 2 |
| [Resolve merge conflicts](https://github.com/skills/resolve-merge-conflicts) | < 30 dk | Çakışmanın nedeni ve GitHub web düzenleyicisinde çözümü | Ders 2 |

### Öğrenci için adımlar

1. GitHub'a giriş yapın ve kursun sayfasını açın.
2. **Copy Exercise** (alıştırmayı kopyala) butonuna basın.
3. Depoyu **Public** (herkese açık) olarak oluşturun. Private depolarda GitHub
   Actions dakikaları harcanır; public depolarda ücretsizdir.
4. Yaklaşık 20 saniye bekleyip sayfayı yenileyin; ilk adımın talimatı çıkar.
5. Talimatları izleyin. Bir adımı bitirdikten sonra bot birkaç saniye içinde
   sonraki adımı yazar; çıkmazsa sayfayı yenileyin ve **Actions** sekmesinde işin
   bitmesini bekleyin.

### Sınıfta nasıl kullanılır?

- **Takip kolaydır:** her öğrencinin kendi depo bağlantısı vardır. Bağlantıları
  bir forma ya da LMS'e topladığınızda, depolara bakarak kimin hangi adımda
  olduğunu görürsünüz.
- Kurslar İngilizcedir; ilk dersten önce sunumun 31. slaytındaki Hello World
  akışını Türkçe anlatmak, öğrencinin talimatları anlamasını kolaylaştırır.
- 45 öğrenci aynı anda başlayabilir: her depo kendi bot işini çalıştırır.
- Hesap açmayı dersten önce ödev verin (bkz. [eğitmen rehberi](egitmen-rehberi.md)).

## 3. Hangisi ne zaman?

```text
Sunum (kavram)  →  Learn Git Branching (Git'te ne oluyor?)  →  GitHub Skills (GitHub'da nasıl yapılır?)  →  Takım deposu (gerçek iş birliği)
```

- **45 dakikalık ders:** yalnızca sunum. Learn Git Branching Giriş 1–3 ve
  Introduction to GitHub kursu dersten sonra isteyenler içindir (sunum, 36. slayt).
  Aynı slayttaki gerçek repo turu için [Gerçek GitHub örnekleri](gercek-ornekler/)
  sayfasını kullanın; popüler depolar, GitHub Trending ve Hacker News arama
  bağlantıları orada hazırdır.

Uygulamalı (2 × 100 dk) sürümde:

- **Ders 1:** Sunum 1–14 → Learn Git Branching Giriş 1–3 (sınıfta, çiftler hâlinde).
- **Ödev:** Introduction to GitHub kursu + Learn Git Branching Remote 1–6.
- **Ders 2:** Sunum 15–37 → Review pull requests ve Resolve merge conflicts →
  takım depolarında uygulama.
