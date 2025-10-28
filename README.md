# 🎧 Whisper CSV Transcriber CLI

一個簡潔實用的 Whisper CLI 工具，可將語音檔（如 `.m4a`, `.mp3`, `.wav`）轉為時間段 + 辨識文字的 **CSV 或 SRT 字幕檔案**，適合逐字稿、字幕製作與語音記錄分析使用。

---

## 🔧 功能特色

- ✅ 支援 Whisper 模型選擇（tiny/base/small/medium/large）
- ✅ 自動使用 GPU（若可用）
- ✅ 支援語言指定（如 zh、en）
- ✅ 產出標準 `.csv` 或 `.srt` 格式（含時間與文字欄位）
- ✅ 可自訂輸出檔案名稱（`--out`，自動加上對應副檔名）

---

## 📦 安裝與設定

### 1. 建立虛擬環境（可選）
```bash
python -m venv whisper-env
source whisper-env/bin/activate
```

### 2. 安裝必要套件
```bash
pip install git+https://github.com/openai/whisper.git
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

如果沒有 GPU，可改安裝 CPU 版本：
pip install torch torchvision torchaudio
```

### 使用方式
```bash
# 輸出 CSV
python transcribe_csv.py --file "你的音檔.m4a" --model medium --lang zh --format csv

# 輸出 SRT 字幕檔
python transcribe_csv.py --file "你的音檔.m4a" --model medium --lang zh --format srt

# 同時輸出 CSV + SRT，並自訂輸出檔名（不含副檔名）
python transcribe_csv.py --file "你的音檔.m4a" --model medium --lang zh --out "逐字稿" --format both
```

## 📥 CLI 參數說明
| 參數     | 說明                         | 範例                  |
|----------|------------------------------|-----------------------|
| `--file` | ✅ 必填：音訊檔案路徑（可含空格） | `"語音 0702.m4a"`     |
| `--model`| Whisper 模型大小（預設：base）   | `tiny`, `base`, `small`, `medium`, `large` |
| `--lang` | 語音語言（預設：zh）            | `zh`, `en`, `ja`, ... |
| `--out`  | 自訂輸出檔名（選填，會自動加上對應副檔名） | `--out result` |
| `--format` | 輸出格式（預設：csv）           | `csv`, `srt`, `both` |

## 📄 輸出範例

以下範例節錄自 Whisper `tiny` 模型跑過一小段示範音檔後的輸出，實際結果會依音檔內容而異：

**SRT**

```srt
1
00:00:00,000 --> 00:00:03,120
大家好，歡迎收聽今天的節目。

2
00:00:03,120 --> 00:00:05,640
我們要聊的是語音轉文字的工作流程。
```

**CSV**

```csv
start,end,text
0.0,3.12,大家好，歡迎收聽今天的節目。
3.12,5.64,我們要聊的是語音轉文字的工作流程。
```

