from hashlib import md5
import os
from requests import post, get
from json import loads
from datetime import datetime
import binascii
import string
import random

ENDPOINT = 'https://api.mhpkms.mhpteam.dev/'
REGISTER = "/api/v1/app/auth/register"
GENERATE = '/api/v1/key/auth/generate'
VALIDATE = '/api/v1/app/auth/validate'
ADDHASH = '/api/v1/app/auth/hash'
DELETE_APP = '/api/v1/app/auth/delete'
DELETE_KEY = '/api/v1/key/auth/delete'
KEY_INFO = '/api/v1/info/key'
KEY_LIST = '/api/v1/info/key/list'
VERIFY = '/api/v1/key/auth/verify'
PUBLICHASH = '/api/v1/public/hash'
_app, _clientkey, _serverkey, _authkey = None, None, None, None
_keys = []

# REGISTER


def register_app(authkey, author="Anonymous", appname="Anonymous") -> dict:
    "Register new app of your authkey."
    try:
        resp = loads(post(ENDPOINT + REGISTER, data={
                     'authkey': authkey, 'author': author, 'appname': appname}).content.decode())
        if resp['status'] == 'success':
            return resp

        else:
            return {"status": "failed", "message": "Got error from server"}
    except:
        return {"status": "failed", "message": "Got error from server"}


def generate_key(authkey, server_key, appid, exp=60, key_type='trial', vld_method='auto', passed=''):
    "Generate new key for end user."
    try:

        resp = loads(post(ENDPOINT + GENERATE, data={'authkey': authkey, 'server-key': server_key, 'appid': appid, "exp": exp,
                                                     'key-type': key_type,
                                                     'validate-method': vld_method, 'passed': passed}).content.decode())
        if resp['status'] == 'success':
            return resp
        else:
            return {"status": "failed", "message": "Got error from server"}
    except:
        return {"status": "failed", "message": "Got error from server"}


def delete_app(authkey, server_key, appid) -> dict:
    "Delete selected appid."
    try:

        resp = loads(post(ENDPOINT + DELETE_APP, data={
                     'authkey': authkey, 'server-key': server_key, 'appid': appid}).content.decode())
        if resp['status'] == 'success':
            return resp
        else:
            return {"status": "failed", "message": "Got error from server"}
    except:
        return {"status": "failed", "message": "Got error from server"}


def delete_key(key, server_key, appid) -> dict:
    "Delete selected key from appid."
    try:

        resp = loads(post(ENDPOINT + DELETE_KEY,
                     data={'key': key, 'server-key': server_key, 'appid': appid}).content.decode())
        if resp['status'] == 'success':
            return resp
        else:
            return {"status": "failed", "message": "Got error from server"}
    except:
        return {"status": "failed", "message": "Got error from server"}


def update_key(key, server_key, appid, passed) -> dict:
    "Verify manual validation key."
    ":param passed: 0 or 1 or True or False"
    try:

        resp = loads(post(ENDPOINT + VERIFY, data={
                     'key': key, 'server-key': server_key, 'appid': appid, 'passed': passed}).content.decode())
        if resp['status'] == 'success':
            return resp
        else:
            return {"status": "failed", "message": "Got error from server"}
    except:
        return {"status": "failed", "message": "Got error from server"}


def add_hash(server_key, appid, digest) -> dict:
    "Add hash to specified app."
    try:

        resp = loads(post(ENDPOINT + ADDHASH, data={
                     'server-key': server_key, 'appid': appid, 'hash': digest}).content.decode())
        if resp['status'] == 'success':
            return resp
        else:
            return {"status": "failed", "message": "Got error from server"}
    except:
        return {"status": "failed", "message": "Got error from server"}


def key_info(server_key, appid, key) -> dict:
    "Get selected key information from selected appid."
    try:

        resp = loads(post(ENDPOINT + KEY_INFO, data={'server-key': server_key, 'appid': appid,
                                                     "key": key}).content.decode())
        if resp['status'] == 'success':
            return resp
        else:
            return {"status": "failed", "message": "Got error from server"}
    except:
        return {"status": "failed", "message": "Got error from server"}


