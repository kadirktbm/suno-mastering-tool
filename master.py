#!/usr/bin/env python3
"""
Suno Mastering Tool
Türkü, Anadolu Rock, Trap Pop, Trap Rock için optimize edilmiş
ses mastering scripti.
"""

import argparse
import sys
import os
import numpy as np

try:
    from pedalboard import (
        Pedalboard, Compressor, Gain, Limiter,
        HighpassFilter, LowShelfFilter, HighShelfFilter,
        Reverb, Chorus, PeakFilter
    )
    from pedalboard.io import AudioFile
    import pyloudnorm as pyln
except ImportError:
    print("Eksik kütüphane! Lütfen önce şunu çalıştır:")
    print("  pip install pedalboard pyloudnorm numpy")
    sys.exit(1)


# ──────────────────────────────────────────────────────────────
# PRESET TANIMLARI
# ──────────────────────────────────────────────────────────────

PRESETS = {

    # ── TÜRKÜ ────────────────────────────────────────────────
    # Hedef: saz teli parlaklığı korunur, insan sesi öne çıkar,
    # doğal dinamikler bozulmaz, fazla parlak olmayan bir ton.
    "turku": {
        "description": "Türkü — Saz ve insan sesi odaklı, doğal dinamikler",
        "target_lufs": -16.0,  # Daha az sıkıştırılmış, nefes alan mix
        "chain": [
            HighpassFilter(cutoff_frequency_hz=60),        # Düşük rumble kes
            LowShelfFilter(cutoff_frequency_hz=150,        # Sazın gövdesi
                           gain_db=1.2),
            PeakFilter(cutoff_frequency_hz=800,            # Vokal netliği
                       gain_db=1.5, q=1.2),
            PeakFilter(cutoff_frequency_hz=3500,           # Saz teli parlaklığı
                       gain_db=2.0, q=1.5),
            PeakFilter(cutoff_frequency_hz=6000,           # Hava / nefes
                       gain_db=1.0, q=1.0),
            Compressor(threshold_db=-20,                   # Hafif comp
                       ratio=2.5,
                       attack_ms=20,
                       release_ms=200),
            Gain(gain_db=1.5),
            Limiter(threshold_db=-1.5, release_ms=150),   # Daha yumuşak limit
        ]
    },

    # ── ANADOLU ROCK ────────────────────────────────────────
    # Hedef: gitar crunch + saz elektrik tonu, davul punch,
    # vokal önde, Erkin Koray / Cem Karaca estetiği.
    "anadolu_rock": {
        "description": "Anadolu Rock — Elektrik gitar + saz, güçlü davul punch",
        "target_lufs": -13.0,  # Yayın için agresif ama tıklamayan seviye
        "chain": [
            HighpassFilter(cutoff_frequency_hz=80),        # Boomy bas kes
            LowShelfFilter(cutoff_frequency_hz=100,        # Kick gövdesi
                           gain_db=2.0),
            PeakFilter(cutoff_frequency_hz=250,            # Gitar beden
                       gain_db=-1.5, q=1.0),               # Boxy tonu azalt
            PeakFilter(cutoff_frequency_hz=1000,           # Orta netlik
                       gain_db=1.0, q=1.2),
            PeakFilter(cutoff_frequency_hz=4000,           # Gitar crunch
                       gain_db=2.5, q=1.5),
            HighShelfFilter(cutoff_frequency_hz=10000,     # Kibarca parlak
                            gain_db=1.5),
            Compressor(threshold_db=-18,                   # Orta agresif comp
                       ratio=4.0,
                       attack_ms=8,
                       release_ms=120),
            Gain(gain_db=3.0),
            Limiter(threshold_db=-1.0, release_ms=80),
        ]
    },

    # ── TRAP POP ────────────────────────────────────────────
    # Hedef: hi-hat netliği, derin 808, vokal üst frekansı,
    # modern streaming mix (Spotify/Apple Music uyumlu).
    "trap_pop": {
        "description": "Trap Pop — 808 derinlik, hi-hat netliği, modern vokal",
        "target_lufs": -14.0,  # Spotify / Apple Music standardı
        "chain": [
            HighpassFilter(cutoff_frequency_hz=30),        # Sub hum kes
            LowShelfFilter(cutoff_frequency_hz=60,         # 808 sub güç
                           gain_db=3.0),
            PeakFilter(cutoff_frequency_hz=200,            # Bas boğukluk azalt
                       gain_db=-2.0, q=1.5),
            PeakFilter(cutoff_frequency_hz=1500,           # Vokal netlik
                       gain_db=1.5, q=1.0),
            PeakFilter(cutoff_frequency_hz=8000,           # Hi-hat air
                       gain_db=2.5, q=1.0),
            HighShelfFilter(cutoff_frequency_hz=12000,     # Parlaklık
                            gain_db=2.0),
            Compressor(threshold_db=-16,                   # Modern ses baskısı
                       ratio=5.0,
                       attack_ms=5,
                       release_ms=80),
            Gain(gain_db=3.5),
            Limiter(threshold_db=-0.5, release_ms=60),    # Agresif limit
        ]
    },

    # ── TRAP ROCK ───────────────────────────────────────────
    # Hedef: trap'ın 808 alt frekansı + rock'ın gitar agresifliği,
    # davul hem punch hem crunch taşır.
    "trap_rock": {
        "description": "Trap Rock — 808 sub + gitar agresifliği, hybrid punch",
        "target_lufs": -13.5,
        "chain": [
            HighpassFilter(cutoff_frequency_hz=35),        # Çok düşük sub kes
            LowShelfFilter(cutoff_frequency_hz=60,         # 808 varlığı
                           gain_db=2.5),
            PeakFilter(cutoff_frequency_hz=180,            # Kick + 808 çakışma
                       gain_db=-1.5, q=1.2),               # Hafif azalt
            PeakFilter(cutoff_frequency_hz=500,            # Orta bulanıklık
                       gain_db=-1.0, q=1.0),
            PeakFilter(cutoff_frequency_hz=3000,           # Gitar presence
                       gain_db=2.0, q=1.5),
            PeakFilter(cutoff_frequency_hz=7000,           # Hi-hat + gitar tiz
                       gain_db=2.0, q=1.0),
            HighShelfFilter(cutoff_frequency_hz=12000,     # Hava
                            gain_db=1.5),
            Compressor(threshold_db=-17,                   # Agresif comp
                       ratio=5.0,
                       attack_ms=6,
                       release_ms=90),
            Gain(gain_db=3.0),
            Limiter(threshold_db=-0.8, release_ms=70),
        ]
    },
}


