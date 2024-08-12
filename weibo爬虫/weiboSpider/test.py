import json
import sys

user_id_list = []
with open("user_id_list.txt", 'rb') as f:
    try:
        lines = f.read().splitlines()
        lines = [line.decode('utf-8-sig') for line in lines]
    except UnicodeDecodeError:
        sys.exit(u'%s文件应为utf-8编码，请先将文件编码转为utf-8再运行程序' )
    for line in lines:
        info = line.split(' ')
        if len(info) > 0 and info[0].isdigit():
            user_id = info[0]
            if user_id not in user_id_list:
                user_id_list.append(user_id)

with open('UserPosts/userName.json', 'w') as f:
    f.seek(0, 2)  # 将文件指针移动到文件末尾

    json.dump(user_id_list, f)