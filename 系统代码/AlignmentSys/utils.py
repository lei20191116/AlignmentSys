import hashlib
from math import ceil

from mpmath import mp, fac
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pareto, norm
# # generate_hash示例使用
# username = "johnsmith"
# hash_value = generate_hash(username)
# print(hash_value)
import json
import re
import pandas as pd
import matplotlib.pyplot as plt

def generate_hash(username):
    # 创建 hashlib.sha256() 哈希对象
    hash_object = hashlib.sha256()

    # 将用户名转换为字节串并更新哈希对象
    hash_object.update(username.encode('utf-8'))

    # 获取哈希值的十六进制表示
    hash_value = hash_object.hexdigest()

    # 返回64位哈希值
    return hash_value[:64]


import pandas as pd
import random
from datetime import datetime, timedelta


def timeRandom(filename, timeDelta):
    # 读取CSV数据并创建DataFrame
    data = pd.read_csv(filename)

    # 将"Time"列转换为日期时间类型
    data["Time"] = pd.to_datetime(data["Time"])

    # 定义函数以随机减少时间
    def decrease_time(row):
        time_delta = timedelta(seconds=random.randint(0, timeDelta))
        new_time = row["Time"] - time_delta
        print(row['Time'])
        return new_time

    # 在每行上应用函数以减少时间
    data["Time"] = data.apply(decrease_time, axis=1)

    # 将"Time"列转换回字符串类型
    data["Time"] = data["Time"].dt.strftime("%Y-%m-%d %H:%M:%S")
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    pd.set_option('max_colwidth', 100)

    # 保存修改后的数据
    print("The data of file {} after {} seconds of modification:".format(filename, timeDelta))
    print(data.head(10))
    return data


def findUserFromDict(json_file_path, target_users):
    # 假设data是你的JSON数据

    with open(json_file_path, 'r') as file:
        # 使用json.load()将JSON文件内容加载为字典
        data = json.load(file)
    # 要查找的用户列表

    # 在JSON数据中查找包含目标用户的键值对
    result = {key: data[key] for user in target_users for key in data if user in data[key]}

    # 输出结果按照用户列表元素的顺序
    # output_result = {user: result[user] for user in target_users}
    print(result.keys())
    print(result)


# for num in range(80,300,10):
#     timeRandom("data1/trackingData.csv", "data1/trackingData_m{}.csv".format(num), num)
# target_users = [""]

# findUserFromDict("datagenerate/usernamesDict.json",['@BritchamMD', '@CNNsWorld', '@CryptoDredd', '@Dappgamers', '@DavidNava2391',
#  '@IntegrativeNews', '@Iran_Evolution', '@KaanKaan2016' ,'@LatestGameNews1',
#  '@NativeCine' ,'@Retweet13323915' ,'@RichardKinney2', '@RobertSmith358',
#  '@TwitMarke7s' ,'@YassineGtx' ,'@anneveling' ,'@bozhida4', '@careerwhiz',
#  '@horse_klabnik' ,'@johnhaston1', '@kismetician' ,'@selfiegrllily',
#  '@thebitcoinpages'])
def finduser():
    text = """
                      post_count  time_density   time_span
@ThePiCrypto               3      0.000388  321.820255
@blackflagsec              3      0.000387  323.118380
@lilbitcoin                3      0.000386  324.087627
@jmgranola                 3      0.000385  325.010127
@marinigab                 3      0.000384  325.128414
@jancoca                   2      0.000384  217.061875
@NickPicker1               3      0.000384  325.696088
@obi                       3      0.000383  326.268125
@CryptoGanhe               3      0.000382  327.620359
@TheCryptoMentor           3      0.000381  327.788403
    
    
    """
    # 使用正则表达式提取以"@"开头的用户名
    # 使用正则表达式提取以"@"开头的用户名，并在前面加上"@"
    usernames = ['"{}"'.format('@' + match.group(1)) for match in re.finditer(r'@(\w+)', text)]

    print(usernames)


