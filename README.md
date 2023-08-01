## Hướng dẫn sử dụng bản MHPKMS Online
___
### Working with framework
Phần hướng dẫn này sẽ giúp các bạn sử dụng MHPKMS với Flask, nhưng bạn cũng có thể áp dụng MHPKMS vào các framework khác.
```python
from flask import (Flask, request, abort, make_response) # Load thư viện flask
from MHPKMS_client import Client # Load Client của MHPKMS

app = Flask(__name__)
client = Client()
# client.set_client(<client-key>)
# client.set_appid(<appid>)

@app.get("/api/secrets")
def secrets():
    # Sử dụng MHPKMS để kiểm tra key
    key = request.args.get('key')
    check = client.activate(key) # Kiểm tra key
    if not check: # Sai key
        abort(401)
    return make_response("Hi, I'm secret.", 200) # Trả về thông tin được bảo vệ
```

### Selenium with framework, and MHPKMS
Bạn thậm chí có thể chạy Selenium (Automation) trên framework! Trong bài viết này, chúng ta sẽ chạy Selenium trên Flask cùng với bảo mật
của MHPKMS
```python
import ... # Thêm các thư viện cần thiết cho Selenium, Flask
from MHPKMS_client import Client

app = Flask(__name__)
client = Client()
# client.set_client(<client-key>)
# client.set_appid(<appid>)

@app.get("/api/tool/dojob")
def dojob():
    # Kiểm tra key trước, giảm resource cần dùng cho server
    key = request.args.get('key')
    check = client.activate(key)
    if not check:
        abort(401)
    driver = ... # Loại driver bạn muốn dùng
    ... # Do job
    return make_response(<kết-quả>, 200) # Return sau khi do job xong
```
```
curl <host>/api/tool/dojob -> 401
```
```
curl <host>/api/tool/dojob?key=<legit-key> -> 200
```

Với mợt vài lệnh cơ bản, bạn đã có thể làm tool mà không lo bị sử dụng trái phép, MHPKMS sẽ bảo vệ bạn khỏi abuse nên bạn không phải lo 
lắng 💖

