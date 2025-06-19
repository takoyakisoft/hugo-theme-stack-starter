import os
import brotli
import argparse
from pathlib import Path
import sys

def compress_file_brotli(input_path, output_path, quality=11):
    """指定されたファイルをBrotliで圧縮します。"""
    try:
        with open(input_path, 'rb') as f_in:
            data = f_in.read()
        compressed_data = brotli.compress(data, quality=quality)
        with open(output_path, 'wb') as f_out:
            f_out.write(compressed_data)
        # 元ファイルのサイズと圧縮後ファイルのサイズを表示
        original_size = os.path.getsize(input_path)
        compressed_size = os.path.getsize(output_path)
        print(f"  -> {output_path.name} ({compressed_size / 1024 / 1024:.2f} MB / 元: {original_size / 1024 / 1024:.2f} MB)")
        return True
    except FileNotFoundError:
        print(f"エラー: ファイルが見つかりません - {input_path}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"エラー: {input_path} の圧縮中にエラーが発生しました - {e}", file=sys.stderr)
        return False

def main():
    parser = argparse.ArgumentParser(description="指定フォルダ内の全ての .wasm と .pck ファイルをBrotli圧縮し、末尾に .br を追加します。")
    parser.add_argument("folder_path", help="対象ファイルが含まれるフォルダのパス")
    parser.add_argument("-q", "--quality", type=int, default=11, help="Brotli圧縮品質 (0-11, デフォルト: 11)")
    parser.add_argument("--keep-original", action="store_true", help="圧縮後も元の .wasm/.pck ファイルを残します。")

    args = parser.parse_args()

    folder = Path(args.folder_path).resolve() # 絶対パスに変換
    quality = args.quality
    keep_original = args.keep_original

    if not folder.is_dir():
        print(f"エラー: 指定されたフォルダが見つかりません - {args.folder_path}", file=sys.stderr)
        sys.exit(1)

    if not (0 <= quality <= 11):
        print("エラー: 圧縮品質は0から11の間で指定してください。", file=sys.stderr)
        sys.exit(1)

    print(f"処理を開始します: フォルダ='{folder}', 圧縮品質={quality}")
    if keep_original:
        print("元の .wasm/.pck ファイルは保持されます。")
    else:
        print("元の .wasm/.pck ファイルは圧縮後に削除されます。")


    files_to_compress = []
    # フォルダ直下のファイルのみを検索
    for item in folder.iterdir():
        if item.is_file() and (item.suffix == '.wasm' or item.suffix == '.pck'):
             # 既に.br圧縮されているファイルは対象外にする
             if not item.name.endswith('.br'):
                 files_to_compress.append(item)


    if not files_to_compress:
        print("\n情報: フォルダ内に圧縮対象の .wasm または .pck ファイルが見つかりませんでした。")
        sys.exit(0) # 処理対象がないので終了

    compressed_files_count = 0
    deleted_files_count = 0

    print("\n--- 圧縮処理 ---")
    for file_path in files_to_compress:
        # 出力ファイル名は 元のファイル名 + ".br"
        br_file_path = file_path.parent / (file_path.name + '.br')

        print(f"圧縮中: {file_path.name}")
        if compress_file_brotli(file_path, br_file_path, quality=quality):
            compressed_files_count += 1

            if not keep_original:
                try:
                    os.remove(file_path)
                    print(f"  削除: 元ファイル {file_path.name}")
                    deleted_files_count +=1
                except Exception as e:
                    print(f"  警告: 元ファイル {file_path.name} の削除に失敗しました - {e}", file=sys.stderr)

    if compressed_files_count > 0:
        print(f"\n{compressed_files_count} 個のファイルを圧縮しました。")
        if not keep_original:
             print(f"{deleted_files_count} 個の元ファイルを削除しました。")
    else:
         print("\n圧縮処理中にエラーが発生したか、対象ファイルがありませんでした。")

    print("\n処理が完了しました。")
    print("Webサーバー側で .br ファイルに対して 'Content-Encoding: br' ヘッダーが正しく設定されているか確認してください。")

if __name__ == "__main__":
    main()