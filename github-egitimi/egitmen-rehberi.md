# Git ve GitHub: Robot Dün Çalışıyordu

32 ana slayt, 12 ek slayt. Ana anlatım ve sorular toplam 45 dakika.

Canlı gösterim, sınıf içi uygulama ve zorunlu ödev yoktur. Ek slaytlar ana anlatım süresinin dışındadır.

## 1. Robot dün çalışıyordu

00:00–00:45 · 45 saniye

Bir çizgi izleyen robot takımını düşünelim. Elif ve Deniz dün aynı projeyle çalışıyordu. Bugün robot çizgiyi kaybediyor ve mesaj grubunda birbirinden farklı dosyalar dolaşıyor. Hangisinden devam edeceklerini bilmiyorlar. Bu ders boyunca onların kararlarını izleyeceğiz. Git ve GitHub adlarını, ihtiyaç duydukları anda açacağız. Amacımız komut ezberlemekten çok, bir değişikliğin nasıl izlenebilir ve paylaşılabilir olduğunu görmek. Bu bir kurgusal ders örneği; ekrandaki eşikler gerçek robot üzerinde ölçülmüş sonuçlar değildir. Canlı uygulama yapmadan, hazırlanmış görüntülerle sorundan ortak karara giden yolu takip edeceğiz.

Kaynaklar:


## 2. Hangi dosyaya güveneceğiz?

00:45–01:30 · 45 saniye

Ekrandaki dosya adları tanıdık gelebilir. Robot, robot final ve robot final son diye ilerliyoruz; fakat dosyanın adını değiştirmek kararın gerekçesini saklamıyor. Elif kendi kopyasını, Deniz başka bir kopyayı gönderince sorun büyüyor. En yeni tarihli dosya mutlaka doğru dosya değildir. Takımın ihtiyacı daha iddialı bir dosya adı değil: neyin, neden ve hangi sırayla değiştiğini görebilmek. Birazdan dosyaların kendisi kadar onların arasındaki ilişkiyi de kaydedeceğiz. Böylece iki kişinin katkısını rastgele bir kopyayı seçerek kaybetmek zorunda kalmayacağız.

Kaynaklar:

