# Eğitmen rehberi

Bu rehber, paketin tamamını bir sınıfta nasıl kullanacağınızı anlatır: tarayıcıda
çalışan **sunum**, hesap gerektirmeyen **Git oyun alanı** ve gerçek GitHub'da
yapılan **uygulama**. 40–45 kişilik bir mekatronik sınıfı düşünülerek yazıldı;
daha küçük gruplarda süreleri kısaltmanız yeterli.

> Kısa yol: Ders 1'de sunumun 1–14. slaytları + oyun alanının 1–5. görevleri;
> Ders 2'de 15–37. slaytlar + oyun alanının 6–13. görevleri + gerçek GitHub'da
> takım uygulaması. Ayrıntılar aşağıda.

## 1. Paketin parçaları

| Parça | Bağlantı | Ne için? | Kim kullanır? |
|---|---|---|---|
| Sunum (TR) | [sunum/](sunum/) | 37 slaytlık ders anlatımı | Eğitmen projeksiyonda; öğrenci evde tekrar |
| Sunum (EN) | [sunum/en/](sunum/en/) | Aynı sunumun İngilizcesi | İngilizce ders / değişim öğrencileri |
| Git oyun alanı (TR) | [oyun-alani/](oyun-alani/) | Hesapsız, risksiz Git simülatörü; 13 görev | Her öğrenci kendi tarayıcısında |
| Git oyun alanı (EN) | [oyun-alani/en/](oyun-alani/en/) | Oyun alanının İngilizcesi | — |
| Örnek eğitim deposu | [ornek-depo/](ornek-depo/) | Gerçek GitHub uygulaması için başlangıç dosyaları | Takımlar |
| Katılımcı el kitabı | [katilimci-el-kitabi.md](katilimci-el-kitabi.md) | Gerçek GitHub'da adım adım alıştırmalar | Öğrenci |
| Alıştırmalar | [alistirmalar.md](alistirmalar.md) | Süreli sınıf içi görevler | Eğitmen |
| Değerlendirme listesi | [degerlendirme-listesi.md](degerlendirme-listesi.md) | Kazanım kontrolü ve çıkış soruları | Eğitmen |

Üç katman birbirini tamamlar:

1. **Sunum** kavramı anlatır (commit nedir, branch neden var).
2. **Oyun alanı** kavramı güvenle denetir: öğrenci butona basar ve dosyaya, commit
   geçmişine ve robota etkisini anında görür. Yanlış yapmak bedavadır.
3. **Gerçek GitHub** aynı akışı gerçek arayüzde ve gerçek bir takımla tekrarlatır.

Her kavram için sıra aynıdır: **anlat → oyun alanında dene → GitHub'da yap**.

## 2. Önerilen ders planı (2 × 100 dakika)

Bütün içerik tek derse sığmaz; iki derse bölün. Aradaki haftada öğrenciler oyun
alanını bitirir ve hesaplarını hazırlar.

### Ders 1 — Tek başına: commit, push, branch

| Dakika | Ne yapılır | Slayt | Oyun alanı |
|---|---|---|---|
| 0–10 | Sorun: `son_GERCEKTEN.ino` klasörü; GitHub nedir | 1–5 | — |
| 10–20 | Terimler, yaşam döngüsü | 6–7 | — |
| 20–35 | Kurulum (yalnızca hesap), repo yapısı, Markdown | 8–11 | — |
| 35–45 | Günlük döngü ve commit mesajları | 12–13 | Projeksiyonda görev 1–3'ü siz yapın |
| 45–70 | **Oyun alanı, çiftler hâlinde** | — | Görev 1–5 |
| 70–80 | Kontrol noktası: “GitHub etiketi neden kımıldamadı?” | — | Görev 2–3 tartışması |
| 80–90 | `.gitignore` ve şifreler | 14 | Görev 9 (isteğe bağlı) |
| 90–100 | Çıkış soruları, ödev | — | — |

