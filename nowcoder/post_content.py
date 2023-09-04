"""
@Name:post_content.py
@Auth:89703 
@Date:2023/8/22
"""



import json
from time import sleep

import requests
import yaml
from jsonpath import jsonpath






def get_content():

    all_yaml = []
    timu = ""
    letters = ["A", "B", "C", "D", "E", "F", "G"]
    cookies = {
        'NOWCODERCLINETID': 'B46BC221825EE9ABEE1C09BF4B9FFC4A',
        'NOWCODERUID': '2D77180B091323A0EBE944156A9907E2',
        'gr_user_id': '2380f540-e194-4944-80df-7cb8126f8be9',
        'isAgreementChecked': 'true',
        'c196c3667d214851b11233f5c17f99d5_gr_last_sent_cs1': '43856501',
        't': '727EC281E4B69C943EA807E171914CC2',
        '_clck': '19olwgk|2|fe9|0|1308',
        'c196c3667d214851b11233f5c17f99d5_gr_session_id': 'e8c31d1b-b73c-49f8-b4df-b2602b731d61',
        'c196c3667d214851b11233f5c17f99d5_gr_last_sent_sid_with_cs1': 'e8c31d1b-b73c-49f8-b4df-b2602b731d61',
        'c196c3667d214851b11233f5c17f99d5_gr_session_id_e8c31d1b-b73c-49f8-b4df-b2602b731d61': 'true',
        'Hm_lvt_a808a1326b6c06c437de769d1b85b870': '1692237986,1692341511,1692501285,1692583839',
        'acw_tc': 'bd3b3a2387dfd72ded3b8d3bc3d03d4158c31637c10c709236751e30344f08da',
        'c196c3667d214851b11233f5c17f99d5_gr_cs1': '43856501',
        'Hm_lpvt_a808a1326b6c06c437de769d1b85b870': '1692588618',
    }
    # 抓取试题内容的请求头
    headers = {
        'authority': 'gw-c.nowcoder.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9,ja;q=0.8',
        'content-type': 'application/json',
        # 'cookie': 'NOWCODERCLINETID=B46BC221825EE9ABEE1C09BF4B9FFC4A; NOWCODERUID=2D77180B091323A0EBE944156A9907E2; gr_user_id=2380f540-e194-4944-80df-7cb8126f8be9; isAgreementChecked=true; c196c3667d214851b11233f5c17f99d5_gr_last_sent_cs1=43856501; t=727EC281E4B69C943EA807E171914CC2; _clck=19olwgk|2|fe9|0|1308; c196c3667d214851b11233f5c17f99d5_gr_session_id=e8c31d1b-b73c-49f8-b4df-b2602b731d61; c196c3667d214851b11233f5c17f99d5_gr_last_sent_sid_with_cs1=e8c31d1b-b73c-49f8-b4df-b2602b731d61; c196c3667d214851b11233f5c17f99d5_gr_session_id_e8c31d1b-b73c-49f8-b4df-b2602b731d61=true; Hm_lvt_a808a1326b6c06c437de769d1b85b870=1692237986,1692341511,1692501285,1692583839; acw_tc=bd3b3a2387dfd72ded3b8d3bc3d03d4158c31637c10c709236751e30344f08da; c196c3667d214851b11233f5c17f99d5_gr_cs1=43856501; Hm_lpvt_a808a1326b6c06c437de769d1b85b870=1692588618',
        'origin': 'https://www.nowcoder.com',
        'referer': 'https://www.nowcoder.com/',
        'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    params = {
        '_': '1692588618212',
    }

    # json_data = {
    #     'testId': 72437927,
    #     'paperId': 13932698,
    # }
    # json_data = {"testId":73110294,"paperId":51799538}
    # 获取 考试id及试题id，
    with open('id.yaml', 'r', encoding='utf-8') as f:
        dict = yaml.safe_load(f)
        # 将字典的key values 分别转换成列表
        test_id_list = list(dict.keys())

        paper_id_list = list(dict.values())

        for test_id in test_id_list:
            for paper_id in paper_id_list:
                # 将字符串转换成int，符合接口要求
                test_id = int(test_id)
                paper_id = int(paper_id)

                json_data = {"testId": test_id, "paperId": paper_id}


            response = requests.post(
                'https://gw-c.nowcoder.com/api/sparta/test/detail',
                params=params,
                cookies=cookies,
                headers=headers,
                json=json_data,
            )
            # 获取试题名称
            paper = jsonpath(response.json(), '$..paperName')
            for item in paper:
                paper_name = item.strip("'")

            # 这是一个列表
            all_details = jsonpath(response.json(), '$..paperQuestionDetails')
            for item in all_details[0]:
                topic_dict = {}
                title = item['content']
                print(f"题目：{title}")
                timu +=title

                # 添加\n换行

                timu +='\n'
                # topic_dict['title'] = title

                choose_list = item['chooseAnswer']

                if choose_list is None:
                    print("简答题")
                    timu += '\n\n\n'

                else:
                    # 选择题部分
                    ch_list = {}
                    j = 0
                    for choose in choose_list:
                        # 在每一题中间添加换行
                        timu += '\n'
                        # 根据选项数量生成ABCDEFG选项
                        key = letters[j]
                        j += 1
                        item_choose = choose['content']
                        print(f"每一个选项：{item_choose}")
                        ch_list[key] = item_choose
                        timu += f'{key}：{item_choose}'
                        timu += '\n'
                    timu += '\n'
                    topic_dict['choose'] = ch_list
                timu += '\n'

            # 试题内容写为字符串a
            a = str.replace(timu, r'\xa0', '&nbsp;')

            # 发布topic的请求地址
            url = "https://ceshiren.com/posts.json"
            # 请求头
            header = {
                "Api-Key": "a462d4b04fc4f4dba62a10075c3b3344363b8476f3015d3b37473c6f344712ab"
            }
            params = {
                "title": paper_name,
                "raw": a,
                "draft_key": "new_topic",
                # 发布的节点
                "category": "231",
            }
            print(params)

            res = requests.post(url, json=params, headers=header)
            print(res)




# 入口函数
if __name__ == '__main__':
    get_content()
