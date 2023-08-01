from requests import post
from json import loads

ENDPOINT = 'https://api.mhpkms.mhpteam.dev'
ACTIVE = '/api/v1/app/auth/validate'

class Client:
    def __init__(self, client=None, appid=None) -> None:
        """
        DESCRIPTION:
        ------------------
        Initialize the API.
        :param client (str): Initialize the client key to authorize later. (Optional, can set later)
        :param appid (str): Initialize the appID used to authorize later. (Optional, can set later)
        
        USAGE:
        ------------------
        `API = Client(client_key="<your-client-key>", appid="<your-appid>")`

        OR

        ```
        API = Client()
        API.set_client("<your-client-key>")
        API.set_appid("<your-appid>")
        ```
        """ 
        self.client = client
        self.appid = appid
    def set_client(self, client_key: str) -> None:
        "Set client key for Client"
        self.client = client_key
    def set_appid(self, appid: str) -> None:
        "Set appid for Client"
        self.appid = appid
    def activate(self, key: str) -> bool:
        """
        DESCRIPTION
        -
        Activate the key.
        If activate failed, it will return False, otherwise will return True.

        USAGE
        -
        ```python
        API = Client(...)

        def secrets():
            check = activate(key) # False | dict

            if check:
                #print("Remaining: " + str(check['remaining']))

                print("This is secrets")
        ```
        """
        _response = loads(post(ENDPOINT + ACTIVE, data={
            "key": key,
            "client-key": self.client,
            "appid": self.appid
        }).content)
        if _response['status'] != 'success':
            return False
        else:
            return _response
