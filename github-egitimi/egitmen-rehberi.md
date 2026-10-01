# Eğitmen rehberi

Bu rehber, paketin tamamını bir sınıfta nasıl kullanacağınızı anlatır: tarayıcıda
çalışan **sunum**, kavramları denemek için **hazır araçlar** (Learn Git Branching
ve GitHub Skills) ve gerçek GitHub'da yapılan **takım uygulaması**. 40–45 kişilik bir mekatronik sınıfı düşünülerek yazıldı;
daha küçük gruplarda süreleri kısaltmanız yeterli.

> Kısa yol: Ders **45 dakika ve yalnızca sunumdur**; öğrencinin bilgisayar
> başında bir şey yapması gerekmez. Sonda 36. slaytı gösterip isteyenlere dört
> devam yolunu söylersiniz (bölüm 2.2). Daha fazla ders saatiniz varsa aynı
> paket 2 × 100 dakikalık uygulamalı bir sürüme genişler (bölüm 2.3).

## 1. Paketin parçaları

| Parça | Bağlantı | Ne için? | Kim kullanır? |
|---|---|---|---|
| Sunum (TR) | [sunum/](sunum/) | 37 slaytlık ders anlatımı | Eğitmen projeksiyonda; öğrenci evde tekrar |
| Sunum (EN) | [sunum/en/](sunum/en/) | Aynı sunumun İngilizcesi | İngilizce ders / değişim öğrencileri |
| Hazır araçlar | [hazir-araclar.md](hazir-araclar.md) | Learn Git Branching (Türkçe, hesapsız) ve GitHub Skills kurslarını derste kullanma | Her öğrenci |
| Örnek eğitim deposu | [ornek-depo/](ornek-depo/) | Gerçek GitHub uygulaması için başlangıç dosyaları | Takımlar |
| Katılımcı el kitabı | [katilimci-el-kitabi.md](katilimci-el-kitabi.md) | Öğrencinin baştan sona rehberi: hesap, Ders 1, ödev, Ders 2 takım alıştırmaları | Öğrenci |
| Alıştırmalar | [alistirmalar.md](alistirmalar.md) | Süreli alıştırma listesi ve başarı ölçütleri (L1–L3, Ö1–Ö2, A–G) | Eğitmen |
| Değerlendirme listesi | [degerlendirme-listesi.md](degerlendirme-listesi.md) | Kanıt kaynakları, kazanım tablosu, puanlama önerisi, çıkış soruları | Eğitmen |

Üç katman birbirini tamamlar:

1. **Sunum** kavramı anlatır (commit nedir, branch neden var).
2. **Learn Git Branching** kavramın Git tarafında ne yaptığını gösterir: öğrenci
   komut yazar, commit ağacı anında değişir. Yanlış yapmak bedavadır.
3. **GitHub Skills** aynı adımları gerçek GitHub arayüzünde, bir botun
   yönlendirmesiyle tek başına yaptırır.
4. **Takım deposu** hepsini gerçek bir takımla tekrarlatır.

Her kavram için sıra aynıdır: **anlat → Learn Git Branching'de dene → GitHub'da yap**.

## 2. Ders planı

### 2.1 45 dakikalık ders: yalnızca sunum (varsayılan)

Bütün sunum 45 dakikada anlatılır. Öğrenci dinler ve izler; hesap açması ya da
bilgisayar getirmesi gerekmez. Hello World'ü siz projeksiyonda canlı yaparsınız.
37 slayt 45 dakikaya ancak çoğu slayt bir dakikadan kısa sürerse sığar; aşağıdaki
tablo nerede durup nerede hızlanacağınızı gösterir.

| Dakika | Slayt | Bölüm | Nerede durun, nerede hızlanın |
|---|---|---|---|
| 0–7 | 1–7 | Giriş | 3'te “Bilgisayarında böyle bir klasör olan?” diye sorun. 6'daki terimleri tek tek okumayın; “hepsi örnekle tekrar gelecek” deyin. |
| 7–17 | 8–14 | 1. bölüm: kişisel repo | 9'daki komut kutusunu atlayın. 12 (günlük döngü) ve 13 (commit mesajı) asıl slaytlar. |
| 17–30 | 15–23 | 2. bölüm: takım | 17 (branch ve PR) ve 20 (conflict) asıl slaytlar. 21–22'yi birer cümleyle geçin. |
| 30–37 | 24–28 | 3. bölüm: yapay zekâ | 26 (güvenli akış) ve 28 (kurallar) yeter; 25 ve 27'yi kısa tutun. |
| 37–43 | 29–32 | Kapanış: test ve Hello World | 30'da öğrenciler bir dakika yanındakiyle tartışsın. 31–32'de Hello World'ü kendi hesabınızda 3–4 dakikada canlı yapın. |
| 43–45 | 33–37 | İsteyenler için | 33'ü yaptırmayın, gösterin. 36'da durun ve dört yolu söyleyin (2.2). |

