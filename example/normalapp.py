import MHPKMS_client


API = MHPKMS_client.Client(
    appid = "secrets",
    client = "secrets",
    exp = 60,
    clear = True
)
API.ensure_checksum()
def main():
    while True:
        print(
            """Choice your option:
> 1. Input Activate Key
> 2. Do something sus (restricted) 
""")
        _cmd = str(input("> Your choice: ")).strip().replace(' ', '')
        if _cmd == '1':
            _key = str(input("> Enter your key: "))
            API.set_keys(_key)
            print("> Đã thêm key của bạn!")
        elif _cmd == '2':
            supersecret()

@API.required
def supersecret():
    print("Baka!")
    print("Yamete~")
    print("DANG, U FOUND ME, I'M VERY SECRET! JEEZ")

main()