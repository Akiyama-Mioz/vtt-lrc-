import re
import os
import sys

def convert_vtt_to_lrc_content(vtt_content):
    lrc_lines = []
    time_pattern = re.compile(r'(\d{2}):(\d{2}):(\d{2})\.(\d{3}) --> \d{2}:\d{2}:\d{2}\.\d{3}')
    lrc_timestamp = None  # 初始化lrc_timestamp
    
    for line in vtt_content:
        time_match = time_pattern.match(line)
        if time_match:
            hours, minutes, seconds, milliseconds = map(int, time_match.groups())
            total_minutes = hours * 60 + minutes
            lrc_timestamp = f"[{total_minutes:02}:{seconds:02}.{milliseconds // 10:02}]"
        elif line.strip() and not line.startswith('WEBVTT'):
            if lrc_timestamp:  # 确保lrc_timestamp已被赋值
                lrc_lines.append(lrc_timestamp + line.strip())
    
    return lrc_lines

def vtt_to_lrc_auto_rename(vtt_file_path):
    # 获取文件名和目录
    file_dir, file_name = os.path.split(vtt_file_path)
    base_name, _ = os.path.splitext(file_name)
    lrc_file_path = os.path.join(file_dir, base_name + '.lrc')

    with open(vtt_file_path, 'r', encoding='utf-8') as vtt_file:
        vtt_content = vtt_file.readlines()

    lrc_lines = convert_vtt_to_lrc_content(vtt_content)

    with open(lrc_file_path, 'w', encoding='utf-8') as lrc_file:
        lrc_file.write('\n'.join(lrc_lines))

    print(f"转换完成: {lrc_file_path}")

def process_multiple_files(file_paths):
    for file_path in file_paths:
        if os.path.isdir(file_path):
            process_directory(file_path)
        else:
            vtt_to_lrc_auto_rename(file_path)

def process_directory(directory_path):
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.vtt'):
                vtt_file_path = os.path.join(root, file)
                vtt_to_lrc_auto_rename(vtt_file_path)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("请提供一个或多个VTT文件路径或文件夹路径作为参数。")
    else:
        process_multiple_files(sys.argv[1:])