**Canlı gösterim için:** dersten önce Hello World'ü bir kez prova edin. Zaman
kalmazsa yalnızca pull request açmayı ve merge'ü gösterin.

**Zaman sıkışırsa sırayla şunları kısaltın:** 3. bölüm (24–28; öğrenciler evde
`N` ile okuyabilir), sonra 13, 14, 21, 22, 29, 34 ve 35. 17, 20, 31–32 ve 36'yı
kısaltmayın.

### 2.2 Dersin sonunda: isteyenler için dört yol

36. slayt kolaydan zora dört yol gösterir. Hepsi isteğe bağlıdır ve tek başına
yapılabilir; adım adım talimatlar sitede hazırdır.

| Yol | Süre | Öğrenci nereden başlar? |
|---|---|---|
| 1. Learn Git Branching, Giriş 1–3 | 15 dk, hesap gerekmez | [Hazır araçlar](hazir-araclar.md), [el kitabı bölüm 2](katilimci-el-kitabi.md) |
| 2. İlk repo (Hello World, slayt 33) | 30 dk | Sunumun 31–34. slaytları; `N` ile açıklamalar |
| 3. GitHub Skills: Introduction to GitHub | yaklaşık 1 saat | [El kitabı bölüm 3.1](katilimci-el-kitabi.md) |
| 4. Kendi projesi için repo | kendi hızında | [El kitabı bölüm 6](katilimci-el-kitabi.md) |

Derste şöyle söyleyebilirsiniz:

> “Bugünkü ders burada bitti; bundan sonrası isteğe bağlı. Merak eden önce
> Learn Git Branching'i açsın: hesap açmadan, 15 dakikada commit ve branch'i
> gözüyle görür. Biraz daha isteyen 33. slayttaki altı adımla ilk reposunu açsın.
> Daha da ileri gitmek isteyen GitHub Skills'in Introduction to GitHub kursunu
> bitirsin; bir bot adım adım yönlendiriyor. Hepsinin bağlantısı atölye
> sayfasında.”

Dersten sonra öğrencilere gönderebileceğiniz mesaj:

```text
Bugünkü GitHub dersinin sunumu ve isteğe bağlı devam yolları:
https://arifsolmaz.github.io/github-egitimi/
Kolaydan zora: (1) Learn Git Branching, 15 dk, hesap gerekmez;
(2) ilk reponuz, sunumun 33. slaytı, 30 dk; (3) GitHub Skills
"Introduction to GitHub", ~1 saat; (4) kendi projeniz için bir repo.
Takıldığınız yeri bir sonraki derste sorun.
```

İsteyenlerin ne yaptığını görmek isterseniz GitHub Skills depo bağlantılarını bir
formla toplayın; [değerlendirme listesindeki](degerlendirme-listesi.md) kanıt
tablosu bunun için de işe yarar. Not vermek zorunlu değildir.

### 2.3 Genişletilmiş sürüm: 2 × 100 dakika

Ders saatiniz varsa paketin tamamı uygulamalı iki derse yayılır. Aradaki haftada
öğrenciler hesaplarını açar ve GitHub Skills'in ilk kursunu bitirir. Bölüm 3, 5
ve 6 bu sürüm içindir.

#### Ders 1 — Tek başına: commit, push, branch

| Dakika | Ne yapılır | Slayt | Oyun alanı |
|---|---|---|---|
| 0–10 | Sorun: `son_GERCEKTEN.ino` klasörü; GitHub nedir | 1–5 | — |
| 10–20 | Terimler, yaşam döngüsü | 6–7 | — |
| 20–35 | Kurulum (yalnızca hesap), repo yapısı, Markdown | 8–11 | — |
| 35–45 | Günlük döngü ve commit mesajları | 12–13 | Projeksiyonda Learn Git Branching 1. seviyeyi siz yapın |
| 45–70 | **Learn Git Branching, çiftler hâlinde** | — | Giriş 1–3 (commit, branch, merge) |
| 70–80 | Kontrol noktası: “Merge commit'inin neden iki ebeveyni var?” | 17 | Hızlanma 4 (revert) hızlı bitirenlere |
| 80–90 | `.gitignore` ve şifreler | 14 | — |
| 90–100 | Çıkış soruları, ödev | — | — |

