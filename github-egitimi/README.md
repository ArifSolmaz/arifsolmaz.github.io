# Git ve GitHub: Birleşik Anlatım

Mekatronik öğrencileri için 45 dakikalık, anlatım ağırlıklı eğitim. Aynı çizgi izleyen robot projesi üzerinden Git ve GitHub ayrımı, kayıt geçmişi, ekip çalışması ve paylaşım anlatılır.

- **32 ana slayt:** anlatım ve sorular toplam 45 dakika.
- **12 ek slayt:** kurulum, SSH ve ayrıntılı komutlar. Ana dersin süresine dahil değildir.
- Canlı gösterim, telefon veya hesap hazırlığı, sınıf içi uygulama ve zorunlu ödev yoktur.

## Güncel girişler

- `index.html`: birleşik sunum. Ana gezinme 32. slaytta biter. “Ek slaytlar” düğmesi teknik ayrıntılara geçer.
- `konusmaci-notlari.html`: dakika planı, her slaytın konuşma metni ve kaynaklar.
- `egitmen-rehberi.md`: aynı notların indirilebilir metni.
- `canli-ders/materyal.html`: dersin dört animasyonu, notlar ve örnek proje.
- `student/`: dersten sonra isteğe bağlı bağımsız kaynaklar.
- `instructor/`: güncel ders bağlantıları.

Eski Türkçe `canli-ders/` ve `sunum/` adresleri ana sunuma, `v2/` teknik eklerin başlangıcına yönlenir. Eski slayt numaraları taşınmaz. İngilizce önceki eğitimler, birleşik Türkçe sunumla aynı içerik değildir.

## Sunum kullanımı

Sol/sağ oklarla gezinilir. `N` notları, `O` genel bakışı, `F` tam ekranı açar. `R` etkin animasyonu tekrar başlatır. Not belgesi ayrı pencerede okunabilir. Yazdırma bütün ana ve ek slaytları içerir. Animasyonlar yazdırılırken sabit son kareleri kullanır.

Animasyonlar yalnız gerektiğinde yüklenir. Ağ veya dosya erişimi başarısız olduğunda sabit görsel kullanılır. Google Fonts yüklenemezse yerel yazı tiplerine geçilir. Paylaşılan kaynaklar öğrenci paketi teklifleri gibi değişebilen bilgilerin güncel resmi adreslerini içerir.

## İçerik bakımı

`ders.json` slayt metinleri, konuşmacı notları, süreler ve kaynakları içerir. `python3 build.py` ana HTML sunumunu ve iki not belgesini üretir. Python standart kütüphanesi yeterlidir. Görseller özgün eğitimden alınmıştır.

Düzeltilmiş önceki teknik başvuru `arsiv/teknik/` altında, önceki Türkçe sunum `arsiv/onceki-sunum/` altında saklanır. Önceki geniş atölye rehberi `arsiv/egitmen-rehberi-atolye.md` dosyasındadır. Bu belgeler güncel ana dersin parçası değildir.
