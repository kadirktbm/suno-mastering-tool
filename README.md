# 🎛 Suno Mastering Tool

Suno AI'dan indirdiğin şarkıları **Türkü, Anadolu Rock, Trap Pop ve Trap Rock** stillerine özel preset zinciriyle masterlar. Android telefonda **Termux** üzerinden çalışır, bilgisayar gerekmez.

---

## Presetler

| Preset | Stil | Hedef LUFS | Ne yapar? |
|---|---|---|---|
| `turku` | Türkü | −16 | Saz teli parlaklığı, vokal öne çıkar, doğal dinamikler |
| `anadolu_rock` | Anadolu Rock | −13 | Elektrik gitar crunch, davul punch, Erkin Koray estetiği |
| `trap_pop` | Trap Pop | −14 | 808 sub derinliği, hi-hat netliği, Spotify standardı |
| `trap_rock` | Trap Rock | −13.5 | 808 + gitar hibrit, agresif ama tıklamayan |

---

## Kurulum (Android — Termux)

### 1. Termux'u yükle
F-Droid'den indir → [f-droid.org](https://f-droid.org) → "Termux" ara  
*(Play Store versiyonu eski kalıyor, F-Droid önerilir)*

### 2. Repo'yu indir ve kur

```bash
pkg install git -y
git clone https://github.com/KULLANICIADIN/suno-mastering-tool
cd suno-mastering-tool
bash setup_termux.sh
```

> `setup_termux.sh` kurulum adımlarını otomatik yapar.  
> Ortada bir pencere açılırsa **"İzin Ver"** de.

### 3. Hazır!

---

## Kullanım

### Tek dosya

```bash
# Suno'dan indirdiğin MP3'ü masterla
python master.py -i /storage/emulated/0/Download/sarki.mp3 -p turku

# Çıktı dosyasını da belirt
python master.py -i sarki.mp3 -o mastered_sarki.wav -p anadolu_rock

# Mevcut presetleri listele
python master.py --list-presets
```

### Toplu işlem (klasördeki hepsi)

```bash
# İndirilenler klasöründeki tüm şarkıları trap_pop ile masterla
python batch_master.py -d /storage/emulated/0/Download/sunolarim -p trap_pop

# Çıktı klasörünü belirt
python batch_master.py -d ./sunolarim -p trap_rock -o ./mastered
```

---

## Tipik iş akışı

```
Suno'da üret → MP3 indir → Download klasörüne kaydet
       ↓
Termux aç → python master.py -i ... -p turku
       ↓
mastered_*.wav → paylaş / yükle
```

---

## Preset detayları

### `turku`
- **HP filter** 60 Hz → alçak rumble keser
- **Low shelf** 150 Hz +1.2 dB → sazın gövdesi
- **Peak** 800 Hz +1.5 dB → vokal netliği
- **Peak** 3.5 kHz +2.0 dB → saz teli parlaklığı
- **Peak** 6 kHz +1.0 dB → hava / nefes
- **Compressor** ratio 2.5:1, hafif → doğal dinamikler
- **Limiter** −1.5 dBTP → yumuşak limit
- **Hedef** −16 LUFS (nefes alan mix)

### `anadolu_rock`
- **HP filter** 80 Hz → boomy bas temizler
- **Low shelf** 100 Hz +2.0 dB → kick gövdesi
- **Peak** 250 Hz −1.5 dB → boxy orta azaltır
- **Peak** 4 kHz +2.5 dB → gitar crunch presence
- **High shelf** 10 kHz +1.5 dB → kibarca parlak
- **Compressor** ratio 4:1 → orta agresif
- **Hedef** −13 LUFS (streaming için güçlü)

### `trap_pop`
- **HP filter** 30 Hz → sub hum kes
- **Low shelf** 60 Hz +3.0 dB → 808 sub güç
- **Peak** 200 Hz −2.0 dB → bas boğukluk azalt
- **Peak** 8 kHz +2.5 dB → hi-hat air ve netlik
- **High shelf** 12 kHz +2.0 dB → modern parlaklık
- **Compressor** ratio 5:1, hızlı attack → yoğun ses
- **Limiter** −0.5 dBTP → agresif limit
- **Hedef** −14 LUFS (Spotify / Apple Music standardı)

### `trap_rock`
- **HP filter** 35 Hz → çok düşük sub kes
- **Low shelf** 60 Hz +2.5 dB → 808 varlığı
- **Peak** 180 Hz −1.5 dB → kick + 808 çakışma azalt
- **Peak** 3 kHz +2.0 dB → gitar presence
- **Peak** 7 kHz +2.0 dB → hi-hat + gitar tiz
- **Compressor** ratio 5:1, hızlı attack → hybrid agresiflik
- **Hedef** −13.5 LUFS

---

## Sorun giderme

**`ModuleNotFoundError: pedalboard`**
```bash
pip install pedalboard pyloudnorm numpy
```

**`clang` veya derleme hatası (Termux'ta)**
```bash
pkg install clang libsndfile -y
pip install pedalboard
```

**Dosyaya erişilemiyor**
```bash
termux-setup-storage
# Sonra /storage/emulated/0/Download/... yolunu kullan
```

**Çıktı çok yüksek / düşük**  
`master.py` içindeki `target_lufs` değerini değiştir:
- Daha sessiz → −16 veya −18
- Daha yüksek → −11 veya −12 *(dikkatli: distortion riski)*

---

## Kütüphaneler

- [pedalboard](https://github.com/spotify/pedalboard) — Spotify'ın açık kaynak ses efekt kütüphanesi
- [pyloudnorm](https://github.com/csteinmetz1/pyloudnorm) — ITU-R BS.1770 LUFS ölçüm
- [numpy](https://numpy.org) — Sayısal işlemler

---

## Lisans

MIT — istediğin gibi kullan, değiştir, paylaş.
