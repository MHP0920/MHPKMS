## Hướng dẫn sử dụng bản MHPKMS Offline
___
### Setting up
Phần hướng dẫn này sẽ giúp các bạn cài đặt cũng như sử dụng MHPKMS bản offline, vì bản offline sẽ phức tạp hơn nhưng cách lại hiệu quả hơn online.

Có nhiều bạn sẽ thắc mắc là "tại sao có bản Pypi rồi nhưng lại cần dùng bản offline riêng?" - Thực chất, bản online đã được tối ưu hiệu năng để
sử dụng trên đám mây (cloud), nên phần bảo mật đã bị lược bỏ bớt. Nhưng bản offline lại khác, sử dụng công nghệ đặc biệt độc quyền của đội ngũ 
phát triển MHPKMS, sẽ bảo vệ sản phẩm của bạn hiệu quả.
___
> #### Download
>
```
git clone --single-branch --branch offline https://github.com/MHP0920/MHPKMS.git
```
```
cd MHPKMS
```
Không có thư viện nào được yêu cầu cài đặt, mọi thứ đã được chuẩn bị sẵn.

Để sử dụng thư viện, bạn hãy copy module "MHPKMS_client.pyd" trong folder vừa giải nén vào nơi đang có source code.

```bash
Folder-chứa-code
│
│── MHPKMS_client.pyd
│── MHPKMS_client.pyi # Typing support
└── Source-của-bạn.py
```

Sau khi chuẩn bị mọi thứ, chúng ta có thể thêm thư viện vào rồi!
> #### Khởi động thư viện
>
```python
import MHPKMS_client
client = MHPKMS_client.Client(
    client="client-key",
    appid="appid",
    clear: bool = False, # Optional
    keys: str | list = None, # Optional,
    exp: int = 1 # Optional
)
#client.set_client(str) # KHÔNG SỬ DỤNG: Hàm này không còn được sử dụng trong bản 1.0.0.2
#client.set_appid(str) # KHÔNG SỬ DỤNG: Hàm này không còn được sử dụng trong bản 1.0.0.2
#client.set_keys(str | list)
#client.set_clearmode(bool)
#client.set_exp(int)
```

Như bạn có thể thấy, API của bản offline hầu như không có gì quá khác biệt so với bản online! Đúng vậy, cả 2 API sẽ gần giống nhau, 
tuy nhiên ở bản offline, bạn sẽ không
thể sử dụng **[.activate(key)](/)** và một số tính năng khác.
____
### Usage example
> #### Ví dụ 1
>
Lấy ví dụ về một ứng dụng cơ sở dữ liệu cơ bản chỉ được phép truy cập trong một số lần và thời gian nhất định, được ứng dụng MHPKMS để đăng nhập
>
Chúng ta có một list [key dùng một lần](# "Key dùng một lần (Onetime key) sẽ chỉ sử dụng được một lần, không giới hạn thời gian lưu trữ.") như sau:
```python
keys = [
"abcdef012345679"
"abcdef012345678"
"abcdef012345677"
"abcdef012345676"
...
]
```
Chúng ta đã tạo sẵn một app trong MHPKMS như sau
```python
clientkey = 'abcdef01234567
appid = '01234567-abcd'
```
>
Phần mềm cơ sở dữ liệu như sau
```python
import json
database = json.loads(open("db.json").read())
>
def load_db():
    print(database)
>
def save_db():
    open("db.json").write(json.dumps(database))
```
Như chúng ta thấy, sẽ có 2 mục nhập xuất cơ bản, nhưng làm sao để chúng ta biết khi nào thì hết quyền được thao tác?
Chúng ta có thể sử dụng datetime, biến đếm, hoặc cũng có thể sử dụng MHPKMS
```python
import MHPKMS_client
import json
>
database = json.loads(open("db.json").read())
API = MHPKMS_client.Client(
    client = clientkey,
    appid = appid,
    keys = keys,
    clear = True, # Clearscreen
    exp: int = 1
)
>
@API.required
def load_db():
    print(database)
>
@API.required
def save_db():
    open("db.json").write(json.dumps(database))
>
# Mỗi khi chạy hàm sẽ load key, mỗi khi sử dụng được trong 1 đến tối đa 60 phút (tùy cài đặt) 
```
Vậy là không cần biến đếm hay datetime, bạn vẫn có thể quản lí được giới hạn thời gian và số lần sử dụng.

____
> #### Ví dụ 2 - Selenium
Bạn là một Python Automation Engineer, đang phát triển nhiều tool, nhưng bạn muốn khách hàng có thể sử dụng thử trong một thời gian quy định?
MHPKMS là giải pháp cho bạn.
Lấy ví dụ chúng ta vẫn dùng tất cả thông tin trên, chỉ khác chúng ta sẽ sử dụng Selenium
```python
import MHPKMS_client
import ... # Thêm selenium
>
API = MHPKMS_client.Client(
    client = clientkey,
    appid = appid
)
client.set_keys(keys) # Keys đã thêm ở trên
client.ensure_checksum() # Kiểm tra tính nguyên vẹn của thư viện
driver = ... # Khởi tạo driver
def main():
    while True:
        key = input("Nhập key: ")
        API.set_keys(key)
        option = input("Lựa chọn job: ")
        if ... dojob1()
        else dojob2()
>
@client.required
def dojob1():
    ... # Do job
>
@client.required
def dojob2():
    ... # Do job
>
main()
```
Như bạn thấy, đoạn code cũng không khác mấy, chỉ khác lần này chúng ta sử dụng Selenium. MHPKMS tương thích với rất nhiều thư viện nên
bạn không phải lo lắng về vấn đề xung đột.

MHPKMS sẽ tiết kiệm cho bạn một khoản chi tiêu lớn. Chỉ với ~53.000 VND, bạn đã có thể tạo ra rất nhiều bản thử nghiệm mà không phải 
suy nghĩ quá nhiều.

### CLI Usage
Sau khi đã setup xong source, chúng ta có thể dùng [CLI](https://mhpkms.mhpteam.dev/docs/API/cli), chọn vào mục "Thêm verify integrity" và chọn file, lúc này
CLI sẽ inject vào code của bạn một đoạn mã dùng để tránh thư viện MHPKMS bị thay thế.

### Final Initialize
Sau khi hoàn thành tất cả, bạn có thể đọc Part 1 & 2 của [Python Protection Project](https://github.com/MHP0920/python-protection-project), áp dụng theo cách được hướng dẫn sẽ giúp bảo
vệ mã nguồn của bạn hoặc có thể chuyển đến [Deployment](https://mhpkms.mhpteam.dev/docs/Deployment)