**Ödev (Ders 2'ye kadar):** GitHub hesabını açıp e-postayı doğrulayın; GitHub
Skills [Introduction to GitHub](https://github.com/skills/introduction-to-github)
kursunu bitirip depo bağlantısını gönderin; Learn Git Branching'de Remote → Push &
Pull 1–6. seviyeleri yapın; GitHub Education'a başvurun (isteğe bağlı).

#### Ders 2 — Takımla: issue, pull request, review, conflict, yapay zekâ

| Dakika | Ne yapılır | Slayt | Oyun alanı / GitHub |
|---|---|---|---|
| 0–10 | Ödevdeki takılmalar; 3–4 öğrencinin Skills deposunu projeksiyonda açın | — | Skills depoları |
| 10–30 | Issue, branch, diff, review, conflict | 15–20 | Projeksiyonda bir Skills deposundaki PR'ın diff'i |
| 30–40 | Pano, milestone, sık hatalar | 21–23 | Learn Git Branching Remote 5 (Fake Teamwork) projeksiyonda |
| 40–55 | Yapay zekâ ajanları | 24–28 | Canlı demo (sizin hesabınızla) |
| 55–60 | Hızlı test | 30 | — |
| 60–65 | Hello World akışı ve nereye tıklanır | 31–32 | — |
| 65–95 | **Gerçek GitHub'da takım uygulaması** | 33–34 | Bölüm 6 |
| 95–100 | Komut özeti, kaynaklar, kapanış | 35–37 | — |

#### Tek uygulamalı ders (120 dakika)

Slayt 1–7 (15 dk) → Learn Git Branching Giriş 1–3 (20 dk) → slayt 15–20
(15 dk) → GitHub Skills Introduction to GitHub, **bireysel** (50 dk) → slayt
33–37 (10 dk) → çıkış (10 dk). 3. bölümü (yapay zekâ) ve takım çalışmasını ikinci bir derse bırakın.

## 3. Dersten önce: kontrol listesi

45 dakikalık sürümde yalnızca **Ders günü** maddeleri, Bölüm 4.3 ve Hello World
provası gerekir. Hazırlık mesajı ve takım depoları genişletilmiş sürüm içindir.

**Bir hafta önce**

- [ ] Öğrencilere hazırlık mesajını gönderin (aşağıda).
- [ ] Laboratuvar bilgisayarlarında güncel bir tarayıcı (Chrome, Edge, Firefox)
      olduğunu ve `arifsolmaz.github.io`, `learngitbranching.js.org` ile
      `github.com`'un açıldığını kontrol edin.
- [ ] Takım depolarını hazırlayın (Bölüm 6).
- [ ] Sunumdaki boş alanları doldurun (Bölüm 4.3).

**Ders günü, 15 dakika önce**

- [ ] Projeksiyonda sunumu `F` ile tam ekran açın; ikinci sekmede
      [Learn Git Branching (Türkçe)](https://learngitbranching.js.org/?locale=tr_TR),
      üçüncüde kendi demo deponuz.
- [ ] Learn Git Branching'i gizli pencerede açın ki seviyeler sıfırdan başlasın.
- [ ] Sınıf Wi-Fi'ı ve projeksiyon çözünürlüğü (sunum 16:9 ölçeklenir).

**Öğrencilere hazırlık mesajı**

```text
Merhaba, [tarih] dersinde GitHub'a başlıyoruz. Lütfen derse gelmeden:
1. github.com'da ücretsiz bir hesap açın (üniversite e-postanızla) ve
   e-postanızı doğrulayın. Kullanıcı adını CV'nize yazabileceğiniz biçimde seçin.
2. Şu sayfayı açıp çalıştığını kontrol edin:
   https://learngitbranching.js.org/?locale=tr_TR
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
| 1 Kapak | Hedefi söyleyin: 45 dakika, bilgisayar gerekmez; isteyenler için devam yolları sonda. |
| 2 Plan | Öğrenme çıktılarını başta okuyun, kapanışta dönün. |
| 3 Sorun | “Bilgisayarında böyle bir klasör olan?” diye sorun; eller kalkar. Dosya adıyla sürüm tutmak elle yapılan bir sürüm kontrolüdür. |
| 4 GitHub nedir | GitHub'ın yalnızca yazılım şirketleri için olmadığını vurgulayın; bizim için “yazılım” firmware, kontrol kodu, simülasyon ve doküman demek. |
| 5 Git ve GitHub | En sık karışan konu. GitLab ve Bitbucket da Git kullanır. |
| 6 Terimler | Ezberletmeyin; deftere yazdırın. Commit, branch, push gibi terimler sektörde İngilizce kullanılır. |
| 7 Yaşam döngüsü | Bu derste ilk üç aşama: planla, oluştur, incele. Actions sonraki konu. |
| 9 Kurulum | Hesap açmak dersin parçası değil; devam etmek isteyenler evde açar. Komut kutusunu atlayın. |
| 10 Repo yapısı | Repo oluştururken “Add a README” ve bir `.gitignore` şablonu (C++/Python) seçtirin. |
| 11 Markdown | README'nin Markdown ile yazıldığını gösterin; Hello World gösteriminde **Preview** sekmesini açın. |
| 12 Günlük döngü | Komutlar yalnızca tanısınlar diye; tarayıcıda tek buton yeter. Learn Git Branching'i isteyenlere önerin. |
| 13 Commit mesajı | “Kp 2.0'dan 1.4'e düşürüldü” mesajı, robot salınım yaparsa neyi geri alacağınızı söyler. |
| 14 `.gitignore` | ESP32 kodunda ev Wi-Fi şifresi klasik hatadır. `secrets_example.h` boş değerlerle commit edilir. |
| 16 Issue | WhatsApp grubunun yerini alır. “Closes #12” yazılan PR birleşince issue kapanır. |
| 17 Branch ve PR | Kural: `main` her zaman robotta çalışan sürüm. |
| 18 Diff | “Files changed”da bir satıra gelip `+` ile satıra yorum bırakmayı gösterin. |
| 19 Review | Comment / Approve / Request changes. Çiftleri eşleştirip birbirlerinin PR'ını inceletin. Pratik için GitHub Skills “Review pull requests”. |
| 20 Conflict | HEAD = sizin branch'iniz, `=======` altı = gelen. İşaretler silinmezse kod derlenmez. Pratik için GitHub Skills “Resolve merge conflicts”. |
| 21 Pano | Haftalık toplantıda “kim ne yaptı?” yerine panoyu açın. Donanım işleri de panoya. |
| 22 Milestone | Haftaları kendi izlencenize göre değiştirin. Katkı grafiği bireysel katkıyı görünür kılar. |
| 23 Sık hatalar | `revert` geçmişi silmez; `--amend` yalnızca push edilmemiş son commit için. Learn Git Branching: Hızlanma 4, Remote 5–6. |
| 25 Claude Code / Codex | İkisi de ücretli plan ya da API kredisi ister. Windows'ta Claude Code PowerShell'de `irm https://claude.ai/install.ps1 \| iex` ile kurulur. Güncel komutlar için dokümanlara bakın. |
| 26 Güvenli ajan akışı | Ajana Türkçe de yazılabilir. 5. adım (donanımda test) pazarlık konusu değil. |
| 27 GitHub içinde ajanlar | Soldaki konuşma örnektir. `@claude` için repoda `/install-github-app` ile kurulum ve yazma yetkisi gerekir. Bir demo reposunda bir kez kurun. |
| 28 Kurallar | Ders politikanızı doldurun. Ajanların commit'leri çoğu zaman `Co-authored-by` satırı taşır. |
| 30 Test | Cevaplar: 1) Git geçmişi tutan program, GitHub onu barındıran site; 2) commit yerel, push GitHub'a; 3) `main` hep çalışmalı, denemeler branch'te; 4) PR birleşince issue #7 kapanır. Kahoot/Mentimeter'a da aktarılabilir. |
| 31 Hello World | GitHub Docs'taki resmî alıştırma. Adlar `hello-world` ve `readme-edits`. |
| 32 Nereye tıklanır | Hello World'ü burada canlı yapın, her tıklamayı söyleyin. Yeni başlayanlar için en önemli an. |
| 33 Kendiniz deneyin | Derste yaptırmayın; “evde 30 dakika” deyin. Sık takılmalar: doğrulama e-postası, branch'e geçmeden düzenlemek. |
| 34 Merge sonrası | Profil README'sini isteyenlere önerin. |
| 35 Komut özeti | Göstermeniz yeter; PDF olarak paylaşın. |
| 36 Bundan sonrası | Burada durun ve dört yolu söyleyin (bölüm 2.2). Atölye sayfasının adresini tahtaya yazın. |