**Ödev (Ders 2'ye kadar):** oyun alanında 13 görevi bitirip tamamlama kartının
ekran görüntüsünü gönderin; GitHub hesabını açın ve e-postayı doğrulayın;
GitHub Education'a başvurun (isteğe bağlı).

### Ders 2 — Takımla: issue, pull request, review, conflict, yapay zekâ

| Dakika | Ne yapılır | Slayt | Oyun alanı / GitHub |
|---|---|---|---|
| 0–10 | Ödevdeki takılmalar; 3–4 kartı projeksiyonda gösterin | — | Kartlar |
| 10–30 | Issue, branch, diff, review, conflict | 15–20 | Görev 6–8 ve 11 projeksiyonda |
| 30–40 | Pano, milestone, sık hatalar | 21–23 | Görev 12 |
| 40–55 | Yapay zekâ ajanları | 24–28 | Canlı demo (sizin hesabınızla) |
| 55–60 | Hızlı test | 30 | — |
| 60–65 | Hello World akışı ve nereye tıklanır | 31–32 | — |
| 65–95 | **Gerçek GitHub'da takım uygulaması** | 33–34 | Bölüm 6 |
| 95–100 | Komut özeti, kaynaklar, kapanış | 35–37 | — |

### Tek ders zorunluysa (120 dakika)

Slayt 1–7 (15 dk) → oyun alanı görev 1–8 (35 dk) → slayt 15–20 (15 dk) →
Hello World uygulaması, **bireysel** (35 dk) → slayt 33–37 (10 dk) → çıkış
(10 dk). 3. bölümü (yapay zekâ) ve takım çalışmasını ikinci bir derse bırakın.

## 3. Dersten önce: kontrol listesi

**Bir hafta önce**

- [ ] Öğrencilere hazırlık mesajını gönderin (aşağıda).
- [ ] Laboratuvar bilgisayarlarında güncel bir tarayıcı (Chrome, Edge, Firefox)
      olduğunu ve `arifsolmaz.github.io` ile `github.com`'un açıldığını kontrol edin.
- [ ] Takım depolarını hazırlayın (Bölüm 6).
- [ ] Sunumdaki boş alanları doldurun (Bölüm 4.3).

**Ders günü, 15 dakika önce**

- [ ] Projeksiyonda sunumu `F` ile tam ekran açın; ikinci sekmede oyun alanı,
      üçüncüde kendi demo deponuz.
- [ ] Oyun alanında **Baştan başla**'ya basın ki gösterim temiz başlasın.
- [ ] Sınıf Wi-Fi'ı ve projeksiyon çözünürlüğü (sunum 16:9 ölçeklenir).

**Öğrencilere hazırlık mesajı**

```text
Merhaba, [tarih] dersinde GitHub'a başlıyoruz. Lütfen derse gelmeden:
1. github.com'da ücretsiz bir hesap açın (üniversite e-postanızla) ve
   e-postanızı doğrulayın. Kullanıcı adını CV'nize yazabileceğiniz biçimde seçin.
2. Şu sayfayı açıp çalıştığını kontrol edin:
   https://arifsolmaz.github.io/github-egitimi/oyun-alani/
Programlama ya da kurulum gerekmiyor; dizüstü bilgisayarınızı getirin.
```

Hesapları dersten önce açtırmanın nedeni: 40 kişi aynı anda, aynı ağdan kayıt
olduğunda doğrulama e-postaları gecikebilir ve ek doğrulama adımları çıkabilir.
Ders süresinin ilk 20 dakikası buna gider.

## 4. Sunumu kullanmak

### 4.1 Kısayollar

| Tuş | İşlev |
|---|---|
| `→` `Space` `PageDown` | Sonraki slayt |
| `←` `PageUp` | Önceki slayt |
| `Home` / `End` | İlk / son slayt |
| `N` | Slaytın sade açıklaması (öğrenciye yönelik) |
| `O` | Tüm slaytlar; tıklayıp atlayın |
| `F` | Tam ekran |
| `P` | Yazdır; “PDF olarak kaydet” ile her slayt bir sayfa olur |

Her slaytın kendi adresi vardır (`sunum/#18` gibi); öğrencilere doğrudan ilgili
slaytı gönderebilirsiniz. TR/EN butonu aynı slaytta dil değiştirir. Telefonda
kaydırarak gezilir.

### 4.2 Açıklamalar öğrenci için yazıldı

`N` ile açılan metinler **öğrenciye** yöneliktir: her terimi ilk geçtiği yerde
açıklar, “siz” diye hitap eder. Projeksiyonda açık bırakırsanız sınıf da okur;
evde tekrar eden öğrenci için asıl destek budur. Sizin için ipuçları aşağıdaki
4.4 bölümündedir.

### 4.3 Derse girmeden doldurmanız gereken yerler

- **Slayt 1:** Tarih web sürümünden kaldırıldı; claude.ai'deki slayt destesinde
  `[Tarih]` hâlâ duruyor.
- **Slayt 22 (milestone):** 3., 6., 10., 14. haftalar örnektir; kendi teslim
  tarihlerinizi yazın.
- **Slayt 28 (yapay zekâ kuralları):** “Ders politikası” kartı boş. Örnek:
  “Projelerde, PR'da belirtilmek şartıyla serbest; sınavlarda yasak.”
- **Slayt 32 (nereye tıklanır):** Dört ekran görüntüsü çerçevesi boş. Kendi
  hesabınızdan alın ki GitHub'ın güncel arayüzüyle eşleşsin; ya da bu adımları
  canlı gösterin.

### 4.4 Slayt slayt eğitmen notları

| Slayt | Eğitmen için |
|---|---|
| 1 Kapak | Hedefi söyleyin: ders sonunda herkesin hesabı, reposu ve birleştirilmiş bir PR'ı olacak. |
| 2 Plan | Öğrenme çıktılarını başta okuyun, kapanışta dönün. |
| 3 Sorun | “Bilgisayarında böyle bir klasör olan?” diye sorun; eller kalkar. Dosya adıyla sürüm tutmak elle yapılan bir sürüm kontrolüdür. |
| 4 GitHub nedir | GitHub'ın yalnızca yazılım şirketleri için olmadığını vurgulayın; bizim için “yazılım” firmware, kontrol kodu, simülasyon ve doküman demek. |
| 5 Git ve GitHub | En sık karışan konu. GitLab ve Bitbucket da Git kullanır. |
| 6 Terimler | Ezberletmeyin; deftere yazdırın. Commit, branch, push gibi terimler sektörde İngilizce kullanılır. |
| 7 Yaşam döngüsü | Bu derste ilk üç aşama: planla, oluştur, incele. Actions sonraki konu. |
| 9 Kurulum | Hesap açmayı ödev verin. Ders tamamen tarayıcıda yürür; Git kurmak gerekmez. |
| 10 Repo yapısı | Repo oluştururken “Add a README” ve bir `.gitignore` şablonu (C++/Python) seçtirin. |
| 11 Markdown | Uygulamada README düzenleyecekler. GitHub'da **Preview** sekmesini gösterin. |
| 12 Günlük döngü | Komutlar yalnızca tanısınlar diye; bugün tarayıcıdayız. Burada oyun alanına geçin. |
| 13 Commit mesajı | “Kp 2.0'dan 1.4'e düşürüldü” mesajı, robot salınım yaparsa neyi geri alacağınızı söyler. |
| 14 `.gitignore` | ESP32 kodunda ev Wi-Fi şifresi klasik hatadır. `secrets_example.h` boş değerlerle commit edilir. Oyun alanı görev 9. |
| 16 Issue | WhatsApp grubunun yerini alır. “Closes #12” yazılan PR birleşince issue kapanır. |
| 17 Branch ve PR | Kural: `main` her zaman robotta çalışan sürüm. |
| 18 Diff | “Files changed”da bir satıra gelip `+` ile satıra yorum bırakmayı gösterin. |
| 19 Review | Comment / Approve / Request changes. Çiftleri eşleştirip birbirlerinin PR'ını inceletin. |
| 20 Conflict | HEAD = sizin branch'iniz, `=======` altı = gelen. İşaretler silinmezse kod derlenmez; oyun alanında robot da “derlenmiyor” der. |
| 21 Pano | Haftalık toplantıda “kim ne yaptı?” yerine panoyu açın. Donanım işleri de panoya. |
| 22 Milestone | Haftaları kendi izlencenize göre değiştirin. Katkı grafiği bireysel katkıyı görünür kılar. |
| 23 Sık hatalar | `revert` geçmişi silmez; `--amend` yalnızca push edilmemiş son commit için. Oyun alanı görev 10 ve 12. |
| 25 Claude Code / Codex | İkisi de ücretli plan ya da API kredisi ister. Windows'ta Claude Code PowerShell'de `irm https://claude.ai/install.ps1 \| iex` ile kurulur. Güncel komutlar için dokümanlara bakın. |
| 26 Güvenli ajan akışı | Ajana Türkçe de yazılabilir. 5. adım (donanımda test) pazarlık konusu değil. |
| 27 GitHub içinde ajanlar | Soldaki konuşma örnektir. `@claude` için repoda `/install-github-app` ile kurulum ve yazma yetkisi gerekir. Bir demo reposunda bir kez kurun. |
| 28 Kurallar | Ders politikanızı doldurun. Ajanların commit'leri çoğu zaman `Co-authored-by` satırı taşır. |
| 30 Test | Cevaplar: 1) Git geçmişi tutan program, GitHub onu barındıran site; 2) commit yerel, push GitHub'a; 3) `main` hep çalışmalı, denemeler branch'te; 4) PR birleşince issue #7 kapanır. Kahoot/Mentimeter'a da aktarılabilir. |
| 31 Hello World | GitHub Docs'taki resmî alıştırma. Adlar `hello-world` ve `readme-edits`. |
| 32 Nereye tıklanır | Altı uygulama adımını önce yavaşça canlı yapın, her tıklamayı söyleyin. Yeni başlayanlar için en önemli slayt. |
| 33 Uygulama | Takılmalar: doğrulama e-postası, branch'e geçmeden düzenlemek. Hızlılar için ek: README'ye fotoğraf, etiketli ikinci issue. |
| 34 Merge sonrası | Ödev önerisi: profil README'si. |
| 35 Komut özeti | PDF olarak verin ya da laboratuvar masalarına koyun. |

