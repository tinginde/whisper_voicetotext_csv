
import whisper
import argparse
import os
import csv
import torch

from whisper.utils import format_timestamp


def transcribe_to_csv(
    audio_file,
    model_size="base",
    language="zh",
    device="cuda",
    output_path=None,
    output_format="csv",
):
    if not os.path.exists(audio_file):
        print(f"❌ 找不到音檔：{audio_file}")
        return

    if device == "cuda" and not torch.cuda.is_available():
        print("⚠️ 沒有可用的 GPU，改用 CPU")
        device = "cpu"

    print(f"\n🔍 載入模型：{model_size}（設備：{device}）")
    model = whisper.load_model(model_size, device=device)

    output_format = output_format.lower()
    if output_format not in {"csv", "srt", "both"}:
        raise ValueError("output_format 必須是 'csv', 'srt' 或 'both'")

    print(f"🎧 開始轉錄：{audio_file}")
    result = model.transcribe(audio_file, language=language, verbose=False)
    segments = result["segments"]

    if output_path is not None:
        base_path = os.path.splitext(output_path)[0]
    else:
        base_path = os.path.splitext(audio_file)[0] + "_transcript"

    def export_csv(path):
        with open(path, mode='w', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['start_time', 'end_time', 'text'])

            for segment in segments:
                writer.writerow([
                    round(segment["start"], 2),
                    round(segment["end"], 2),
                    segment["text"].strip()
                ])

    def export_srt(path):
        with open(path, mode='w', encoding='utf-8') as f:
            for idx, segment in enumerate(segments, start=1):
                start_ts = format_timestamp(
                    segment["start"], always_include_hours=True, decimal_marker="," 
                )
                end_ts = format_timestamp(
                    segment["end"], always_include_hours=True, decimal_marker="," 
                )
                text = segment["text"].strip()

                f.write(f"{idx}\n")
                f.write(f"{start_ts} --> {end_ts}\n")
                f.write(f"{text}\n\n")

    exported_files = []

    if output_format in {"csv", "both"}:
        csv_path = base_path + ".csv"
        export_csv(csv_path)
        exported_files.append(csv_path)

    if output_format in {"srt", "both"}:
        srt_path = base_path + ".srt"
        export_srt(srt_path)
        exported_files.append(srt_path)

    for path in exported_files:
        print(f"\n✅ 已輸出檔案：{path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Whisper CLI 工具：語音檔轉為時間段 + 文字的 CSV/SRT 檔"
    )
    parser.add_argument('--file', type=str, required=True, help="輸入音檔路徑，例如 sample.m4a")
    parser.add_argument('--model', type=str, default="base", help="Whisper 模型大小：tiny, base, small, medium, large")
    parser.add_argument('--lang', type=str, default="zh", help="語音語言，例如 zh、en")
    parser.add_argument('--out', type=str, help="輸出檔案名稱（選填，預設為音檔同名加 _transcript）")
    parser.add_argument('--format', type=str, default="csv", choices=["csv", "srt", "both"], help="輸出格式：csv, srt 或 both")

    args = parser.parse_args()
    transcribe_to_csv(
        args.file,
        args.model,
        args.lang,
        output_path=args.out,
        output_format=args.format,
    )