def key_list(server_key, appid) -> dict:
    "Generate new key for end user."
    try:

        resp = loads(post(ENDPOINT + KEY_LIST, data={'server-key': server_key, 'appid': appid
                                                     }).content.decode())
        if resp['status'] == 'success':
            return resp
        else:
            return {"status": "failed", "message": "Got error from server"}
    except:
        return {"status": "failed", "message": "Got error from server"}

def get_checksum():
    "Return checksum of Offline version"
    try:

        resp = loads(get(ENDPOINT + PUBLICHASH).content.decode())
        if resp['status'] == 'success':
            return resp
        else:
            return {"status": "failed", "message": "Got error from server"}
    except:
        return {"status": "failed", "message": "Got error from server"}


def set_appid(appid):
    global _app
    _app = appid


def set_clientkey(client):
    global _clientkey
    _clientkey = client


def set_serverkey(server):
    global _serverkey
    _serverkey = server


def add_key(key):
    global _keys
    _keys.append(key)


def get_info():
    return {"appid": _app, "client": _clientkey, "server": _serverkey, 'keys': _keys, 'authkey': _authkey}


strs = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'


def shifttext(shift, txt):
    data = []
    for i in txt:
        if i.strip() and i in strs:
            data.append(strs[(strs.index(i) + shift) % 52])
        else:
            data.append(i)
    output = ''.join(data)
    return output


def salty_hash(message):
    message_2 = ''
    lst_salty = []
    for c in message:
        salty = random.randint(1, 10000)
        while chr(salty + ord(c)) == '^' or chr(salty + ord(c)) == '*' or chr(salty) == '^' or chr(salty) == '*':
            salty = random.randint(1, 10000)
        message_2 += chr(ord(c) + salty)
        lst_salty.append(salty)
    message_2 += '^%s*' % ''.join(chr(i) for i in lst_salty)
    return message_2


def _shifttext(shift, txt):
    data = []
    for i in txt:
        if i.strip() and i in strs:
            data.append(strs[(strs.index(i) + shift) % 26])
        else:
            data.append(i)
    output = ''.join(data)
    return output


def _salty_decrypt(message):
    lst_salty = [ord(x) for x in message.split('^')[1].split('*')[0]]
    return ''.join([chr(ord(c) - lst_salty.pop(0)) if lst_salty else chr(ord(c)) for c in message.split('^')[0]])


_inject_function = '''
import os as _os
import sys as _sys
from _sha512 import sha512 as _sha512
strs = 'abcdefghijklmnopqrstuvwxyz'
def _shifttext(shift, txt):
    data = []
    for i in txt:                     
        if i.strip() and i in strs:                 
            data.append(strs[(strs.index(i) + shift) % 26])    
        else:
            data.append(i)          
    output = ''.join(data)
    return output
def _salty_decrypt(message):
    lst_salty = [ord(x) for x in message.split('^')[1].split('*')[0]]
    return ''.join([chr(ord(c) - lst_salty.pop(0)) if lst_salty else chr(ord(c)) for c in message.split('^')[0]])
'''
_inject_data_0 = 'MHPKMS_client.pyd'
_inject_data_1 = ['MHPKMS_client', 'MHPKMS_client.pyc',
                  'MHPKMS_client.py', 'MHPKMS_client.cp311-win_amd64.pyd']
_inject_sha = get_checksum()
_inject_shift = random.randint(1, 52)
_inject_payload = '''
_dt0 = _shifttext({}, _salty_decrypt(''.join({}))) # data 0
_dt1 = [_shifttext({}, _salty_decrypt(''.join(x))) for x in {}] # data 1
_sa = _shifttext({}, _salty_decrypt(''.join({}))) # sha
_ensure = []
_exited = False
for _i in _dt1:
    try:
        open(_i, 'w').close()
        _ensure.append(open(_i, 'a'))
    except:
        _exited = True
        _sys.exit()
if _sha512(open(_dt0, 'rb').read()).hexdigest() != _sa:
    _exited = True
    _sys._exit()
while _exited:
    try:
        _sys.exit(0)
    except SystemExit:
        _os._exit(0)
'''


def obfuscate():
    _inject_data_0_coded = list(salty_hash(
        shifttext(_inject_shift, _inject_data_0)))
    _inject_data_1_coded = [
        list(salty_hash(shifttext(_inject_shift, x))) for x in _inject_data_1]
    _inject_sha_coded = list(salty_hash(shifttext(_inject_shift, _inject_sha)))
    _inject_payload_modified = _inject_payload.format(
        -_inject_shift, _inject_data_0_coded, -_inject_shift, _inject_data_1_coded, -_inject_shift, _inject_sha_coded)
    return _inject_payload_modified


