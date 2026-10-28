#!/usr/bin/env python3
"""
Toplu mastering — bir klasördeki tüm MP3/WAV dosyalarını işler.
Kullanım: python batch_master.py -d ./sunolarim -p trap_pop
"""

import argparse
import os
import sys
from pathlib import Path
from master import master_track, PRESETS

SUPPORTED = {".mp3", ".wav", ".flac", ".aiff", ".aif"}


def batch_process(directory: str, preset: str, output_dir: str = None) -> None:
    source = Path(directory)
    if not source.is_dir():
        print(f"Hata: '{directory}' bir klasör değil.")
        sys.exit(1)

    files = [f for f in source.iterdir() if f.suffix.lower() in SUPPORTED]
    if not files:
        print(f"'{directory}' içinde desteklenen ses dosyası bulunamadı.")
        sys.exit(1)

    out_dir = Path(output_dir) if output_dir else source / "mastered"
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n📁  Kaynak    : {source}")
    print(f"💾  Çıktı     : {out_dir}")
    print(f"🎛  Preset    : {PRESETS[preset]['description']}")
    print(f"📝  Dosya sayısı: {len(files)}\n")
    print("─" * 50)

    success, failed = 0, []
    for i, f in enumerate(sorted(files), 1):
        print(f"[{i}/{len(files)}] {f.name}")
        out_path = str(out_dir / f"mastered_{f.stem}.wav")
        try:
            master_track(str(f), out_path, preset)
            success += 1
        except Exception as e:
            print(f"   ❌ Hata: {e}")
            failed.append(f.name)

    print("─" * 50)
    print(f"\n✅  Başarılı : {success}/{len(files)}")
    if failed:
        print(f"❌  Hatalı   : {', '.join(failed)}")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Toplu Mastering — bir klasördeki tüm dosyaları işle"
    )
    parser.add_argument("-d", "--dir",     required=True, help="Kaynak klasör")
    parser.add_argument("-p", "--preset",  required=True,
                        choices=list(PRESETS.keys()), help="Preset adı")
    parser.add_argument("-o", "--output",  help="Çıktı klasörü (varsayılan: kaynak/mastered/)")
    args = parser.parse_args()

    batch_process(args.dir, args.preset, args.output)


if __name__ == "__main__":
    main()
