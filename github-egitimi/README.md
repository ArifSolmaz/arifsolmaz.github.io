# Git ve GitHub: Birleşik Anlatım

Mekatronik öğrencileri için 45 dakikalık, anlatım ağırlıklı eğitim. Aynı çizgi izleyen robot projesi üzerinden Git ve GitHub ayrımı, kayıt geçmişi, ekip çalışması ve paylaşım anlatılır.

- **32 ana slayt:** anlatım ve sorular toplam 45 dakika.
- **12 ek slayt:** kurulum, SSH ve ayrıntılı komutlar. Ana dersin süresine dahil değildir.
- Canlı gösterim, telefon veya hesap hazırlığı, sınıf içi uygulama ve zorunlu ödev yoktur.

## Güncel girişler

- `index.html`: birleşik sunum. Ana gezinme 32. slaytta biter. “Ek slaytlar” düğmesi teknik ayrıntılara geçer.
- `en/index.html`: aynı 44 slaytın İngilizce sürümü; dil değiştirirken slayt numarası korunur.
- `konusmaci-notlari.html`: dakika planı, her slaytın konuşma metni ve kaynaklar.
- `en/konusmaci-notlari.html`: bütün slaytların İngilizce konuşmacı notları ve aynı dakika planı.
- `egitmen-rehberi.md`: aynı notların indirilebilir metni.
- `pdf/git-github-tr.pdf` ve `pdf/git-github-en.pdf`: 44 sayfalık, 16:9 Türkçe ve İngilizce slayt çıktıları.
- `canli-ders/materyal.html`: dersin dört animasyonu, notlar ve örnek proje.
- `student/`: dersten sonra isteğe bağlı bağımsız kaynaklar.
- `instructor/`: güncel ders bağlantıları.

Eski Türkçe `canli-ders/` ve `sunum/` adresleri ana sunuma, İngilizce karşılıkları `en/` sunumuna, `v2/` teknik eklerin başlangıcına yönlenir. Eski slayt numaraları taşınmaz. Önceki sürümler arşivde korunur.

## Sunum kullanımı

Sol/sağ oklarla gezinilir. `N` notları, `O` genel bakışı, `F` tam ekranı açar. `R` etkin animasyonu tekrar başlatır. Not belgesi ayrı pencerede okunabilir. Yazdırma bütün ana ve ek slaytları içerir. Animasyonlar yazdırılırken sabit son kareleri kullanır.

Animasyonlar yalnız gerektiğinde yüklenir. Ağ veya dosya erişimi başarısız olduğunda sabit görsel kullanılır. Google Fonts yüklenemezse yerel yazı tiplerine geçilir. Paylaşılan kaynaklar öğrenci paketi teklifleri gibi değişebilen bilgilerin güncel resmi adreslerini içerir.

## Sunumu düzenleme

Sunumdaki **Düzenle** düğmesi, seçili slaydın yanında düzenleme alanlarını açar. Başlık, açıklama, maddeler, sütun metinleri, kod, konuşmacı notları, süre ve renk teması değiştirilebilir. Önizlemedeki metne tıklamak ilgili düzenleme alanına geçer. Düzenlemeler Türkçe ve İngilizce için ayrı saklanır.

Değişiklikler bu tarayıcıda otomatik kaydedilir. Paylaşmak için **HTML indir**, yedeklemek veya başka tarayıcıda düzenlemeye devam etmek için **Düzenleme dosyasını indir** kullanılır. İndirilen HTML, görselleri ve sunum araçlarını canlı siteden yükler; internet bağlantısı gerekir. **Dosyadan aç** ile düzenleme dosyası geri yüklenebilir.

Güncellenen konuşmacı notları ayrıca indirilebilir. Düzenlenmiş slaytların PDF çıktısı için **Yazdır** kullanılır; tarayıcıda hedef olarak PDF seçilir. Bir düzenleme varsa PDF düğmesi bu güncel yazdırma akışını açar. Özgün PDF dosyaları ilk yayımlanan 44 slaydın çıktılarıdır.

Tarayıcıdaki düzenlemeler herkesin gördüğü siteyi değiştirmez. Site içeriğini kalıcı güncellemek için indirilen düzenleme dosyasının içerikleri ilgili kaynak dosyasına uygulanıp sunum yeniden üretilir ve yayımlanır. Tarayıcı verileri temizlenmeden önce düzenleme dosyası indirilmelidir.

## İçerik bakımı

`ders.json` Türkçe, `lesson-en.json` İngilizce slayt metinleri, konuşmacı notları, süreler ve kaynakları içerir. `python3 build.py` iki dilde HTML sunumlarını ve not belgelerini üretir. Python standart kütüphanesi yeterlidir. Görseller özgün eğitimden alınmıştır. İçerik değiştiğinde PDF çıktıları da yenilenmelidir.

Düzeltilmiş önceki teknik başvuru `arsiv/teknik/` altında, önceki Türkçe sunum `arsiv/onceki-sunum/` altında saklanır. Önceki geniş atölye rehberi `arsiv/egitmen-rehberi-atolye.md` dosyasındadır. Bu belgeler güncel ana dersin parçası değildir.