## 5. Git oyun alanı ile 40–45 kişilik sınıf

### 5.1 Nasıl çalışıyor?

- **Sunucu yok.** Sayfa bir kez yüklenir; bütün simülasyon öğrencinin kendi
  tarayıcısında çalışır. 45 kişi aynı anda açsa da kimse diğerini yavaşlatmaz;
  GitHub Pages yalnızca küçük bir dosya (yaklaşık 60 KB) gönderir.
- **Herkesin kendi dünyası var.** Bir öğrencinin yaptığı commit başkasının
  ekranında görünmez. “Takım arkadaşın push etsin” butonu ortak çalışmayı
  simüle eder; gerçek ortak çalışma Bölüm 6'daki gerçek GitHub uygulamasındadır.
- **Gerçek GitHub'a dokunmaz.** Hesap, giriş, internet üzerinden yazma yok.
  “Push”, “Pull request” ve “Merge” aynı sayfadaki sahte bir GitHub'a gider.
- **İlerleme o tarayıcıda saklanır.** Sekme kapanıp açılınca kaldığı yerden
  devam eder. Gizli pencerede, tarayıcı kapanınca silinir. Başka bir bilgisayara
  taşınmaz.
- **İnternet kesilirse:** Sayfa yüklendikten sonra internetsiz çalışır (yazı tipi
  yalnızca daha sade görünür).

