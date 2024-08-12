from flask import Flask, render_template, request, jsonify, session
from Services.entityService import *
from controller import alignment1, alignment2
from mysql_dealer import *
from forms import AddressForm
from flask_wtf.csrf import CSRFProtect
import requests

app = Flask(__name__)
csrf = CSRFProtect(app)
app.config['SECRET_KEY'] = 'your_secret_key_here'


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


# 路由定义
@app.route('/')
def index():
    websitecontext = get_userportion_all()
    # 定义英文网站名到中文网站名的映射字典
    english_to_chinese = {
        'Twitter': '推特',
        'Reddit': 'Reddit',
        'Sina': '微博',
        # 添加其他网站的映射
    }
    webnum = get_website_num()
    return render_template('index.html', websitecontext=websitecontext, english_to_chinese=english_to_chinese,
                           webnum=webnum)


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/usersearch', methods=['GET', 'POST'])
def usersearch():
    return render_template('usersearch.html')


@app.route('/alignmentdetail', methods=['GET', 'POST'])
def alignmentdetail():
    username = request.values["username"]
    starttime = request.values["starttime"]
    website = request.values["website"]
    weblink = "https://weibo.com/u/{}".format(username)
    print(username, starttime, website)
    users = alignment1(username, starttime, website, "1")
    context = {
        "starttime": starttime,
        "sourceusername": username,
        "sourcewebsite": website
    }
    return render_template('alignmentdetail.html', context=context, users=users)


@app.route('/record_user', methods=['GET', 'POST'])
def record_user():
    sourceusername = request.values['sourceusername']
    targetusername = request.values['targetusername']
    sourcewebsite = request.values['sourcewebsite']
    targetwebsite = request.values['targetwebsite']
    record_alignment(sourceusername, targetusername, sourcewebsite, targetwebsite)
    alignment_infos = alignmentuser_return()
    return render_template('identityAlignment.html', alignment_infos=alignment_infos)


@app.route('/record_user2', methods=['GET', 'POST'])
def record_user2():
    sourceusername1 = request.values['sourceusername1']
    sourceusername2 = request.values['sourceusername2']
    sourcewebsite1 = request.values['sourcewebsite1']
    sourcewebsite2 = request.values['sourcewebsite2']
    targetusername = request.values['targetusername']
    record_alignment2(targetusername, '1', sourceusername1, sourcewebsite1, sourceusername2, sourcewebsite2)
    alignment_infos = alignmentuser_return()
    return render_template('identityAlignment.html', alignment_infos=alignment_infos)


@app.route('/historyrecord')
def historyrecord():
    alignment_infos = alignmentuser_return()
    return render_template('identityAlignment.html', alignment_infos=alignment_infos)


@app.route('/identity_address')
def identity_address():
    users = users_return()
    return render_template('adduser.html', users=users)


# 用户所有的地址
@app.route('/adduser', methods=['GET', 'POST'])
def adduser():
    users = users_return()
    addr = ""
    return render_template('adduser1.html', addr=addr, users=users)


# 1LZTzxUaJu9gDJokvcRYVz7n8adXY8LoJJ
# 根据搜索地址得到的结果
# 根据加密数字货币地址搜索得到其拥有着详细信息
@app.route('/adduserdetail', methods=['GET', 'POST'])
def adduserdetail():
    address = request.values["address"]
    users = [getaddsusers(address)]
    return render_template('adduser2.html', addr=address, users=users)


@app.route('/useradd', methods=['GET', 'POST'])
def useradd():
    username = ""
    addresses = addr_user_return_all()
    return render_template('useradd.html', username=username, addresses=addresses)


@app.route('/useradddetail', methods=['GET', 'POST'])
def useradddetail():
    username = request.values["username"]
    addresses = addr_return_user(username)
    return render_template('useradd.html', username=username, addresses=addresses)


@app.route('/addrOverview')
def addrOverview():
    addresses = get_address_all()
    return render_template('addrOverview.html', addresses=addresses)


@app.route('/addrVerify')
def addrVerify():
    addresses = get_address_all()
    return render_template('addrVerify.html', addresses=addresses)


@app.route('/verifyDetail')
def verifyDetail():
    address = request.values["address"]
    addresses = get_verify_detail(address)
    print(addresses)
    return render_template('addrVerify.html', addresses=addresses)


@app.route('/addrValidation', methods=['GET', 'POST'])
def addrValidation():
    form = AddressForm()
    if form.validate_on_submit():
        # 在这里处理表单提交逻辑
        address = form.address.data
        # 进行其他处理...
    return render_template('addrValidation.html', form=form)


@app.route('/address_details/<addr_hash>')
def address_details(addr_hash):
    # 根据地址哈希值获取地址详情
    # ...
    # 渲染地址详情页面模板
    addr_detail = get_address_detail(addr_hash)
    if not addr_detail:
        return render_template('404.html'), 404
    return render_template('addressDetail.html', addr_detail=addr_detail)


@app.route('/addrTypeSearch', methods=['GET', 'POST'])
def addrTypeSearch():
    criminal_type = request.values['criminal_type']
    addresses = get_type_address(criminal_type)
    return render_template('addrOverview.html', addresses=addresses)


@app.route('/multipleAccount')
def multipleAccount():
    return render_template('multipleAccount.html')


@app.route('/multipleAccountAlignment')
def multipleAccountAlignment():
    account1website = request.values['account1website']
    account2website = request.values['account2website']
    account1starttime = request.values['account1starttime']
    account2starttime = request.values['account2starttime']
    account1username = request.values['account1username']
    account2username = request.values['account2username']
    context1 = {
        "starttime": account1starttime,
        "sourceusername": account1username,
        "sourcewebsite": account1website
    }
    context2 = {
        "starttime": account2starttime,
        "sourceusername": account2username,
        "sourcewebsite": account2website
    }
    usercontext = alignment2(account1website, account1starttime, account1username, account2website, account2starttime,
                             account2username, "1")

    return render_template('alignmentdetail2.html', context1=context1, context2=context2, users=usercontext)


@app.route('/identityAlignment')
def identityAlignment():
    alignment_infos = alignmentuser_return()
    return render_template('identityAlignment.html', alignment_infos=alignment_infos)


@app.route('/color')
def color():
    return render_template('utilities-color.html')


@app.route('/other')
def other():
    return render_template('utilities-other.html')


@app.route('/charts')
def charts():
    return render_template('charts.html')


@app.route('/forgot_password')
def forgot_password():
    return render_template('forgot-password.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/buttons')
def buttons():
    return render_template('buttons.html')


@app.route('/cards')
def cards():
    return render_template('cards.html')


@app.route('/animation')
def animation():
    return render_template('utilities-animation.html')


# @app.route('/eventuser')
# def eventuser():
#     user1 = {"trackerID": "6jYWJjqukkuR8RZG4IXaXjBib0803Mruj7WN9mLIO6MgphTz2v2O7uwVtxJLVnJ4", "domain": "Sina",
#              "username": "123"}
#     user2 = {"trackerID": "6jYWJjqukkuR8RZG4IXaXjBib0803Mruj7WN9mLIO6MgphTz2v2O7uwVtxJLVnJ4", "domain": "Sina",
#              "username": "456"}
#     users = [user1, user2]
#     return render_template('eventuser.html', users=users)

if __name__ == '__main__':
    app.run()
