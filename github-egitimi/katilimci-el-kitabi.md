# Katılımcı el kitabı

Bu sayfa, Git ve GitHub dersinde neyi neden yapacağınızı adım adım anlatır.
Amaç komut ezberlemek değil; bir projede değişiklikleri güvenli, görünür ve
geri döndürülebilir biçimde yönetmeyi öğrenmektir. Programlama, komut satırı ya
da kurulum bilmeniz gerekmiyor.

**Yanınızda açık tutun:**
[Neden Git?](neden-git/) ·
[Gerçek GitHub örnekleri](gercek-ornekler/) ·
[Sunum](sunum/) ·
[Learn Git Branching (Türkçe)](https://learngitbranching.js.org/?locale=tr_TR) ·
[GitHub Skills — Introduction to GitHub](https://github.com/skills/introduction-to-github)

## Önce bunu okuyun: ders ve isteğe bağlı yollar

Kısa ders **45 dakika ve yalnızca sunumdur**. Derste önce Git'in neden var
olduğunu, hangi işlerde gerekli olduğunu ve iyi kullanım alışkanlıklarını
göreceksiniz. Bilgisayar getirmeniz gerekmez. Bu sayfadaki pratik adımlar
**isteğe bağlıdır**: ders sonrası devam etmek isteyenler içindir.

## Dersin asıl fikri

- Git, “son_final2.docx” karmaşasını azaltır.
- GitHub, değişiklikleri ekipçe görmeyi, tartışmayı ve onaylamayı kolaylaştırır.
- İyi kullanım, komut bilmekten çok küçük değişiklik, açık mesaj, review ve gizli veri disipliniyle ilgilidir.
- Her proje Git istemez; ama geçmişi, ekip çalışması veya güvenli deneme ihtiyacı varsa erken başlamak rahatlatır.

Kolaydan zora dört yol (sunumun 36. slaytı):

| Yol | Süre | Nereden? |
|---|---|---|
| 1. Learn Git Branching: commit, branch, merge'ü canlı bir ağaçta görün | 15 dk, hesap gerekmez | Aşağıda bölüm 2 |
| 2. İlk reponuz: GitHub Docs “Hello World” | 30 dk | [Sunum, 33. slayt](sunum/#33) |
| 3. GitHub Skills: Introduction to GitHub | yaklaşık 1 saat | Aşağıda bölüm 3.1 |
| 4. Gerçek repo turu: popüler ve iyi yönetilen depoları okuyun | kendi hızınızda | [Gerçek GitHub örnekleri](gercek-ornekler/) |

Hocanız uygulamalı (2 × 100 dakikalık) sürümü yapıyorsa aşağıdaki yol haritası
ve takım alıştırmaları (bölüm 4) da geçerlidir.

## Yol haritası (uygulamalı sürüm)

| Ne zaman? | Ne yapacaksınız? | Süre |
|---|---|---|
| Dersten önce | GitHub hesabı açın, e-postanızı doğrulayın | 10 dk |
| Ders 1 | Sunum + Learn Git Branching'de commit, branch, merge | 100 dk |
| Ödev | GitHub Skills “Introduction to GitHub” kursu + Learn Git Branching push/pull | 1–1,5 saat |
| Ders 2 | Sunum + takım deponuzda issue, branch, pull request, review, çakışma | 100 dk |
| Sonrası | Gerçek repo turu, kendi projeniz için bir depo, profil README'si | — |

## Temel kavramlar

| Kavram | Kısa anlamı |
|---|---|
| Repository (repo, depo) | Projenin klasörü ve tüm geçmişi |
| Commit | Mesajı olan, kaydedilmiş bir anlık kayıt |
| Branch | Ana sürümü (`main`) bozmadan çalışılan ayrı kopya |
| Push / Pull | Değişiklikleri GitHub'a göndermek / GitHub'dan almak |
| Pull request (PR) | Branch'teki değişikliği `main`'e almayı önermek |
| Review | Birinin PR'ını okuyup yorum yapmak, onaylamak |
| Merge | Onaylanan değişikliği `main`'e katmak |
| Issue | Yapılacak iş, hata ya da soru kaydı |
| Conflict (çakışma) | İki kişinin aynı satırı farklı değiştirmesi; kararı insan verir |

---

## 1. Dersten önce: hesap açın

1. [github.com](https://github.com) adresinde **Sign up** ile ücretsiz hesap açın.
   Üniversite e-postanızı kullanın.
2. Kullanıcı adınızı dikkatli seçin: ileride CV'nize yazacaksınız
   (`ayse-yilmaz` gibi; `xXrobotXx` gibi değil).
3. Gelen e-postadaki bağlantıyla **e-postanızı doğrulayın**. Gelmezse spam
   klasörüne bakın.
4. [Learn Git Branching](https://learngitbranching.js.org/?locale=tr_TR) sayfasının
   açıldığını kontrol edin.
5. İsteğe bağlı: [GitHub Education](https://education.github.com)'a öğrenci olarak
   başvurun; ücretsiz araçlar verir.

Hocanız uygulamalı sürümü yapacaksa derse dizüstü bilgisayarınızı getirin.
Kısa sunum dersinde bilgisayar gerekmez.

## 2. Ders 1: commit, branch, merge

Hoca sunumu anlatırken siz takip edin. Ardından yanınızdakiyle **çift olarak**
Learn Git Branching'e geçin: biri yazar, diğeri seviyenin anlatımını okur. Her
seviyede rol değiştirin.

### Learn Git Branching'de ne yapacaksınız?

1. [Türkçe sayfayı](https://learngitbranching.js.org/?locale=tr_TR) açın.
2. Seviye menüsünü açmak için sol tarafa `levels` yazın (ya da menüye tıklayın).
3. **Main** sekmesinde ilk diziyi (Introduction Sequence) seçin ve sırayla yapın:

| Seviye | Konu | Ne öğreneceksiniz? |
|---|---|---|
| 1 | Commit | `git commit` her seferinde geçmişe yeni bir nokta ekler. |
| 2 | Branch | `git branch` yeni bir kopya açar; `git checkout` ile ona geçersiniz. |
| 3 | Merge | `git merge` iki hattı birleştirir; birleşme noktasının iki “ebeveyni” olur. |

**İpuçları**

- Her seviye önce ne yazacağınızı gösteren kısa bir anlatımla başlar; okuyun.
- Sağdaki ağacı hedefle karşılaştırmak için `show goal` yazın.
- Yanlış yazdınız mı? `undo` son adımı, `reset` seviyeyi geri alır.
- Hızlı bitirdiyseniz: **Main** sekmesinde “Ramping Up” dizisinin 4. seviyesi
  (Reversing Changes): hatalı bir commit'i `revert` ile geri almak.

## 3. Ödev (Ders 2'ye kadar)

### 3.1 GitHub Skills: Introduction to GitHub (yaklaşık 1 saat)

Bu kursta gerçek GitHub'da, kendi hesabınızda branch açacak, commit edecek,
pull request açıp merge edeceksiniz. Bir bot her adımı kontrol eder ve sonrakini
yazar.

1. GitHub'a giriş yapın ve [kurs sayfasını](https://github.com/skills/introduction-to-github) açın.
2. **Copy Exercise** butonuna basın.
3. Açılan sayfada depoyu **Public** (herkese açık) olarak oluşturun.
4. Yaklaşık 20 saniye bekleyin ve sayfayı yenileyin; ilk adımın talimatı çıkar.
5. Talimatları sırayla yapın. Kurs İngilizce; takıldığınız kelimeleri tarayıcının
   çeviri özelliğiyle çevirebilirsiniz.
6. Bir adımdan sonra talimat gelmezse: birkaç saniye bekleyip sayfayı yenileyin,
   ya da **Actions** sekmesinde işin bitmesini bekleyin.
7. Bitirince **deponuzun bağlantısını** hocanızın istediği yere (form, LMS) gönderin.
   (Adres çubuğundaki `https://github.com/kullanici-adiniz/...` bağlantısı.)

### 3.2 Learn Git Branching: push ve pull (yaklaşık 20 dakika)

**Remote** sekmesinde “Push & Pull” dizisinin 1–6. seviyeleri: başkasının
değişikliğini almak (`pull`) ve kendi değişikliğinizi göndermek (`push`).

### 3.3 İsteğe bağlı

[Communicate using Markdown](https://github.com/skills/communicate-using-markdown)
kursu: README'leri güzel yazmayı öğretir.

## 4. Ders 2: takım deposunda çalışmak

Dörder kişilik takımlara ayrılacaksınız. Hoca her takıma bir depo verir
(`takim-01`, `takim-02` …) ve sizi davet eder.

### 4.1 Daveti kabul edin

E-postanıza ya da [github.com/notifications](https://github.com/notifications)'a
gelen daveti açıp **Accept invitation**'a basın.

### 4.2 Takım rolleri

| Rol | Ne yapar? |
|---|---|
| Firmware | `firmware/` klasöründe değişiklik yapar, PR açar |
| Elektronik | README'ye bağlantı şeması ya da pin tablosu ekler, PR açar |
| Dokümantasyon | README'yi düzenler, issue'ları ve panoyu takip eder |
| İnceleyici | Takımdaki PR'ları okur, yorum yapar, onaylar ve merge eder |

Rolünüz ne olursa olsun, aşağıdaki alıştırmaların hepsini herkes yapar.

### 4.3 Alıştırma A — depoyu tanı

1. Takım deponuzu açın; `README.md`'yi okuyun.
2. **Issues** sekmesini açın; size atanmış issue'yu bulun.
3. Sağ üstteki **commits** (saat simgesi) bağlantısından geçmişe bakın:
   son değişikliği kim, ne zaman yapmış?

### 4.4 Alıştırma B — kendi dosyanı yeni bir branch'te ekle

1. `katilimcilar/` klasörünü açın.
2. **Add file → Create new file** seçin.
3. Dosya adına kendi adınızı yazın:

```text
katilimcilar/ad-soyad.md
```

4. İçeriği doldurun:

```md
# Ad Soyad

- Takımdaki rolüm:
- İlgi alanım:
- Bugün öğrendiğim ilk kavram:
```

5. **Commit changes**'e basın. Açılan pencerede:
   - Commit mesajı: `Ad Soyad profilini ekle`
   - **Create a new branch for this commit and start a pull request** seçeneğini
     işaretleyin. `main`'e doğrudan commit etmeyin.
6. **Propose changes**'e basın.

### 4.5 Alıştırma C — pull request aç

1. Açılan sayfada başlığı kontrol edin: `Ad Soyad profilini ekle`.
2. Açıklamaya şunu yazın; `#3` yerine size atanmış issue'nun numarasını yazın:

```md
## Ne değişti?
katilimcilar klasörüne profil dosyamı ekledim.

Closes #3

## Kontrol
- [ ] Dosya adı doğru mu?
- [ ] İçerik anlaşılır mı?
```

3. **Create pull request**'e basın.
4. **Files changed** sekmesinde diff'e bakın: yeşil satırlar eklediklerinizdir.

`Closes #3` yazdığınız için PR birleşince 3 numaralı issue kendiliğinden kapanır.

### 4.6 Alıştırma D — bir takım arkadaşının PR'ını incele

1. **Pull requests** sekmesinde bir arkadaşınızın PR'ını açın.
2. **Files changed** sekmesine geçin.
3. Bir satırın üzerine gelin, çıkan **+** işaretine basın ve yorum yazın.
4. Sağ üstteki **Review changes**'e basın ve birini seçin:
   - **Comment**: sadece yorum
   - **Approve**: uygun, birleştirilebilir
   - **Request changes**: önce bir şey düzeltilmeli

İyi yorum kibar, somut, bir satıra bağlı ve gerekçelidir:

```text
✗ Burası yanlış.
✓ Dosya adında Türkçe karakter var; diğerleri gibi “ayse-yilmaz.md” yazabilir misin?
```

İnceleyici, onaylanan PR'ları **Merge pull request → Confirm merge** ile
birleştirir, sonra **Delete branch**'e basar.

### 4.7 Alıştırma E — çakışma çöz

1. Hoca söyleyince herkes `cakisma-alani.md` dosyasındaki aynı satırı kendi
   önerisiyle değiştirir; Alıştırma B'deki gibi yeni branch ve PR açar.
2. İlk PR birleşince diğerlerinde “This branch has conflicts” uyarısı çıkar.
3. **Resolve conflicts** butonuna basın. Dosyada şuna benzer bir bölüm görürsünüz:

```text
<<<<<<< ad-soyad-branch
Atölyeden sonra GitHub’ı şu iş için kullanabiliriz: ders projeleri
=======
Atölyeden sonra GitHub’ı şu iş için kullanabiliriz: takım ödevleri
>>>>>>> main
```

4. Takımla karar verin: hangi cümle kalacak (ya da ikisini birleştirin).
5. `<<<<<<<`, `=======` ve `>>>>>>>` satırlarını silin; sadece son metin kalsın.
6. **Mark as resolved → Commit merge**'e basın. Sonra PR'ı birleştirin.

Çakışma bir hata değildir; iki iyi niyetli değişikliğin aynı yere denk gelmesidir.

### 4.8 Takımlar arası review

Son 10 dakikada hocanın verdiği eşleşmeye göre (takım 1 → takım 2 …) başka bir
takımın açık bir PR'ına en az bir yorum bırakın.

## 5. Sık sorunlar

| Sorun | Çözüm |
|---|---|
| Doğrulama e-postası gelmedi | Spam klasörüne bakın; birkaç dakika bekleyip yeniden gönderin. |
| Davet görünmüyor | [github.com/notifications](https://github.com/notifications)'a bakın; kullanıcı adınızı hocaya doğru yazdığınızdan emin olun. |
| Yanlışlıkla `main`'e commit ettim | Sorun değil. Hocaya söyleyin; aynı değişikliği bu kez yeni branch ile yapın. |
| “Create a new branch” seçeneğini görmedim | Takım deposunda `main` korumalıysa GitHub zaten yeni branch açtırır; değilse commit penceresindeki ikinci seçeneği işaretleyin. |
| GitHub Skills'te talimat gelmedi | 20 saniye bekleyip sayfayı yenileyin; **Actions** sekmesinde iş kırmızıysa adımı kontrol edin (doğru branch adı, doğru dosya). |
| Skills deposunu private açtım | Public olarak yeniden kopyalayın. |
| Learn Git Branching'de ilerlemem kayboldu | Farklı tarayıcı ya da gizli pencere kullanmış olabilirsiniz; seviyeler kısa, yeniden yapın. |

## 6. Dersten sonra

- Eski bir Arduino ya da ders projenizi README'li yeni bir depoya koyun.
- **Profil README'si:** kullanıcı adınızla tam aynı adda bir depo açın
  (`ayse-yilmaz/ayse-yilmaz`); içindeki `README.md` profilinizin en üstünde görünür.
- [Review pull requests](https://github.com/skills/review-pull-requests) ve
  [Resolve merge conflicts](https://github.com/skills/resolve-merge-conflicts)
  kurslarıyla pratik yapın.
- Bilgisayarınızda çalışmak isterseniz [GitHub Desktop](https://desktop.github.com)'u
  kurun; aynı akışı butonlarla yaparsınız.
