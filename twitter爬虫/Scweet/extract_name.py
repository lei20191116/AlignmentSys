import csv
import io
import json
import os

# 存储用户名的集合
usernames = set()

# 文件夹路径
folder_path = 'usernameOutputs'

# 遍历文件夹下的所有CSV文件
for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):  # 仅处理CSV文件
        file_path = os.path.join(folder_path, filename)
        if os.path.getsize(file_path) > 4:  # 判断文件大小是否大于0
            with io.open(file_path, 'r', newline='', encoding='utf-8', errors='ignore') as f:
                reader = csv.reader((line.replace('\0', '') for line in f), delimiter=",")
                next(reader, None)  # 跳过表头

                for row in reader:
                    cleaned_row = [cell.replace('\x00', '') for cell in row]  # 清理无效字符
                    print(cleaned_row[1])
                    username = cleaned_row[1]  # 根据表头中的位置提取用户名
                    usernames.add(username)
usernamelist = list(usernames)
# 打印去重后的用户名集合
print(usernamelist)
print(len(usernames))
with open('username.json', 'w') as f:
    json.dump(usernamelist, f)