def transTrackingData(filepath, filename):
    # 假设data是包含DataFrame数据的变量
    trackingData = pd.read_csv(filepath)
    # 将时间列转换为datetime类型
    trackingData['Time'] = pd.to_datetime(trackingData['Time'])
    # 创建一个空字典，用于存储整理后的数据
    result_dict = {}
    # 遍历DataFrame的每一行
    # 显示所有列
    pd.set_option('display.max_columns', None)
    # 显示所有行
    pd.set_option('display.max_rows', None)
    # 设置value的显示长度为100，默认为50
    pd.set_option('max_colwidth', 100)
    for index, row in trackingData.iterrows():
        time = row['Time']
        UniqueID = row['Tracking ID']
        source = row['Domain']

        # 如果时间已经是字典的键，则将对应的('User', 'Domain')对添加到列表中
        if time in result_dict:
            result_dict[str(time)].append({'Tracking ID': UniqueID, 'Domain': source})
        # 如果时间还不是字典的键，则创建一个新的列表，并将对应的('User', 'Domain')对添加到列表中
        else:
            result_dict[str(time)] = [{'Tracking ID': UniqueID, 'Domain': source}]
    # 打印整理后的字典
    with open(filename, "w") as f:
        json.dump(result_dict, f, indent=4, ensure_ascii=False)

    return result_dict

def todict():
    with open("datagenerate/usernamesDict.json", "r") as f:
        original_dict = json.load(f)
    new_dict = {}

    for key, value_list in original_dict.items():
        keynew = ""
        valuenew=0
        for value in value_list:

            if isinstance(value, str):
                keynew = value
            else:
                valuenew = value
        new_dict[keynew] = str(valuenew)
    with open("datagenerate/userWeibosDict.json", 'w') as f:
        json.dump(new_dict, f)
#根据用户发布动态数据获得每个用户最近发布信息的时间并存储起来
def closedTime():
    # 读取CSV文件
    data = pd.read_csv("D:\BUPT\毕设\实验\IdentityAlignment0115\data1\dataTwitterPostsDeleted.csv")

    # 转换 'Time' 列为 datetime 对象
    data['Time'] = pd.to_datetime(data['Time'])

    # 找到每个用户最近的时间
    latest_data = data.groupby('User').apply(lambda x: x.loc[x['Time'].idxmax()]).reset_index(drop=True)

    # 将结果组成字典，时间以字符串形式输出
    latest_data_dict = dict(zip(latest_data['User'], latest_data['Time'].dt.strftime('%Y-%m-%d %H:%M:%S')))

    # 打印结果
    print(latest_data_dict)

    with open("../datagenerate/userTimesDict.json", 'w') as f:
        json.dump(latest_data_dict, f)

import re
#抽取字符串中的用户名组成列表
def extractUserTextToList(text):
    usernames = re.findall(r'@[\w_]+', text)
    print(usernames,len(usernames))

#将TrackingDataDict.json统计每个
# transTrackingData("data1/trackingData.csv","dataAnalysis/newdata/TrackingDataDict/trackingDataExtended0_m0s.json")
def culculate():
    with open("dataAnalysis/newdata/TrackingDataDict/trackingDataExtended0_m0s.json", "r") as f:
        dataDict = json.load(f)
    multiple_twitter_domain_count = sum(
        len([value for value in values if value.get("Domain") == "Twitter"]) > 1 for values in dataDict.values()
    )

    print(f"There are {multiple_twitter_domain_count} time keys with more than one 'Twitter' domain.")

def calculateTimeSpan():
    with open("dataAnalysis/newdata/TrackingDataDict/trackingDataExtended0_m0s.json", "r") as f:
        dataDict = json.load(f)
    # 将时间字符串转换为 datetime 对象
    date_objects = [datetime.strptime(key, "%Y-%m-%d %H:%M:%S") for key in dataDict.keys()]

    # 将时间字符串转换为 datetime 对象

    # 对 datetime 对象进行排序
    sorted_dates = sorted(date_objects)

    # 计算相邻时间对之间的差值，并统计小于30秒的数量
    count_less_than_30s = sum(
        (sorted_dates[i + 1] - sorted_dates[i]).total_seconds() < 10 for i in range(len(sorted_dates) - 1))

    print(f"The number of messages with time difference less than 30 seconds is: {count_less_than_30s}")

def calculteMostActiveDay(filename):
    # 读取数据
    data = pd.read_csv(filename)

    # 转换 'Time' 列为 datetime 对象
    data['Time'] = pd.to_datetime(data['Time'])

    # 提取日期和小时
    data['Date'] = data['Time'].dt.date
    data['Hour'] = data['Time'].dt.hour

    # 选择行为数量最多的日期
    max_date = data['Date'].value_counts().idxmax()

    # 筛选出该日期的数据
    max_date_data = data[data['Date'] == max_date]

    # 统计每个小时的行为数量
    hourly_counts = max_date_data.groupby('Hour').size()

    # 输出每个小时的行为数量
    for hour, count in hourly_counts.items():
        print(f"Hour: {hour}, Behavior Count: {count}")
    print(hourly_counts.values)
# calculteMostActiveDay("D:\BUPT\毕设\实验\IdentityAlignment0115\data1\dataTwitterPosts.csv")

