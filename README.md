# 🎧 Whisper CSV Transcriber CLI

一個簡潔實用的 Whisper CLI 工具，可將語音檔（如 `.m4a`, `.mp3`, `.wav`）轉為時間段 + 辨識文字的 **CSV 檔案**，適合逐字稿、語音記錄分析使用。

---

## 🔧 功能特色

- ✅ 支援 Whisper 模型選擇（tiny/base/small/medium/large）
- ✅ 自動使用 GPU（若可用）
- ✅ 支援語言指定（如 zh、en）
- ✅ 產出標準 `.csv` 格式（含時間與文字欄位）
- ✅ 可自訂輸出檔案名稱（`--out`）

---

## 📦 安裝與設定

### 1. 建立虛擬環境（可選）
```bash
python -m venv whisper-env
source whisper-env/bin/activate

### 2. 安裝必要套件
pip install git+https://github.com/openai/whisper.git
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

如果沒有 GPU，可改安裝 CPU 版本：
pip install torch torchvision torchaudio

### 使用方式
python transcribe_csv.py --file "你的音檔.m4a" --model medium --lang zh --out "逐字稿.csv"

##📥 CLI 參數說明
參數	說明	範例
--file	✅ 必填：音訊檔案路徑（可含空格）	"語音 0702.m4a"
--model	Whisper 模型大小（預設：base）	tiny, base, small, medium, large
--lang	語音語言（預設：zh）	zh, en, ja, ...
--out	自訂輸出 CSV 檔名（選填）	--out result.csv
