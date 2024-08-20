# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :Test.py.py
# @Time      :2024/8/19 下午10:34
# @Author    :Wenjie Xu
# @Email     :wenjie_xu2000@outlook.com

import json
import os
from ResilienceAssessmentJD.core.UnifiedModel import UnifiedModel


input_path = r"E:\ResilienceAssessmentJD\ResilienceAssessmentJD\data\data_test.json"
output_path = r"E:\ResilienceAssessmentJD\ResilienceAssessmentJD\data"
# 读取输入文件
with open(input_path, "r", encoding="utf-8") as file:
    request_json = json.load(file)

# 初始化模型并执行
model = UnifiedModel(request_json)
result = model.execute()

# 自动生成输出文件名
base_name = os.path.basename(input_path)  # 获取输入文件名
name, ext = os.path.splitext(base_name)  # 分离文件名和扩展名
output_filename = f"{name}_result.json"  # 新文件名
output_file_path = os.path.join(output_path, output_filename)

# 保存结果
with open(output_file_path, "w", encoding="utf-8") as file:
    json.dump(result, file, ensure_ascii=False, indent=4)