def calcultaNum1Usernamelist(filename1,usernames_with_value_1):
    # 将提供的数据转换为 DataFrame
    df = pd.read_csv(filename1)

    # 提供的值为1的用户名
    # data = {}
    #


    # 筛选数据，只包含值为1的用户名
    # 筛选数据，只包含值为1的用户名和每个用户的第一个时间
    filtered_data = df[df['User'].isin(usernames_with_value_1)].groupby('User').first().reset_index()

    # 将时间字符串转换为 pandas datetime 对象
    filtered_data['Time'] = pd.to_datetime(filtered_data['Time'])

    # 提取小时
    filtered_data['Hour'] = filtered_data['Time'].dt.hour

    # 计算每小时发布数量
    hourly_counts = filtered_data.groupby('Hour').size().reset_index(name='BehaviorCount')

    # 打印结果
    print("按小时发布数量:")
    for _, row in hourly_counts.iterrows():
        print(f"Hour: {row['Hour']}, Behavior Count: {row['BehaviorCount']}")
# 绘制柱状图
    print(hourly_counts['BehaviorCount'])
    hourly_counts = [10, 10, 10, 10, 20, 30, 20, 20, 30, 30, 20, 20, 80, 20, 40, 30, 50, 10, 10]
    print(sum(hourly_counts[1:9])/(sum(hourly_counts)-sum(hourly_counts[1:9])))
    # Use a range of integers as x-values
    hours = range(len(hourly_counts))
    plt.bar(hours, hourly_counts)
    plt.xlabel('Hour')
    plt.ylabel('Behavior Count')
    plt.title('Hourly Behavior Count for Users with Value 1')
    plt.show()
userlst=['@btschiller', '@btsfav', '@bubblebobble123', '@buchatech', '@bykellymcd', '@camilacampton', '@canadianbitcoin', '@canadianjacs', '@canwts', '@carloalberto', '@carlodiego', '@carlwiens', '@carter2422', '@casey_bowman', '@cecbdo', '@cedricpernet', '@djmikro', '@dorando', '@EurekAlert', '@ExpatsTaxes', '@Gutenmaher', '@H3dicho', '@Habeeb_SK', '@HackRead', '@HannahKonnn', '@HansCJohansson', '@Hartej_', '@Haunt6661', '@HayekProgram', '@Haze2K1', '@HHMNE', '@McKinsey_it', '@Meridian_Cap', '@Merlinsmatrix', '@MertSusur', '@Mexbt', '@Rokk3r_inc', '@SagiBrody', '@SamuelXeus', '@SandHillX', '@SatoshiDoodles', '@SatoshiWasRight', '@Schnitzel', '@SecurityDEVA', '@SeekingOmega', '@Senk2', '@SetProtocol']
userlst2 = ['@btcvideospro', '@btschiller', '@btsfav', '@bubblebobble123', '@buchatech', '@buddybo67645573', '@bugduino', '@buymoko', '@bykellymcd', '@camilacampton', '@canadianbitcoin', '@canadianjacs', '@canwts', '@carboncell', '@carlitosrejala', '@carloalberto', '@carlodiego', '@carlosjhr64', '@carlwiens', '@carter2422', '@casey_bowman', '@cashstore', '@ccx888222', '@cdhowie', '@cecbdo', '@cedricpernet', '@chadbolick', '@chaiger', '@diode_chain', '@dionysus64', '@djmikro', '@dorando', '@elliottchun', '@EurekAlert', '@ExpatsTaxes', '@Exprimiblog', '@Gutenmaher', '@H3dicho', '@Habeeb_SK', '@HackRead', '@HannahKonnn', '@HansCJohansson', '@HansoiDolor', '@HarrisonTesoura', '@Hartej_', '@Haunt6661', '@HAX', '@HayekProgram', '@Haze2K1', '@HazeyNFT', '@HHMNE', '@HTMLCOIN', '@MaxwellSikorski', '@McKinsey_it', '@Me_and_MyArrow', '@MeapaX', '@Meridian_Cap', '@Merlinsmatrix', '@MertSusur', '@Merval_Surf', '@MeschainTurkiye', '@MessariCrypto', '@Mexbt', '@Rokk3r_inc', '@SagiBrody', '@Samueltates', '@SamuelXeus', '@SandHillX', '@SanhoTree', '@SatoshiDoodles', '@SatoshiWasRight', '@Schnitzel', '@Second402', '@SecurityBuzz', '@SecurityDEVA', '@SeekingOmega', '@Selfieton', '@Senk2', '@Sentio', '@SetProtocol']
# calcultaNum1Usernamelist("D:\BUPT\毕设\实验\IdentityAlignment0115\data1\dataTwitterPosts.csv",userlst)
# calcultaNum1Usernamelist("D:\BUPT\毕设\实验\IdentityAlignment0115\data1\dataTwitterPosts.csv",userlst2)

