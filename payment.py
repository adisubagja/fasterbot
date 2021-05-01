from enum import Enum
from typing import Dict


class PaymentChannel:
    __name: str
    __channel_id: int
    __options: Dict[str, str]
    __version: int

    def __init__(self, name: str, channel_id: int, options: Dict[str, str] = None, version: int = 2):
        self.__name = name
        self.__channel_id = channel_id
        self.__options = options
        self.__version = version

    def name(self) -> str:
        return self.__name

    def channel_id(self) -> int:
        return self.__channel_id

    def options(self) -> Dict[str, str]:
        return self.__options

    def version(self) -> int:
        return self.__version

    def has_option(self) -> bool:
        return self.__options is not None


class PaymentChannelList(Enum):
    ALFAMART = PaymentChannel("Alfamart", 8003200)
    INDOMART = PaymentChannel("Indomart iSaku", 8003001)
    AKULAKU = PaymentChannel("Akulaku", 8000700, {
        "Akulaku Cicilan 1x": "8000700-25",
        "Akulaku Cicilan 2x": "8000700-26",
        "Akulaku Cicilan 3x": "8000700-27",
        "Akulaku Cicilan 6x": "8000700-28",
        "Akulaku Cicilan 9x": "8000700-29",
        "Akulaku Cicilan 12x": "8000700-30"
    })
    TRANSFER_BANK = PaymentChannel("Transfer Bank", 8005200, {
        "Transfer Bank BCA (Dicek Otomatis)": "89052001",
        "Transfer Bank Mandiri (Dicek Otomatis)": "89052002",
        "Transfer Bank BNI (Dicek Otomatis)": "89052003",
        "Transfer Bank BRI (Dicek Otomatis)": "89052004",
        "Transfer Bank Syariah (Dicek Otomatis)": "89052005",
        "Transfer Bank Permata (Dicek Otomatis)": "89052006"
    })
    COD = PaymentChannel("COD (Bayar di Tempat)", 89000, version=1)
    SHOPEE_PAY = PaymentChannel("Shopee Pay", 8001400)
