from json        import dumps
from enum        import Enum
from random      import choices
from string      import ascii_letters, digits
from colorama    import Fore, init
import requests


class OTPChannel(Enum):
    WHATSAPP = 0
    SMS = 1


class Login:
    csrf_token: str
    session: requests.Session
    user: str
    user_agent: str

    def __init__(self, user: str, hash_: str):
        self.user = user

        user_agent_ = open("user_agent.txt", 'r')
        self.user_agent = user_agent_.read()
        user_agent_.close()

        self.session = requests.Session()
        self.session.post("https://shopee.co.id/buyer/login")
        self.session.cookies.set("csrftoken", Login.randomize_token())
        self.csrf_token = self.session.cookies.get("csrftoken")

        login_using = "username"
        if "@" in user:
            login_using = "email"
        elif user.isdigit():
            login_using = "phone"
        resp = self.session.post(
            url="https://shopee.co.id/api/v2/authentication/login",
            headers=self.__default_headers(),
            data=dumps({
                login_using: user,
                "password": hash_,
                "support_ivs": True,
                "support_whats_app": True
            }),
            cookies=self.session.cookies.get_dict()
        )
        data = resp.json()
        if data["error"] != 77:
            raise Exception(f"failed to login, invalid username or password, code: {data['error']}")

    def __default_headers(self) -> dict:
        return {
            "accept": "application/json",
            "content-type": "application/json",
            "if-none-match-": "*",
            "referer": "https://shopee.co.id/buyer/login",
            "user-agent": self.user_agent,
            "x-csrftoken": self.csrf_token
        }

    def get_cookie_as_string(self) -> str:
        output = ""
        for k, v in self.session.cookies.get_dict().items():
            output += f"{k}={v}; "
        return output[:-2]

    def send_otp(self, channel: OTPChannel = OTPChannel.SMS):
        self.session.post(
            url="https://shopee.co.id/api/v2/authentication/resend_otp",
            headers=self.__default_headers(),
            data=dumps({
                "channel": channel.value,
                "force_channel": True,
                "operation": 5,
                "support_whats_app": True
            })
        )

    def verify(self, code: str) -> str:
        resp = self.session.post(
            url="https://shopee.co.id/api/v2/authentication/vcode_login",
            headers=self.__default_headers(),
            data=dumps({
                "otp": code,
                "phone": self.user,
                "support_ivs": True
            })
        )

        data = resp.json()
        if data["error"] is not None:
            raise Exception("failed to login, invalid otp code")

    @staticmethod
    def randomize_token() -> str:
        return ''.join(choices(ascii_letters + digits, k=32))


if __name__ == "__main__":
    init()
    INFO = Fore.LIGHTBLUE_EX + "[*]" + Fore.BLUE
    INPUT = Fore.LIGHTGREEN_EX + "[?]" + Fore.GREEN
    ERROR = Fore.LIGHTRED_EX + "[!]" + Fore.RED

    print(INFO, "Masukkan username/email/nomor telepon")
    user = input(INPUT + " username/email/nomor: ")
    print(INFO, "Masukkan Hash")
    hash_ = input(INPUT + " hash: ")
    print(INFO, "Sedang login...")

    login = Login(user, hash_)
    login.send_otp()
    print(INFO, "OTP Dikirim lewat SMS")
    code = input(INPUT + " kode otp: ")
    print(INFO, "Memverifikasi...")
    login.verify(code)
    print(INFO, "Verifikasi berhasil")
    with open("cookie.txt", 'w') as f:
        f.write(login.get_cookie_as_string())

    print(INFO, "Login sukses")
