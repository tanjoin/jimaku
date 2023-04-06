import importlib
import argparse
jimaku = importlib.import_module('lib.jimaku')
font_config = importlib.import_module('lib.font_config')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='字幕をつけます')
    parser.add_argument('-s', '--src', help='画像ファイル', default = 'res/screen.png')
    parser.add_argument('-t', '--text', help='入力したいテキスト')
    parser.add_argument('-f', '--file', help='入力したいテキストファイル')
    parser.add_argument('-o', '--output', help='出力先ディレクトリ', default = "dst/")

    args = parser.parse_args()
    src = args.src
    text = args.text
    file = args.file
    output = args.output
    if not output.endswith('/'):
            output = output + '/'

    if text:
        print(text)
        jimaku.put(src, text, font_config.FontConfig(),  output)

    if file:
        print(file.rsplit('/', 1)[-1])
        jimaku.puts(src, file, font_config.FontConfig(), output)