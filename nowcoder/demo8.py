"""
@Name:demo8.py
@Auth:89703 
@Date:2023/9/4
"""

# import re
#
# url = "https://www.nowcoder.com/exam/test/73113614/detail?pid=52037159"
#
# # 使用正则表达式匹配数字
# match_exam_id = re.search(r'/(\d+)/detail\?pid=(\d+)', url)
#
# if match_exam_id:
#     exam_id = match_exam_id.group(1)
#     pid = match_exam_id.group(2)
#     print("Exam ID:", exam_id)
#     print("PID:", pid)
# else:
#     print("未找到匹配的数字")

import yaml

with open('id.yaml', 'r', encoding='utf-8') as f:
    dict = yaml.safe_load(f)
    test_id_list = list(dict.keys())

    paper_id_list = list(dict.values())
    print(test_id_list)
    print(paper_id_list)
    print(len(test_id_list))
    print(len(paper_id_list))
