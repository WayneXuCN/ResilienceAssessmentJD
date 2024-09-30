import argparse
import json
import os

from .core.UnifiedModel import UnifiedModel


def main():
    parser = argparse.ArgumentParser(description="Run Resilience Assessment.")
    parser.add_argument("input_path", type=str, help="Path to the input JSON file.")
    parser.add_argument("output_path", type=str, help="Path to the output JSON file.")

    args = parser.parse_args()

    # 读取输入文件
    with open(args.input_path, encoding="utf-8") as file:
        request_json = json.load(file)

    # 初始化模型并执行
    model = UnifiedModel(request_json)
    result = model.execute()

    # 自动生成输出文件名
    base_name = os.path.basename(args.input_path)  # 获取输入文件名
    name, ext = os.path.splitext(base_name)  # 分离文件名和扩展名
    output_filename = f"{name}_result.json"  # 新文件名
    output_file_path = os.path.join(args.output_path, output_filename)

    # 保存结果
    with open(output_file_path, "w", encoding="utf-8") as file:
        json.dump(result, file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()