### 5.2 Sınıfı düzenlemek

- **Çiftler hâlinde çalıştırın** (yaklaşık 22 çift). Biri klavyede (sürücü),
  diğeri görev metnini okur ve “Gözle” kısmını kontrol eder (yönlendirici).
  Her 4–5 görevde rol değiştirsinler. 45 ayrı ekrandan daha az soru gelir ve
  öğrenciler kavramı birbirine anlatır.
- **Dizüstü ya da laboratuvar bilgisayarı kullanın.** Telefonda çalışır ama
  dosya, grafik ve robot alt alta dizildiği için çok kaydırma gerekir.
- **Ortak laboratuvar bilgisayarlarında:** her grup çıkarken **Baştan başla**'ya
  bassın; yoksa sonraki öğrenci önceki ilerlemeyi görür.
- **Asistan ya da gönüllü öğrenci:** 40+ kişide bir yardımcı çok fark eder.
  Oyun alanını önceden bitirmiş 3–4 öğrenciyi “yardımcı” yapın.

### 5.3 Senkron ilerlemek: kontrol noktaları

Herkes kendi hızında ilerler ama sınıfı üç noktada durdurun ve projeksiyonda
birlikte bakın:

| Kontrol noktası | Görevler | Sınıfa sorun |
|---|---|---|
| A | 1–3 | “Commit ettiniz ama GitHub etiketi neden kımıldamadı? Robot neden değişmedi?” |
| B | 4–8 | “Branch'te README'yi değiştirdiniz; main'e geçince neden yoktu? Merge'den sonra neden Pull yapmanız gerekti?” |
| C | 9–13 | “Revert neden geçmişi silmiyor? Çakışmada kararı kim verdi?” |

Hızlı bitirenlere: `.gitignore`'dan `secrets.h` satırını silip commit etmeyi ve
ne olduğunu gözlemlemeyi önerin (sayfa uyarı verir), ya da yavaş bir çifte
yardımcı olmalarını isteyin.