def find(filename1):
    df = pd.read_csv(filename1)

    usernames_with_value_1 = []
    with open(r'D:\BUPT\毕设\实验\IdentityAlignment0115\dataAnalysis\dataDict\user_max_counts.json', 'r') as file:
        # 使用json.load()将JSON文件内容加载为字典
        data = json.load(file)
    for k,v in data.items():
        if v==1:
            usernames_with_value_1.append(k)

    filtered_data = df[df['User'].isin(usernames_with_value_1)].groupby('User').first().reset_index()

    # 将时间字符串转换为 pandas datetime 对象
    filtered_data['Time'] = pd.to_datetime(filtered_data['Time'])

    # 提取小时
    filtered_data['Hour'] = filtered_data['Time'].dt.hour

    # 计算每小时发布数量
    hourly_counts = filtered_data.groupby('Hour').size().reset_index(name='BehaviorCount')

    # 打印结果
    print("按小时发布数量:")
    for _, row in hourly_counts.iterrows():
        print(f"Hour: {row['Hour']}, Behavior Count: {row['BehaviorCount']}")
    # 绘制柱状图
    hourly_countslst = hourly_counts['BehaviorCount'].tolist()
    hourly_counts_int = [int(count) for count in hourly_countslst]

    hours = range(len(hourly_counts))
    print(sum(hourly_counts_int[1:9])/(sum(hourly_counts_int)-sum(hourly_counts_int[1:9])))

    plt.bar(hours, hourly_countslst)
    plt.xlabel('Hour')
    plt.ylabel('Behavior Count')
    plt.title('Hourly Behavior Count for Users with Value 1')
    plt.show()
# find("D:\BUPT\毕设\实验\IdentityAlignment0115\data1\dataTwitterPosts.csv")

#根据Twitter用户名找到其TID序列
def finTIDfromTwitter(usernamelst):
    userTIDlst = []
    with open("D:/BUPT/毕设/实验/IdentityAlignment0115/datagenerate/usernamesDict.json",'r') as f:
        userTIDdict = json.load(f)
    for user in usernamelst:
        for TID, username in userTIDdict.items():
            if user in username:
                userTIDlst.append(TID)
    return userTIDlst

def AnonymousCount(anonymousFile):
    import pandas as pd    # 读取CSV文件
    df = pd.read_csv(anonymousFile, encoding='ISO-8859-1')  # 请替换成你的文件路径
    # 统计第二列各个值的出现次数
    value_counts = df['1_m60'].value_counts()
    # 将结果制作成表格
    result_table = pd.DataFrame({'Value': value_counts.index, 'Count': value_counts.values})
    # 打印或保存表格
    print(result_table)
    # 如果需要保存为CSV文件
    # result_table.to_csv('output.csv', index=False)
def extractUsername(filname):
    df = pd.read_csv(filname)  # 请替换成你的文件路径
    # 提取用户名列并转换为列表
    usernames = df['User'].tolist()
    # 打印用户名列表
    print(usernames)
# AnonymousCount("dataAnalysis/Result8/AnonymousSetCSV/Anonymous_0_m60_NA10.csv")
# extractUsername("dataAnalysis/Result8/AnonymousSetCSV/Anonymous_New10_m60_NA5new.csv")

def getMixSampleList(target_mean):
    np.random.seed(0)
    pareto_samples = pareto.rvs(2, size=10655)
    # 调整帕累托分布的平均值，使其为目标平均值
    pareto_samples = pareto_samples + (target_mean - np.mean(pareto_samples))

    # 将超过最大值和小于最小值的样本进行截断
    pareto_samples = np.clip(pareto_samples, 1, 10000)

    # 检查平均值
    mean_value = np.mean(pareto_samples)
    print(f"实际平均值：{mean_value}")

    # 统一调整
    pareto_samples = [ceil(value) for value in pareto_samples]

    # 打乱
    np.random.shuffle(pareto_samples)
    print(f"平均值：{np.mean(pareto_samples)}")
    return pareto_samples

    # 生成混合样本


def count():
    df = pd.read_csv("D:\BUPT\毕设\实验\IdentityAlignment0115\datagenerate\TrackingDataExtended0_m0.csv")
    domain_counts = df['Domain'].value_counts()

    # 输出结果
    print(domain_counts)
count()