## 5. Hazır araçlarla 40–45 kişilik sınıf

Kullanım ayrıntıları ve seviye/kurs listesi: [hazir-araclar.md](hazir-araclar.md).

### 5.1 Learn Git Branching (sınıfta)

- **Sunucu yükü yok:** sayfa bir kez yüklenir, her şey öğrencinin tarayıcısında
  çalışır. 45 kişi aynı anda kullanabilir; hesap gerekmez.
- **Türkçe açın:** `https://learngitbranching.js.org/?locale=tr_TR`. Sola `levels`
  yazmak seviye menüsünü açar; `reset` seviyeyi, `undo` son adımı geri alır.
- **Çiftler hâlinde** çalıştırın (yaklaşık 22 çift): biri yazar, diğeri seviyenin
  anlatımını okur ve hedef ağaçla karşılaştırır. Her seviyede rol değiştirsinler.
- **Dizüstü ya da laboratuvar bilgisayarı** kullanın; telefonda komut yazmak zor.
- **İlerleme o tarayıcıda saklanır;** farklı bilgisayarda ya da gizli pencerede
  baştan başlar.

**Kontrol noktaları.** Herkes kendi hızında ilerler ama sınıfı üç kez durdurup
projeksiyonda birlikte bakın:

| Nokta | Seviye | Sınıfa sorun |
|---|---|---|
| A | Giriş 1–2 | “`git branch` yeni bir commit oluşturdu mu? Yıldız (*) neyi gösteriyor?” |
| B | Giriş 3 | “Merge commit'inin neden iki ebeveyni var? GitHub'da PR'ı merge edince ne olur?” |
| C | Hızlanma 4 (hızlılar) | “`revert` ile `reset` arasındaki fark ne? Ortak bir branch'te hangisi güvenli?” |

