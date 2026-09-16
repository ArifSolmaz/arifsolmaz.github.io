# Eğitmen rehberi

Bu rehber, GitHub’ı ilk kez düzenli kullanacak bir gruba uygulamalı eğitim
vermek için hazırlanmıştır.

## Eğitimden önce

### 1. Eğitim deposunu hazırlayın

GitHub’da `github-egitimi` veya kurumunuza uygun başka bir adla yeni bir depo
açın. İlk eğitim için depo herkese açık olmak zorunda değildir; kurum içi
katılımcılarla çalışıyorsanız özel depo daha rahat olabilir.

Bu klasördeki `ornek-depo/` içeriğini eğitim deposuna koyun.

### 2. Katılımcıları davet edin

Katılımcıların GitHub hesabı açmasını isteyin. Dersten önce şu hazırlık mesajını
gönderebilirsiniz:

```text
Atölye için lütfen github.com üzerinde bir hesap açın ve giriş yapabildiğinizi
kontrol edin. Eğitimde komut satırı kullanmak zorunda değilsiniz; ilk oturumda
GitHub web arayüzü yeterli olacak.
```

### 3. Eğitim deposunda issue’lar açın

Aşağıdaki issue başlıklarını önceden oluşturun:

- Katılımcı profilini ekle
- README’ye bir kaynak önerisi ekle
- Proje notlarında bir yazım hatası düzelt
- Çakışma alıştırması için aynı satırı düzenle
- Bir pull request’i incele ve yorum yap

Her issue’ya bir katılımcı atayın. Grup kalabalıksa aynı issue’nun kopyalarını
açabilirsiniz.

## 2 saatlik akış

### 0–10 dk: Neden GitHub?

GitHub’ı “kod sitesi” diye değil, “ortak çalışma ve kayıt sistemi” diye anlatın.
Örnekler:

- Bir web sayfasını birlikte güncellemek
- Bir belge setinin geçmişini tutmak
- Gönüllü ekiplerin işlerini issue’larla takip etmek
- Değişiklikleri yayınlamadan önce gözden geçirmek

### 10–25 dk: Depo turu

Ekran paylaşarak şu alanları gösterin:

- `README.md`
- dosya listesi
- commit geçmişi
- Issues
- Pull requests
- branch seçici

Bu bölümde terimlere boğmayın. “Birazdan hepsini kullanacağız” demek yeterli.

### 25–45 dk: İlk düzenleme ve commit

Katılımcılardan `katilimcilar/` klasöründe kendi adlarıyla bir dosya açmalarını
isteyin.

Örnek dosya adı:

```text
katilimcilar/ayse-yilmaz.md
```

Dosya içeriği:

```md
# Ayşe Yılmaz

- İlgi alanım:
- GitHub’dan beklentim:
- Bugün öğrendiğim ilk kavram:
```

Herkes bu değişikliği doğrudan ana branch’e değil, yeni branch açarak yapsın.

### 45–70 dk: Pull request

Katılımcılar kendi branch’lerinden pull request açsın. Her PR’da şu üç şeyi
yazmalarını isteyin:

- Ne değişti?
- Neden değişti?
- Kontrol edilmesi gereken bir şey var mı?

Sonra herkes başka birinin PR’ına kısa bir yorum yazsın.

### 70–90 dk: Review ve merge

Bir veya iki PR’ı sınıfta birlikte inceleyin. Şunları gösterin:

- satıra yorum bırakma
- değişiklik isteme
- onaylama
- merge etme

Bu noktada “review hata aramak değil, ortak kalite kurmaktır” vurgusu işe yarar.

### 90–110 dk: Çakışma alıştırması

Herkesten `cakisma-alani.md` dosyasındaki aynı satırı farklı biçimde değiştirmesini
isteyin. İlk kişi merge edince diğerlerinde conflict oluşur.

Çakışmayı panik konusu değil, iki değişikliğin aynı yere denk gelmesi olarak
anlatın. Bir örneği birlikte çözün.

### 110–120 dk: Kapanış

Katılımcılardan şu üç soruya yanıt alın:

- Bugün hangi işi tek başıma yapabilirim?
- Hangi adım hâlâ karışık?
- Kendi işimizde GitHub’ı nerede kullanabiliriz?

## 3 saatlik akışta ekleyin

- GitHub Desktop kurulumu ve clone
- Yerelde dosya düzenleme
- Sync / push / pull
- Daha gerçekçi issue panosu
- Küçük takım projesi

## Eğitmenin dikkat edeceği noktalar

- İlk oturumda komut satırını merkeze almayın.
- “Yanlış yaparsanız geri dönebiliriz” güvenini sık sık hatırlatın.
- Her kavramı bir eylemle bağlayın.
- Teknik terimi söyledikten sonra gündelik karşılığını da verin.
- Kalabalık grupta iki kişilik eşleşmeler yaptırın.

## Sık takılma noktaları

### Davet gelmedi

Katılımcının GitHub kullanıcı adını doğru verdiğinden ve e-postasını doğruladığından
emin olun.

### Commit doğrudan ana branch’e gitti

Bu kötü bir felaket değildir. Commit geçmişini gösterin, sonra aynı değişikliği
branch + pull request akışıyla tekrar yaptırın.

### Conflict korkuttu

Çakışmayı “iki kişi aynı cümleyi değiştirdi, hangisini tutacağımıza karar
veriyoruz” diye sadeleştirin.

### Grup hız farkı yaşadı

Hızlı ilerleyenlerden yavaş ilerleyenlere review yapmalarını isteyin. Böylece
bekleme süresi de öğrenmeye dönüşür.

