#!/data/data/com.termux/files/usr/bin/bash
# ─────────────────────────────────────────────────────────────
# Termux kurulum scripti — Suno Mastering Tool
# Çalıştır: bash setup_termux.sh
# ─────────────────────────────────────────────────────────────

set -e

echo ""
echo "🎛  Suno Mastering Tool — Termux Kurulumu"
echo "─────────────────────────────────────────"

# Paket güncellemesi
echo "📦 Paketler güncelleniyor..."
pkg update -y && pkg upgrade -y

# Gerekli sistem paketleri
echo "📦 Sistem paketleri kuruluyor..."
pkg install -y python python-pip ffmpeg clang libsndfile

# Python kütüphaneleri
echo "🐍 Python kütüphaneleri kuruluyor..."
pip install --upgrade pip
pip install pedalboard pyloudnorm numpy

# Storage izni (dosyalara erişim için)
echo ""
echo "📂 Depolama izni isteniyor..."
echo "   (Çıkan pencerede 'İzin Ver' ye bas)"
termux-setup-storage

echo ""
echo "✅ Kurulum tamamlandı!"
echo ""
echo "Kullanım:"
echo "  python master.py -i /storage/emulated/0/Download/suno.mp3 -p turku"
echo "  python master.py --list-presets"
echo ""
