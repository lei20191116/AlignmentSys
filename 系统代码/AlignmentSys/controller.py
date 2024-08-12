import json
import pymysql
from datetime import datetime, timedelta
from collections import defaultdict
from mysql_dealer import startDb, get_domainid


def find_user_in_twitter(cursor, domainid,username, start_datetime, time_window_days):
    search_condition_times = []
    end_datetime = start_datetime + timedelta(days=time_window_days)
    print("end time:", str(end_datetime))
    query = """
        SELECT post_time
        FROM websitepostdata
        WHERE post_domain = %s AND user_id = %s AND post_time BETWEEN %s AND %s;
    """
    cursor.execute(query, (domainid,username, start_datetime, str(end_datetime)))
    results = cursor.fetchall()
    for row in results:
        post_time = row[0]
        post_time_dt = datetime.strptime(post_time, "%Y-%m-%d %H:%M:%S")  # 转换为 datetime 对象
        search_condition_times.append(post_time_dt)
    return search_condition_times

def find_uid_in_tracking(cursor,domainid, search_condition_times, time_period_seconds, threshold):
    twitter_data = defaultdict(list)
    query = """
        SELECT actiontime, trackingid
        FROM trackingdata
        WHERE domainid = %s;
    """
    cursor.execute(query,(domainid,))
    results = cursor.fetchall()
    for row in results:
        record_time = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")  # 转换为 datetime 对象
        tracking_id = row[1]
        twitter_data[record_time].append(tracking_id)
    id_counts = defaultdict(int)
    for time in search_condition_times:
        before_target_time = time - timedelta(seconds=time_period_seconds)
        after_target_time = time + timedelta(seconds=time_period_seconds)
        for record_time, tracking_ids in twitter_data.items():
            if before_target_time <= record_time <= after_target_time:
                for tracking_id in tracking_ids:
                    id_counts[tracking_id] += 1
    unique_ids = [uid for uid, count in id_counts.items() if count >= threshold - 1]
    return unique_ids

def get_sina_tracking_times(domainid,unique_ids):
    sina_times = []
    connection = startDb("identityalignment_db")
    try:
        with connection.cursor() as cursor:
            for unique_id in unique_ids:
                query = """
                    SELECT actiontime FROM trackingdata
                    WHERE trackingid = %s AND domainid = %s
                """
                cursor.execute(query, (unique_id,domainid))
                results = cursor.fetchall()
                sina_times.append([datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S") for row in results])  # 转换为 datetime 对象
    finally:
        connection.close()
    return sina_times

def get_sina_user_dict_from_db(domainid):
    sina_user_dict = defaultdict(list)
    connection = startDb("identityalignment_db")
    try:
        with connection.cursor() as cursor:
            query = """
                SELECT user_id, post_time FROM websitepostdata
                WHERE post_domain = %s
            """
            cursor.execute(query,(domainid,))
            results = cursor.fetchall()
            for row in results:
                user_id = row[0]
                post_time = datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S")  # 转换为 datetime 对象
                sina_user_dict[user_id].append(post_time)
    finally:
        connection.close()
    return sina_user_dict

def find_user_info_by_uid(domainid, unique_ids, time_period):
    sina_times = get_sina_tracking_times(domainid,unique_ids)
    sina_user_dict = get_sina_user_dict_from_db(domainid)
    usernames_list_uni = []
    for sina_time in sina_times:
        for user, times in sina_user_dict.items():
            user_valid = True
            for time in times:
                time_valid = False
                for sina_time_item in sina_time:
                    time_diff = abs(time - sina_time_item)
                    if time_diff.total_seconds() <= time_period:
                        time_valid = True
                        break
                if not time_valid:
                    user_valid = False
                    break
            if user_valid:
                usernames_list_uni.append(user)
    return usernames_list_uni

def alignment(domainidtarget,domainidsource, username, start_datetime):
    db = startDb("identityalignment_db")
    try:
        with db.cursor() as cursor:
            time_window_days = 1
            time_period_seconds = 60
            search_condition_times = find_user_in_twitter(cursor,domainidsource, username, start_datetime, time_window_days)
            unique_ids = find_uid_in_tracking(cursor, domainidsource,search_condition_times, time_period_seconds,
                                              len(search_condition_times))
            usernameslistUni = find_user_info_by_uid(domainidtarget,unique_ids, time_period_seconds)
            return usernameslistUni
    finally:
        db.close()

def multiplealignment(account1website, account1starttime, account1username, account2website, account2starttime,account2username,targetwebsite):
    db = startDb("identityalignment_db")
    account1starttime = datetime.strptime(account1starttime, "%Y-%m-%d %H:%M:%S")
    account2starttime = datetime.strptime(account2starttime, "%Y-%m-%d %H:%M:%S")
    sourcedomainid1 = get_domainid(account1website)
    sourcedomainid2 = get_domainid(account2website)

    try:
        with db.cursor() as cursor:
            time_window_days = 1
            time_period_seconds = 60
            search_condition_times1 = find_user_in_twitter(cursor,sourcedomainid1, account1username, account1starttime, time_window_days)
            search_condition_times2 = find_user_in_twitter(cursor,sourcedomainid2, account2username, account2starttime, time_window_days)

            unique_ids1 = find_uid_in_tracking(cursor, sourcedomainid1,search_condition_times1, time_period_seconds,
                                              len(search_condition_times1))
            unique_ids2 = find_uid_in_tracking(cursor, sourcedomainid2,search_condition_times2, time_period_seconds,
                                              len(search_condition_times2))
            unique_ids = inetrsection(unique_ids1,unique_ids2)
            usernameslistUni = find_user_info_by_uid(targetwebsite,unique_ids, time_period_seconds)
            return usernameslistUni
    finally:
        db.close()
def inetrsection(id_list1, id_list2):
    intersectlist = []
    for id in id_list1:
        if id in id_list2:
            intersectlist.append(id)
    return intersectlist

def alignment2(account1website, account1starttime, account1username, account2website, account2starttime,account2username,targetwebsite):
    usernameResultList = multiplealignment(account1website, account1starttime, account1username, account2website, account2starttime,account2username,targetwebsite)
    usercontext = []
    for user in usernameResultList:
        website = "Sina"
        weblink = "https://weibo.com/u/{}".format(user)
        usercontext.append([website,user,weblink])
    return usercontext
def alignment1(username1, starttime1, website1,targetwebsite):
    starttime1 = datetime.strptime(starttime1, "%Y-%m-%d %H:%M:%S")
    sourcedomainid = get_domainid(website1)
    usernameResultList = alignment(targetwebsite,sourcedomainid,username1,starttime1)
    usercontext = []
    for user in usernameResultList:
        website = "Sina"
        weblink = "https://weibo.com/u/{}".format(user)
        usercontext.append([website,user,weblink])
    return usercontext

# print(alignment1("@DLCeMoney","2023-03-28 15:03:17","Twitter",'1'))
#@vivisko_2
# print(multiplealignment("Twitter","2023-03-28 15:03:17","@DLCeMoney","Reddit","2023-04-10 13:16:15","@vivisko_2","1"))