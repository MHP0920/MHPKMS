# MHPKMS - Collab with PPP (Python Protection Project) 💖💖💖

![Penguin logo](https://github.com/MHP0920/MHPKMS/blob/tutorial/logo.png?raw=true)

## Project link

> **https://mhpkms.mhpteam.dev**

> **https://pypi.org/project/MHPKMS/**

## Giới thiệu

Đây là hướng dẫn sử dụng chính thức của MHP Key Management Service (MHPKMS), nơi bạn có thể tìm thấy những thông tin chi
tiết về cách sử dụng.

MHPKMS hỗ trợ ứng dụng chạy trên [cloud (online)](/docs/API/client/online) cũng như chạy [trên máy (offline)](/docs/API/client/offline).

Khi cần trợ giúp có thể tham khảo [Những câu hỏi thường gặp](/faq). Ngoài ra bạn cũng có thể hỏi đáp trong nhóm [discord](https://discord.gg/bB365YwE) của chúng tôi.

Nếu phát hiện lỗi hoặc có ý kiến đóng góp, vui lòng tạo [Issue](/).

___

### Cài đặt

> #### Online
>
```
pip install MHPKMS
```
```python
import MHPKMS_client
API = MHPKMS_client.Client()
```
___
> #### Offline
>
```
git clone https://github.com/MHP0920/MHPKMS.git
```
**hoặc [Tải xuống](https://github.com/MHP0920/python-protection-project)**
>
Nếu clone từ git, sử dụng:
```
cd MHPKMS
```
Nếu tải từ latest release, bạn hãy giải nén và truy cập vào thư mục được giải nén.
```python
import MHPKMS_client
API = MHPKMS_client.Client()
```

**Note: Các bạn không nên sử dụng bản Online cho sản phẩm Offline và ngược lại. [Xem thêm](/)**


### Cập nhật

> #### Online
>
```
pip install MHPKMS --upgrade
```
____
> #### Offline
>
Bản offline sẽ tự động thông báo nếu người dùng bật [ensure_checksum](/docs/API/usage#ensure_checksum) 
hoặc có thể [tải xuống](https://github.com/MHP0920/python-protection-project).

## How it works?

### Idea

Được lên ý tưởng và nghiên cứu lâu dài về các công nghệ bảo mật cũng như bảo mật trong Python, MHPKMS
quyết định sử dụng công nghệ quản lí key để hướng đến các khách hàng đang làm về app, game, automation, nhưng muốn bán sản phẩm theo thời gian
sử dụng. Cơ chế của MHPKMS rất đơn giản, chỉ với thao tác đơn giản là nhập key, bạn có thể giới hạn được người dùng muốn sử dụng sản phẩm của bạn.

### Example

```python
def secret(*args, **kwargs):
    print("Chỉ những người đặc biệt mới được sử dụng")
```
Ở đoạn code trên, chúng ta có thể thấy hàm `secret` cần được giới hạn, theo cách thông thường, chúng ta có thể làm như sau
```python
def secret(*args, **kwargs):
    username = input("Nhập username: ")
    password = input("Nhập password: ")
    if username == 'admin' and password == 'admin':
        print("Chỉ những người đặc biệt mới được sử dụng")
```
Như bạn có thể thấy, chúng ta đã cập nhật thêm tên đăng nhập và mật khẩu, nhưng cách này vẫn chưa thực sự an toàn, những người muốn sử dụng trái phép
có thể tìm đến phần chữ "admin" và đăng nhập như bình thường, hoặc phổ biến hơn, [brute-force attack](https://en.wikipedia.org/wiki/Brute-force_attack).

Nhưng với MHPKMS, những vấn đề trên đã được giải quyết. Với dãy kí tự được tạo theo công nghệ đặc biệt, bảo vệ bằng sha512 và salt, brute-force hay tìm
được key là một chuyện gần như bất khả thi, vì key được lưu trên cloud.
```python
import MHPKMS_client # Load thư viện

API = MHPKMS_client.Client() # Khởi tạo API
API.set_client("client-key") # Thêm client key (Thêm trước)
API.set_appid("appid") # Thêm appid (Thêm trước)

key = input("Nhập key được cấp từ trước: ") # Nhập vào key đã được cấp, những người được chỉ định sở hữu key

API.set_keys(key) # Thêm key vào dữ liệu

@API.required # Tính năng đột phá của MHPKMS, dễ đọc code, dễ sử dụng
def secret(*args, **kwargs):
    print("Chỉ những người đặc biệt mới được sử dụng") # Làm mọi thứ như bình thường, không cần thay đổi cấu trúc
```
Khi được sử dụng, đoạn code trên chỉ yêu cầu người dùng nhập vào key đã được đăng kí từ trước, trong code không chứa bất kì key nào nên việc tìm ra
là bất khả thi.

## Contributions
____
### Contributors
- [Trần Minh Hiếu](https://www.facebook.com/py.hacker.hieu)
- [Notch Apple](https://www.facebook.com/notchapple1703)
- [Lê Nguyễn Quỳnh Hương](https://www.facebook.com/profile.php?id=100082163187491)

Want to become a contributor? [Join us](https://discord.gg/PFTYkjWWEW)

### Roles
- **Head Developer**: Trần Minh Hiếu
- **Security Researcher**: Trần Minh Hiếu
- **API Development**: Trần Minh Hiếu
- **CLI Development**: Trần Minh Hiếu
- **Server Management**: Trần Minh Hiếu
- **Database Management**: Trần Minh Hiếu
- **Payment Information**: Trần Minh Hiếu
- **Payment Designer**: Notch Apple
- **Debuggers & Security Testers**: Trần Minh Hiếu & Notch Apple
- **Exploiters**: Notch Apple
- **Documentations Arrangement**: Trần Minh Hiếu & Notch Apple
- **Icon Designer**: Lê Nguyễn Quỳnh Hương
- **Thumbnail Designer**: Lê Nguyễn Quỳnh Hương
- **Bootstrap**: Docusaurus

### J4F🐧
**Cảm ơn** *electricity, tinh hoa đất trời, dòng suối thiên nhiên* đã hỗ trợ mọi người trong quá trình làm  
**Cảm ơn** *laptop* đã gồng gánh 60 tabs để nghiên cứu  
**Cảm ơn** *Microsoft* đã tạo ra vertical tab cho Edge nên Trần Minh Hiếu không chết oan  
**Cảm ơn** *VSCODE* đã gánh Trần Minh Hiếu 10 tabs code + 60 tabs Edge mà không crash  
**Cảm ơn** *Spotify* đã bật nhạc suốt ngày đêm để hồi máu cho Trần Minh Hiếu  
**Cảm ơn** *Mozilla* đã tạo ra Firefox vì Firefox đẹp hơn Chrome 😱 - Notch Apple -  
**Cảm ơn** *Jetbrains* đã tạo ra Pycharm vì Pycharm iz da bezt 🗿 - Notch Apple -  
**Cảm ơn** *C418 và Adrian Talens* đã bật nhạc hồi máu cho Notch Apple  

## Copyright
Copyright © MHP 2023. _This work is licensed under a [CC BY-ND 4.0 license](http://creativecommons.org/licenses/by-nd/4.0/)._

![image](https://i.creativecommons.org/l/by-nd/4.0/88x31.png)