### 5.2 GitHub Skills (ödev ve Ders 2)

- Her öğrenci kursu **kendi hesabına** kopyalar (Copy Exercise) ve depoyu
  **Public** yapar; private depoda Actions dakikası harcanır.
- Bot her adımı kontrol edip sonrakini yazar. 45 öğrenci aynı anda başlayabilir;
  her depo kendi işini çalıştırır.
- **Takip:** depo bağlantılarını bir forma ya da LMS'e toplayın. Depoyu açınca
  öğrencinin hangi adımda olduğu görünür; bu, sınıfta el kaldırtmaktan daha
  güvenilir bir kanıttır.
- Kurslar İngilizcedir. Ders 1'de slayt 31 (Hello World) ve slayt 32'yi Türkçe
  anlattıysanız talimatlar zorlamaz.

### 5.3 Sık takılmalar

| Araç | Takılma | Çözüm |
|---|---|---|
| Learn Git Branching | Seviye geçmiyor | Hedef ağaçla karşılaştırsın (`show goal`); `reset` ile baştan. |
| Learn Git Branching | Yanlış komut yazdı | `undo` son adımı geri alır. |
| Learn Git Branching | İlerleme kayboldu | Farklı tarayıcı ya da gizli pencere; seviyeler kısa, yeniden yapılır. |
| GitHub Skills | Talimat çıkmadı | 20 saniye bekleyip sayfayı yenilesin. |
| GitHub Skills | Adımdan sonra bot yazmadı | **Actions** sekmesinde işin bitmesini beklesin; kırmızıysa adımı kontrol etsin (doğru branch adı, doğru dosya). |
| GitHub Skills | Depoyu private açtı | Public olarak yeniden kopyalasın. |

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
ekler; [katılımcı el kitabındaki](katilimci-el-kitabi.md) Alıştırma B–D budur.

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
| Introduction to GitHub deposu | GitHub Skills | Branch → commit → PR → merge akışını tek başına yaptı |
| Seviye menüsünün ekran görüntüsü | Learn Git Branching | Commit, branch, merge kavramlarını denedi |
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
karar veriyoruz.” GitHub Skills “Resolve merge conflicts” kursunu ödev verin.

**Grup hız farkı.** Hızlılar yavaşların PR'larını incelesin ya da yardımcı olsun.

**Learn Git Branching'de ilerleme kayboldu.** Gizli pencere ya da farklı
bilgisayar. Seviyeler kısadır, yeniden yapılır.

**GitHub Skills'te bot cevap vermiyor.** Actions sekmesine baktırın; depo private
açıldıysa public olarak yeniden kopyalatın.

## 10. Paketi güncellemek

- Sunumun kaynağı claude.ai'deki iki slayt destesidir (TR ve EN). Destede
  yaptığınız değişiklikler web sürümüne kendiliğinden geçmez; `sunum/` yeniden
  oluşturulup bu depoya gönderilmelidir.
- Learn Git Branching ve GitHub Skills dış araçlardır; dönem başında bağlantıların
  ve kurs adlarının değişmediğini kontrol edin.
- GitHub'ın arayüzü zamanla değişir; slayt 32'deki ekran görüntülerini dönem
  başında yenileyin. Claude Code ve Codex kurulum komutlarını da dönem başında
  kendi dokümanlarından kontrol edin.
