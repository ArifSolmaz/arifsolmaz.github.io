# Git ve GitHub: Birlikte Üretmenin Mantığı

34 ana slayt, 6 ek slayt. Ana anlatım ve sorular toplam 45 dakika.

Canlı gösterim, sınıf içi uygulama ve zorunlu ödev yoktur. Ek slaytlar ana anlatım süresinin dışındadır.

## 1. Git ve GitHub

00:00–00:45 · 45 saniye

Bir proje yalnızca ortaya çıkan ürün değildir. Onu yaparken verdiğimiz kararlar, denediğimiz yollar ve öğrendiklerimiz de projenin parçasıdır. Bugün terminal komutlarını öğrenmeyeceğiz. Bunun yerine, bir çalışmanın zaman içinde nasıl değiştiğini ve birkaç insanın aynı çalışmaya nasıl katkı verebildiğini konuşacağız. Örneklerimiz öğrenci projelerinden, araştırmadan, şirketlerden ve açık kaynaktan gelecek. Git ve GitHub adlarını birbirinden ayıracağız; birinin tuttuğu geçmiş ile diğerinin sunduğu ortak çalışma ortamı farklı şeylerdir. Kullanmanın kazandırdıklarını konuşurken öğrenme, düzen ve koordinasyon maliyetini de göreceğiz. Dersin sonunda amaç bir aracı hemen kullanabilmek değil, hangi sorunu çözdüğünü ve kendi çalışmalarımızda nerede anlamlı olacağını anlayabilmek. Güzel bir proje kadar, o projeden devam edebilmek de önemlidir.

Görsel: ders için üretilmiş temsili çizim. Gerçek bir grubun fotoğrafı değildir.

Kaynaklar:

- [Git What is Git?](https://git-scm.com/book/en/v2/Getting-Started-What-is-Git%3F)
- [GitHub What is GitHub?](https://docs.github.com/en/get-started/start-your-journey/what-is-github)

## 2. Değişen projeler ve kişisel hafıza

00:45–01:45 · 60 saniye

Bir mikrodenetleyici programının hız ayarı değişebilir. Bir deneyin analiz yöntemi yenilenebilir. Grup raporunun bir bölümü yeniden yazılabilir. Bu örneklerin ortak noktası yalnızca dosyaların değiştirilmesi değildir: her değişiklikte bir karar veririz. Güncel dosyada o kararın sonucu vardır; önceki seçenekler ve gerekçe ise çoğu zaman kaybolur. İki hafta sonra bir sorun çıktığında, değişikliği yapan kişi bile neden öyle yaptığını hatırlamayabilir. Dosya adlarına tarih yazmak, kopya oluşturmak ve mesaj grubuna son sürümü göndermek bir yere kadar işe yarar. İnsan ve değişiklik sayısı büyüdükçe kopyalar arasındaki ilişkiyi anlamak zorlaşır. Sürüm kontrolü ihtiyacı burada başlar. Aradığımız şey daha fazla dosya değil, değişikliklerin anlaşılabilir bir geçmişidir.

Kaynaklar:

- [Git About Version Control](https://git-scm.com/book/en/v2/Getting-Started-About-Version-Control)

## 3. Tek başına: geçmişini bulabilmek

01:45–03:00 · 75 saniye

Git kullanmak için büyük bir ekibin üyesi olmak gerekmez. Tek başına yazdığınız bir programı üç ay sonra açtığınızı düşünün. Dosyaları tanırsınız ama hangi ayarın neden değiştiğini hatırlamayabilirsiniz. Anlaşılır bir geçmiş, geçmişteki kendinizle yeniden konuşmanın yoludur. Hangi değişiklikten önce davranışın farklı olduğunu görebilir, iki hâli karşılaştırabilir ve kaydettiğiniz bir hâlden devam edebilirsiniz. Bu, hata bulma sürecini daraltır; hatanın nedenini otomatik olarak açıklamaz. Bir denemenin sonuç vermemesi de bütün çalışmayı çöpe atmanız anlamına gelmez. Kazanç yalnızca eski dosyayı kurtarmak değildir. Tahmin ederek uğraşmak yerine inceleyebileceğiniz kayıtlarınız olur. Bunun için değişiklikleri gerçekten kaydetmek ve açıklamalarını anlaşılır yazmak gerekir. Git, henüz kaydetmediğiniz çalışmayı kendiliğinden hatırlamaz.

Kaynaklar:

- [GitHub About Git](https://docs.github.com/en/get-started/using-git/about-git)

## 4. Hangi dosyadan devam edeceğiz?

03:00–04:15 · 75 saniye

Bir öğrenci takımının proje klasöründe son, son2 ve gercek_son adlarıyla farklı kopyalar biriktiğini düşünün. Ekip hangi dosyanın teslim edildiğini, hangisinin çalıştığını ve neden değiştirildiğini yalnızca adlardan anlayamaz. Bir kişi sensör konumunu değiştirmiş, diğeri filtreleme eklemiş, üçüncüsü rapor grafiğini düzeltmiş olabilir. Kopyaları ayrı ayrı saklamak, bu kararların ilişkisini görünür kılmaz. Sürüm kontrolü, kaydedilmiş hâlleri ve aralarındaki değişiklikleri birlikte incelemeyi sağlar. Dosya adını uzatmak yerine hangi değişikliğin hangi kayıtla geldiğine bakarız. Bu geçmiş, araştırmaya başlangıç sağlar; ölçüm sorununun kesin nedenini kendi başına kanıtlamaz. Donanım ve çevre koşulları da etkili olabilir. Buradaki kazanç, bütün soruları otomatik cevaplamak değil, hangi hâlden devam edeceğimizi ve neyi araştıracağımızı daha iyi belirlemektir.

Kaynaklar:

- [Git About Version Control](https://git-scm.com/book/en/v2/Getting-Started-About-Version-Control)

## 5. Sürüm kontrolü neyi kaydeder?

04:15–05:30 · 75 saniye

Sürüm kontrolü, bir çalışmanın zaman içindeki hâllerini izlemek için kullanılan yöntemlerin genel adıdır. Git bu işi yapan araçlardan biridir. Dosyaların yalnızca son içeriğini değil, kaydedilen geçmişini de tutar. Böylece hangi hâlin önce, hangisinin sonra geldiğini anlayabiliriz. Kayıt açıklamaları iyi yazıldığında değişikliğin amacı da görünür olur. Dosya kopyalamaktan farkı, bu hâller arasındaki ilişkiyi düzenli biçimde saklamasıdır. Her klavye vuruşu otomatik kayıt olmaz; hangi çalışmayı ne zaman kaydedeceğinize siz karar verirsiniz. Bu yüzden sürüm kontrolü bir araç kadar çalışma alışkanlığıdır. Kayıt tutmanın değerini, proje büyüdüğünde veya geçmişe bir soru sormanız gerektiğinde hissedersiniz. Küçük bir projede de aynı temel düşünce geçerlidir: devam edebilmek için değişimi anlaşılır hâle getirmek.

Kaynaklar:

- [Git What is Git?](https://git-scm.com/book/en/v2/Getting-Started-What-is-Git%3F)

## 6. Git: projenin geçmişini tutan araç

05:30–07:00 · 90 saniye

Git, bilgisayarınızda çalışabilen bir sürüm kontrol aracıdır. Git ile izlenen proje alanına depo, İngilizce adıyla repository denir. Bir depo, yalnızca internetteki bir sayfa değildir. Bilgisayarınızdaki proje dosyalarıyla onların kaydedilmiş geçmişi birlikte düşünülebilir. Örneğin bir robotun yazılımı, kurulum açıklaması ve metin biçimindeki test sonuçları aynı depoda bulunabilir. Depodaki her dosyanın izlenip izlenmeyeceğini düzenleyebilirsiniz; her klasörü gelişigüzel depoya eklemek gerekmez. Git kaydedilmiş hâlleri ilişkilendirir ve onları karşılaştırmanızı sağlar. Bunun için GitHub hesabı zorunlu değildir. Buradaki düşünceyi bir klasörün içine tarihçe eklemek gibi hayal edebilirsiniz. Ancak kayıtların anlamlı olması, hangi değişikliği neden yaptığınızı açıklamanıza bağlıdır. Araç dosyaları saklar; kararın gerekçesini sizin yazmanız gerekir.

Kaynaklar:

- [Git What is Git?](https://git-scm.com/book/en/v2/Getting-Started-What-is-Git%3F)
- [GitHub About Git](https://docs.github.com/en/get-started/using-git/about-git)

## 7. GitHub: değişikliği birlikte konuşmak

07:00–08:30 · 90 saniye

Git ile GitHub çoğu zaman aynı şey gibi kullanılıyor; ama farklı işleri var. Git değişiklik geçmişini tutan araçtır. GitHub, Git depolarını barındıran ve insanların bu depolar etrafında birlikte çalışmasını sağlayan platformlardan biridir. Projeyi paylaşabilir, bir sorun üzerine konuşabilir, önerilen değişikliği inceleyebilir ve kabul edilip edilmeyeceğine karar verebilirsiniz. GitHub’ın değeri yalnızca dosyaların internette bulunması değildir. Dosyanın yanında konuşma, gerekçe ve karar da görünür hâle gelebilir. Bunun herkesin görmesi gerekmez; erişime bağlı özel projeler de vardır. Git kullanırken başka barındırma platformları seçmek veya hiç çevrimiçi platform kullanmamak mümkündür. Burada anlattığımız işbirliği fikri, belirli bir şirketin tekeline ait değildir. GitHub, bu fikrin yaygın kullanılan ortamlarından biridir.

Kaynaklar:

- [GitHub What is GitHub?](https://docs.github.com/en/get-started/start-your-journey/what-is-github)

## 8. Yerel çalışma ve paylaşım

08:30–09:45 · 75 saniye

Git dağıtık bir yapıya sahiptir. Bir projeyi bilgisayarınıza aldığınızda genellikle dosyalarla birlikte geçmişinin yerel bir kopyasını da alırsınız. İnternet yokken dosyaları değiştirebilir, geçmişi inceleyebilir ve yeni kayıtlar oluşturabilirsiniz. Bağlantı geldiğinde paylaşım yaptığınız diğer depolarla değişiklikleri alışveriş edebilirsiniz. Bu, herkesin sürekli aynı merkezdeki dosyayı düzenlemek zorunda olmamasını sağlar. Bir öğrenci evinde, diğeri laboratuvarda kendi çalışmasına devam edebilir. Bağımsızlık, sonradan kendiliğinden uzlaşma demek değildir. Farklı kişilerin çalışmalarını buluştururken karar vermek ve gerekirse anlaşmazlığı çözmek gerekir. Ayrıca bilgisayarınızdaki henüz paylaşılmamış kayıtlar diğer insanların bilgisayarında görünmez. Git’in yaklaşımı önce kendi kopyanızda çalışabilmek, ardından uygun zamanda ortak geçmişle buluşmaktır. Paylaşım bir adım, yerel kayıt tutmak başka bir adımdır.

Kaynaklar:

- [Git About Version Control](https://git-scm.com/book/en/v2/Getting-Started-About-Version-Control)
- [Git What is Git?](https://git-scm.com/book/en/v2/Getting-Started-What-is-Git%3F)

## 9. Commit: açıklamalı bir kayıt

09:45–11:00 · 75 saniye

Commit, Git’te projenin belirli bir hâlini geçmişe kaydetme işlemidir; ortaya çıkan kayda da commit denir. Onu açıklamalı bir durak gibi düşünebilirsiniz. Örneğin sensör okumasına filtre eklediğinizde, yaptığınız değişikliği ve amacını bir kayıtta toplarsınız. Commit bir dosyanın yalnızca adını değiştirmek veya kaydet düğmesine basmakla aynı şey değildir. Git geçmişine bilinçli bir kayıt eklenir. Projenin o hâline daha sonra başvurabilirsiniz. Bir commit’in varlığı, çalışmanın doğru veya tamamlanmış olduğunu göstermez. Açıklama, o kayıtla neyin amaçlandığını anlamanıza yardımcı olur. Git’te yerel commit oluşturmak, bunu GitHub’a göndermekten de farklıdır. İlkinde kendi geçmişinize bir kayıt ekler, ikincisinde bu kaydı başkalarının ulaşabileceği bir depoyla paylaşırsınız. Bu ayrım, ilk kez kullananlar için özellikle önemlidir.

Kaynaklar:

- [Git What is Git?](https://git-scm.com/book/en/v2/Getting-Started-What-is-Git%3F)

## 10. Geçmiş neyi kanıtlar?

11:00–12:00 · 60 saniye

Bir proje geçmişi, mühendislikte elimizdeki kanıtın kalitesini artırabilir. “Geçen hafta bir şey değiştirmiştik” yerine hangi dosyanın hangi kayıtta değiştiğini gösterebiliriz. İyi bir açıklama varsa amaçlanan sonucu da okuyabiliriz. Ancak kayıt, doğruluk belgesi değildir. Hatalı kodu da eksik bir raporu da commit olarak kaydedebilirsiniz. Bir programın derlenmesi, bir robotun güvenli çalışması veya bir deneyin geçerli olması başka tür doğrulamalar gerektirir. Ayrıca kayıt açıklamaları insanların yazdığı ifadelerdir; gerekçeyi yeniden değerlendirmek gerekebilir. Git geçmişi, iddialarımızı daha izlenebilir hâle getirir. Test, ölçüm, inceleme ve bilimsel yöntem yine gereklidir. Dolayısıyla Git’in vaadi bütün sorunları çözmek değildir. Sorularımızı daha somut kayıtlarla sorabilmek ve verdiğimiz kararların izini daha sonra yeniden okuyabilmektir.

Kaynaklar:

- [Google What to look for in a code review](https://google.github.io/eng-practices/review/reviewer/looking-for.html)

## 11. Küçük değişiklik, anlaşılır karar

12:00–13:15 · 75 saniye

Bir commit içine aynı anda motor kontrolü, arayüz rengi, rapor başlığı ve klasör düzenini koyarsak geçmişte bir durak oluşur; fakat o durağı anlamak zorlaşır. Sonradan bir sorun çıktığında hangi değişikliğin ilgili olduğunu ayırmak için daha çok emek harcarız. Birbiriyle ilişkili işleri birlikte, farklı amaçları ayrı kaydetmek geçmişi daha okunur kılar. Bu, her satır için ayrı kayıt oluşturmak demek değildir. Ölçüt satır sayısı değil, değişikliğin anlaşılabilir bir amacı olmasıdır. “Bir şeyler düzeltildi” yerine “sensör gürültüsünü azaltmak için ortalama eklendi” gibi bir açıklama, gelecekteki okuyucuya daha fazla bilgi verir. Böyle bir kayıt yazmak da zaman alır. Ancak bugünkü küçük açıklama, haftalar sonra kendinizin veya başka birinin tahmin yürütmesini azaltabilir. Git’i faydalı kılan alışkanlıklardan biri budur.

Kaynaklar:

- [Google Small CLs](https://google.github.io/eng-practices/review/developer/small-cls.html)

## 12. Branch: ayrı bir çalışma yolu

13:15–14:30 · 75 saniye

Branch, Türkçe adıyla dal, aynı proje geçmişinden ayrı bir yönde ilerlemenizi sağlar. Örneğin kullanılmaya devam edilen bir robot yazılımı varken yeni bir kontrol yaklaşımı deneyebilirsiniz. Bu deneme kendi dalında gelişir; ortak çalışma yoluna hemen girmek zorunda değildir. Başka bir kişi aynı başlangıçtan farklı bir iş üzerinde çalışabilir. Dalı, baştan sona kopyalanmış yeni bir proje klasörü olarak düşünmek yerine, geçmiş içinde izlenen bir çalışma yolu olarak düşünmek daha uygundur. Dallar denemeye alan açar; denemenin iyi sonuç vereceğini garanti etmez. İhtiyaç karşılanırsa değişiklik ortak akışa alınabilir, karşılanmazsa alınmayabilir. Çok sayıda uzun ömürlü dal kullanmak da koordinasyonu zorlaştırabilir. Buradaki felsefe, her fikri doğrudan herkesin kullandığı hâle koymadan önce üzerinde çalışabilecek bir alan yaratmaktır.

Kaynaklar:

- [Git Branches in a Nutshell](https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell)

## 13. Merge: çalışmaları buluşturmak

14:30–16:00 · 90 saniye

Ayrı dallarda çalışmanın anlamı, uygun değişiklikleri daha sonra buluşturabilmektir. Git’te buna merge, yani birleştirme denir. Farklı dosyalarda veya birbirinden bağımsız alanlarda yapılan değişiklikler çoğu zaman otomatik birleştirilebilir. İki kişi aynı satırı farklı biçimlerde değiştirdiyse Git hangi seçimin doğru olduğuna karar veremeyebilir. Böyle bir çatışma, conflict, insanların seçim yapmasını gerektirir. Ekranda çatışma çıkmaması da bütün kararların uyumlu olduğunu göstermez. Örneğin yazılımın beklediği sensör bağlantısı başka bir belgede değiştirilmiş olabilir. Dosyalar birleşir ama sistem çalışmayabilir. Birleştirme bu yüzden teknik bir işlem kadar değerlendirme sürecidir. Fikirlerin amacı, sonuçları ve ortak projeye etkisi konuşulur. Git hangi parçaların çakıştığını gösterebilir; mühendislik açısından nasıl birlikte çalışmaları gerektiğini ekip belirler.

Kaynaklar:

- [GitHub Merge conflicts](https://docs.github.com/en/pull-requests/reference/merge-conflicts)

## 14. Takımda: birbirini durdurmadan ilerlemek

16:00–17:15 · 75 saniye

Bir öğrenci takımında herkes aynı kişinin dosya göndermesini bekliyorsa işler sıraya girer. Ayrı çalışma yolları, insanların farklı görevleri aynı zamanda yürütebilmesini sağlar. Biri sensör verisini iyileştirirken diğeri kurulum açıklamasını güncelleyebilir. Ancak bağımsızlık, birbirinden habersiz çalışmak değildir. Görevlerin sınırı, beklenen sonuç ve ortak projeye ne zaman alınacağı konuşulmalıdır. Git ve GitHub bu konuşmayı kayıtlarla ilişkilendirmeyi kolaylaştırır. Bir değişikliği inceleyen kişi, yalnızca yeni dosyayı değil, önceki hâlle farkını ve açıklamasını da görebilir. Takımın kazancı daha hızlı yazmakla sınırlı değildir. Bir kişinin çalışmasını anlayarak kabul etmek, gerektiğinde değiştirmesini istemek ve kararın izini korumak mümkün olur. Bu düzen anlaşmazlığı yok etmez; anlaşmazlığı dosya kopyaları yerine açık değişiklikler üzerinden konuşabilmeye yardım eder.

Kaynaklar:

- [GitHub GitHub flow](https://docs.github.com/en/get-started/using-github/github-flow)

## 15. İnsanlar bunu günlük işte nasıl kullanır?

17:15–18:30 · 75 saniye

Günlük çalışma, çok sayıda komutun art arda yazıldığı bir tören olmak zorunda değildir. Bir ihtiyacı anlamakla başlayabilir: ölçüm grafiği okunmuyor, kurulum açıklaması eksik veya bir hata raporlanmış olabilir. Sonra biri bu ihtiyaca yönelik bir değişiklik hazırlar. Değişiklik kaydedilir, paylaşılır ve başka bir kişi tarafından incelenebilir. Uygun bulunursa ortak projeye alınır; gerekirse üzerinde yeniden çalışılır. Bu akışın ayrıntıları ekipten ekibe değişir. Tek çalışan kişi daha sade bir yol seçebilir; büyük bir projede ek kontroller olabilir. Git geçmişi, bu adımların dosyalara etkisini tutar. GitHub ise ihtiyaç, öneri, görüş ve kararın aynı ortamda bulunmasını sağlayabilir. Birazdan issue ve pull request adlarını bu günlük akış içindeki yerleriyle açıklayacağız. Her ekibin aynı yöntemi aynen uygulaması gerekmez.

Kaynaklar:

- [GitHub GitHub flow](https://docs.github.com/en/get-started/using-github/github-flow)

## 16. Issue: konuşulabilir bir ihtiyaç

18:30–19:30 · 60 saniye

GitHub’da issue, bir konu için açılan konuşma ve takip kaydıdır. Bu konu bir hata olabileceği gibi, geliştirme önerisi veya açıklığa kavuşması gereken bir soru da olabilir. Örneğin “robot bazen duruyor” demek bir başlangıçtır; ama hangi koşulda, hangi sürümde ve ne sıklıkta olduğunu yazmak konuyu araştırılabilir hâle getirir. Başkaları bu kayıt üzerinden soru sorabilir veya ek bilgi verebilir. Böylece konu mesajların arasında kaybolmak yerine proje bağlamında bulunabilir. Her issue mutlaka kod değişikliğine dönüşmez. Bazen açıklama yeterli olur, bazen öneri uygun bulunmaz. Issue kullanmak da zorunlu değildir; ekip başka araçlar seçebilir. Değeri, bir isteği yalnızca kişilerin hafızasında bırakmadan, neyin konuşulduğu ve neyin beklendiği anlaşılabilen bir yerde tutmasıdır.

Kaynaklar:

- [GitHub About issues](https://docs.github.com/en/issues/tracking-your-work-with-issues/learning-about-issues/about-issues)

## 17. Pull request: bir değişiklik önerisi

19:30–20:45 · 75 saniye

Pull request, kısaca PR, hazırladığınız değişikliğin başka bir çalışma akışına alınmasını önerdiğiniz görüşme alanıdır. GitHub’da kod farkı, değişikliğin açıklaması, yorumlar ve yapılan kontroller bu öneriyle birlikte görülebilir. PR açmak, değişikliği herkesin kullandığı hâle otomatik olarak katmak değildir. İnceleyen kişi sorular sorabilir, değişiklik isteyebilir veya öneriyi uygun bulmayabilir. Katkı yapan kişinin önerisi böylece tartışılabilir bir nesne hâline gelir. PR yalnızca yazılım koduna ait olmak zorunda değildir; bir açıklama dosyasının düzeltilmesi de önerilebilir. Buradaki önemli düşünce, değişiklik yapma ile ortak projeye alma kararını ayırmaktır. Bir fikri denemek için izin almanız gerekmeyebilir; fakat onu ortak çalışmaya katmak başka insanları etkiler. PR bu kararın açıklamalar ve kayıtlar üzerinden verilebileceği bir ortam sağlar.

Kaynaklar:

- [GitHub About pull requests](https://docs.github.com/en/pull-requests/get-started/about-pull-requests)

## 18. Review: ikinci bir göz

20:45–22:15 · 90 saniye

Bir değişikliği başka birinin incelemesi, yalnızca yazım hatası aramak değildir. İnceleyen kişi amacın anlaşılıp anlaşılmadığına, değişikliğin başka bölümleri nasıl etkilediğine ve verilen açıklamanın yeterli olup olmadığına bakabilir. Matplotlib projesindeki bir öneride, grafik açıklamasına eklenen ayrıntının örneğin odağını dağıtıp dağıtmadığı konuşuluyor. Konu yalnızca kod değil, okuyucunun anlayacağı mesaj. Bu bir kabul edilmiş sonuç değil, görüşülen değişiklik örneğidir. İkinci bir göz, çalışmayı yapan kişinin varsayımlarını soruya dönüştürebilir. Ancak inceleme kusursuzluk garantisi değildir; insanların zamanı ve bilgisi sınırlıdır. Somut, saygılı ve gerekçeli yorumlar daha yararlıdır. İnceleme, kişiyi değil önerilen çalışmayı değerlendirme alışkanlığıdır. Bu alışkanlık yoksa yorum alanı çatışmayı büyütebilir; varsa teknik kararlar daha anlaşılır biçimde konuşulabilir.

Kaynaklar:

- [Google What to look for in a code review](https://google.github.io/eng-practices/review/reviewer/looking-for.html)
- [Matplotlib PR #32416](https://github.com/matplotlib/matplotlib/pull/32416)

## 19. Kayıt, inceleme ve test farklı işlerdir

22:15–23:15 · 60 saniye

Bir proje için geçmiş tutmak, değişikliği incelemek ve sonucu test etmek farklı ihtiyaçlara karşılık verir. Git geçmişi neyin değiştiğini izleyebilmemizi sağlar. İnsan incelemesi, amaçları ve varsayımları değerlendirmemize yardım eder. Test veya deney ise seçtiğimiz koşullarda davranışın beklentiyle uyuşup uyuşmadığı hakkında bilgi verir. GitHub’da otomatik kontrollerin sonuçları da bir önerinin yanında gösterilebilir; fakat bunların hazırlanması gerekir. Bir depo açınca bütün testler kendiliğinden oluşmaz. Bir otomatik kontrolün başarılı olması, ölçülmeyen koşullar hakkında sınırsız bir güvence vermez. Özellikle fiziksel sistemlerde gerçek donanım ve çevre koşulları önemlidir. Bu ayrımı ilk günden öğrenmek yararlıdır. Git ve GitHub çalışma hakkında kanıtları bir araya getirebilir; hangi kanıtın yeterli olduğu konusunda mühendislik değerlendirmesi yine insanlara aittir.

Kaynaklar:

- [Google What to look for in a code review](https://google.github.io/eng-practices/review/reviewer/looking-for.html)
- [GitHub GitHub flow](https://docs.github.com/en/get-started/using-github/github-flow)

## 20. Öğrenci projesinde: ortak teslim

23:15–24:45 · 90 saniye

Dört kişilik bir mekatronik öğrenci grubu düşünün. Bir kişi gömülü yazılımla, biri veri kaydıyla, biri kurulum açıklamasıyla, biri sonuç raporuyla ilgileniyor. Bir depoda uygun dosyaları bir araya getirmek, teslimin hangi hâlden üretildiğini açık tutabilir. İşlerin bir listesi ve değişiklik önerileri varsa grubun neyi beklediği de daha anlaşılır olur. Bu düzen, grup üyelerinin eşit emek verdiğini otomatik olarak göstermez. Kayıt sayısı çalışmanın kalitesinin veya kişinin katkısının tek ölçütü değildir. Laboratuvar ölçümü, donanım tasarımı ve yüz yüze tartışma da önemli iştir. Ayrıca herkesin ilk gün bütün özellikleri öğrenmesi gerekmez. Küçük bir ekip basit bir çalışma düzeniyle başlayabilir. Temel kazanç, teslim dosyasının bir kişinin bilgisayarına ve hafızasına bağlı kalmamasıdır.

Kaynaklar:

- [GitHub GitHub flow](https://docs.github.com/en/get-started/using-github/github-flow)

## 21. Araştırmada: yöntemin izini korumak

24:45–26:00 · 75 saniye

Araştırmada yalnızca son grafik değil, o grafiğe nasıl ulaşıldığı da önemlidir. Analiz kodu, kullanılan ayarlar ve yöntemi anlatan metinler geçmişle ilişkilendirildiğinde, bir sonucu hangi çalışma hâlinin ürettiğini belirtmek kolaylaşır. Başka bir araştırmacı veya aylar sonraki kendiniz, değişen varsayımları inceleyebilir. Git bu izlenebilirliğe katkı verir; tek başına bir çalışmayı yeniden üretilebilir yapmaz. Verilerin nerede bulunduğu, gerekli ortam, yazılım sürümleri ve işlem adımları da açıklanmalıdır. Büyük veri dosyaları, gizli veriler ve kişisel veriler için ayrıca uygun depolama ve erişim kararları gerekir. Araştırma ekibinin paylaşabileceği ile paylaşmaması gerekeni ayırması önemlidir. Buradaki kazanç, sonucun yanına yöntemin geçmişini koyabilmektir. Bilimsel geçerlilik ise kayıt tutmanın ötesinde ölçüm, yöntem ve değerlendirme gerektirir.

Kaynaklar:

- [Matplotlib Contributing guide](https://matplotlib.org/devdocs/devel/contributing.html)
- [GitHub About READMEs](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)

## 22. Şirkette: değişikliği kontrollü paylaşmak

26:00–27:30 · 90 saniye

Bir şirkette aynı ürün üzerinde farklı uzmanlıkların çalışması olağandır. Yeni bir özellik müşteriye fayda sağlarken, bakım, güvenlik veya başka bir bileşen açısından maliyet yaratabilir. Değişiklikleri ayrı hazırlamak ve ortak ürüne almadan önce incelemek, bu etkileri konuşmaya alan açar. Yetkiler, sorumluluklar ve kontroller projenin ihtiyaçlarına göre düzenlenebilir. Her şirket aynı GitHub akışını kullanmaz; başka platformlar veya daha basit yöntemler seçilebilir. Büyük ekiplerde otomatik testler, ürün sürümleri ve dağıtım süreçleri geçmişle ilişkilendirilebilir. Bunların kurulması ve işletilmesi ayrıca emek ister. GitHub hesabı açmak kurumsal süreç kurmakla aynı şey değildir. Buradaki fayda, ürünün birden çok kişi tarafından değiştirildiği yerde kararları daha izlenebilir ve değerlendirilebilir hâle getirmektir. Sürecin ayrıntısı ürünün riskine ve ekip yapısına bağlıdır.

Kaynaklar:

- [GitHub GitHub flow](https://docs.github.com/en/get-started/using-github/github-flow)
- [Google What to look for in a code review](https://google.github.io/eng-practices/review/reviewer/looking-for.html)

## 23. Açık kaynakta: tanımadığın insanla üretmek

27:30–29:00 · 90 saniye

Açık kaynak projelerinde birbirini tanımayan insanlar katkı verebilir. Bir hata bildirmek veya belirsiz bir açıklamayı düzeltmek de katkıdır. Arduino Servo projesinde bir kullanıcı sorun bildiriyor; başka bir kişi belgedeki ilgili bilgiyi düzeltmeyi önerip o kayda bağlantı veriyor. Bu, kabul edilmiş bir sonuç değil, gözlemden öneriye uzanan gerçek bir örnektir. GitHub’da fork, başka bir deponun hesabınız altında ilişkili bir kopyasını oluşturur. Ana projeye yazma yetkiniz olmadan kendi kopyanızda çalışabilir ve öneri sunabilirsiniz. Proje yöneticileri öneriyi kabul etmek zorunda değildir. Ayrıca internette okunabilen her depo açık kaynak lisansına sahip değildir; yeniden kullanım koşullarını lisans belirler. Açık kaynak işbirliğinin değeri yalnızca erişim değildir. Kurallar, açıklamalar ve görünür kararlar farklı insanların birlikte çalışmasını mümkün kılar.

Kaynaklar:

- [Arduino Servo issue #64](https://github.com/arduino-libraries/Servo/issues/64)
- [Arduino Servo PR #130](https://github.com/arduino-libraries/Servo/pull/130)

## 24. Projeyi sonraki kişiye devretmek

29:00–30:15 · 75 saniye

Bir öğrenci takımı mezun olduğunda veya bir çalışan başka bir göreve geçtiğinde proje yaşamaya devam edebilir. Yeni gelen kişinin eline yalnızca son dosyaları vermek yeterli olmayabilir. Hangi hâl kullanılıyor, kurulum nasıl yapılıyor, hangi sorunlar biliniyor ve belli bir karar neden alınmış? İyi geçmiş, açıklama ve konuşma kayıtları bu sorulara birlikte cevap verebilir. Yine de her bilgi otomatik olarak depoda bulunmaz. Donanım bağlantıları, fiziksel ölçümler ve kuruma özgü süreçler ayrıca belgelenebilir. Devretme kazancı, her şeyi ayrılan kişiye yeniden sormak zorunda kalmamaktır. Bir projenin okunabilir olması, başka birinin güvenle devam edebilmesi için temel koşuldur. Git ve GitHub bunu destekleyen araçlardır; sürdürülebilirlik ise insanların neyi açıklamaya değer bulduğuna ve kayıtları ne kadar güncel tuttuğuna bağlıdır.

Görsel: ders için üretilmiş temsili çizim. Gerçek bir grubun fotoğrafı değildir.

Kaynaklar:

- [GitHub About READMEs](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)
- [GitHub Backing up a repository](https://docs.github.com/en/repositories/archiving-a-github-repository/backing-up-a-repository)

## 25. README: projenin giriş kapısı

30:15–31:30 · 75 saniye

Bir depoda README adıyla sık karşılaşılan dosya, projenin ilk açıklama sayfasıdır. Yeni gelen kişinin bütün dosyaları açarak ne olduğunu tahmin etmesi yerine, projenin amacını ve başlangıç bilgisini burada bulması beklenir. Ne yapıyor, kimin için, nasıl hazırlanıyor ve çalıştırılıyor, hangi sınırlar var? Bir mekatronik projesinde gerekli kart ve bağlantı bilgileri uygun yerde açıklanabilir. README bütün ayrıntıların tek dosyaya doldurulması değildir; başka belgelere yönlendirme yapabilir. Okuyucunun ihtiyacına göre düzenlenmiş ve güncel açıklama daha yararlıdır. MDN Web Docs’taki bir öneride, yazar açıklamayı düzeltmeden önce cümlelerin niyetini anlamak için geçmişe baktığını anlatıyor. Bu örnek, belge ile geçmişin birlikte işe yarayabildiğini gösterir. Devretme veya katkı alma düşüncesi varsa ilk okuyucunun sorularını ciddiye almak gerekir.

Kaynaklar:

- [GitHub About READMEs](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)
- [MDN PR #45998](https://github.com/mdn/content/pull/45998)

## 26. Çalışma kültürü ve ortak sorumluluk

31:30–32:45 · 75 saniye

Bir depodaki bütün değişiklikler görünür olabilir; yine de ekip birbirini anlamayabilir. Açıklamasız kayıtlar, belirsiz görevler veya gerekçesiz yorumlar araçların değerini azaltır. GitHub’ın sunduğu konuşma alanı, insanların iyi iletişim kuracağını garanti etmez. Katkıda bulunan kişiden ne beklendiğinin açık olması, eleştirinin çalışma üzerinden yapılması ve kararın nedeninin yazılması önemlidir. Her küçük tercih için uzun tartışma gerekmez; fakat başkalarını etkileyen kararların bağlamı kaybolmamalıdır. Ekip, nasıl birlikte çalışacağını kendi ihtiyaçlarına göre belirleyebilir. Kim neyi inceleyecek, ne zaman paylaşılacak, hangi değişiklik ayrıca doğrulanacak? Bunlar sosyal ve teknik kararlardır. Git ile kayıt tutmak, GitHub ile konuşmayı görünür kılmak yardımcı olur. İşbirliğinin niteliği ise bu alanları kullanan insanların alışkanlıkları ve birbirine karşı tutumuyla oluşur.

Kaynaklar:

- [Google What to look for in a code review](https://google.github.io/eng-practices/review/reviewer/looking-for.html)

## 27. Bedel: öğrenmek ve kayıt tutmak

32:45–34:00 · 75 saniye

Git kullanmak ücretsiz erişilebilen bir araçla bile zaman ve dikkat ister. Yeni terimler öğrenirsiniz; dosyayı değiştirmek, geçmişe kaydetmek ve paylaşmak arasındaki farkı anlamanız gerekir. Küçük işleri anlaşılır kayıtlara bölmek ve açıklama yazmak da anlık bir maliyettir. Bu yüzden ilk gün yalnızca dosya kopyalamaktan daha yavaş hissedebilirsiniz. Beklenen karşılık, geçmişe dönmeniz veya başka biriyle birlikte çalışmanız gerektiğinde ortaya çıkar. Ancak bu karşılık her proje için aynı büyüklükte değildir. Tek seferlik küçük bir taslakta çok karmaşık bir düzen kurmak gereksiz olabilir. Yeni başlayan kişinin her özelliği aynı anda öğrenmesi de gerekmez. Araçtan yararlanmak için zamanla anlaşılır bir çalışma alışkanlığı geliştirilir. Maliyeti saklamak yerine, projenin ihtiyaçlarıyla birlikte değerlendirmek daha gerçekçidir.

Kaynaklar:

- [Git About Version Control](https://git-scm.com/book/en/v2/Getting-Started-About-Version-Control)

## 28. Bedel: koordinasyon ve bekleme

34:00–35:30 · 90 saniye

Bir değişikliği paylaşmak, hemen kullanılacağı anlamına gelmez. Başka birinin incelemesini beklemek, yorumlara cevap vermek ve çalışmayı yeniden düzenlemek gerekebilir. Ekip büyüdükçe bu koordinasyon maliyeti artabilir. Uzun süre ayrı ilerleyen çalışmaların buluşması zorlaşabilir; aynı alanı değiştiren kişiler seçim yapmak zorunda kalabilir. Bir akışın çok sıkı olması küçük işleri yavaşlatabilir, çok gevşek olması da ortak projeyi anlamayı zorlaştırabilir. Her değişikliğe aynı süreç uygulanmak zorunda değildir. Öğrenci grubuyla büyük bir şirketin ihtiyacı farklıdır. Git ve GitHub bu kararları uygulamak için imkân sunar; doğru düzeni kendiliğinden seçmez. Kullanmanın bedeli, yalnızca teknik aracı öğrenmek değildir. Ortak çalışmayı konuşmak, sıraya koymak ve sürdürmek için de insanların zaman ayırması gerekir. Git geçmişinin bir kopyasını tutmak, platformdaki bütün görüşmeleri ve iş takibini otomatik olarak saklamak anlamına gelmez. Platform değişikliği de ayrıca planlanacak bir iştir.

Kaynaklar:

- [GitHub GitHub flow](https://docs.github.com/en/get-started/using-github/github-flow)
- [Google Small CLs](https://google.github.io/eng-practices/review/developer/small-cls.html)
- [GitHub — About GitHub Importer](https://docs.github.com/en/migrations/importing-source-code/using-github-importer/about-github-importer)

## 29. Görünürlük: paylaşırken sınır koymak

35:30–37:00 · 90 saniye

GitHub’da bir deponun herkese açık veya erişimi sınırlı olması farklı sonuçlar doğurur. Açık bir depo çalışmanızı gösterebilir ve başkalarının incelemesini kolaylaştırabilir. Aynı görünürlük, paylaşmamanız gereken bilgilerin de görünmesi anlamına gelebilir. Parolalar, erişim anahtarları, kişisel veriler ve kuruma ait gizli bilgiler proje dosyalarına gelişigüzel eklenmemelidir. Geçmiş tutan bir araçta güncel dosyadan bir bilgiyi silmek, geçmişteki bütün kopyalardan onu kaldırmakla aynı şey değildir. Yayımlanmış bir erişim anahtarı iptal edilmeli veya yenilenmelidir; yalnızca dosyayı silmek yeterli değildir. Özel depo da bütün güvenlik sorumluluğunu ortadan kaldırmaz; erişim ve paylaşım kararları yine önemlidir. Temel düşünce, neyi kimin görmesini istediğinize bilinçli karar vermek ve paylaşımın geçmişi de içerdiğini hatırlamaktır.

Kaynaklar:

- [GitHub Removing sensitive data](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)
- [GitHub What is GitHub?](https://docs.github.com/en/get-started/start-your-journey/what-is-github)

## 30. Herkese açık depo ve lisans

37:00–38:15 · 75 saniye

Bir projenin GitHub’da herkese açık görünmesi, içindeki her şeyi istediğimiz gibi kopyalayabileceğimiz anlamına gelmez. Lisans, çalışmanın hangi koşullarla kullanılabileceğini, değiştirilebileceğini ve paylaşılabileceğini belirler. Açık kaynak lisansları farklı şartlar içerebilir; hepsi aynı değildir. Kendi projenizi paylaşırken de başkasından aldığınız kodun veya malzemenin koşullarını anlamanız gerekir. Bir dosyayı değiştirerek kullanmak, o dosyanın önceki haklarını kendiliğinden ortadan kaldırmaz. Lisans konusu hukuk ayrıntılarıyla doludur; burada bütün lisansları karşılaştırmıyoruz. İlk bilinmesi gereken ayrım, okunabilir olma ile yeniden kullanma hakkının farklı olmasıdır. Katkı vereceğiniz projede lisans ve katkı açıklamalarına bakmak bu yüzden çalışma akışının parçasıdır. Paylaşım düşüncesi, insanların neye izin verdiğini ve hangi koşullarda verdiğini anlaşılır kılınca daha sürdürülebilir olur.

Kaynaklar:

- [GitHub Licensing a repository](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository)

## 31. Git hangi sorunları çözmez?

38:15–39:30 · 75 saniye

Git özellikle metin biçimindeki dosyalardaki değişiklikleri karşılaştırmada kullanışlıdır. Büyük ikili dosyalar, CAD dosyaları veya büyük deney verileri için ek araçlar ve farklı depolama kararları gerekebilir. Git bazı dosyaları saklayabilir; fakat onların içeriğini anlamlı biçimde karşılaştırmak veya birleştirmek her zaman mümkün değildir. Ayrıca bir robotun fiziksel bağlantısını, laboratuvardaki ayarı veya sensörün yerini yalnızca dosya geçmişinden öğrenemeyebilirsiniz. Bunların da uygun biçimde belgelenmesi gerekir. Git bir test sistemi değildir; doğru sonucu otomatik doğrulamaz. Kaydedilmemiş çalışmayı kendiliğinden korumaz ve kapsamlı bir yedekleme planının yerine geçmez. Ortak geçmişin başka kopyalarda bulunması yararlı olabilir ama bütün cihaz, veri ve erişim risklerini kapsamaz. Aracı yerli yerinde kullanmak, sağladığı hafızayı diğer mühendislik kayıtları ve kontrollerle tamamlamaktır. Büyük dosya depolama hizmetlerinin kullanım miktarına bağlı ücretleri olabilir.

Kaynaklar:

- [GitHub About Git LFS](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-git-large-file-storage)
- [GitHub Backing up a repository](https://docs.github.com/en/repositories/archiving-a-github-repository/backing-up-a-repository)
- [GitHub — Git LFS billing](https://docs.github.com/en/billing/concepts/product-billing/git-lfs)

## 32. Her işte aynı düzen gerekli mi?

39:30–40:45 · 75 saniye

Bir yöntemin yaygın kullanılması, her iş için aynı şekilde uygulanacağı anlamına gelmez. Sık değişen metin ve kod, geçmişe dönme ihtiyacı, ekip çalışması ve devretme beklentisi varsa Git’in değeri artar. Tek seferlik küçük bir taslak için karmaşık dallar ve zorunlu çok aşamalı inceleme gereksiz yük yaratabilir. Temel kayıt tutma ile ağır bir ekip süreci de aynı şey değildir. Yalnız çalışan biri Git’i sade biçimde kullanabilir. İkili tasarım dosyalarının baskın olduğu bir projede ise dosya türüne uygun başka araçlarla birlikte kullanmak daha anlamlı olabilir. Karar, “herkes kullanıyor” diye değil, hangi sorunu çözmek istediğinize göre verilmelidir. Öğrenilen alışkanlığın sonraki projelere taşınması da fayda yaratabilir. Ancak seçilen düzenin sürdürülmesi için zaman ve dikkat gerektiğini hesaba katmak gerekir.

Kaynaklar:

- [GitHub What is GitHub?](https://docs.github.com/en/get-started/start-your-journey/what-is-github)
- [GitHub About Git LFS](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-git-large-file-storage)

## 33. Bir sonraki projeye üç soru

40:45–42:00 · 75 saniye

Bugün bütün terimleri ezberlemeniz gerekmiyor. Bir sonraki grup projenizde üç soruyu hatırlamak daha yararlı olabilir. Çalışan hâlin hangi dosyalardan ve hangi kararlardan oluştuğu belli mi? Yaptığınız değişikliğin gerekçesi, başka birinin anlayabileceği bir yerde duruyor mu? Siz olmadığınızda bir başkası devam edebilecek kadar açıklama bulabilir mi? Git ve GitHub bu sorulara cevap üretmek için kullanılabilecek araçlardır. Tek başına araç seçmek, cevapları oluşturmaz; kayıt, açıklama ve birlikte karar verme alışkanlığı gerekir. Küçük bir projede basit bir düzenle başlanabilir, ihtiyaç büyüdükçe akış geliştirilebilir. Dersin hedefi bir hesap açma veya uygulama görevi vermek değil, değişimi daha anlaşılır yönetmenin ne kazandırdığını görmekti. Teknik ayrıntılar öğrenilirken bu nedenleri hatırlamak, komutların neye hizmet ettiğini anlamayı kolaylaştırır.

Kaynaklar:

- [GitHub About READMEs](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)

## 34. Sorular ve tartışma

42:00–45:00 · 180 saniye

Son üç dakikayı sorulara ayırın. Öğrencilerden hemen bir araç kullanmalarını veya canlı uygulama yapmalarını istemeyin. İsterlerse kendi deneyimlerinden örnekler paylaşabilirler: hangi dosyadan devam ettiklerini bilememek, ekipte yapılan değişikliği anlayamamak veya eski bir projeyi yeniden çalıştıramamak gibi. Soruları Git ile GitHub ayrımına, kayıt ile paylaşım ayrımına ve aracın sınırlarına bağlayın. “Bunu kullanınca hata olmaz mı?” sorusunda geçmişin doğruluğu garanti etmediğini hatırlatın. “Tek başıma neden kullanayım?” sorusunda gelecekteki kendinizin de okuyucu olduğunu vurgulayın. Lisans veya gizli bilgi sorusu ayrıntılıysa ilgili resmi kaynaklara yönlendirin. Dersin genel kazanımı, anlaşılır geçmişin ve görünür kararların kişisel ve ortak çalışmada sağlayabileceği faydayı, gereken emekle birlikte değerlendirebilmektir. Ek slaytlar ayrıntılı sorular ve sonradan başvuru için kullanılabilir.

Kaynaklar:


## Ek 1. Dört temel kelime

Ek slayt · ana anlatım süresinin dışında

Bu başvuru sayfası ana akıştaki dört temel terimi birlikte gösterir. Depo, commit, dal ve pull request aynı şey değildir. Bir depo projenin izlenen dosyalarıyla geçmişini barındırır. Commit belirli bir hâlin açıklamalı kaydıdır. Dal, aynı geçmişten ayrı ilerleyiştir. Pull request ise GitHub gibi bir ortamda değişikliği ortak akışa alma önerisidir. Depo ve commit yalnızca internette bulunmaz; Git ile yerel olarak kullanılabilir. PR bir commit’in yerine geçmez, onun etrafındaki görüşmeye ve karara alan açar.

Kaynaklar:

- [Git What is Git?](https://git-scm.com/book/en/v2/Getting-Started-What-is-Git%3F)
- [GitHub About pull requests](https://docs.github.com/en/pull-requests/get-started/about-pull-requests)

## Ek 2. Bir README neleri cevaplayabilir?

Ek slayt · ana anlatım süresinin dışında

README için tek ve her projeye uyan bir şablon yoktur. Bu sayfadaki sorular, projeyi ilk kez gören kişinin başlangıç ihtiyaçlarını hatırlatır. Kurulum adımları ile kullanım adımları farklı olabilir. Donanım kullanılan projede bağlantı ve güvenli çalışma bilgileri uygun belgelere yönlendirilmelidir. Lisans, yardım kanalı ve bilinen sınırlar da projenin niteliğine göre açıklanabilir. Bir belgeyi uzun yapan ayrıntı sayısı değil, okunabilirliği ve güncelliğidir. Amaç, okuyucunun bütün dosyalara bakarak ne yapacağını tahmin etmek zorunda kalmamasıdır.

Kaynaklar:

- [GitHub About READMEs](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)

## Ek 3. Anlaşılır bir değişiklik önerisi

Ek slayt · ana anlatım süresinin dışında

Bir pull request açıklaması, inceleyen kişinin yeni dosyadan fazlasını anlamasına yardım eder. Hangi ihtiyaca cevap verildiği, değişikliğin sınırı, nasıl doğrulandığı ve açık kalan konular belirtilebilir. Küçük bir düzeltmenin kısa bir açıklaması yeterli olabilir; daha riskli veya kapsamlı bir değişiklik daha fazla bağlam ister. Amaç uzun metin yazmak değil, karar için gereken bilgiyi vermektir. Bir issue ile ilişkiliyse bağlantı kurulabilir. İnceleyen kişi bu bilgiler üzerinden soru sorabilir veya değişiklik isteyebilir. Açıklama, yapılan testin ya da deneyin yerine geçmez; ilgili kanıtın nerede olduğunu gösterir.

Kaynaklar:

- [GitHub About pull requests](https://docs.github.com/en/pull-requests/get-started/about-pull-requests)
- [Google What to look for in a code review](https://google.github.io/eng-practices/review/reviewer/looking-for.html)

## Ek 4. Projenin ihtiyacına göre seçim

Ek slayt · ana anlatım süresinin dışında

Bu sayfa bir puanlama testi değildir. Git’in nerede değer sağlayabileceğini düşünmek için birkaç karşılaştırma sunar. Sık değişen kod ve metinlerde geçmişi karşılaştırmak kolaydır. Birlikte çalışma ve devretme ihtiyacı varsa açıklamalar ile görüşme kayıtlarının değeri artar. Büyük ikili dosyalar veya özel tasarım biçimleri hâkimse, o dosyalar için uygun depolama ve karşılaştırma araçları gerekir. Git bunlarla birlikte kullanılabilir. Seçilen süreç ihtiyaçtan büyük olmamalıdır; sürdürülemeyen ayrıntılı düzen, basit ve düzenli bir alışkanlıktan daha yararlı olmayabilir.

Kaynaklar:

- [GitHub About Git LFS](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-git-large-file-storage)
- [Git About Version Control](https://git-scm.com/book/en/v2/Getting-Started-About-Version-Control)

## Ek 5. İşe yarayan dört alışkanlık

Ek slayt · ana anlatım süresinin dışında

Bu başvuru sayfasındaki alışkanlıklar, kullanılan platformun bütün ayrıntılarını bilmeden de anlaşılabilir. İlişkili işleri birlikte kaydetmek geçmişin okunmasını kolaylaştırır. Amaç ve gerekçeyi yazmak, gelecekteki okuyucunun varsayım üretmesini azaltır. Ortak bir işe alınacak değişikliği ihtiyaç kadar incelemek, kararın etkisini görmeye yardım eder. Projeyi tanıtan açıklamaları güncel tutmak ise devretme ve yeniden başlama maliyetini azaltabilir. Hiçbir alışkanlık kusursuzluk sağlamaz; düzenin ekip için sürdürülebilir olması önemlidir. Küçük bir projede kısa açıklamalar ve sade bir akış yeterli olabilir.

Kaynaklar:

- [Google Small CLs](https://google.github.io/eng-practices/review/developer/small-cls.html)
- [GitHub About READMEs](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)

## Ek 6. Kaynaklar ve devam yolu

Ek slayt · ana anlatım süresinin dışında

Kaynak bağlantıları, dersin kavramsal çerçevesini ayrıntılandırmak ve sonraki öğrenmeyi desteklemek içindir. Git kitabı sürüm kontrolünü ve Git’in temel düşüncesini açıklar. GitHub belgeleri depo, issue, pull request ve inceleme alanlarını anlatır. README, lisans ve erişim konularında da ilgili resmi rehberlere başvurulabilir. Bu kaynakların bir kısmı teknik ayrıntıya geçer; hepsini ders süresinde okumak beklenmez. Önce hangi soruya cevap arandığını belirlemek, sonra ilgili bölümü okumak daha uygundur. Ana sunum komut öğretmez; teknik kullanım öğrenilirken kavramların amaçlarını bu akışla ilişkilendirmek mümkündür.

Kaynaklar:

- [Pro Git kitabı: Git’in temel yaklaşımı](https://git-scm.com/book/en/v2/Getting-Started-What-is-Git%3F)
- [GitHub Docs: GitHub ve ortak çalışma](https://docs.github.com/en/get-started/start-your-journey/what-is-github)
- [Arduino Servo: bir kullanıcı katkısı](https://github.com/arduino-libraries/Servo/pull/130)
- [Matplotlib: birlikte yapılan inceleme](https://github.com/matplotlib/matplotlib/pull/32416)
- [MDN: dokümantasyona küçük katkı](https://github.com/mdn/content/pull/45998)