- [Commit geçmişini incelemek](https://git-scm.com/book/en/v2/Git-Basics-Viewing-the-Commit-History)

## 3. Dosya var. Karar nerede?

01:30–03:00 · 90 saniye

Elif ve Deniz dosyalara bakabiliyor, ancak hangi değişikliğin bugünkü davranışa yol açtığını anlatan bir kayıt bulamıyor. Dün kullanılan değer neydi? Deniz hangi satıra dokundu? Elif hangi dosyadan devam etti? Bunları hafızadan çıkarmaya çalışmak yerine bir değişiklik geçmişi tutabiliriz. Bu geçmiş tek başına robotun doğru çalıştığını kanıtlamaz; önce soruyu daraltmamıza yardım eder. İlk hedefimiz robotu hemen düzeltmek değil, tahmin yürütmeden neyin değiştiğini bulmak. Bu ayrım dersin geri kalanında da önemli olacak: araç kayıt tutar, mühendislik kararını takım verir.

Kaynaklar:

- [Commit geçmişini incelemek](https://git-scm.com/book/en/v2/Git-Basics-Viewing-the-Commit-History)

## 4. Dünle bugünü nasıl karşılaştırırız?

03:00–04:30 · 90 saniye

Takımın kaydettiği geçmişe baktığımızı düşünelim. Bir commit içinde sensör eşiğinin 500 değerinden 900 değerine değiştiğini görüyoruz. Kayıt, yazar ve açıklama bilgisiyle birlikte bulunabiliyor. Artık “bir şey değişmiş” demek yerine hangi satırın değiştiğini söyleyebiliyoruz. Animasyondaki değerler IR sensör okuması için kurgusal eşiklerdir; farklı robotlarda aynı sayıları kullanmak doğru bir kalibrasyon yöntemi değildir. Ayrıca bu kayıt, değişikliğin yanlış olduğunu kendiliğinden kanıtlamaz. Bize inceleyebileceğimiz bir aday neden verir. Şimdi bu geçmişi hangi araç tutuyor, takım nereden görüyor sorusunu ayıralım.

Kaynaklar:

- [Commit geçmişini incelemek](https://git-scm.com/book/en/v2/Git-Basics-Viewing-the-Commit-History)

## 5. Bu işin hangi tarafı Git?

04:30–05:45 · 75 saniye

Git ve GitHub isimlerini burada ayırmak işimizi kolaylaştırıyor. Git, bilgisayardaki sürüm kontrol aracı; seçtiğimiz değişiklikleri kaydeder, geçmişi ve dalları yönetir. Birçok yerel işlem internet bağlantısı olmadan yapılabilir. GitHub ise depoyu barındıran ve bu geçmişin çevresinde takım çalışmasını düzenleyen platformdur. Elif’in dosyayı kaydetmesi, Deniz’in GitHub’da onu göreceği anlamına gelmez. Bilgisayardaki kayıt ile ortak depoya aktarım ayrı adımlardır. Git’i terminalden veya bir editörün arayüzünden kullanabiliriz. Ekrandaki düğmeler değişse bile az sonra izleyeceğimiz kayıt ve paylaşım ilişkisi aynı kalır.

Kaynaklar:

- [GitHub nedir?](https://docs.github.com/en/get-started/start-your-journey/what-is-github)

## 6. Neyi birlikte saklayalım?

05:45–07:00 · 75 saniye

Takımın robot.ino dosyasını, bağlantı şemasını, proje fotoğrafını ve açıklamasını aynı depoda topladığını düşünelim. Repository yani depo, dosyalarla birlikte kaydedilmiş geçmişi de taşır. Böylece kodun yanında onu hangi donanımla kullandığımız anlaşılır. Animasyon dosyaların GitHub’da bir araya gelişini gösteriyor; tarayıcıdan yüklenen dosyalar için de commit oluşur. Yerelde çalışırken ise kayıt ve gönderim ayrı yapılır. Metin dosyalarında satır farklarını incelemek kolaydır. Fotoğraf ve PDF de saklanabilir, fakat değişimlerini kod satırları kadar ayrıntılı karşılaştırmayı beklememeliyiz. Depo bize projenin bağlamını bir arada tutma imkânı verir.

Kaynaklar:

- [Depolar](https://docs.github.com/en/repositories/creating-and-managing-repositories/about-repositories)

## 7. O satırda ne değişmiş?

07:00–08:15 · 75 saniye

Bu görünümün adı diff, yani fark. Eksi işaretli satır karşılaştırmanın önceki tarafında, artı işaretli satır sonraki tarafında yer alıyor. Robot kodunda eşik 500’den 900’e çıkarılmış. Bunlar iki sensörün ölçümü değil, aynı değişkenin iki farklı kayıt içindeki değerleri. Commit ise projenin seçilmiş hâlini geçmişe alan kayıt noktasıdır; kimliği ve açıklaması vardır. Dosyayı editörde kaydetmek kendiliğinden commit oluşturmaz. Fark görünümü sayesinde dosyanın tamamı yerine değişen bölgeye odaklanırız. Yine de bir satırın küçük görünmesi etkisinin küçük olduğu anlamına gelmez. Şimdi bu değişikliği nasıl değerlendireceğiz?

Kaynaklar:

- [git commit](https://git-scm.com/docs/git-commit)
- [git diff](https://git-scm.com/docs/git-diff)

## 8. 900 yanlış mı?

08:15–09:15 · 60 saniye

Burada kısa bir duraklama önemli. Dünkü dosyada 500, bugünkü dosyada 900 olması, her koşulda 500 doğru demek değildir. Işık, zemin ve sensör yerleşimi davranışı etkileyebilir. Git bize hangi satırın değiştiğini anlatır; robotun beklenen davranışını değerlendirip uygun koşullarda denemek bizim işimizdir. Elif ve Deniz önce değişikliğin gerekçesini ve varsa ölçüm kaydını inceler. 500’e dönmek bir aday çözüm olabilir, henüz onaylanmış sonuç değildir. Bu yüzden bir sonraki adım doğrudan ana dosyanın üzerine yazmak olmayacak. Denemeyi görünür bir işe çevirip ayrı bir çalışma çizgisi açacağız.

Kaynaklar:

- [Commit geçmişini incelemek](https://git-scm.com/book/en/v2/Git-Basics-Viewing-the-Commit-History)
- [git diff](https://git-scm.com/docs/git-diff)

## 9. Bu sorunu kim takip ediyor?

09:15–10:45 · 90 saniye

Takımın sorusu artık somut: robot çizgiyi hangi koşulda kaybediyor ve eşik değişikliğiyle ilişkisi ne? Bunu bir issue içinde kaydedebiliriz. Açıklamaya beklenen davranışı, görülen sorunu ve ilgili dosyayı yazar; işi Elif’e atayabiliriz. Böylece yapılacak iş mesaj grubunda kaybolmaz. Ekrandaki animasyon fotoğraf ekleme işi üzerinden issue arayüzünü gösteriyor; bizim hikâyemizdeki iş sensör eşiğini incelemek. Issue çözümün kendisi değil, takip edilen ihtiyaçtır. Daha sonra hazırlayacağımız değişiklik önerisini bu kayda bağlayabiliriz. İş kapansa bile konuşmalar ve gerekçeler projede kalır; takım kararı yeniden bulabilir.

Kaynaklar:

- [Issue kavramı](https://docs.github.com/en/issues/tracking-your-work-with-issues/learning-about-issues/about-issues)

## 10. Main aynı kalırken nasıl deneriz?

10:45–12:00 · 75 saniye

Elif eşiği yeniden değerlendirmek istiyor, ama ortak ana çizgide herkesin denemesini birbirine karıştırmak istemiyoruz. Branch yani dal, aynı başlangıçtan ayrı bir çalışma çizgisi sağlar. Elif’in bu dalda oluşturduğu commit’ler main dalını kendiliğinden değiştirmez. Main de başka kabul edilmiş işlerle ilerleyebilir. Şemada bu iki çizgiyi görüyorsunuz. Dal açmak yeni bir fiziksel proje klasörü üretmek zorunda değildir; dal adı bir commit’e işaret eder. Başlangıç için bir ana dal ve kısa ömürlü iş dalları yeterli bir düzen olabilir. Denemenin ana dala ne zaman alınacağını inceleme ve doğrulama sonunda belirleyeceğiz.

Kaynaklar:

- [Git dalları](https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell)
- [Dal düzenleri](https://git-scm.com/book/en/v2/Git-Branching-Branching-Workflows)

## 11. Dosyayı kaydettim. Deniz gördü mü?

12:00–13:45 · 105 saniye

Bu soruya şimdi dört bölgeyle cevap verebiliriz. Çalışma alanı dosyayı açıp değiştirdiğimiz yerdir. Hazırlık alanı bir sonraki commit’e hangi değişikliklerin gireceğini seçer. Yerel depo bilgisayardaki kayıtlı geçmişimizdir. Uzak depo ise burada GitHub’da ortak paylaştığımız geçmiş. Eşiği düzenlemek ilk bölgede olur. Add seçer, commit yerelde kaydeder, push kayıtları ortak depoya gönderir. Dolayısıyla editörde kaydettiğim değişiklik henüz Deniz’e ulaşmamıştır. Aynı şekilde GitHub’da yeni kayıt oluşunca bilgisayardaki kopyam kendiliğinden güncellenmez. Şimdi Elif’in tek sensör değişikliğini bu bölgeler arasında adım adım taşıyacağız.

Kaynaklar:

- [Git: çalışma modeli](https://git-scm.com/book/en/v2/Getting-Started-What-is-Git%3F)

## 12. Aynı başlangıcı nasıl alırız?

13:45–15:00 · 75 saniye

Elif’in yeni bir bilgisayarda çalıştığını düşünelim. Clone ile var olan robot deposunun yerel kopyasını oluşturuyor. Normal bir klonlamada dosyalar, kayıtlı geçmiş ve uzak adres bağlantısı gelir; böylece hem kodu açabilir hem geçmişi inceleyebilir. Depo-adresi ekrandaki yer tutucudur, gerçek klonlama adresiyle değiştirilir. Herkese açık depoyu HTTPS üzerinden okumak çoğunlukla hesapla giriş gerektirmez; özel depoda yetki gerekir. Klonlayabilmek gönderim yetkisine sahip olmak değildir. ZIP indirmek ise seçilen hâlin dosyalarını verir, yerel Git geçmişini kurmaz. Elif’in geçmişle çalışması ve yeni kayıt göndermesi için burada klonlama yolunu izliyoruz.

Kaynaklar:

- [Depoyu klonlamak](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository)

## 13. Deneme hangi dalda yapılacak?

15:00–16:15 · 75 saniye

Klonlanan projede şimdi main dalındayız. Switch c seçeneğiyle feature sensor esigi adlı yeni dalı oluşturup o dala geçiyoruz. Branch listesindeki yıldız etkin dalı gösterir. Bundan sonra yapacağımız commit bu çizgide ilerleyecek. Henüz kodu değiştirmedik; dal oluşturmak tek başına sensör sorununu çözmez. Dal adını işin amacını anlatacak şekilde seçmek, takımın hangi çizgide ne geliştirildiğini bulmasını kolaylaştırır. Burada main ortak ana çizgi, iş dalı aday çözüm içindir. Başka projelerin dal adları ve katkı kuralları farklı olabilir. Sıradaki adım gerçekten dosyayı düzenlemek; böylece kayda alınacak bir değişiklik oluşacak.

Kaynaklar:

- [Git dalları](https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell)
- [Dal düzenleri](https://git-scm.com/book/en/v2/Git-Branching-Branching-Workflows)
- [git switch](https://git-scm.com/docs/git-switch)
- [git diff](https://git-scm.com/docs/git-diff)

## 14. Hangi çözümü deniyoruz?

16:15–17:45 · 90 saniye

Şimdi Elif robot.ino içindeki eşiği 900’den 500’e değiştirip dosyayı kaydediyor. Bu, dünkü değere dönüş adayımız; robotu düzelttiği henüz kanıtlanmış değil. Git status çalışma alanının önceki kayıttan farklı olduğunu, diff ise değişen satırı gösterir. Yeni commit henüz oluşmadı ve GitHub’daki dosya hâlâ önceki hâlinde. Bu aşamada değişikliği tekrar okuyabilir, test planını belirleyebilir veya vazgeçebiliriz. Komut sırası tek başına bir geliştirme değildir; clone ve dal açmanın ardından gerçekten yapılan düzenleme budur. Diğer bütün kayıt ve paylaşım adımları birazdan bu aynı sensör satırını taşıyacak.

Kaynaklar:

- [git diff](https://git-scm.com/docs/git-diff)
- [git status](https://git-scm.com/docs/git-status)

## 15. Bu kayda ne girecek?

17:45–19:15 · 90 saniye

Add, internet yüklemesi değil, bir sonraki commit’in içeriğini seçme işlemidir. Elif sensör eşiğini seçiyor ve hazırlanan farkı kontrol ediyor. Aynı anda README’de yarım kalan bir açıklama varsa onu bu kayda katmak zorunda değil. Böylece commit’in amacı anlaşılır kalır. Buradaki diff cached, birazdan geçmişe yazılacak içeriği gösterir. Add dosyanın o andaki hâlini hazırlar; daha sonra dosyayı yeniden düzenlersek yeni hâli de kayda almak için tekrar add gerekebilir. Her değişikliği tek seferde toplamak yerine mantıklı kapsam seçmek hem incelemeyi hem gerekirse geri almayı kolaylaştırır. Şimdi yalnız seçilen sensör değişikliğini kaydedeceğiz.

Kaynaklar:

- [git add](https://git-scm.com/docs/git-add)

## 16. Ne yaptığımızı nasıl kaydederiz?

19:15–20:30 · 75 saniye

Elif hazırladığı sensör değişikliğini commit ile yerel geçmişe alıyor. Mesajda “eşik için 500 dönüş adayı” diyoruz; henüz yapılmamış doğrulamayı yapılmış gibi anlatmıyoruz. Log oneline ile yeni kaydın kimliği ve açıklaması görülebilir. Commit hazırlık alanının seçilmiş hâlini kaydeder; bilgisayardaki geçmiş ilerler. Önceki 900 kaydı da geçmişte bulunur. İnternet olmadan bu kayıt oluşturulabilir. Şimdi bir kez daha başlıktaki soruya dönelim: Deniz bu değişikliği gördü mü? Henüz değil, çünkü Elif yalnız kendi bilgisayarında kayıt oluşturdu. Yerel commit ile takımın ortak depoya erişmesi ayrı şeylerdir. Sıradaki gönderim bu ayrımı tamamlıyor.

Kaynaklar:

- [git commit](https://git-scm.com/docs/git-commit)
- [Commit geçmişini incelemek](https://git-scm.com/book/en/v2/Git-Basics-Viewing-the-Commit-History)

## 17. Deniz şimdi görebilir mi?

20:30–22:00 · 90 saniye

Elif yeni commit’i origin üzerindeki sensör dalına gönderiyor. U seçeneği bu yerel dalın hangi uzak dalı izleyeceğini kaydeder. Gönderim başarılı olduğunda Deniz GitHub’da aday çözümü görebilir. Main hâlâ kendiliğinden değişmemiştir; yalnız iş dalı güncellenmiştir. Push çalışma alanındaki commit edilmemiş dosyaları doğrudan yüklemez, kayıtları aktarır. Bunun için doğru uzak adres, yazma izni ve uygun kimlik doğrulama gerekir; ayrıntılar eklerde duruyor. Gönderim reddedilirse ortak geçmişi anlamadan zorla üzerine yazmayız. Şimdi takım aynı değişikliğe bakabiliyor, fakat görünür olması kabul edildiği anlamına gelmiyor. Kabul sorusunu pull request ile soracağız.

Kaynaklar:

- [git push](https://git-scm.com/docs/git-push)
- [git branch](https://git-scm.com/docs/git-branch)

## 18. Bu çözümü main’e alalım mı?

22:00–23:30 · 90 saniye

Elif iş dalından main’e bir pull request açıyor. Kaynak dal aday sensör çözümünü, hedef dal ortak ana çizgiyi gösteriyor. Açıklamada sorunu, 900’den 500’e dönüşü ve hangi doğrulamanın beklendiğini yazıyoruz. Yapılmamış bir testi yapılmış gibi sunmuyoruz. PR açılması değişikliği hemen kabul ettirmez; tartışma ve inceleme için görünür kılar. Issue ile ilişki de burada kurulabilir: issue yapılacak ihtiyacı, PR önerilen çözümü anlatır. Aynı sorunu farklı çözümlerle ele alan başka öneriler olabilir. Takım kaynak ve hedef dalı, kod farkını ve gerekçeyi birlikte değerlendirir. Şimdi Deniz’in incelemede neye bakacağını görelim.

Kaynaklar:

- [Issue kavramı](https://docs.github.com/en/issues/tracking-your-work-with-issues/learning-about-issues/about-issues)
- [Pull request](https://docs.github.com/en/pull-requests/reference/pull-requests)

## 19. Deniz neye bakacak?

23:30–25:00 · 90 saniye

Deniz Files changed görünümünde sensör satırını inceliyor. “Neden 500?” ve “Hangi koşulda denenecek?” diye soruyor. Bunlar kişiye değil, önerinin dayanağına yönelen sorular. Elif geri bildirim üzerine aynı dalda yeni commit gönderirse PR güncellenir; yeni bir PR açması gerekmez. Projede otomatik kontroller varsa onların sonucu da değerlendirmeye katılır, fakat her kontrol gerçek robot davranışının yerine geçmez. Onay verebilmek ve birleştirme yetkisine sahip olmak da ayrı olabilir. Takımın kuralı, uygun gerekçe ve doğrulama olmadan aday değişikliği ana çizgiye almamak. Bu sırada main başka bir kabul edilmiş değişiklikle ilerlerse iki çizginin buluşması ayrıca gerekebilir.

Kaynaklar:

- [Pull request incelemeleri](https://docs.github.com/en/pull-requests/reference/pull-request-reviews)

## 20. Aynı satıra iki karar gelirse?

25:00–26:15 · 75 saniye

Hikâyeye şimdi sık karşılaşılan bir durum ekleyelim. Elif çalışırken Deniz’in başka bir değişikliği incelemeyle main’e alınmış ve aynı eşik 700 olmuş olsun. Elif’in dalında aday 500 var. İş dalındayken main’i birleştirdiğimiz merge örneğinde Git bu satır için otomatik karar veremez ve çakışma işaretleriyle durur. HEAD bulunduğumuz iş dalının tarafını, main ise gelen tarafı gösterir; HEAD her zaman doğru seçenek demek değildir. Git farklı bölgeleri çoğu zaman birleştirebilir; aynı satırdaki anlam çatışmasını takımın çözmesi gerekir.

Kaynaklar:

- [Birleştirme çakışmaları](https://docs.github.com/en/pull-requests/reference/merge-conflicts)

## 21. Hangisini seçiyoruz?

26:15–28:00 · 105 saniye

Hikâyemizde Elif ve Deniz iki değişikliğin gerekçesini karşılaştırıp 500 adayını sürdürmeye karar veriyor. Bu, kurgusal örneğin kararıdır; her robot için kullanılacak eşik değeri değildir. Son dosyada tek eşik kalıyor, çakışma işaretleri kalkıyor. Takım dosyayı kaydedip projeye uygun doğrulamayı tamamlıyor. Ardından add ve commit ile merge çözümünü kayda alıyor, push ile PR’yi güncelliyor. Editörün seçenek düğmeleri işlemi kolaylaştırıyor; kararın gerekçesini takım yazıyor. Sonraki aşamayı, bu adayın gerekli inceleme ve doğrulamayı geçtiği varsayımıyla göstereceğiz. Böylece aynı değişikliğin ana çizgiye ve takımın bilgisayarlarına ulaşmasını izleyebiliriz.

Kaynaklar:

- [Çakışmayı çözmek](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/resolving-a-merge-conflict-using-the-command-line)

## 22. Karar ortak geçmişe nasıl girer?

28:00–29:30 · 90 saniye

Şimdi kabul noktasına geldik. Bu örnekte 500 adayının gerekli inceleme ve doğrulamayı geçtiğini varsayalım. Takımın yetkili kişisi değişikliği main’e birleştiriyor. PR içindeki konuşmalar ve değişiklik gerekçesi daha sonra bulunabilir. Merge yöntemi geçmişin görünümünü etkiler; her yöntem aynı biçimde merge commit üretmez. İlk derste ayrıntılı yöntem seçimini ezberlemek yerine şunu görmek yeterli: bir dalda denemek, göndermek, onaylamak ve ana çizgiye almak ayrı adımlardır. Kabul edilmiş değişiklik artık ortak depodadır. Elif’in bilgisayarı ise henüz otomatik güncellenmiş değildir.

Kaynaklar:

- [Pull request incelemeleri](https://docs.github.com/en/pull-requests/reference/pull-request-reviews)
- [GitHub akışı](https://docs.github.com/en/get-started/using-github/github-flow)
- [git switch](https://git-scm.com/docs/git-switch)

## 23. GitHub güncel. Bilgisayarım da mı?

29:30–30:45 · 75 saniye

Elif önce yerel main dalına geçer, ardından ortak depodaki yenilikleri alır. Pull uzaktaki değişiklikleri getirip yerel dala dahil eder. Önce status ile çalışma alanının durumuna bakmak iyi bir alışkanlık. Buradaki ff only, yerel main ayrı bir yönde ilerlememişse onu ileri taşır; iki tarafta farklı commit’ler varsa durur. O durumda geçmişlerin nasıl birleştirileceğine ayrıca karar verilir. Elif’in ve Deniz’in bilgisayarları ancak bu güncellemeyle ortak kabul edilmiş hâle ulaşır. Push bizden ortak depoya, pull ortak depodan bize doğru ilişkiyi kurar. Bir PR açmakla pull yapmak aynı işlem değildir. Artık projeyi devralacak birinin ne göreceğini düşünelim.

Kaynaklar:

- [git pull](https://git-scm.com/docs/git-pull)
- [GitHub akışı](https://docs.github.com/en/get-started/using-github/github-flow)
- [git switch](https://git-scm.com/docs/git-switch)

## 24. Yeni biri robota nereden başlar?

30:45–32:15 · 90 saniye

Takıma yeni bir öğrenci katıldığını düşünelim. Commit geçmişi kararların izini gösteriyor, ama robotun bağlantısını ve çalıştırma yolunu tek başına açıklamıyor. README bu giriş ihtiyacını karşılar. Ne yaptığımızı, kullanılan donanımı, bağlantı şemasını ve kalibrasyon adımlarını açıkça yazabiliriz. Eşiği yalnız bir sayı olarak kopyalatmak yerine hangi koşullarda yeniden ayarlanması gerektiğini anlatmak daha yararlıdır. Markdown başlıklarla okunabilir bir sayfa oluşturur. README’nin güzel görünmesi kadar gerçek proje dosyalarıyla eşleşmesi de önemlidir. Böylece Elif ve Deniz projeden ayrılsa bile bir sonraki kişi yalnız “son dosya”yı değil, nasıl devam edeceğini gösteren bir rehberi devralır.

Kaynaklar:

- [README dosyası](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)

## 25. Herkes görsün mü, herkes yazsın mı?

32:15–34:00 · 105 saniye

Takım projeyi paylaşmaya hazırlanırken iki soruyu ayırır. Public depo herkesin görmesine ve klonlamasına açıktır; herkesin ana depoya yazma yetkisi olduğu anlamına gelmez. Private depoda erişim yetkili kişilerle sınırlıdır. Ders veya takım çalışmasında hangi dosyaların yayımlanacağını baştan düşünmek gerekir. Kod ve bağlantı şeması paylaşılabilirken parola, erişim anahtarı ve kişisel bilgiler başka tür içeriktir. Hassas bilgi bir commit’e girdiyse son dosyadan silmek önceki kayıtlardan kaldırmaz. Geçmiş tuttuğumuz için bu sorumluluk da görünür hâle gelir. Bir sonraki adım, başka bir projeden alacağımız kodu hangi koşullarda kullanabildiğimizi kontrol etmek.

Kaynaklar:

- [Depo görünürlüğü](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/managing-repository-settings/setting-repository-visibility)
- [Hassas veriyi kaldırmak](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)

## 26. Bulduğumuz kodu hemen kullanalım mı?

34:00–35:30 · 90 saniye

Elif sensör kalibrasyonunu anlatan başka bir depo bulmuş olsun. Hazır kod başlangıcı hızlandırabilir, ama aynı sensör adını görmek uyum garantisi vermez. Kart, bağlantı, kullanılan kütüphane ve örneğin hangi koşullarda çalıştığı incelenir. README ve açık sorunlar bağlam sağlar. Yıldız sayısı ilgi veya kaydetme davranışıyla ilişkilidir; robotumuzda doğruluk ve kullanım yaygınlığı ölçümü değildir. Yakın tarihte güncelleme olması da tek başına üstünlük anlamına gelmez; olgun bir proje daha seyrek değişebilir. Takım önce ihtiyacını, sonra uyumu ve bakım durumunu değerlendirir. Böylece yeni bir kod parçasını anlamadan mevcut projenin içine taşımak yerine gerekçeli seçim yapar.

Kaynaklar:

- [Yıldızların anlamı](https://docs.github.com/en/get-started/exploring-projects-on-github/saving-repositories-with-stars)

## 27. Görebildiğimiz kodu kullanabilir miyiz?

35:30–36:30 · 60 saniye

Bir depoyu tarayıcıda görebilmek, her amaçla kullanma hakkı vermez. Lisans kodun kullanımını, değiştirilmesini ve dağıtılmasını hangi koşullarla kabul ettiğini anlatır. Elif’in bulduğu örneği robota eklerken lisans bildirimini ve varsa bağlı parçaların koşullarını incelemek gerekir. Bazı lisanslar atıf veya lisans metninin korunmasını ister; başka yükümlülükler de bulunabilir. Lisans yoksa “GitHub’da buldum” diyerek sınırsız kullanım varsaymayız. Takım kendi robot projesini başkalarının kullanmasını istiyorsa uygun lisansı açıkça belirtir. Buradaki amaç lisans türlerini ezberlemek değil, görünürlük ile kullanım hakkının aynı karar olmadığını fark etmek.

Kaynaklar:

- [Depo lisansları](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository)

## 28. Dış projeye düzeltmeyi nasıl öneririz?

36:30–38:00 · 90 saniye

Takımın bulduğu örnekte bir açıklama eksikliği fark ettiğini düşünelim. Asıl depoya yazma izni olmayabilir. Public projeyi okumak veya klonlamak için fork şart değildir; kendi hesabımızda gönderim yapabileceğimiz uzak kopya istediğimizde fork kullanabiliriz. Önce katkı kılavuzunu okur, kabul edilen hedef dalı öğreniriz. Sonra fork’u klonlar, iş dalında değiştirir, commit’leri kendi fork’umuza göndeririz. PR’nin kaynağı bizim fork’umuz, hedefi asıl projedir. Bakımcılar öneriyi değerlendirir. Robot takımında öğrendiğimiz kayıt, paylaşım ve inceleme döngüsü burada da çalışır. Yalnız gönderim yaptığımız depo ve kabul kararını veren taraf değişir.

Kaynaklar:

- [Fork kavramı](https://docs.github.com/en/pull-requests/reference/forks)

## 29. Bu proje bizi nasıl anlatır?

38:00–39:30 · 90 saniye

Robot projesi bir portfolyo örneği olacaksa yalnız depo bağlantısı yeterli değildir. Elif ve Deniz hangi sorunu ele aldıklarını, takım içindeki katkılarını ve kararların gerekçesini açıklayabilir. Bir fotoğraf, kısa gösterim ve çalıştırma rehberi projeyi somutlaştırır. Sonuçlarla birlikte çalışmadığı koşulları ve bilinen sınırları dürüstçe yazmak da değerlidir. Ekrandaki profil animasyonu projeleri öne çıkarmanın örneğini gösteriyor. Yeşil katkı kareleri tüm çalışma süresini ölçmez; donanım hazırlığı ve laboratuvar düşüncesi tamamen grafiğe yansımaz. Bir staj değerlendirmesinde amaç yalnız etkinlik sayısı değil, kişinin ne yaptığını ve proje içinde nasıl karar verdiğini anlaşılır kılmaktır.

Kaynaklar:

- [Katkı grafiğinin ölçütleri](https://docs.github.com/en/account-and-profile/reference/profile-contributions-reference)

## 30. Dersten sonra nereden devam edilir?

39:30–40:30 · 60 saniye

Bugün bütün komutları kullanmadık; aynı değişikliğin yolunu anlamaya çalıştık. Daha sonra kavramları tekrar etmek için Pro Git kitabına, bir GitHub işleminin ayrıntısı için GitHub Docs’a bakabilirsiniz. GitHub Skills kendi zamanınızda adım adım alıştırma sunar; sınıfta canlı uygulama yapmamız şart değil. Kurulum ve günlük komutlar sunumun on iki başvuru slaytında da duruyor. Öğrenci araçlarına ihtiyaç duyarsanız GitHub Education’ın güncel resmî koşullarını inceleyebilirsiniz; teklifler ve başvuru gereklilikleri değişebilir. Önce yapmak istediğiniz işi belirleyip ilgili kaynağı açmak, uzun bir araç listesi toplamaktan daha yararlıdır. Son olarak başlangıçtaki dosya karmaşasına dönelim.

Kaynaklar:

- [Pro Git · Türkçe](https://git-scm.com/book/tr/v2)
- [Git ve GitHub kaynakları](https://docs.github.com/en/get-started/start-your-journey/git-and-github-learning-resources)
- [Introduction to GitHub](https://github.com/skills/introduction-to-github)
- [GitHub Education](https://docs.github.com/en/education/about-github-education/github-education-for-students/about-github-education-for-students)
- [GitHub Copilot Student](https://docs.github.com/en/copilot/how-tos/copilot-on-github/set-up-copilot/enable-copilot/set-up-for-students)

## 31. Takımın elinde şimdi ne var?

40:30–42:00 · 90 saniye

Başlangıçta Elif ve Deniz farklı son dosyalarla ne yapacaklarını bilmiyordu. Bu kurgusal örnekte önce geçmişi ve farkı bulduk, sonra sorunu issue ile görünür yaptık. Adayı bir dalda geliştirdik; seçip kaydettik, paylaştık ve incelemeye açtık. Çakışma çıktığında araçtan doğru sensör değerini seçmesini beklemedik. Kabul için gerekçe ve uygun doğrulama gerektiğini gördük; ortak main’i aldıktan sonra yerel kopyaları güncelledik. README ile sonraki kişinin giriş yolunu bıraktık. Kazandığımız şey bir komut zinciri değil, izlenebilir bir proje kararı. Gerçek robotun davranışını yine donanım koşullarında doğrularız; Git bu doğrulamanın kaydını ve paylaşımını düzenlemeye yardım eder.

Kaynaklar:

- [Git ve GitHub kaynakları](https://docs.github.com/en/get-started/start-your-journey/git-and-github-learning-resources)
- [Introduction to GitHub](https://github.com/skills/introduction-to-github)

## 32. Yarın yine çizgiyi kaybederse?

42:00–45:00 · 180 saniye

Kapanışta başlangıçtaki robota yeniden bakıyoruz. Bir gün davranış yine değişirse artık yalnız en son adlı dosyayı aramayız. Geçmişi, satır farkını, ilgili iş kaydını ve değişikliğin gerekçesini inceleyebiliriz. Dosyayı kaydetmek, commit etmek ve push etmek ayrı adımlar; PR ise takımın kabul değerlendirmesidir. Bu ilişkiler kendi projenizde hangi değişikliğin nerede durduğunu anlatmanıza yardım eder. Son üç dakikada soruları alabiliriz. Soru gelmezse, yeni bir takım arkadaşının projeyi devralması için hangi kaydın ve açıklamanın gerekli olduğunu bu robot üzerinden kısaca toparlayabiliriz. Ayrıntılı kurulum ve komutlar sonraki on iki başvuru slaytında duruyor.

Kaynaklar:

- [GitHub Docs](https://docs.github.com/en/get-started/start-your-journey/git-and-github-learning-resources)
- [Pro Git · Türkçe](https://git-scm.com/book/tr/v2)
- [GitHub Skills](https://github.com/skills/introduction-to-github)
- [GitHub Education](https://education.github.com/pack)

## Ek 1. Git kurulumu

Ek slayt · ana anlatım süresinin dışında

Bu ek kurulum sırasında başvuru içindir. Git version komutu kurulu Git'in sürümünü gösterir. Kurulu değilse işletim sistemine uygun yöntem resmî Git sayfasından seçilir. macOS'ta Git'in her cihazda hazır olduğunu varsaymayalım; kullanılan ortam bunu değiştirebilir. Windows'ta Git for Windows ile Git Bash kullanılabilir. Linux'ta dağıtımın paket yöneticisi yaygın yoldur. Kurulum seçeneği Git kavramlarını değiştirmez.

Kaynaklar:

- [Git kurulumu](https://git-scm.com/install/)

## Ek 2. Commit kimliği

Ek slayt · ana anlatım süresinin dışında

Bu üç ayar, kayıtların kimlik bilgisini ve yeni depoların varsayılan dal adını belirler. Ekrandaki ad ve e-posta örnektir; gerçek kullanımda kişinin tercih ettiği doğru bilgiler yazılır. Global ayar kullanıcı hesabının genel ayarıdır; bir depoda ayrıca yerel ayar tanımlanabilir. Commit e-postası herkese açık geçmişte görünüyorsa gizlilik tercihi de düşünülür. Bu bilgiler GitHub'a giriş veya push yetkisi sağlamaz; kimlik doğrulama ayrı konudur.

Kaynaklar:

- [Git kimlik ayarları](https://git-scm.com/book/en/v2/Getting-Started-First-Time-Git-Setup)

## Ek 3. Editör ve terminal

Ek slayt · ana anlatım süresinin dışında

VS Code bir seçenek, Git ise ayrı araçtır. Editörün Source Control görünümü değişen dosyaları, hazırlık alanını ve commit işlemlerini görsel olarak sunabilir. Entegre terminalden aynı komutlar çalıştırılabilir. Terminalin ne yaptığı açıkça görünür; grafik arayüzde farkları incelemek kolay olabilir. İki yol birbirini dışlamaz ve biri tek başına kavramları anlama garantisi değildir. Ana dersteki çalışma alanı, hazırlık, yerel depo ve uzak depo modeli her iki kullanımda da geçerlidir.

Kaynaklar:

- [VS Code sürüm kontrolü](https://code.visualstudio.com/docs/sourcecontrol/overview)

## Ek 4. .git ve .gitignore

Ek slayt · ana anlatım süresinin dışında

Git klasörü commit'ler, dallar ve ayarlar için yerel veritabanını içerir. Elle silmek veya düzenlemek yerel geçmişe zarar verebilir. Gitignore ise henüz izlenmeyen dosyalardan hangilerinin normal izleme kapsamına alınmayacağını belirtir. Derleme çıktıları ve ortam ayarları için kullanılabilir. Fakat daha önce commit edilmiş bir dosyayı gitignore'a yazmak geçmişten kaldırmaz. Hassas bir bilgi yanlışlıkla gönderildiyse yalnız ignore eklemek yeterli çözüm değildir; ilgili erişim bilgisi iptal edilmeli ve resmî temizleme süreci izlenmelidir.

Kaynaklar:

- [gitignore](https://git-scm.com/docs/gitignore)
- [Hassas veriyi kaldırmak](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)

## Ek 5. SSH anahtar çifti

Ek slayt · ana anlatım süresinin dışında

SSH kimlik doğrulamasında açık ve özel anahtar çifti kullanılır. Ed25519 güncel belgelerde önerilen anahtar türüdür; eski sistemlerde alternatif gerekebilir. Açık anahtarın pub dosyası GitHub hesabındaki SSH and GPG keys bölümüne eklenir. Özel anahtar paylaşılmaz ve depoya yüklenmez. Komut örneğindeki e-posta yalnız etikettir. Anahtara parola eklemek koruma sağlar; bir SSH ajanı bu anahtarı oturumda kullanmayı kolaylaştırır. Yeni anahtar oluştururken var olan dosyanın üzerine istemeden yazılmaması gerekir.

Kaynaklar:

- [SSH anahtarı ve ajanı](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)
- [GitHub'a açık anahtar eklemek](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account)

## Ek 6. SSH ajanı ve bağlantı

Ek slayt · ana anlatım süresinin dışında

Bu komutlar Bash veya Git Bash için kısa bir ajan örneği. macOS Anahtar Zinciri ile çalışma ve Windows OpenSSH hizmeti için ayrıntılar farklıdır. Her işletim sistemine aynı yapılandırmayı zorunluymuş gibi kopyalamamak gerekir. SSH testindeki ilk bağlantıda sunucu kimliği kontrol edilir; doğrulama için GitHub'ın yayımladığı anahtar parmak izleri kullanılır. Başarılı kimlik doğrulama mesajı GitHub hesabına SSH ile erişildiğini gösterir; GitHub genel kabuk erişimi sağlamaz. Anahtar bağlantısı başarılı olsa bile depo yazma izinleri ayrıca değerlendirilir.

Kaynaklar:

- [SSH anahtarı ve ajanı](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)

## Ek 7. Yerel klasörden depoya

Ek slayt · ana anlatım süresinin dışında

Init mevcut klasörde yerel bir Git deposu başlatır. Örnekte main dal adını açıkça veriyoruz ve var olan README ile robot kodunu ilk kayda alıyoruz. Remote add, origin adına uzak adresi bağlar. Origin yaygın bir addır; özel bir parola veya hizmet değildir. Init GitHub'da depo oluşturmaz. Buradaki uzak depoyu ayrıca açılmış ve boş varsayıyoruz. Uzak tarafta README gibi başlangıç commit'leri varsa bağımsız iki geçmiş yaratmak yerine depoyu klonlamak daha sade bir başlangıç olabilir.

Kaynaklar:

- [git init](https://git-scm.com/docs/git-init)
- [git remote](https://git-scm.com/docs/git-remote)

## Ek 8. İlk gönderim ve izleme

Ek slayt · ana anlatım süresinin dışında

İlk push sırasında u seçeneği yerel main ile uzak origin main arasında izleme bağlantısı kurar. Bundan sonra uygun ayarlarda kısa push ve pull komutları hedefi bu bağlantıdan öğrenebilir. Bu izlenen uzak dal bazen upstream diye adlandırılır. Fork akışında asıl projeye verilen upstream uzak adıyla aynı kullanım değildir; kelime iki farklı bağlamda görülebilir. Dal adı main olmak zorunda değildir, ancak sunumdaki örnekler main kullanır. Her durumda gerçek dal adı ve uzak adres kontrol edilir.

Kaynaklar:

- [git branch](https://git-scm.com/docs/git-branch)

## Ek 9. Dal ve fark komutları

Ek slayt · ana anlatım süresinin dışında

Switch c yeni dalı oluşturur ve o dala geçer. Branch listesinde yıldız etkin dalı gösterir. İki dalı diff ile karşılaştırırken ilk ad önceki, ikinci ad sonraki taraftır; eksi ve artı işaretleri buna göre okunur. Üç noktalı karşılaştırma ise ortak başlangıca göre ikinci dalın getirdiği değişiklikleri gösterir. Tab tamamlama kullanılabiliyorsa feature gibi dalın başlangıcı yazılır; dalın ortasındaki bir kelimenin her ortamda tamamlanması beklenmez. Kabuk ve tamamlama ayarları sonucu etkiler.

Kaynaklar:

- [git switch](https://git-scm.com/docs/git-switch)
- [git diff](https://git-scm.com/docs/git-diff)

## Ek 10. Geri alırken niyeti seç

Ek slayt · ana anlatım süresinin dışında

Geri alma deyince önce neyi geri almak istediğimizi belirlemek gerekir. Yanlışlıkla add edilen dosyayı restore staged ile hazırlıktan çıkarabiliriz; düzenleme dosyada kalır. Paylaşılmış bir commit'in etkisini geri almak için revert yeni bir kayıt üretir, böylece ortak geçmiş korunur. Reset ise dalın işaret ettiği kaydı ve seçilen moda göre hazırlık alanını veya dosyaları değiştirebilir. Varsayılan mixed reset çalışma dosyalarını korur fakat geçmiş konumunu taşır. Bu yüzden reset ile revert aynı amaç ve sonuçlara sahip değildir.

Kaynaklar:

- [git restore](https://git-scm.com/docs/git-restore)
- [git revert](https://git-scm.com/docs/git-revert)
- [git reset](https://git-scm.com/docs/git-reset)

## Ek 11. Hard reset ve kurtarma sınırları

Ek slayt · ana anlatım süresinin dışında

Hard reset dalı seçilen commit'e taşırken hazırlık alanını ve izlenen çalışma dosyalarını o hâle eşitler. Commit edilmemiş düzenlemeler kaybolabilir; yoluna çıkan bazı izlenmeyen dosyalar da etkilenebilir. Önceden commit edilmiş bir kayıt bazen yerel reflog üzerinden bulunabilir, bu yüzden bütün durumlar için geri alınamaz demek doğru değildir. Ama reflog bir genel yedek değildir ve sonsuza kadar her şeyi tutmaz. Özellikle hiç commit edilmemiş çalışmanın kurtarılacağı varsayılmamalıdır. Önce status ve değişiklikler incelenir; komutun etkisi anlaşılmadan hard reset kullanılmaz.

Kaynaklar:

- [git reset](https://git-scm.com/docs/git-reset)
- [git reflog](https://git-scm.com/docs/git-reflog)

## Ek 12. Komutlara kısa bakış

Ek slayt · ana anlatım süresinin dışında

Bu son ek günlük akışa yeniden bakmak için kısa bir başvuru sayfası. Clone ile başlanır, fakat sonraki commit için önce gerçek bir dosya düzenlemesi yapılır. Status durumumuzu gösterir, add seçer, commit kaydeder ve push gönderir. Takımın yeniliklerini pull ile alırız. Ayrı bir iş için dal açılır; değişiklikler PR ile incelenebilir. Bütün komutları her seferinde sırayla çalıştırmak gerekmez. Hangi adımın gerekli olduğuna, değişikliğin çalışma alanında mı hazırlıkta mı yerel geçmişte mi olduğuna bakarak karar veririz.

Kaynaklar:

- [Git ve GitHub kaynakları](https://docs.github.com/en/get-started/start-your-journey/git-and-github-learning-resources)