# ──────────────────────────────────────────────────────────────
# MASTERING FONKSİYONU
# ──────────────────────────────────────────────────────────────

def master_track(input_path: str, output_path: str, preset_name: str) -> None:
    if preset_name not in PRESETS:
        raise ValueError(f"Bilinmeyen preset: {preset_name}. "
                         f"Geçerli presetler: {list(PRESETS.keys())}")

    preset = PRESETS[preset_name]
    print(f"\n🎛  Preset  : {preset['description']}")
    print(f"📂  Girdi   : {input_path}")
    print(f"💾  Çıktı   : {output_path}")
    print(f"🔊  Hedef   : {preset['target_lufs']} LUFS\n")

    # Dosyayı oku
    with AudioFile(input_path) as f:
        audio = f.read(f.frames)
        sample_rate = f.samplerate
    print(f"   Sample rate : {sample_rate} Hz")
    print(f"   Kanal sayısı: {audio.shape[0]}")
    print(f"   Süre        : {audio.shape[1] / sample_rate:.1f} sn")

    # Giriş LUFS ölç
    meter = pyln.Meter(sample_rate)
    input_loudness = meter.integrated_loudness(audio.T)
    print(f"\n   Giriş LUFS  : {input_loudness:.1f}")

    # Pedalboard uygula
    board = Pedalboard(preset["chain"])
    processed = board(audio, sample_rate)

    # LUFS normalizasyon
    output_loudness = meter.integrated_loudness(processed.T)
    gain_db = preset["target_lufs"] - output_loudness
    factor = 10 ** (gain_db / 20)
    processed = processed * factor

    # Klip kontrolü
    peak = np.max(np.abs(processed))
    if peak > 0.99:
        print(f"   ⚠️  Peak {peak:.3f} — hafif clip koruması uygulandı")
        processed = processed * (0.99 / peak)

    # Kaydet
    with AudioFile(output_path, "w", sample_rate, processed.shape[0]) as f:
        f.write(processed)

    # Sonuç raporu
    final_loudness = meter.integrated_loudness(processed.T)
    peak_db = 20 * np.log10(np.max(np.abs(processed)) + 1e-9)
    print(f"\n✅  Mastering tamamlandı!")
    print(f"   Çıkış LUFS  : {final_loudness:.1f}")
    print(f"   True Peak   : {peak_db:.1f} dBTP")
    print(f"   Kaydedildi  : {output_path}\n")


# ──────────────────────────────────────────────────────────────
# CLI
# ──────────────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Suno Mastering Tool — Türkü / Anadolu Rock / Trap Pop / Trap Rock",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Örnekler:
  python master.py -i suno.mp3 -p turku
  python master.py -i suno.wav -p trap_pop -o mastered_trap.wav
  python master.py --list-presets
        """
    )
    parser.add_argument("-i", "--input",   help="Giriş dosyası (.mp3 veya .wav)")
    parser.add_argument("-o", "--output",  help="Çıkış dosyası (varsayılan: mastered_<giriş>.wav)")
    parser.add_argument("-p", "--preset",  help="Preset adı", choices=list(PRESETS.keys()))
    parser.add_argument("--list-presets",  action="store_true", help="Mevcut presetleri listele")
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.list_presets:
        print("\nMevcut presetler:\n")
        for name, info in PRESETS.items():
            print(f"  {name:<16} → {info['description']}  (hedef: {info['target_lufs']} LUFS)")
        print()
        return

    if not args.input or not args.preset:
        parser.print_help()
        sys.exit(1)

    if not os.path.exists(args.input):
        print(f"Hata: '{args.input}' bulunamadı.")
        sys.exit(1)

    if args.output:
        output_path = args.output
    else:
        base = os.path.splitext(os.path.basename(args.input))[0]
        output_path = f"mastered_{base}.wav"

    master_track(args.input, output_path, args.preset)


if __name__ == "__main__":
    main()