### 5.4 Takip ve değerlendirme

Sayfanın sunucusu olmadığı için eğitmen paneli yoktur. Bunun yerine:

- Görevler panelinin altındaki **Tamamlama kartı**: öğrenci adını yazar; kart adı,
  kaç görevin bittiğini, saati ve 1–13 arası kutuları gösterir.
- Ödev olarak kartın ekran görüntüsünü LMS'e ya da bir forma yüklettirin.
- Sınıfta “Kartında kaç yeşil kutu var?” diye el kaldırtmak hızlı bir yoklamadır.

Kart bir sınav aracı değildir (aynı tarayıcıda başkası da bitirebilir). Asıl
ölçüm, gerçek GitHub'daki PR'lar ve review yorumlarıdır (Bölüm 8).

### 5.5 Görevlerde sık takılmalar

| Görev | Takılma | Çözüm |
|---|---|---|
| 2 Commit | Mesaj yazmadan Commit'e basıyor | Sayfa mesaj ister; “ne değişti?” diye sorun. |
| 5 Güvende | Değişikliği commit etmeden main'e geçmeye çalışıyor | Sayfa izin vermez; önce commit. Gerçek Git'te de benzer bir uyarı çıkar. |
| 6 PR | Branch listesi boş | Branch push edilmemiş. PR, GitHub'daki branch'ten açılır. |
| 7 Merge | Issue kapanmadı | PR açıklamasında `Closes #1` yok; yeni PR'da yazsın. |
| 10 Revert | Robot hâlâ bozuk | Revert yerel; Push'a basmadı. Bu görevin asıl dersi bu. |
| 11 Conflict | Merge'e basınca çakışma çıkmadı | İki tarafta da aynı Kp satırı değişmeli **ve** ikisi de push edilmeli. |
| 12 Reddedilen push | Pull da reddedildi | Önce yerel değişiklikler commit edilmeli. |

### 5.6 Oyun alanı ve sunum eşleşmesi

| Görev | Slayt |
|---|---|
| 1–3 Değiştir, commit, push | 12 Günlük döngü, 13 Commit mesajları |
| 4–5 Branch | 17 Branch ve pull request |
| 6–7 PR, review, merge | 16 Issue, 18 Diff, 19 Review |
| 8 Pull | 23 Sık hatalar |
| 9 `.gitignore` | 14 Repoya girmemesi gerekenler |
| 10 Revert | 23 Sık hatalar |
| 11 Conflict | 20 Merge conflict |
| 12 Reddedilen push | 23 Sık hatalar |
| 13 Branch silme | 34 Merge sonrası |

## 6. Gerçek GitHub uygulaması: 40–45 kişi

Tek bir depoya 45 kişiyi davet etmek işe yaramaz: PR listesi kalabalıklaşır,
çakışmalar rastgele olur, kimin neyi incelediği izlenemez. Bunun yerine
**takım depoları** kullanın.

### 6.1 Kurulum

1. Ders için ücretsiz bir GitHub **organizasyonu** açın (ör. `istun-mekatronik-2026`).
   Depolar sizin kişisel hesabınızı kalabalıklaştırmaz.
2. `ornek-depo/` içeriğiyle bir **şablon depo** oluşturun (Settings → Template
   repository).
3. Şablondan **11 takım deposu** üretin (“Use this template”): `takim-01` …
   `takim-11`, her biri 4 kişi.
4. Her depoya takım üyelerini davet edin ve [issue şablonlarındaki](ornek-depo/issue-sablonlari.md)
   issue'ları açın.
5. İsteğe bağlı: `main` için branch koruması (Settings → Branches) açın; doğrudan
   main'e commit engellenir, herkes PR açmak zorunda kalır.

Alternatif: **GitHub Classroom** ile aynı şablondan her takım ya da öğrenci için
depoyu otomatik oluşturabilirsiniz; davet bağlantısıyla öğrenciler kendileri
katılır. Dönem boyunca ödev de verecekseniz bu yol daha az iş çıkarır.

### 6.2 Takım içinde roller (4 kişi)

| Rol | Görev |
|---|---|
| Firmware | `firmware/` altında değişiklik, PR |
| Elektronik | README'ye bağlantı şeması / pin tablosu, PR |
| Dokümantasyon | README düzeni, issue'lar, pano |
| İnceleyici | Takımdaki PR'ları inceler, onaylar, merge eder |