def _inject_source(filename):
    buffer = open(filename, 'r', encoding='utf-8').read()
    _inject = obfuscate()
    open(filename, 'wb').write((_inject_function + '\n' + _inject + '\n' + buffer).encode('utf-8'))


title = '''
                      _          __
              |\/||_||_)__|/|\/|(_
              |  || ||    |\|  |__)
                                                  
'''


def GUI():
    global _app, _serverkey, _clientkey, _keys, _authkey
    dct = {'1': register_app, '2': generate_key, '3': key_info, '4': key_list,
           '5': get_info, '6': update_key, '7': delete_app, '8': delete_key}
    while True:
        os.system("cls")
        _done = False
        print("".center(50, "-"))
        print(title.center(60, ' '))
        print(">> CLI được làm bởi MHP :3")
        print(">> Credit: https://fb.com/py.hacker.hieu")
        print("".center(50, "-"))
        print()
        print("Bảng tính năng".upper().center(50, ' '))
        print(">> 1. Tạo app mới")
        print(">> 2. Tạo key mới")
        print(">> 3. Xem thông tin key")
        print(">> 4. Xem tất cả key có trong app")
        print(">> 5. Xem thông tin hiện tại")
        print(">> 6. Bật/tắt key")
        print(">> 7. Xóa app")
        print(">> 8. Xóa key")
        print(">> 9. Thêm verify integrity (Có thể gây lỗi nếu dùng chế độ onefile)")
        print(">> 10. Set client key")
        print(">> 11. Set server key")
        print(">> 12. Set app hash")
        print(">> 13. Thêm key")
        print(">> 14. Set app")
        print(">> 15. Exit")
        print()
        _inp = input(
            ">> Lựa chọn của bạn (Nhập số): ").strip().replace(" ", '')
        if _inp == '1':
            try:
                os.system('cls')
                while not _done:
                    while not _authkey:
                        _authkey = input(">> Có vẻ bạn chưa nhập authkey: ")
                    _author_temp = input(
                        ">> Nhập tên tác giả của app (Anonymous nếu Enter): ")
                    if not _author_temp:
                        _author_temp = "Anonymous"
                    _appname_temp = input(
                        ">> Nhập tên app (Anonymous nếu Enter): ")
                    if not _appname_temp:
                        _appname_temp = "Anonymous"
                    result = register_app(_authkey, _author_temp, _appname_temp)
                    if result['status'] != 'success':
                        print(">> Lỗi: " + result['message'])
                        prmt = input(
                            ">> Có vẻ tạo app đã thất bại, bạn có muốn thử lại? (y/n): ").strip().lower()
                        if prmt != 'y':
                            _done = True
                    else:
                        print(">> Tạo app thành công :)")
                        print(">> Info:")
                        print(">> AppID: " + result['appid'])
                        print(">> Server key: " + result['server-key'])
                        print(">> Client key: " + result['client-key'])
                        print(
                            ">> NOTE: VUI LÒNG LƯU LẠI NHỮNG THÔNG TIN TRÊN, NẾU NHƯ MẤT SẼ KHÔNG THỂ KHÔI PHỤC.")
                        _app = result['appid']
                        _serverkey = result['server-key']
                        _clientkey = result['client-key']
                        input(">> Enter để về home page")
                        _done = True
            except:
                input(">> Đã có lỗi xảy ra, vui lòng Enter để về Home page")
                _done = True
        elif _inp == '2':
            try:
                # Authkey | serverkey | appid | exp | key type | vld method | passed
                os.system("cls")
                while not _done:
                    while not _authkey:
                        _authkey = input(">> Có vẻ bạn chưa nhập authkey: ")
                    while not _serverkey:
                        _serverkey = input(">> Có vẻ bạn chưa có server key: ")
                    while not _app:
                        _app = input(">> Có vẻ bạn chưa có appid: ")
                    _kt_temp = input(
                        ">> Nhập loại key bạn muốn tạo (trial/onetime): ").strip().lower()
                    while _kt_temp != 'trial' and _kt_temp != 'onetime':
                        _kt_temp = input(
                            ">> Nhập loại key bạn muốn tạo (trial/onetime): ").strip().lower()
                    if _kt_temp == 'onetime':
                        _exp_temp = 0
                    else:
                        _exp_temp = input(
                            ">> Nhập thời gian bạn muốn key tồn tại: ")
                        while not _exp_temp.isdigit():
                            _exp_temp = input(
                                ">> Nhập thời gian bạn muốn key tồn tại: ")

                    _vldmethod_temp = input(
                        ">> Phương thức kiểm tra key (manual/auto): ").strip().lower()
                    while _vldmethod_temp != 'manual' and _vldmethod_temp != 'auto':
                        _vldmethod_temp = input(
                            ">> Phương thức kiểm tra key (manual/auto): ").strip().lower()
                    if _vldmethod_temp == 'auto':
                        _passed_temp = True
                    else:
                        _passed_temp = False

                    result = generate_key(
                        _authkey, _serverkey, _app, _exp_temp, _kt_temp, _vldmethod_temp, _passed_temp)
                    if result['status'] != 'success':
                        print(">> Lỗi: " + result['message'])
                        prmt = input(
                            ">> Có vẻ tạo key đã thất bại, bạn có muốn thử lại? (y/n): ").strip().lower()
                        if prmt != 'y':
                            _done = True
                    else:
                        print(">> Tạo key thành công :)")
                        print(">> Info:")
                        print(">> Key: " + result['key'])
                        print(
                            ">> NOTE: VUI LÒNG LƯU LẠI NHỮNG THÔNG TIN TRÊN, NẾU NHƯ MẤT SẼ KHÔNG THỂ KHÔI PHỤC.")
                        _keys.append(result['key'])
                        input(">> Enter để về home page")
                        _done = True
            except:
                input(">> Đã có lỗi xảy ra, vui lòng Enter để về Home page")
                _done = True
        elif _inp == '3':
            try:
                os.system('cls')
                while not _done:
                    if not _keys:
                        print(">> Bạn không có key :v")
                        _done = True
                        break
                    else:
                        print(">> Tất cả key của bạn: ")
                        _l = 0
                        for key in _keys:
                            print(">> " + str(_l) + ". " + key)
                            _l += 1
                        prmt = input(">> Chọn key bạn muốn xem thông tin (Số, 0 -> cuối): ")
                        try:
                            _chosen = _keys[int(prmt)]
                        except:
                            input(">> Đã có lỗi xảy ra, vui lòng Enter để về Home page")
                            _done = True
                            break
                        while not _serverkey:
                            _serverkey = input(">> Có vẻ bạn chưa có server key: ")
                        while not _app:
                            _app = input(">> Có vẻ bạn chưa có appid: ")
                        result = key_info(_serverkey, _app, _chosen)
                        if result['status'] != 'success':
                            print(">> Lỗi: " + result['message'])
                            prmt = input(
                                ">> Có vẻ tra cứu key đã thất bại, bạn có muốn thử lại? (y/n): ").strip().lower()
                            if prmt != 'y':
                                _done = True
                        else:
                            _info = result['info']
                            print(">> Thông tin key: ")
                            print(">> Trạng thái: " + _info['status'])
                            print(">> Ngày hết hạn: " + datetime.fromtimestamp(_info['exp']).strftime("%m/%d/%Y, %H:%M:%S") + " (UTC)")
                            print(">> Phương thức xác thực: " + _info['validate-method'])
                            print(">> Được quyền truy cập: " + "Có" if _info['passed'] else "Không")
                            input(">> Enter để về home page")
                            _done = True
            except:
                input(">> Đã có lỗi xảy ra, vui lòng Enter để về Home page")
                _done = True
        elif _inp == '4':
            try:
                os.system('cls')
                while not _done:
                    while not _serverkey:
                        _serverkey = input(">> Có vẻ bạn chưa có server key: ")
                    while not _app:
                        _app = input(">> Có vẻ bạn chưa có appid: ")
                    result = key_list(_serverkey, _app)
                    if result['status'] != 'success':
                        print(">> Lỗi: " + result['message'])
                        prmt = input(
                            ">> Có vẻ tra cứu tất cả key đã thất bại, bạn có muốn thử lại? (y/n): ").strip().lower()
                        if prmt != 'y':
                            _done = True
                    else:
                        _info = result['info']
                        print(">> Thông tin tất cả key: ")
                        for k, v in _info.items():
                            print(">> Key: " + k)
                            print(">> Trạng thái: " + v['status'])
                            print(">> Ngày hết hạn: " + datetime.fromtimestamp(v['exp']).strftime("%m/%d/%Y, %H:%M:%S") + " (UTC)")
                            print(">> Phương thức xác thực: " + v['validate-method'])
                            print(">> Được quyền truy cập: " + "Có" if v['passed'] else "Không")
                        input(">> Enter để về home page")
                        _done = True
            except:
                input(">> Đã có lỗi xảy ra, vui lòng Enter để về Home page")
                _done = True
        elif _inp == '5':
            try:
                os.system('cls')
                _info = get_info()
                print(">> Authkey: " + str(_info['authkey']))
                print(">> AppID: " + str(_info['appid']))
                print(">> Client key: " + str(_info['client']))
                print(">> Server key: " + str(_info['server']))
                print(">> Keys: " + str(_info['keys']))
                input(">> Enter để về home page")
                _done = True
            except:
                input(">> Đã có lỗi xảy ra, vui lòng Enter để về Home page")
                _done = True
        elif _inp == '6':
            try:
                os.system('cls')
                while not _done:
                    while not _serverkey:
                        _serverkey = input(">> Có vẻ bạn chưa có server key: ")
                    while not _app:
                        _app = input(">> Có vẻ bạn chưa có appid: ")
                    if not _keys:
                        _key_temp = input(">> Nhập key muốn chỉnh sửa: ")
                    else:
                        print(">> Tất cả key của bạn: ")
                        _l = 0
                        for key in _keys:
                            print(">> " + str(_l) + ". " + key)
                            _l += 1
                        prmt = input(">> Chọn key bạn muốn chỉnh sửa (Số, 0 -> cuối): ")
                        _key_temp = _keys[int(prmt)]
                    _passed_temp = int(input(">> Đặt lại quyền truy cập của key (0: False/1: True): "))
                    result = update_key(_key_temp, _serverkey, _app, _passed_temp)
                    if result['status'] != 'success':
                        print(">> Lỗi: " + result['message'])
                        prmt = input(
                            ">> Có vẻ tra cứu tất cả key đã thất bại, bạn có muốn thử lại? (y/n): ").strip().lower()
                        if prmt != 'y':
                            _done = True
                    else:
                        print(">> Cập nhật thành công, trạng thái hiện tại của key là " + "Khả dụng" if _passed_temp else "Không khả dụng")
                        input(">> Enter để về home page")
                        _done = True
            except:
                input(">> Đã có lỗi xảy ra, vui lòng Enter để về Home page")
                _done = True
        elif _inp == '7':
            try:
                os.system('cls')
                while not _done:
                    while not _authkey:
                        _authkey = input(">> Có vẻ bạn chưa nhập authkey: ")
                    while not _serverkey:
                        _serverkey = input(">> Có vẻ bạn chưa có server key: ")
                    while not _app:
                        _app = input(">> Có vẻ bạn chưa có appid: ")
                    WARNING = input("CẢNH BÁO: BẠN CÓ MUỐN THỰC SỰ XÓA APP? ĐÂY LÀ HÀNH ĐỘNG KHÔNG THỂ KHÔI PHỤC, VUI LÒNG NHẬP VÀO TÊN APPID CỦA BẠN: ")
                    if WARNING != _app:
                        _done = True
                        break
                    result = delete_app(_authkey, _serverkey, _app)
                    if result['status'] != 'success':
                        print(">> Lỗi: " + result['message'])
                        prmt = input(
                            ">> Có vẻ xóa app đã thất bại, bạn có muốn thử lại? (y/n): ").strip().lower()
                        if prmt != 'y':
                            _done = True
                    else:
                        print(">> Đã xóa app: " + _app)
                        input(">> Enter")
                        _done = True
            except:
                input(">> Đã có lỗi xảy ra, vui lòng Enter để về Home page")
                _done = True
        elif _inp == '8':
            try:
                os.system('cls')
                while not _done:
                    if not _keys:
                        _key_temp = input(">> Nhập key muốn chỉnh sửa: ")
                    else:
                        print(">> Tất cả key của bạn: ")
                        _l = 0
                        for key in _keys:
                            print(">> " + str(_l) + ". " + key)
                            _l += 1
                        prmt = input(">> Chọn key bạn muốn chỉnh sửa (Số, 0 -> cuối): ")
                        _key_temp = _keys[int(prmt)]
                    while not _serverkey:
                        _serverkey = input(">> Có vẻ bạn chưa có server key: ")
                    while not _app:
                        _app = input(">> Có vẻ bạn chưa có appid: ")
                    WARNING = input("CẢNH BÁO: BẠN CÓ MUỐN THỰC SỰ XÓA KEY? ĐÂY LÀ HÀNH ĐỘNG KHÔNG THỂ KHÔI PHỤC, VUI LÒNG NHẬP VÀO TÊN APPID CỦA BẠN: ")
                    if WARNING != _app:
                        _done = True
                        break
                    result = delete_key(_key_temp, _serverkey, _app)
                    if result['status'] != 'success':
                        print(">> Lỗi: " + result['message'])
                        prmt = input(
                            ">> Có vẻ xóa key đã thất bại, bạn có muốn thử lại? (y/n): ").strip().lower()
                        if prmt != 'y':
                            _done = True
                    else:
                        print(">> Đã xóa key: " + _key_temp)
                        input(">> Enter")
                        try:
                            _keys.remove(_key_temp)
                        except:
                            pass
                        _done = True
            except:
                input(">> Đã có lỗi xảy ra, vui lòng Enter để về Home page")
                _done = True
        elif _inp == '9':
            try:
                filename = input("> Vui lòng nhập đủ đường dẫn tới file: ")
                _inject_source(filename)
                input("> Đã thêm verify integrity thành công.")
            except:
                input(">> Đã có lỗi xảy ra, vui lòng Enter để về Home page")
                _done = True
        elif _inp == '10':
            try:
                set_clientkey(input("> Nhập vào client key mới: "))
                input("> Đã sửa lại client key")
            except:
                input(">> Đã có lỗi xảy ra, vui lòng Enter để về Home page")
                _done = True
        elif _inp == '11':
            try:
                set_serverkey(input("> Nhập vào server key mới: "))
                input("> Đã sửa lại server key")
            except:
                input(">> Đã có lỗi xảy ra, vui lòng Enter để về Home page")
                _done = True
        elif _inp == '12':
            try:
                os.system('cls')
                while not _done:
                    while not _serverkey:
                        _serverkey = input(">> Có vẻ bạn chưa có server key: ")
                    while not _app:
                        _app = input(">> Có vẻ bạn chưa có appid: ")
                    _file = input("Nhập full đường dẫn đến file: ")
                    md5_hash = md5()
                    file = open(_file, "rb")
                    md5_hash.update(file.read())
                    digest = md5_hash.hexdigest()
                    result = add_hash(_serverkey, _app, digest)
                    if result['status'] != 'success':
                        print(">> Lỗi: " + result['message'])
                        prmt = input(
                            ">> Có vẻ thêm app hash đã thất bại, bạn có muốn thử lại? (y/n): ").strip().lower()
                        if prmt != 'y':
                            _done = True
                    else:
                        print(">> Đã thêm hash của app: " + _app)
                        input(">> Enter")
                        _done = True
            except Exception as e:
                print(e)
                input(">> Đã có lỗi xảy ra, vui lòng Enter để về Home page")
                _done = True
        elif _inp == '13':
            try:
                add_key(input("> Nhập vào key muốn thêm: "))
                input("> Đã thêm key")
            except:
                input(">> Đã có lỗi xảy ra, vui lòng Enter để về Home page")
                _done = True
        elif _inp == '14':
            try:
                set_appid(input("> Nhập vào app mới: "))
                input("> Đã sửa lại app")
            except:
                input(">> Đã có lỗi xảy ra, vui lòng Enter để về Home page")
                _done = True
        elif _inp == '15':
            WARNING = input("CẢNH BÁO: BẠN CÓ MUỐN THOÁT CLI, VUI LÒNG LƯU LẠI THÔNG TIN, NẾU MẤT SẼ KHÔNG THỂ LẤY LẠI (y để tiếp tục) ")
            if WARNING.lower().strip() == 'y':
                exit()
if __name__ == '__main__':
    GUI()
