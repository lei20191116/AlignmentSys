import itertools

import pymysql

import config


def startDb(database):
    db = pymysql.connect(host=config.mysql_ip, user=config.mysql_user, password=config.mysql_psw, database=database,
                         port=config.mysql_port)
    return db


class mysql_dealer():
    db = None
    cursor = None

    def __init__(self, database):
        try:
            self.db = pymysql.connect(host=config.mysql_ip, user=config.mysql_user, password=config.mysql_psw,
                                      database=database, port=config.mysql_port)
            self.cursor = self.db.cursor()
        except Exception as e:
            print("MySQL连接失败1" + str(e))

    def __del__(self):
        try:
            self.cursor.close()
            self.db.close()
        except:
            print("MySQL连接失败2")

    def get_cursor_exe_result(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()


def get_address_all():
    addresses = []
    fields = []
    db = startDb("identityalignment_db")
    cursor = db.cursor()
    cursor.execute("select * from suspiciousbitcoinaddress")
    results = cursor.fetchall()
    for id, field in enumerate(cursor.description):
        fields.append(field[0])
    for row in results:
        address = {}
        for id in range(len(fields)):

            if id == 0:
                address[fields[id]] = row[id]
            else:
                address[fields[id]] = row[id]
        addresses.append(address)
    print(addresses)
    return addresses


def users_return():
    db = startDb("identityalignment_db")
    cursor = db.cursor()
    users = []
    user = {}
    user["user"] = []
    sql1 = "select SourceUserID , TargetUserID from identityalignment"
    cursor.execute(sql1)
    webuser_ids = cursor.fetchall()
    flat_ids = [item for sublist in webuser_ids for item in sublist]  ## 使用列表推导将嵌套的元组拍扁
    unique_ids = list(set(flat_ids))
    for webuser_id in unique_ids:
        sql2 = "SELECT WebsiteUser.webuser_name, WebsiteUser.webuser_link, WebsiteUser.webid FROM WebsiteUser WHERE WebsiteUser.webuser_id = '{}';".format(
            webuser_id)
        cursor.execute(sql2)
        userinfos = cursor.fetchone()
        if userinfos:
            users.append(userinfos)
    print(users)
    return users


def get_website_num():
    db = startDb("identityalignment_db")
    cursor = db.cursor()
    sql = """
    SELECT COUNT(*) AS website_count FROM websiteinfo;
    """
    cursor.execute(sql)
    result = cursor.fetchone()[0]
    return result


# 这个方法需要重写，因为其中的owner要被弃用了
# 输入地址
# 输出用户名和网站
def get_address_user(address):
    addresses = []
    fields = []
    db = startDb("identityalignment_db")
    cursor = db.cursor()
    sql1 = "select OuserID from ownerrelation where Oaddr='{}'".format(address)
    cursor.execute(sql1)
    owneruserID = cursor.fetchall()
    flattened_data = list(itertools.chain(*owneruserID))
    print(flattened_data)
    user = {}
    user["user"] = []
    for webuser_id in flattened_data:
        sql2 = "SELECT WebsiteUser.webuser_name, WebsiteUser.webuser_link, WebsiteInfo.web_name FROM WebsiteUser INNER JOIN WebsiteInfo ON WebsiteUser.webid = WebsiteInfo.web_id WHERE WebsiteUser.webuser_id = '{}';".format(
            webuser_id)
        cursor.execute(sql2)
        userinfos = cursor.fetchall()
        for userinfo in userinfos:
            user["user"].append(userinfo)
    print(user)
    return user


def get_domainid(website):
    domain_id = []
    db = startDb("identityalignment_db")
    cursor = db.cursor()
    sql1 = "select web_id from websiteinfo where web_name='{}'".format(website)
    cursor.execute(sql1)
    result = cursor.fetchone()
    if result:
        domain_id = result[0]
    else:
        print("No such user found.")
        db.close()
        return []
    return domain_id


def get_type_address(type):
    addresses = []
    fields = []
    db = startDb("identityalignment_db")
    cursor = db.cursor()
    cursor.execute("select * from SuspiciousBitcoinAddress where criminal_type='{}'".format(type))
    results = cursor.fetchall()
    print(results)
    for id, field in enumerate(cursor.description):
        fields.append(field[0])
    for row in results:
        address = {}
        for id in range(len(fields)):
            if id == 0:
                address[fields[id]] = row[id]
            else:
                address[fields[id]] = row[id]
        addresses.append(address)
    return addresses


# 这个方法需要重写因为其中的owner要被弃用了
# 通过用户名查找其拥有的地址
def addr_return_user(username):
    db = startDb("identityalignment_db")
    cursor = db.cursor()
    cursor.execute("SELECT webuser_id FROM WebsiteUser WHERE webuser_name = '{}'".format(username))
    result = cursor.fetchone()
    if result:
        webuser_id = result[0]
    else:
        print("No such user found.")
        db.close()
        return []
    sql1 = """SELECT SourceUserID FROM IdentityAlignment WHERE TargetUserID = %s"""
    sql2 = """SELECT TargetUserID FROM IdentityAlignment WHERE SourceUserID = %s"""
    sql3 = """SELECT Oaddr FROM ownerrelation WHERE OuserID = %s"""
    # result1
    cursor.execute(sql1, webuser_id)
    result1 = cursor.fetchall()
    cursor.execute(sql2, webuser_id)
    result2 = cursor.fetchall()
    data = [result, result1, result2]
    flattened_data = [item for sublist in data for subsublist in (sublist if isinstance(sublist, tuple) else ()) for
                      item in (subsublist if isinstance(subsublist, tuple) else (subsublist,))]
    addresses = []
    addressdetails = []
    for userid in flattened_data:
        cursor.execute(sql3, userid)
        addresses.extend(cursor.fetchall())
    # 关闭数据库连接
    unique_addresses = list({item for sublist in addresses for item in sublist})
    for address in unique_addresses:
        cursor.execute(
            "SELECT addr, criminal_type , addr_type FROM suspiciousbitcoinaddress WHERE addr = '{}'".format(address))
        for addressdetail in cursor.fetchall():
            addressdetails.append(addressdetail)
    db.close()
    return addressdetails


# print(addr_return_user("Viola"))

def addr_user_return_all():
    db = startDb("identityalignment_db")
    cursor = db.cursor()
    # cursor.execute("SELECT webuser_id FROM WebsiteUser")
    # results = cursor.fetchall()
    # addresses = []
    # resultlst = []
    # for result in results:
    #     webuser_id = result[0]
    #     sql3 = """SELECT Oaddr FROM ownerrelation WHERE OuserID = %s"""
    #     cursor.execute(sql3,webuser_id)
    #     re = cursor.fetchall()
    #     if re:
    #         resultlst.append(re)
    # flattened_unique_data = list({item for sublist in resultlst for inner_sublist in sublist for item in inner_sublist})

    cursor.execute("SELECT addr, criminal_type , addr_type FROM suspiciousbitcoinaddress")
    addresses = cursor.fetchall()
    db.close()
    return addresses


def alignmentuser_return():
    db = startDb("identityalignment_db")
    cursor = db.cursor()
    cursor.execute("""
        SELECT ws1.web_name AS source_web_name, wu1.webuser_name AS source_username,
               ws2.web_name AS target_web_name, wu2.webuser_name AS target_username
        FROM IdentityAlignment ia
        JOIN WebsiteUser wu1 ON ia.SourceUserID = wu1.webuser_id
        JOIN WebsiteUser wu2 ON ia.TargetUserID = wu2.webuser_id
        JOIN WebsiteInfo ws1 ON wu1.webid = ws1.web_id
        JOIN WebsiteInfo ws2 ON wu2.webid = ws2.web_id
    """)
    alignment_info = cursor.fetchall()
    db.close()
    print(alignment_info)
    return alignment_info


def get_addr_detail(address):
    db = startDb("identityalignment_db")
    cursor = db.cursor()
    cursor.execute(
        "SELECT addr, criminal_type, tagsource, addr_type FROM suspiciousbitcoinaddress WHERE addr = '{}'".format(
            address))
    addr_info = cursor.fetchall()[0]
    print(addr_info)
    db.close()
    return addr_info


def get_website_name(username):
    connection = startDb("identityalignment_db")
    try:
        with connection.cursor() as cursor:
            # 尝试从数据库中查询用户名对应的网站名
            sql_select = """
                SELECT w.web_name
                FROM WebsiteUser u
                JOIN WebsiteInfo w ON u.webid = w.web_id
                WHERE u.webuser_name = %s
            """
            cursor.execute(sql_select, (username,))
            result = cursor.fetchone()
            if result:
                # 如果找到了用户名，直接返回对应的网站名
                return result[0]
            else:
                # 如果没有找到用户名，根据用户名是否为数字构建相应的websiteid
                if username.isdigit():
                    website_id = 1
                else:
                    website_id = 2
                # 插入用户名到数据库中
                sql_insert = """
                    INSERT INTO WebsiteUser (webuser_id, webuser_name, webid)
                    VALUES (%s,%s, %s)
                """
                cursor.execute(sql_insert, (username, username, website_id))
                connection.commit()
                # 返回网站名，这里可以根据情况自定义一个默认的网站名
                return "Default Website Name"
    except Exception as e:
        print("Error:", e)
        return None
    finally:
        connection.close()


def add_webuser(username, websiteid):
    connection = startDb("identityalignment_db")
    cursor = connection.cursor()
    new_id = username
    if websiteid == '1':
        website_id = 1
        weblink = "https://weibo.com/u/" + username
    elif websiteid == '2':
        website_id = 2
        weblink = "https://twitter.com/" + username
    else:
        website_id = 3
        weblink = "https://reddit.com/" + username
    sql_insert = """
                        INSERT INTO WebsiteUser (webuser_id,webuser_name,webuser_link, website_id)
                        VALUES (%s, %s, %s, %s)
                    """
    cursor.execute(sql_insert, (new_id, username, weblink, website_id))
    connection.commit()
    return "Default Website Name"


# 根据用户名找到用户ID
def get_usernameid(username):
    db = startDb("identityalignment_db")
    cursor = db.cursor()
    cursor.execute("SELECT webuser_id, webid FROM websiteuser WHERE webuser_name = '{}'".format(username))
    results = cursor.fetchall()
    if results:
        # 如果查询结果不为空，取第一条记录
        information = results[0]
        user_id = information[0]

    else:
        # 如果查询结果为空，进行相应处理，例如设置默认值或者返回空值
        information = None
        user_id = None
        # 或者显示错误信息给用户
        print("未找到相关信息，请重试或联系管理员")
    db.close()
    return user_id


# def add_user()
def add_alignemtn_record(sourceuserID, targetuserID):
    sql_dealer = mysql_dealer("identityalignment_db")
    insert_sql = """
            INSERT INTO identityalignment (SourceUserID, TargetUserID)
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE sourceUserID=sourceUserID;
            """
    sql_dealer.cursor.execute(insert_sql, (sourceuserID, targetuserID))
    sql_dealer.db.commit()


def alignment_record_return():
    records = []
    fields = []
    db = startDb("identityalignment_db")
    cursor = db.cursor()
    sqlsearch = "SELECT su1.webuser_name AS sourceusername, wi1.web_name AS sourcewebsite, su2.webuser_name AS targetusername, wi2.web_name AS targetwebsite FROM IdentityAlignment AS ia JOIN WebsiteUser AS su1 ON ia.SourceUserID = su1.webuser_id JOIN WebsiteUser AS su2 ON ia.TargetUserID = su2.webuser_id JOIN WebsiteInfo AS wi1 ON su1.webid = wi1.web_id JOIN WebsiteInfo AS wi2 ON su2.webid = wi2.web_id;"
    cursor.execute(sqlsearch)
    results = cursor.fetchall()
    for id, field in enumerate(cursor.description):
        fields.append(field[0])
    for row in results:
        record = {}
        for id in range(len(fields)):
            if id == 0:
                record[fields[id]] = row[id]
            else:
                record[fields[id]] = row[id]
        records.append(record)
    return records


def addr_type_return(addr_hash):
    db = startDb("identityalignment_db")
    cursor = db.cursor()
    cursor.execute("SELECT addr_type FROM suspiciousbitcoinaddress WHERE addr = '{}'".format(addr_hash))
    result = cursor.fetchone()
    if result:
        addr_type = result[0]
    else:
        print("No such user found.")
        db.close()
        return []
    return addr_type


def criminal_type_return(addr_hash):
    criminal_type = []
    db = startDb("identityalignment_db")
    cursor = db.cursor()
    cursor.execute("SELECT criminal_type FROM suspiciousbitcoinaddress WHERE addr = '{}'".format(addr_hash))
    result = cursor.fetchone()
    if result:
        criminal_type = result[0]
    else:
        print("No such user found.")
        db.close()
        return []
    return criminal_type


def tag_source_return(addr_hash):
    tag_source = []
    db = startDb("identityalignment_db")
    cursor = db.cursor()
    cursor.execute("SELECT tagsource FROM suspiciousbitcoinaddress WHERE addr = '{}'".format(addr_hash))
    result = cursor.fetchone()
    if result:
        tag_source = result[0]
    else:
        print("No such user found.")
        db.close()
        return []
    return tag_source


# 输入地址
# 输出其拥有着的用户名和网站
def owner_return(addr_hash):
    db = startDb("identityalignment_db")
    cursor = db.cursor()
    records = []
    fields = []
    cursor.execute(
        "SELECT wu.webuser_name AS owner_username,wi.web_name AS website_name FROM OwnerRelation AS ow JOIN WebsiteUser AS wu ON ow.OuserID = wu.webuser_id JOIN WebsiteInfo AS wi ON wu.webid = wi.web_id WHERE ow.Oaddr = '{}'".format(
            addr_hash))
    results = cursor.fetchall()
    print(results)
    if results:
        for id, field in enumerate(cursor.description):
            fields.append(field[0])
        for row in results:
            record = {}
            for id in range(len(fields)):
                if id == 0:
                    record[fields[id]] = row[id]
                else:
                    record[fields[id]] = row[id]
            records.append(record)
    return records


def identity_return(addr_hash):
    db = startDb("identityalignment_db")
    cursor = db.cursor()
    records = []
    fields = []
    sql = "SELECT  wu.webuser_name AS identity_username, wi.web_name AS website_name FROM ownerrelation AS ol JOIN identityalignment AS ia ON ol.OuserID = ia.SourceUserID JOIN websiteuser AS wu ON ia.TargetUserID = wu.webuser_id JOIN  websiteinfo AS wi ON wu.webid = wi.web_id WHERE ol.Oaddr = %s AND ia.TargetUserID NOT IN ( SELECT wu.webuser_name FROM ownerrelation AS ow JOIN websiteuser AS wu ON ow.OuserID = wu.webuser_id WHERE ow.Oaddr = %s);"
    cursor.execute(sql, (addr_hash, addr_hash))
    results = cursor.fetchall()
    print(results)
    if results:
        for id, field in enumerate(cursor.description):
            fields.append(field[0])
        for row in results:
            record = {}
            for id in range(len(fields)):
                if id == 0:
                    record[fields[id]] = row[id]
                else:
                    record[fields[id]] = row[id]
            records.append(record)
    return records


def userwebsiteportion_return():
    db = startDb("identityalignment_db")
    cursor = db.cursor()
    fields = []
    websites = []
    cursor.execute(
        "SELECT wi.web_name AS website_name, COUNT(wu.webuser_id) AS user_count,COUNT(wu.webuser_id) * 100.0 / (SELECT COUNT(*) FROM WebsiteUser) AS user_percentage FROM WebsiteUser AS wu JOIN WebsiteInfo AS wi ON wu.webid = wi.web_id GROUP BY wi.web_name; ")
    results = cursor.fetchall()
    print(results)
    for id, field in enumerate(cursor.description):
        fields.append(field[0])
    print(fields)
    for row in results:
        record = {}
        for id in range(len(fields)):
            if id == 0:
                record[fields[id]] = row[id]
            else:
                record[fields[id]] = row[id]
        websites.append(record)
    return websites


def websitereturn(username):
    db = startDb("identityalignment_db")
    cursor = db.cursor()
    fields = []
    websites = []
    sql = """
        SELECT w.web_name
        FROM WebsiteUser u
        JOIN WebsiteInfo w ON u.webid = w.web_id
        WHERE u.webuser_name = {}
    """.format(username)
    cursor.execute(sql)
    result = cursor.fetchone()
    if result:
        websites = result[0]
    else:
        print("No such user found.")
        db.close()
        return []
    return websites


# get_addr_detail("14KAHCHKLuSi5rzr4rAufFuBtUgjJDppiZ")
# get_trackermapping('002bwPUbBwdXiBrBkdEfUYYaP8Oej6B0dkvNkVJr5vfeFfC5J7rYtZUTY5FEDumT')
# get_webuser('1')
# get_type_address("drug")
# users_return()
# addr_return_user("Viola")

# alignmentuser_return()

# addr_user_return_all()
# get_address_all()

# print(owner_return( "1LZTzxUaJu9gDJokvcRYVz7n8adXY8LoJJ"))
# print(userwebsiteportion_return())

# print(users_return())

# print(get_domainid("Twitter"))
print(owner_return("1LZTzxUaJu9gDJokvcRYVz7n8adXY8LoJJ"))
