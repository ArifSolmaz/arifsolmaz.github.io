# What's GitHub Good For? · Class kit

A 45-minute beginner class. No terminal, branches or pull requests; everything happens in the browser and on the phone.

## What's in the kit

- `example-project/`: the example project you upload during the live demo (README, Arduino code, circuit diagram, report, picture)
- `ornek-proje/`: the same project in Turkish
- `qr-sinif-sayfasi.png`: QR code for the class page → github.com/arifsolmaz/sinif-duvari/issues/1
- The animations are in separate zip files: GIF (for the slides) and MP4

## Before class (5 minutes)

1. **Repository for the class page:** github.com/new → name: `sinif-duvari` → Public → Create repository. If it already exists, use it.
2. **Class page:** Issues → New issue → paste the title and text below → Create. You can pin it from the right-hand menu with **Pin issue**.
3. **Check the QR:** Look at the issue number. If it's #1, the QR on the slide is right. If not, make a new one: on the issue page in Chrome, right-click the page → "Create QR Code for this page", and show that instead of the QR on the slide.
4. **Example project:** Put the `example-project` folder on the desktop. Check that `robot.ino` says `THRESHOLD = 500`; in the time-machine demo you'll change it to 900.
5. **Arduino IDE** open (for the ready-made code demo).
6. **Test with a phone:** Scan the QR; does the page open, can you comment? You can delete your test comment or keep it as an example.
7. **Message the students:** Send the message below a day or two before class.

## Class page: issue text

**Title:** Our class repositories

**Text:**

```
Create your first repository and post its link as a comment below.

1. github.com/new → name: my-first-project → Add README: On → Create repository
2. Tap the pencil on the README → write 2 lines about yourself → Commit changes
3. Come back to this page → post your repository link as a comment → Comment

Example comment: github.com/your-username/my-first-project
```

## Live demos

Details are in the slides' speaker notes.

| Slide | What to do |
|---|---|
| Benefit 1 · Never lost | Show your own GitHub profile on your phone. |
| Put your project on GitHub | github.com/new → `example-project` → Add README: On → Create repository → Add file → Upload files → drag in the folder's files → Commit changes |
| Benefit 2 · Time machine | `robot.ino` → pencil → `THRESHOLD = 500` → `900` → Commit changes → History → click the save |
| Benefit 3 · Team to-do list | Issues → New issue → "Take photos of the robot" → Assignees: you → Create → Close issue |
| Benefit 4 · Ready-made code | Search "DHT sensor library" → adafruit/DHT-sensor-library → Code → Download ZIP → Arduino IDE: Sketch → Include Library → Add .ZIP Library... |
| Benefit 5 · Portfolio | github.com/arifsolmaz → pinned repositories → a good README |
| Benefit 6 · Free for students | education.github.com/pack |

## Messages for students

**A day or two before class:**

> Hi! In [day]'s class we'll use GitHub. Before class, please create a free account at github.com/signup; it takes two or three minutes and you'll need to enter a code from your email. Pick a username that's easy to remember; you'll use it on your CV later. Bring your phone, charged.

**After class:**

> Today's slides and animations: [link]. This week's task: put one of your projects on GitHub (code, a diagram, a photo and a README) and post its link as a comment on the class page: github.com/arifsolmaz/sinif-duvari/issues/1. For the Student Pack: education.github.com/pack

## If something goes wrong

- **No internet:** The animations show every step; the GIF and MP4 files play offline.
- **A student has no account:** They pair with a neighbor and do the task at home.
- **Can't find the pencil:** Top-right corner of the README box; otherwise tap the README.md file and use the pencil there.
- **"already exists" warning:** Pick another name: `my-first-project-2`.

## Privacy

The class page lives in a public repository. Students should post only their repository link; no phone or student numbers.
