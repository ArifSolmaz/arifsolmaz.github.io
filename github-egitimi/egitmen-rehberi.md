# Git ve GitHub: Tek Projede Temeller

32 ana slayt, 12 ek slayt. Ana anlatım ve sorular toplam 45 dakika.

Canlı gösterim, sınıf içi uygulama ve zorunlu ödev yoktur. Ek slaytlar ana anlatım süresinin dışındadır.

## 1. Git ve GitHub

00:00–00:45 · 45 saniye

Hoş geldiniz. Bugün bir robot projesinin ilk dosyasından ekip çalışmasına kadar aynı hikâyeyi izleyeceğiz. Önce GitHub'ın bize ne kazandırdığını, ardından bu kazancın Git ile nasıl oluştuğunu konuşacağız. Dersin sonunda komut ezberlemekten çok, bir değişikliğin nerede durduğunu ve takıma nasıl ulaştığını anlayabilmenizi istiyorum. Kod, devre şeması ve açıklamayı aynı proje içinde düşünmek, yalnız yazılımda değil mekatronik projelerinde de işimizi kolaylaştırır.

Kaynaklar:


## 2. 45 dakikalık rota

00:45–01:30 · 45 saniye

Dersi dört bölümde izleyeceğiz. İlk bölümde dağınık dosya sorununu çözerek temel kavramları yerleştireceğiz. İkinci bölümde bir dosya değişikliğinin bilgisayardan GitHub'a giden yolunu takip edeceğiz. Üçüncü bölümde iki kişinin aynı projede nasıl çalıştığını göreceğiz. Son bölümde hazır kod seçimi, portfolyo ve öğrenci kaynakları var. Son üç dakikayı sorulara ayırdım. Kurulum ve ayrıntılı komutlar sunumun sonundaki eklerde duruyor; ana akışın odağı kavramlar ve aralarındaki ilişkiler.

Kaynaklar:


## 3. Son dosya hangisi?

01:30–03:00 · 90 saniye

Bir robot takımında Elif motorları, Deniz çizgi sensörlerini düzenliyor. Kod mesaj grubunda paylaşıldıkça robot, robot_final ve robot_final_SON gibi kopyalar ortaya çıkıyor. Dosya adından hangisinin çalıştığını, kimin hangi değişikliği yaptığını anlayamıyoruz. İki kişinin düzeltmesini birleştirmek de elle karşılaştırma gerektiriyor. Git'in çözümü her kayıt için yeni bir dosya adı üretmek değil, projenin geçmişini tutmak. Böylece bugünkü dosya ile geçmişteki kayıtlar birbirinden ayrılıyor. Yine robot.ino dosyası üzerinde çalışıyoruz; yanında hangi değişikliklerin hangi sırayla kaydedildiğini anlatan bir zaman çizgisi oluşuyor. Bu çizgi yalnız seçip commit ettiğimiz değişiklikleri içeriyor.

Kaynaklar:

- [Commit geçmişini incelemek](https://git-scm.com/book/en/v2/Git-Basics-Viewing-the-Commit-History)

## 4. Git ve GitHub

03:00–04:30 · 90 saniye

Bu iki adı ayırmak bütün dersin anahtarı. Git bilgisayarımızdaki sürüm kontrol aracı. Dosyalardaki değişiklikleri kaydetmek ve yerel geçmişi incelemek için internet gerekmiyor. GitHub ise Git depolarını barındıran ve bu depolar etrafında ekip çalışmasını düzenleyen platform. Dolayısıyla GitHub hesabına sahip olmak, bilgisayarda yaptığımız her değişikliğin kendiliğinden internete gideceği anlamına gelmiyor. İki taraf arasındaki aktarımı birazdan push ve pull ile açıklayacağız. GitHub'ı tarayıcıdan, Git'i terminalden veya bir grafik arayüzden kullanabiliriz. Menüleri farklı olsa da temel kavramlar aynıdır. Burada önemli olan hangi düğmeye basıldığı kadar işlemin neyi kaydettiğini anlamak.

Kaynaklar:

- [GitHub nedir?](https://docs.github.com/en/get-started/start-your-journey/what-is-github)

## 5. Depo dosya ve geçmiştir

04:30–05:45 · 75 saniye

Repository kelimesini depo diye kullanacağız. Depo yalnız internette duran bir klasör değildir; projenin dosyalarıyla birlikte kaydedilmiş geçmişini de taşır. Robot örneğimizde robot.ino kodu, IR sensörlerin bağlantı şeması, README açıklaması ve birkaç proje fotoğrafı aynı bağlamda duruyor. Animasyon bu dosyaların GitHub'da bir araya gelişini gösteriyor. Tarayıcıdan dosya yüklerken de bir commit oluşturulur. Yerelde çalışırkense kayıt ve gönderim iki ayrı işlemdir. Metin dosyalarında satır farklarını kolayca inceleyebiliriz. Fotoğraf ve PDF gibi dosyalar da saklanabilir; ancak onların değişimini metin kadar ayrıntılı karşılaştırmayı beklememeliyiz.

Kaynaklar:

- [Depolar](https://docs.github.com/en/repositories/creating-and-managing-repositories/about-repositories)

## 6. Commit bir kayıt noktası

05:45–07:00 · 75 saniye

Commit, projenin belirli bir andaki hâlinin kayıt noktasıdır. Bir dosyayı editörde kaydetmek çalışma dosyasını değiştirir; bu işlem tek başına Git geçmişine girmez. Değişiklikleri seçip commit ettiğimizde geçmişte incelenebilen bir kayıt oluşur. Mesajı da bu kaydın neyi amaçladığını anlatır. Robot için “güncelleme” yerine “IR sensör eşiği artırıldı” demek, aylar sonra neden değişiklik yapıldığını anlamayı kolaylaştırır. Commit'in bir kimliği vardır; önceki kayıtlarla ilişkisi sayesinde zaman çizgisi kurulur. Bu kayıt bilgisayarda oluşturulduysa hâlâ yereldedir. Takımın GitHub'da görebilmesi için gönderilmesi gerekir. Bu ayrımı birazdan dört bölgeyle somutlaştıracağız.

Kaynaklar:

- [git commit](https://git-scm.com/docs/git-commit)

## 7. README giriş kapısıdır

07:00–08:15 · 75 saniye

README, projeyi ilk kez gören kişiye rehberlik eder. Kodun bütün ayrıntılarını burada anlatmak gerekmiyor; robotun ne yaptığı, hangi malzemeleri kullandığı ve nasıl çalıştırıldığı anlaşılmalı. Bizim örneğimizde çizgi algılayan IR sensörler ve kontrol kartı Arduino. Bir bağlantı şeması, bir fotoğraf ve kullanılan kütüphanelerin adları açıklamayı tamamlar. README.md dosyası Markdown biçimindedir; başlık ve listeler basit işaretlerle yazılır. GitHub bunu okunabilir bir sayfa olarak gösterir. İyi açıklama takım arkadaşına olduğu kadar projeyi değerlendiren hocaya veya staj başvurusunu inceleyen kişiye de yardım eder. Çalıştırma adımlarının gerçekten projeyle eşleşmesi, güzel görünmesinden daha önemlidir.

Kaynaklar:

- [README dosyası](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)

## 8. Kim görebilir?

08:15–09:15 · 60 saniye

Depoyu açarken görünürlüğünü seçiyoruz. Public depo herkes tarafından görülebilir ve klonlanabilir; bu, herkesin ana depoyu değiştirebildiği anlamına gelmez. Yazma yetkisi ayrı bir izindir. Private depo ise erişimi yetkili kişilerle sınırlar. Bir ders veya takım projesinde hangi dosyaların paylaşılacağına baştan karar vermek gerekir. Bağlantı şeması ve robot kodu başka, parola veya erişim anahtarı başka tür bilgidir. Hassas bir bilgi geçmişe girdiyse son dosyadan silmek önceki commit'leri ortadan kaldırmaz. Bu yüzden paylaşmadan önce dosyaların içeriği ve proje izinleri düşünülmelidir. Görünürlük tercihiyle birlikte lisans konusuna da kapanışta döneceğiz.

Kaynaklar:

- [Depo görünürlüğü](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/managing-repository-settings/setting-repository-visibility)
- [Hassas veriyi kaldırmak](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)

## 9. Dün çalışıyordu

09:15–10:45 · 90 saniye

Robot dün çizgiyi takip ediyordu; bugün davranışı farklı. İlk tepki son dosyayı suçlamak olabilir. Geçmişe baktığımızda ise değişikliğin hangi commit ile geldiğini bulabiliriz. Animasyonda eşiğin 500'den 900'e geçtiği bir kayıt var. Ders kitindeki örnek robot, IR sensör değerlerini analogRead ile okur; bu sayılar sensör okumasını karşılaştırmak için seçilmiş örnek eşiklerdir. Bütün robotlar için geçerli kalibrasyon değerleri değildir. Kayıtta yazar, zaman ve açıklama bulunur. Bunlar değişikliği kimin yaptığını gösterir, ama doğru olduğunu tek başına kanıtlamaz. İncelememiz ve robot üzerinde doğrulamamız gerekir. Geçmişin değeri tartışmayı hatırlamak yerine kaydedilmiş hâlleri karşılaştırabilmektir.

Kaynaklar:

- [Commit geçmişini incelemek](https://git-scm.com/book/en/v2/Git-Basics-Viewing-the-Commit-History)

## 10. Satır farkı nasıl okunur?

10:45–12:00 · 75 saniye

Diff kelimesi fark görünümünü anlatır. Eksi işareti karşılaştırmanın önceki tarafındaki satırı, artı işareti sonraki tarafındaki satırı gösterir. İki satır iki farklı sensörün çıktısı değil, aynı değişkenin eski ve yeni değeridir. Bu örnekte IR sensörün analog okuma eşiği 500'den 900'e çıkarılmış. Renkler olmasa bile artı ve eksi işaretlerinden fark okunabilir. Bu görünüm kod incelemesinde işe yarar: bütün dosyayı baştan okumak yerine değişen bölgeye odaklanırız. Fakat bağlamı da anlamalıyız; küçük bir sayı değişikliği robot davranışını etkileyebilir. İki dalı karşılaştırırken hangi tarafın önce ve hangi tarafın sonra olduğunu açık yazmak önemlidir.

Kaynaklar:

- [git diff](https://git-scm.com/docs/git-diff)

## 11. Değişiklik dört yerde durur

12:00–13:45 · 105 saniye

Bu dört bölgeyi dersin merkezine yerleştirelim. Çalışma alanı dosyaları açıp düzenlediğimiz yerdir. Hazırlık alanı bir sonraki kayda hangi değişikliklerin gireceğini seçer. Yerel depo bilgisayardaki commit geçmişidir. Uzak depo ise burada GitHub'da paylaştığımız geçmiş. Bunlar dört ayrı proje üretmek anlamına gelmiyor; aynı projenin farklı durumlarını anlatıyor. README'yi düzenlemek ilk bölgede olur. Add değişikliği hazırlığa alır. Commit hazırlanan hâli yerel geçmişe yazar. Push kayıtları uzak depoya gönderir. GitHub'da bir değişiklik yapılırsa bilgisayardaki kopya kendiliğinden güncellenmez; o değişikliği getirmek gerekir. Şimdi bu okların her birini aynı robot deposunda sırayla izleyeceğiz.

Kaynaklar:

- [Git: çalışma modeli](https://git-scm.com/book/en/v2/Getting-Started-What-is-Git%3F)

## 12. Clone ile yerel kopya

13:45–15:00 · 75 saniye

Clone, var olan bir Git deposunun yerel kopyasını oluşturur. Normal bir klonlamada dosyalarla birlikte kayıtlı geçmiş ve uzak depo adresi de gelir. Örneğin robot-projem deposunu bilgisayara aldığımızda README'yi düzenleyebilir ve önceki kayıtları inceleyebiliriz. Ekrandaki depo-adresi, gerçek projenin klonlama adresi için yer tutucudur. Herkese açık bir depo HTTPS üzerinden okunurken genellikle hesapla kimlik doğrulamak gerekmez. Özel bir depo için erişim yetkisi gerekir. Klonlayabilmek, projeye değişiklik gönderebilmekle aynı şey değildir. Download ZIP ise çoğunlukla seçili hâlin dosyalarını verir; yerel Git geçmişini oluşturmaz. Geçmişle çalışmak istediğimizde bu ayrım önem kazanır.

Kaynaklar:

- [Depoyu klonlamak](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository)

## 13. Önce dosyayı değiştiririz

15:00–16:15 · 75 saniye

Klonlama ile kayıt arasında mutlaka bir değişiklik olmalı. Robotun README dosyasına IR sensörlerin görevini ve bağlantı şemasının yerini eklediğimizi düşünelim. Dosyayı editörde kaydettik; şimdi çalışma alanı önceki commit'ten farklı. Git status bu durumu gösterir. Henüz yeni commit yok ve GitHub'da da yeni içerik görünmez. Bu noktada metni tekrar okuyup yanlış bir bilgi ekleyip eklemediğimizi kontrol edebiliriz. Dikkat edilmesi gereken küçük ama önemli bir ayrıntı var: bir komut listesinde clone'dan hemen sonra add yazılması, sanki klonlama kendi başına yeni kayıt üretmiş gibi anlaşılabilir. Asıl işi yapan düzenleme burada gerçekleşiyor; sonraki işlemler bu değişikliği seçiyor ve kaydediyor.

Kaynaklar:

- [git status](https://git-scm.com/docs/git-status)

## 14. Add ile değişikliği seçeriz

16:15–17:45 · 90 saniye

Add bir yükleme komutu değil; bir sonraki commit'in içeriğini hazırlama komutu. Burada yalnız README değişikliğini seçiyoruz. Robot kodunda aynı anda başka bir deneme varsa onu bu açıklama kaydına katmak zorunda değiliz. Git diff cached hazırlanan farkı gösterir; birazdan kaydedeceğimiz şey budur. Bir dosyayı add ettikten sonra yeniden düzenlersek hazırlık alanında önceki seçilmiş hâli kalabilir. Yeni düzenlemeyi de kayda almak istiyorsak yeniden add yaparız. Bu ayrıntı hazırlığın bir klasörü tamamen taşımak değil, değişikliği belirli bir anda seçmek olduğunu gösterir. Küçük ve anlaşılır kayıtlar üretmek, sonraki kod incelemesini ve gerektiğinde geri almayı kolaylaştırır.

Kaynaklar:

- [git add](https://git-scm.com/docs/git-add)

## 15. Commit ile yerelde kaydederiz

17:45–19:15 · 90 saniye

Hazırladığımız README değişikliğini şimdi commit ile geçmişe yazıyoruz. Mesaj “IR sensör bağlantıları README'de açıklandı” diyor; böylece dosyanın hangi amaçla değiştiğini anlayabiliyoruz. Git log oneline geçmişi kısa bir liste hâlinde gösterir. Listede yeni kaydın kimliği ve açıklaması bulunur. Daha önceki robot kodu kaydı da geçmişte kalır. Bu işlem için internet şart değildir ve bilgisayardaki yerel depo güncellenir. Commit mesajı bir sonuç iddiası da taşıyabilir; bu yüzden “sensör düzeltildi” yazıyorsak gerçekten neyi doğruladığımızı açıklamak iyi olur. Buradaki değişiklik yalnız belgede; sensörün çalıştığına dair bir test sonucu üretmiyor. Şimdi bu yerel kaydı takımın ortak deposuna göndereceğiz.

Kaynaklar:

- [git commit](https://git-scm.com/docs/git-commit)
- [Commit geçmişini incelemek](https://git-scm.com/book/en/v2/Git-Basics-Viewing-the-Commit-History)

## 16. Push ile GitHub'a göndeririz

19:15–20:30 · 75 saniye

Push yerel commit'leri uzak depoya gönderir. İşlem başarılı olunca takım README açıklamasını GitHub'da görebilir. Push dosyayı editörde kaydetmenin başka adı değildir; commit edilmemiş çalışma alanı değişikliklerini doğrudan göndermiyoruz. Gönderim için uzak adres, hedef dal, yazma izni ve uygun kimlik doğrulama gerekir. HTTPS için bir erişim yöntemi veya SSH anahtarı kullanılabilir; ayrıntıları ek slaytlarda var. Burada hesabın normal parolasını terminalde kullanmak yeterli kabul edilmemelidir. İlk gönderimde izleme bağlantısı ayarlamak gerekebilir. Ayrıca uzakta yeni kayıtlar varsa Git gönderimi reddedebilir. Bu durumu zorla üzerine yazmak yerine takımın değişikliklerini anlayıp yerel çalışmaya dahil etmek gerekir.

Kaynaklar:

- [git push](https://git-scm.com/docs/git-push)

## 17. Pull ile yenilikleri alırız

20:30–22:00 · 90 saniye

Deniz robot kodunu GitHub'a gönderdiyse Elif'in bilgisayarındaki dosya kendi kendine değişmez. Pull uzaktaki güncellemeleri getirip yerel dala dahil eder. Önce status ile çalışma alanında commit edilmemiş değişiklik olup olmadığına bakılır. Buradaki ff-only seçeneği, yerel geçmiş ayrı bir yöne gitmemişse dalı ileri taşır. İki tarafta da farklı yeni commit'ler oluşmuşsa durur; bu durumda merge veya rebase gibi bir yöntemle geçmişlerin nasıl birleştirileceği seçilir. Genel pull davranışı ayarlara bağlı olabilir. Başlangıç için asıl ilişkiyi hatırlamak yeterli: push bizden ortak depoya, pull ortak depodan bize. GitHub'daki en yeni sürümü görebilmek ile bilgisayardaki kopyanın güncel olması aynı şey değildir.

Kaynaklar:

- [git pull](https://git-scm.com/docs/git-pull)

## 18. Issue işi görünür kılar

22:00–23:30 · 90 saniye

Takımın işleri mesaj grubunda kaybolmasın diye issue açarız. Issue bir hata bildirimi, yapılacak iş veya geliştirme önerisi olabilir. Robot örneğimizde “IR sensör eşiğini incele” başlıklı bir kayıt düşünelim. Açıklamada robotun hangi koşulda çizgiyi kaybettiğini, beklenen davranışı ve ilgili dosyayı yazarız. Bir sorumlu atanabilir ve etiket eklenebilir. İş numarası konuşmalarda ve pull request içinde referans verir. Animasyonda bir fotoğraf işi gösteriliyor; aynı düzen sensör hatası veya README eksikliği için de kullanılabilir. Issue kapandığında geçmişi yok olmaz. Hangi kararların verildiğini daha sonra bulabiliriz. Böylece “ne yapacağız?” sorusu kod dosyasından ayrı ama projeyle bağlantılı durur.

Kaynaklar:

- [Issue kavramı](https://docs.github.com/en/issues/tracking-your-work-with-issues/learning-about-issues/about-issues)

## 19. Dal ayrı bir çalışma çizgisidir

23:30–25:00 · 90 saniye

Branch yani dal, projede ayrı bir çalışma çizgisi oluşturur. Ana çizgideki mevcut commit'ten IR sensör eşiğini düzenlemek için yeni bir dal açtığımızı düşünelim. O dalda yaptığımız yeni kayıtlar main dalını otomatik değiştirmez. Başka biri README üzerinde ayrı bir dalda çalışabilir. Branch açmayı bütün proje klasörünü fiziksel olarak kopyalamak gibi düşünmek pratikte kolay görünse de Git'in modeli böyle değildir. Dal adı bir commit'e işaret eder ve yeni kayıtlarla ilerler. Dosyaları hangi daldan açtığımız, çalışma alanında gördüğümüz hâli belirler. Dal bize düzenli çalışmayı sağlar; yapılan değişikliğin iyi veya hatasız olduğunu garanti etmez. Birleştirmeden önce inceleme ve doğrulama gerekir.

Kaynaklar:

- [Git dalları](https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell)

## 20. Başlangıç için sade dal düzeni

25:00–26:15 · 75 saniye

Başlangıç düzeyindeki robot takımı için bir ana dal ve kısa süreli iş dalları yeterli bir düzen. Ana dalı bu sunumda main diye adlandırıyoruz. Başka projelerde master veya farklı adlar görülebilir; komutta gerçek dal adı kullanılır. Büyük projelerde dev, staging veya sürüm dalları bulunabilir, fakat bunları herkesin uygulaması gereken tek doğru düzen olarak sunmamak gerekir. Dışarıdaki bir projeye katkı verirken hedef dalı alışkanlıkla seçmeyiz. Önce CONTRIBUTING dosyasına veya katkı belgelerine bakarız. Projenin bakımcıları hangi dala ve hangi koşullarda katkı kabul edildiğini belirler. Dal sayısını artırmanın amacı düzen kurmak olmalı; anlaşılması güç bir süreç yaratmak değil.

Kaynaklar:

- [Dal düzenleri](https://git-scm.com/book/en/v2/Git-Branching-Branching-Workflows)

## 21. Pull request bir öneridir

26:15–28:00 · 105 saniye

Pull request, bir dalı başka bir dala birleştirme önerisidir. Kaynak bizim sensör eşiği dalımız, hedef main. Bir PR açmak değişikliği hemen kabul ettirmek anlamına gelmez; inceleme için görünür hâle getirir. Başlık somut işi anlatır. Açıklamada sorun, değişiklik ve doğrulama yer alır. Burada 500 değerinden 900 değerine geçen eşik var. Gerçek projede hangi koşullarda denendiğini yazmak gerekir; sunumdaki örnek için yapılmamış bir testi yapılmış gibi göstermiyoruz. PR aynı zamanda ilgili issue'ya bağlantı kurabilir. “Ne yapacağız?” sorusu issue'da, “Bu çözümü kabul ediyor muyuz?” sorusu PR'da tartışılır. Kaynak ve hedef dalı doğru seçmek, içerik kadar önemlidir.

Kaynaklar:

- [Pull request](https://docs.github.com/en/pull-requests/reference/pull-requests)

## 22. İnceleme çözümü güçlendirir

28:00–29:30 · 90 saniye

Kod incelemesi yalnız yazım hatası aramak değildir. Takım arkadaşı eşiğin neden değiştiğini, analog okuma değerinin hangi koşullarda ölçüldüğünü ve başka bir davranışı etkileyip etkilemediğini sorabilir. GitHub'ın Files changed görünümünde yorum doğrudan ilgili satıra bağlanır. Yazar geri bildirime göre aynı dalda yeni commit oluşturup gönderirse PR güncellenir; baştan yeni bir PR açması gerekmez. Bir projede otomatik kontroller varsa onların sonuçları da görünür. İncelemenin amacı kişiyi değerlendirmekten çok çözümü anlaşılır ve güvenilir hâle getirmektir. Onay vermekle birleştirme yetkisine sahip olmak aynı şey olmayabilir. Takımın kuralları hangi koşullarda değişikliğin ana dala alınacağını belirler.

Kaynaklar:

- [Pull request incelemeleri](https://docs.github.com/en/pull-requests/reference/pull-request-reviews)

## 23. Birleştirme sonrası herkes günceller

29:30–30:45 · 75 saniye

İnceleme tamamlanınca değişiklik GitHub'da main dalına birleştirilebilir. Ancak bizim bilgisayardaki main hâlâ önceki commit'te olabilir. Bu yüzden yerelde main'e geçip uzaktaki yeni hâli alırız. Slayttaki ff-only örneği yerel main'de ayrı yeni commit olmadığı varsayımıyla ilerler. Bundan sonra sensör eşiği değişikliği ana çalışma çizgisinde görünür. İş dalı artık gerekmiyorsa temizlenebilir. Main’e alınan içerik korunur. Geçmişin biçimi birleştirme yöntemine bağlıdır. GitHub'da farklı birleştirme yöntemleri vardır ve hepsi aynı geçmiş biçimini üretmez. Başlangıçta yöntem ayrıntısından önce şu döngüyü oturtmak önemli: değişikliği öner, incele, kabul et ve takımın yerel kopyalarını güncelle.

Kaynaklar:

- [GitHub akışı](https://docs.github.com/en/get-started/using-github/github-flow)
- [git switch](https://git-scm.com/docs/git-switch)

## 24. Çakışma kararı bize bırakır

30:45–32:15 · 90 saniye

Git farklı bölgelerdeki değişiklikleri çoğu zaman otomatik birleştirir. Ama ortak başlangıçta 500 olan aynı eşik, bir dalda 900 diğer dalda 700 yapılmışsa hangi değerin doğru olduğunu bilemez. O noktada çakışma işaretleriyle durur. Bu örnekte sensör eşiği dalındayız ve main'i o dala birleştiriyoruz. HEAD bölümünde 900, gelen main tarafında 700 var. HEAD sözcüğü her zaman “doğru olan taraf” anlamına gelmez; bulunduğumuz konumu gösterir. Bir dosyanın bir dalda silinip diğerinde değiştirilmesi de çakışma doğurabilir. Git'in durması bütün projenin bozulduğu anlamına gelmez. Takımın çözmesi gereken bir kararı görünür kılar.

Kaynaklar:

- [Birleştirme çakışmaları](https://docs.github.com/en/pull-requests/reference/merge-conflicts)

## 25. Çakışmayı anlamıyla çözeriz

32:15–34:00 · 105 saniye

Çözüm, iki seçenekten rastgele birini kabul etmek değildir. Eşiği değiştiren iki kişinin gerekçesini okuyup robotun beklenen davranışına karar veririz. Son dosyada tek ve anlamlı bir eşik kalmalı; çakışma işaretleri kaldırılmalı. Bazen iki değişikliği birleştirmek veya üçüncü bir çözüm yazmak gerekir. Dosyayı kaydettikten sonra projeye uygun doğrulama yapılır. Ardından add ve commit ile bu merge çözümü tamamlanır. Slayttaki komutlar merge örneği içindir; rebase sırasında devam adımı farklıdır. VS Code gibi editörler seçenekleri kolaylaştırır, fakat hangi içeriğin doğru olduğuna bizim karar vermemiz gerekir. İşaretleri silmek teknik işlemi bitirebilir; gerçek sorunun çözüldüğünü anlamak ise kodu ve proje davranışını incelemeyi gerektirir.

Kaynaklar:

- [Çakışmayı çözmek](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/resolving-a-merge-conflict-using-the-command-line)

## 26. Hazır kodu nasıl seçeriz?

34:00–35:30 · 90 saniye

Çizgi izleyen robota ayrıca HC-SR04 mesafe sensörü eklemek istediğimizi düşünelim. GitHub'da bir kütüphane bulmak başlangıcı hızlandırabilir. Ama yıldızı en çok olanı seçmek yeterli bir değerlendirme değildir. Yıldız bir kişinin projeyi kaydetmesi veya ilgi göstermesiyle ilişkilidir; kaç kişinin üründe kullandığını ya da kodun doğru olduğunu doğrudan ölçmez. Önce sensör ve Arduino ortamımızla uyuma bakarız. README'de bağlantı bilgisi ve örnek var mı, açık sorunlar neleri anlatıyor, projenin bakımı sürüyor mu diye inceleriz. Yakın tarihte güncelleme olması tek başına üstünlük de değildir; oturmuş bir proje daha seyrek değişebilir. Son olarak lisans koşullarını kontrol ederiz. Bu slayt bir belirli kütüphaneyi tavsiye etmiyor, seçim ölçütlerini gösteriyor.

Kaynaklar:

- [Yıldızların anlamı](https://docs.github.com/en/get-started/exploring-projects-on-github/saving-repositories-with-stars)

## 27. Lisans kullanım şartlarını anlatır

35:30–36:30 · 60 saniye

Bir depoyu public görmek, bütün kullanım haklarının serbest olduğu sonucunu vermez. Lisans kodun hangi koşullarda kullanılabileceğini, değiştirilebileceğini ve dağıtılabileceğini açıklar. Robot projesine bir kütüphane eklerken hem o kütüphanenin hem bağlı olduğu parçaların koşullarına bakılır. Bazı lisanslar atıf veya lisans bildirimini korumayı ister; başka yükümlülükler de olabilir. Lisans yoksa “GitHub'da buldum, o yüzden her yerde kullanabilirim” varsayımıyla ilerlememek gerekir. Kendi projemizi başkalarının kullanmasını istiyorsak uygun lisansı açıkça belirtmek de işe yarar. Buradaki amaç lisans türlerini ezberlemek değil, paylaşım kararının teknik dosyalardan ibaret olmadığını fark etmek.

Kaynaklar:

- [Depo lisansları](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository)

## 28. Fork ile dış projeye katkı

36:30–38:00 · 90 saniye

Kendi takımımızın deposuna yazma yetkimiz olabilir; dışarıdaki bir açık kaynak projede olmayabilir. Public projeyi okumak ve klonlamak için fork şart değildir. Ama kendi hesabımızda gönderim yapabileceğimiz bir uzak kopya istiyorsak fork kullanabiliriz. Önce katkı kılavuzunu okur, hangi dala katkı kabul edildiğini öğreniriz. Ardından fork'umuzu klonlayıp bir iş dalında değişiklik yaparız. Commit'leri kendi fork'umuza gönderdikten sonra asıl projeye PR açarız. Kaynak dal bizim fork'umuzda, hedef dal asıl projededir. Hedef her projede dev değildir; CONTRIBUTING veya bakımcıların talimatı belirler. Böylece yazma izni olmadan da projeye düzenli bir değişiklik önerisi sunabiliriz.

Kaynaklar:

- [Fork kavramı](https://docs.github.com/en/pull-requests/reference/forks)

## 29. Portfolyo projeyi anlaşılır kılar

38:00–39:30 · 90 saniye

GitHub profili bir portfolyo olabilir, ama depoların anlaşılır olması gerekir. Robot projesinde hangi sorunu çözmeye çalıştığımızı, takım içindeki katkımızı, kullanılan donanımı ve elde edilen sonucu açıklayabiliriz. Bir fotoğraf veya kısa gösterim projeyi canlandırır; aynı zamanda çalışmadığı koşulları dürüstçe yazmak değerlidir. Profilde birkaç iyi projeyi öne çıkarmak gezmeyi kolaylaştırır. Yeşil katkı karelerini ise bütün çalışma süresi gibi yorumlamayalım. GitHub belirli etkinlikleri ve belirli koşullardaki commit'leri sayar; laboratuvar çalışması veya tasarım düşüncesi bu grafiğe tamamen yansımaz. Bir başvuruda önemli olan kare sayısından çok, projenin ve kişinin katkısının somut biçimde görülebilmesidir.

Kaynaklar:

- [Katkı grafiğinin ölçütleri](https://docs.github.com/en/account-and-profile/reference/profile-contributions-reference)

## 30. Öğrenci kaynakları

39:30–40:30 · 60 saniye

GitHub Education öğrencilere öğrenme kaynakları ve çeşitli araç avantajları sunuyor. Student Developer Pack içinde iş ortaklarının teklifleri yer alıyor; bunların sayısı ve koşulları zaman içinde değişebilir. Doğrulanmış öğrenciler için Copilot Student erişimi de var. Bu avantajlar her hesabın kendiliğinden alacağı sınırsız hizmetler olarak düşünülmemeli. Başvuru öğrenci durumunun doğrulanmasını gerektirir; gerekli e-posta veya belgeler başvuruya göre belirlenir. Bazı avantajların ayrıca etkinleştirilmesi gerekebilir. Burada sabit teklif sayısı veya kesin onay süresi vermek yerine resmî güncel sayfayı kaynak olarak bırakıyorum. İhtiyaç duyulan araç seçilmeli; bir aracın ücretsiz olması projenin ihtiyaçlarına uygun olduğu anlamına gelmez.

Kaynaklar:

- [GitHub Education](https://docs.github.com/en/education/about-github-education/github-education-for-students/about-github-education-for-students)
- [Öğrenci başvurusu](https://docs.github.com/en/education/about-github-education/github-education-for-students/apply-to-github-education-as-a-student)
- [Copilot Student](https://docs.github.com/en/copilot/how-tos/copilot-on-github/set-up-copilot/enable-copilot/set-up-for-students)

## 31. Bir projenin bütün akışı

40:30–42:00 · 90 saniye

Robotun çizgiyi kaybetme sorunundan başladık. Issue ile işi görünür yaptık, bir dalda değişikliği geliştirdik ve commit ile kaydettik. Push ile ortak platforma ulaştırdık; PR üzerinden inceleyip birleştirdik ve yerel kopyayı güncelledik. Bu akışın yanında README projeyi açıklıyor, geçmiş neyin değiştiğini gösteriyor ve lisans paylaşım şartlarını belirliyor. Üç ayrımı hatırlarsak geri kalan kavramlar yerine oturur: Git ile GitHub farklıdır; dosyayı kaydetmek, commit etmek ve push etmek farklıdır; issue ile PR farklı soruları cevaplar. Sunumun ekleri komutlara yeniden bakmak için kullanılabilir. Daha sonra isteyenler resmî GitHub Docs, Pro Git kitabı ve GitHub Skills kaynaklarından bağımsız olarak ilerleyebilir.

Kaynaklar:

- [Git ve GitHub kaynakları](https://docs.github.com/en/get-started/start-your-journey/git-and-github-learning-resources)
- [Introduction to GitHub](https://github.com/skills/introduction-to-github)

## 32. Sorular

42:00–45:00 · 180 saniye

Teşekkürler. Soruları üç başlık etrafında düşünebiliriz: değişiklik şu anda nerede duruyor, kimler bu değişikliği görebiliyor ve takımın ortak çizgisine nasıl alınacak? Bir dosyanın kaydedildiği ama commit edilmediği durumla, commit edildiği ama gönderilmediği durum artık farklı anlamlar taşıyor. Bir dalda çalışmakla main'e birleştirmek de farklı adımlar. Son üç dakikada bu ilişkiler veya kendi projelerinizin nasıl düzenlenebileceğiyle ilgili soruları ele alabiliriz.

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
