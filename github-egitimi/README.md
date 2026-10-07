# Git ve GitHub: Birlikte Üretmenin Mantığı

Git ve GitHub’ı hiç bilmeyen öğrenciler için 45 dakikalık anlatım dersi. Sunum, değişen bir projeye nasıl güvenileceğinden başlar; Git’in çalışma belleğini, GitHub’ın ortak çalışma alanını ve insanların bunları günlük işlerinde nasıl kullandığını anlatır. Kazanımların yanında öğrenme, bakım, gizlilik ve iş yükü gibi maliyetleri de ele alır.

- **34 ana slayt:** anlatım ve sorular toplam 45 dakika.
- **6 ek slayt (35–40):** kavram sözlüğü, kaynaklar ve ders sonrası başvuru. Ana dersin süresine dahil değildir.
- Ana anlatım, kavramlar ve çalışma alışkanlıkları üzerinden ilerler. Komut ezberi veya kurulum gerektirmez.
- Canlı gösterim, telefon veya hesap hazırlığı, sınıf içi uygulama ve zorunlu ödev yoktur.

## Güncel girişler

- `index.html`: çalışma felsefesi üzerinden ana sunum. Ana gezinme 34. slaytta biter. “Ek slaytlar” düğmesi 35–40 arasındaki başvuru sayfalarına geçer.
- `en/index.html`: aynı 40 slaytın İngilizce sürümü; dil değiştirirken slayt numarası korunur.
- `konusmaci-notlari.html`: dakika planı, her slaytın konuşma metni ve kaynaklar.
- `en/konusmaci-notlari.html`: bütün slaytların İngilizce konuşmacı notları ve aynı dakika planı.
- `egitmen-rehberi.md`: aynı notların indirilebilir metni.
- `pdf/git-github-tr.pdf` ve `pdf/git-github-en.pdf`: 40 sayfalık, 16:9 Türkçe ve İngilizce slayt çıktıları.
- `canli-ders/materyal.html`: sunum, notlar ve isteğe bağlı örnek animasyonlar.
- `student/`: dersten sonra isteğe bağlı bağımsız kaynaklar.
- `instructor/`: güncel ders bağlantıları.

Eski Türkçe `canli-ders/` ve `sunum/` adresleri ana sunuma, İngilizce karşılıkları `en/` sunumuna yönlenir. `v2/` adresi arşivdeki teknik başvuru sunumunu açar. Eski slayt numaraları ana sunuma taşınmaz. Önceki teknik içerikler arşivde, önceki yayımlar Git geçmişinde korunur.

## Sunum kullanımı

Sol/sağ oklarla gezinilir. `N` notları, `O` genel bakışı, `F` tam ekranı açar. `R` etkin animasyonu tekrar başlatır. Not belgesi ayrı pencerede okunabilir. Yazdırma bütün ana ve ek slaytları içerir. Animasyonlar yazdırılırken sabit görseller kullanır.

Sunumdaki animasyonlar yalnız gerektiğinde yüklenir. Ağ veya dosya erişimi başarısız olduğunda sabit görsel kullanılır. Google Fonts yüklenemezse yerel yazı tiplerine geçilir. Kaynak bağlantıları kavramları doğrulamak ve ders sonrasında gerçek projeleri incelemek içindir.

## Sunumu düzenleme

Sunumdaki **Düzenle** düğmesi, seçili slaydın yanında düzenleme alanlarını açar. Başlık, açıklama, maddeler, sütun metinleri, kod, ekranda görünen kod açıklamaları, konuşmacı notları, süre ve renk teması değiştirilebilir. Önizlemedeki metne tıklamak ilgili düzenleme alanına geçer. Düzenlemeler Türkçe ve İngilizce için ayrı saklanır.

Değişiklikler bu tarayıcıda otomatik kaydedilir. Felsefe sunumunun taslakları, önceki kod ağırlıklı sunumun taslaklarından ayrı tutulur; eski tarayıcı verileri silinmez. Paylaşmak için **HTML indir**, yedeklemek veya başka tarayıcıda düzenlemeye devam etmek için **Düzenleme dosyasını indir** kullanılır. İndirilen HTML, görselleri ve sunum araçlarını canlı siteden yükler; internet bağlantısı gerekir. **Dosyadan aç** ile düzenleme dosyası geri yüklenebilir.

Güncellenen konuşmacı notları ayrıca indirilebilir. Düzenlenmiş slaytların PDF çıktısı için **Yazdır** kullanılır; tarayıcıda hedef olarak PDF seçilir. Bir düzenleme varsa PDF düğmesi bu güncel yazdırma akışını açar. PDF dosyaları, tarayıcıdaki düzenlemeler öncesindeki yayımlanan sunumun çıktılarıdır.

Tarayıcıdaki düzenlemeler herkesin gördüğü siteyi değiştirmez. Site içeriğini kalıcı güncellemek için indirilen düzenleme dosyasının içerikleri ilgili kaynak dosyasına uygulanıp sunum yeniden üretilir ve yayımlanır. Tarayıcı verileri temizlenmeden önce düzenleme dosyası indirilmelidir.

## İçerik bakımı

`ders.json` Türkçe, `lesson-en.json` İngilizce slayt metinleri, konuşmacı notları, süreler ve kaynakları içerir. `python3 build.py` iki dilde HTML sunumlarını ve not belgelerini üretir. Python standart kütüphanesi yeterlidir. Önceki eğitimden kalan animasyonlar ve bu ders için hazırlanan görseller kullanılır. İçerik değiştiğinde PDF çıktıları da yenilenmelidir.

Düzeltilmiş önceki teknik başvuru `arsiv/teknik/` altında, önceki Türkçe sunum `arsiv/onceki-sunum/` altında saklanır. Önceki geniş atölye rehberi `arsiv/egitmen-rehberi-atolye.md` dosyasındadır. Bu belgeler güncel ana dersin parçası değildir.
