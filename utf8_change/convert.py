import os
import chardet


def convert_to_utf8(file_path):
    with open(file_path, 'rb') as file:
        raw_data = file.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']
        print(f"Converting {file_path} from {encoding} to UTF-8")

        if encoding != 'utf-8':
            try:
                with open(file_path, 'r', encoding=encoding) as file:
                    content = file.read()
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(content)
            except Exception as e:
                print(f"Failed to convert {file_path}: {e}")


def check_and_convert_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            convert_to_utf8(file_path)


# 检查并转换当前目录
check_and_convert_directory('app')
