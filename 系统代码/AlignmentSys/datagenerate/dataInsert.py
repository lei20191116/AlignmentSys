import csv
import json
import pymysql

# 数据库连接配置
from mysql_dealer import startDb

def insertWebsiteUser(filepath,weblink,webid):
    db = startDb("identityalignment_db")
    # 读取 JSON 文件
    with open(filepath, 'r') as file:
        data = json.load(file)

    # 用户名列表
    user_list = data

    # SQL 插入语句
    insert_sql = """
    INSERT INTO WebsiteUser (webuser_id, webuser_name, webuser_link, webid)
    VALUES (%s, %s, %s, %s)
    """
    sql = '''
            INSERT INTO WebsiteUser (webuser_id, webuser_name, webuser_link, webid)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE 
                webuser_name = VALUES(webuser_name),
                webuser_link = VALUES(webuser_link),
                webid = VALUES(webid)
            '''

    try:
        with db.cursor() as cursor:
            for user_id in user_list:
                webuser_id = str(user_id)
                webuser_name = str(user_id)
                webuser_link = weblink+str(user_id)
                webid = webid
                cursor.execute(insert_sql, (webuser_id, webuser_name, webuser_link, webid))
        db.commit()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()


def postdatatouserlist(csv_file_path,exportpath):

    # 读取 CSV 文件并提取唯一的用户列表
    unique_users = set()

    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            unique_users.add(row['User'])

    # 将唯一用户列表转换为 JSON 并存储到文件中
    unique_users_list = list(unique_users)

    with open(exportpath, mode='w', encoding='utf-8') as file:
        json.dump(unique_users_list, file, ensure_ascii=False, indent=4)

    print("Unique users have been written to", exportpath)

def insertpostdata(csv_file_path,webid):
    db = startDb("identityalignment_db")
    try:
        with db.cursor() as cursor:
            # 打开并读取 CSV 文件
            with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
                csv_reader = csv.reader(csvfile)
                next(csv_reader)  # 跳过标题行

                # 遍历 CSV 数据并插入到数据库
                for row in csv_reader:
                    _, user_id, post_time, post_domain = row

                    # 插入数据到 WebsitePostData 表
                    sql = '''
                    INSERT INTO WebsitePostData (user_id, post_time, post_domain)
                    VALUES (%s, %s, %s)
                    '''
                    cursor.execute(sql, (user_id, post_time, webid))

        # 提交事务
        db.commit()

    except Exception as e:
        print(f"An error occurred: {e}")
        db.rollback()
def domain_to_id(domain):
    mapping = {
        "Sina": 1,
        "Twitter": 2,
        "Reddit": 3
    }
    return mapping.get(domain, None)

def import_csv_to_trackingdata(csv_file_path):
    db = startDb("identityalignment_db")
    # 连接到数据库
    try:
        with db.cursor() as cursor:
            # 打开并读取 CSV 文件
            with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
                csv_reader = csv.reader(csvfile)
                next(csv_reader)  # 跳过标题行

                # 遍历 CSV 数据并插入到数据库
                for row in csv_reader:
                    _, actiontime, actiontype, domain, trackingid = row

                    # 将 Domain 转换为 domainid
                    domainid = domain_to_id(domain)
                    if domainid is None:
                        print(f"Unknown domain '{domain}' in row: {row}")
                        continue

                    # 插入数据到 trackingdata 表
                    sql = '''
                    INSERT INTO trackingdata (actiontime, actiontype, domainid, trackingid)
                    VALUES (%s, %s, %s, %s)
                    '''
                    cursor.execute(sql, (actiontime, actiontype, domainid, trackingid))

        # 提交事务
        db.commit()

    except Exception as e:
        print(f"An error occurred: {e}")
        db.rollback()

    finally:
        # 关闭连接
        db.close()

    print("Data has been inserted successfully.")


def extract_unique_tracking_ids(csv_file_path):
    tracking_ids = set()  # 使用集合确保唯一性
    try:
        with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
            csv_reader = csv.reader(csvfile)
            next(csv_reader)  # 跳过标题行

            for row in csv_reader:
                if len(row) < 4:
                    continue
                tracking_id = row[4]  # 确保索引与实际列索引匹配
                tracking_ids.add(tracking_id)
    except Exception as e:
        print(f"Error reading CSV file: {e}")

    return list(tracking_ids)


def save_to_json(data, json_file_path):
    try:
        with open(json_file_path, 'w', encoding='utf-8') as jsonfile:
            json.dump(data, jsonfile, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error writing JSON file: {e}")


def insert_tids_to_entity(tid_list):
    db = startDb("identityalignment_db")
    try:
        with db.cursor() as cursor:
            for tid in tid_list:
                sql = "INSERT INTO Entity (TID) VALUES (%s)"
                cursor.execute(sql, (tid,))

        db.commit()
        print("TIDs have been successfully inserted into the Entity table.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()


# insertWebsiteUser(filepath='SinaAlignmentUser1.json',weblink='https://Weibo.com/u/',webid='1')
#
# postdatatouserlist("../dataTwitterPosts.csv","TwitterUsers.json")
# insertWebsiteUser(filepath='TwitterUsers.json',weblink='https://twitter.com/',webid='2')
#
# postdatatouserlist("../dataRedditPosts.csv","RedditUsers.json")
# insertWebsiteUser(filepath='RedditUsers.json',weblink='https://www.reddit.com/r/',webid='3')
# insertpostdata("../dataSinaPosts.csv",'1')
# insertpostdata("../dataTwitterPosts.csv",'2')
# insertpostdata("../dataRedditPosts.csv",'3')

# 提取唯一的Tracking ID
# unique_tracking_ids = extract_unique_tracking_ids('trackingData2.csv')
# print(unique_tracking_ids)
# insert_tids_to_entity(unique_tracking_ids)
# # 保存到JSON文件
# json_file_path = 'unique_tracking_ids.json'
# save_to_json(unique_tracking_ids, json_file_path)
#
# print(f"Unique tracking IDs have been saved to {json_file_path}")

csv_file_path = 'trackingData2.csv'
import_csv_to_trackingdata(csv_file_path)