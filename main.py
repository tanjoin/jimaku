import importlib
import argparse
jimaku = importlib.import_module('lib.jimaku')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='字幕をつけます')
    parser.add_argument('src_file', help='画像ファイル')
    parser.add_argument('text', help='入力したいテキスト')

    args = parser.parse_args()
    src_file = args.src_file
    text = args.text

    print(src_file.rsplit('/', 1)[-1])
    print(text)

    jimaku.put(src_file, text)

