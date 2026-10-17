# Çizgi izleyen robot

Mekatronik dersi için yapılmış, siyah bir çizgiyi takip eden küçük bir robot.

![Robotun üstten çizimi](fotograflar/robot.png)

## Malzemeler

- Arduino Uno
- L298N motor sürücü
- 2 adet DC motor ve tekerlek
- 3 adet kızılötesi çizgi sensörü (TCRT5000)
- 7.4 V Li-ion pil

## Nasıl çalışır?

Üç sensör zemini okur. Siyah çizgi ortadaki sensörün altındaysa robot düz gider. Çizgi sola ya da sağa kayarsa robot o tarafa döner. Ayarlar `robot.ino` dosyasının en üstünde:

| Ayar | Değer | Ne işe yarar? |
|---|---|---|
| `HIZ` | 200 | Düz yolda hız (0-255) |
| `VIRAJ_HIZI` | 120 | Virajda hız |
| `ESIK` | 500 | Bu değerin üstü siyah çizgi sayılır |

## Bağlantılar

Devre şeması: [devre-semasi.png](devre-semasi.png)

| Parça | Arduino pini |
|---|---|
| L298N ENA / ENB (motor hızı) | 5 / 6 |
| L298N IN1, IN2, IN3, IN4 (yön) | 7, 8, 9, 10 |
| Sol / orta / sağ sensör | A0 / A1 / A2 |

## Dosyalar

- `robot.ino`: Arduino kodu
- `devre-semasi.png`: bağlantı şeması
- `proje-raporu.pdf`: proje raporu
- `fotograflar/`: robotun görselleri

## Ekip

[Adınız Soyadınız] · Mekatronik Mühendisliği
