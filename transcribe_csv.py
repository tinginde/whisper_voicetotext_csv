
import whisper
import argparse
import os
import csv
import torch

def transcribe_to_csv(audio_file, model_size="base", language="zh", device="cuda", output_path=None):
    if not os.path.exists(audio_file):
        print(f"❌ 找不到音檔：{audio_file}")
        return

    if device == "cuda" and not torch.cuda.is_available():
        print("⚠️ 沒有可用的 GPU，改用 CPU")
        device = "cpu"

    print(f"\n🔍 載入模型：{model_size}（設備：{device}）")
    model = whisper.load_model(model_size, device=device)

    print(f"🎧 開始轉錄：{audio_file}")
    result = model.transcribe(audio_file, language=language, verbose=False)

    if output_path is None:
        output_path = os.path.splitext(audio_file)[0] + "_transcript.csv"

    with open(output_path, mode='w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['start_time', 'end_time', 'text'])

        for segment in result["segments"]:
            writer.writerow([
                round(segment["start"], 2),
                round(segment["end"], 2),
                segment["text"].strip()
            ])

    print(f"\n✅ 已輸出為 CSV 檔：{output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Whisper CLI 工具：語音檔轉為時間段 + 文字的 CSV 檔"
    )
    parser.add_argument('--file', type=str, required=True, help="輸入音檔路徑，例如 sample.m4a")
    parser.add_argument('--model', type=str, default="base", help="Whisper 模型大小：tiny, base, small, medium, large")
    parser.add_argument('--lang', type=str, default="zh", help="語音語言，例如 zh、en")
    parser.add_argument('--out', type=str, help="輸出 CSV 檔案名稱（選填）")

    args = parser.parse_args()
    transcribe_to_csv(args.file, args.model, args.lang, output_path=args.out)
