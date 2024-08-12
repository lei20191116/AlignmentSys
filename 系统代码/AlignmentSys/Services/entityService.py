import config
from mysql_dealer import *


# log = log.init_logger(config.log_filepath)



def getaddsusers(address):
    usersdetail = get_address_user(address)
    return usersdetail


def get_verify_detail(address):
    addrdict = get_addr_detail(address)
    addrcontext = {}
    addrcontext["addr"] = addrdict[0]
    addrcontext["criminal_type"] = addrdict[1]
    addrcontext["tagsource"] = addrdict[2]
    addrcontext["addr_type"] = addrdict[3]
    addrcontexts = [addrcontext]
    return addrcontexts


def get_verify_detail(addresses):
    addrdict = get_addr_detail(addresses)
    addrcontext = {}
    addrcontext["addr"] = addrdict[0]
    addrcontext["criminal_type"] = addrdict[1]
    addrcontext["tagsource"] = addrdict[2]
    addrcontext["addr_type"] = addrdict[3]
    addrcontexts = [addrcontext]
    return addrcontexts


# get_userdetail("002bwPUbBwdXiBrBkdEfUYYaP8Oej6B0dkvNkVJr5vfeFfC5J7rYtZUTY5FEDumT")

def get_verify_detail(addresses):
    addrdict = get_addr_detail(addresses)
    addrcontext = {}
    addrcontext["addr"] = addrdict[0]
    addrcontext["criminal_type"] = addrdict[1]
    addrcontext["tagsource"] = addrdict[2]
    addrcontext["addr_type"] = addrdict[3]
    addrcontexts = [addrcontext]
    return addrcontexts


def record_alignment(sourceusername, targetusername,sourcewebsite,targetwebsite):
    sourceuserid, sourcewensite = record_alignment_check_user(sourceusername,sourcewebsite)
    targetuserid, targetwebsite = record_alignment_check_user(targetusername,targetwebsite)
    print(sourceuserid, targetuserid)
    add_alignemtn_record(sourceuserid, targetuserid)


def record_alignment2(targetusername, targetwebsite, sourceusername1, sourcewebsite1, sourceusername2, sourcewebsite2):
    userid1, websiteid1 = record_alignment_check_user(sourceusername1, sourcewebsite1)
    userid2, websiteid2 = record_alignment_check_user(sourceusername2, sourcewebsite2)
    userid0, websiteid0 = record_alignment_check_user(targetusername, targetwebsite)
    add_alignemtn_record(userid1, userid0)
    add_alignemtn_record(userid2, userid0)


def record_alignment_check_user(username, website):
    websiteid = get_domainid(website)
    if get_usernameid(username):
        userid = get_usernameid(username)
    else:
        add_webuser(username, websiteid)
        userid = get_usernameid(username)
    return userid, websiteid


def get_history():
    print(alignment_record_return()[0])
    return alignment_record_return()[0]


# 输入地址哈希，输出地址对应的账户用户名和网站以及地址的犯罪类型和加密数字货币类型
# addr_hash
# owner:[[website,username]]
# type criminalType
def get_address_detail(addr_hash):
    address_context = {}
    address_context["hash"] = addr_hash
    addr_type = addr_type_return(addr_hash)
    criminal_type = criminal_type_return(addr_hash)
    tag_source = tag_source_return(addr_hash)
    address_context["tag_source"] = tag_source
    address_context["addr_type"] = addr_type
    address_context["criminal_type"] = criminal_type
    address_context["owner"] = owner_return(addr_hash)
    address_context["identity"] = identity_return(addr_hash)

    print(address_context)
    return address_context


# get_address_detail("1LZTzxUaJu9gDJokvcRYVz7n8adXY8LoJJ")


def get_userportion_all():
    websiteportions = userwebsiteportion_return()
    return websiteportions