Herkes kendi profil dosyasını (`katilimcilar/ad-soyad.md`) ayrı branch ve PR ile
ekler; [katılımcı el kitabındaki](katilimci-el-kitabi.md) Alıştırma 2–4 budur.

### 6.3 Çakışma alıştırması

Takımın dört üyesi de `cakisma-alani.md` dosyasındaki aynı satırı kendi önerisiyle
değiştirip PR açar. İlk PR birleşince diğer üçünde çakışma çıkar; takım birlikte
çözer. 11 takım aynı anda yaptığı için siz yalnızca dolaşıp yardım edersiniz.

### 6.4 Takımlar arası review

Son 10 dakikada her takım bir başka takımın açık bir PR'ına yorum bıraksın
(takım 1 → 2, 2 → 3 …). Review dili için slayt 19 ve
[katkı rehberi](ornek-depo/CONTRIBUTING.md).

## 7. Yapay zekâ bölümü (slayt 24–28)

- Claude Code ve Codex ücretli plan ya da API kredisi gerektirir; öğrencilerin
  çoğunun erişimi olmayabilir. Bu bölümü **sizin hesabınızla canlı demo** olarak
  yapın.
- Demo için bir takım deposunun kopyasında: issue aç → branch → ajandan önce plan
  iste → diff'i birlikte oku → PR. Ajanın commit'indeki `Co-authored-by` satırını
  gösterin.
- Ders politikanızı (slayt 28) açıkça söyleyin ve izlencede yazılı olsun.

## 8. Değerlendirme

| Kanıt | Nereden | Ne gösterir |
|---|---|---|
| Tamamlama kartı (13/13) | Oyun alanı | Kavramları denedi |
| Birleştirilmiş PR + `Closes #` | Takım deposu | Branch → PR → merge akışını yaptı |
| Anlamlı bir review yorumu | Takım deposu | İnceleme yapabiliyor |
| Çözülmüş conflict commit'i | Takım deposu | Çakışmayı anladı |
| Çıkış soruları | [Değerlendirme listesi](degerlendirme-listesi.md) | Neyin hâlâ karışık olduğu |

İlk seviye başarı: kendi branch'inde küçük bir değişiklik yapar, ne yaptığını
anlatan bir PR açar ve başkasının PR'ına anlamlı bir yorum bırakır.

## 9. Sık takılma noktaları

**Doğrulama e-postası gelmedi.** Spam klasörüne baktırın; üniversite e-postası
gecikiyorsa kişisel e-postayla açıp sonra üniversite e-postasını ekletin.

**Davet gelmedi.** Kullanıcı adının doğru yazıldığını ve davetin
github.com/notifications ya da e-postada kabul edildiğini kontrol edin.

**Commit doğrudan main'e gitti.** Felaket değil. Commit geçmişini gösterin, sonra
aynı değişikliği branch + PR ile tekrar yaptırın. Branch koruması açıksa bu olmaz.

**Branch'e geçmeden düzenledi.** GitHub web düzenleyicisi commit sırasında
“Create a new branch” seçeneği sunar; onu seçtirin.

**Conflict korkuttu.** “İki kişi aynı cümleyi değiştirdi; hangisini tutacağımıza
karar veriyoruz.” Oyun alanında görev 11'i birlikte yapın.

**Grup hız farkı.** Hızlılar yavaşların PR'larını incelesin ya da yardımcı olsun.

**Oyun alanında ilerleme kayboldu.** Gizli pencere ya da farklı bilgisayar.
Görevler 5–10 dakikada yeniden yapılabilir.

**Oyun alanı başkasının ilerlemesini gösteriyor.** Ortak bilgisayar; **Baştan
başla**.

## 10. Paketi güncellemek

- Sunumun kaynağı claude.ai'deki iki slayt destesidir (TR ve EN). Destede
  yaptığınız değişiklikler web sürümüne kendiliğinden geçmez; `sunum/` yeniden
  oluşturulup bu depoya gönderilmelidir.
- Oyun alanı tek bir HTML dosyasıdır (`oyun-alani/index.html`, İngilizcesi
  `oyun-alani/en/index.html`); görev metinleri dosyanın içindedir.
- GitHub'ın arayüzü zamanla değişir; slayt 32'deki ekran görüntülerini dönem
  başında yenileyin. Claude Code ve Codex kurulum komutlarını da dönem başında
  kendi dokümanlarından kontrol edin.
