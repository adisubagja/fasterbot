from bot          import Bot
from user         import User
from checkoutdata import PaymentInfo, PaymentChannel, PaymentChannelOptionInfo
from colorama     import Fore, init
from time         import sleep
from datetime     import datetime
import os

init()
INFO = Fore.LIGHTBLUE_EX + "[*]" + Fore.BLUE
INPUT = Fore.LIGHTGREEN_EX + "[?]" + Fore.GREEN
PROMPT = Fore.LIGHTRED_EX + "[!]" + Fore.RED


def int_input(prompt_: str, max_: int = -1, min_: int = 1) -> int:
    input_: str
    while True:
        input_ = input(f"{INPUT} {prompt_}")
        if input_.isdigit():
            input_int = int(input_)
            if max_ == -1:
                return input_int
            elif min_ <= input_int <= max_:
                return input_int
            elif input_int > max_:
                print(PROMPT, "Angka terlalu banyak!")
                continue
            elif input_int < min_:
                print(PROMPT, "Angka terlalu sedikit!")
                continue
        print(PROMPT, "Masukkan angka!")


if os.name.lower() == "nt":
    os.system("cls")
else:
    os.system("clear")
print(INFO, "Mengambil informasi user...", end='\r')
cookie = open("cookie.txt", 'r')
user = User.login(cookie.read())
cookie.close()
print(INFO, "Welcome", Fore.GREEN, user.name, ' ' * 10)
print()

print(INFO, "Masukan url barang yang akan dibeli")
bot = Bot(user)
item = bot.fetch_item_from_url(input(INPUT + " url: " + Fore.RESET))

print(Fore.RESET, "-" * 32)
print(Fore.LIGHTBLUE_EX, "Nama:", Fore.GREEN, item.name)
print(Fore.LIGHTBLUE_EX, "Harga:", Fore.GREEN, item.get_price(item.price))
print(Fore.LIGHTBLUE_EX, "Brand:", Fore.GREEN, item.brand)
print(Fore.LIGHTBLUE_EX, "Stok:", Fore.GREEN, item.stock)
print(Fore.LIGHTBLUE_EX, "Lokasi Toko:", Fore.GREEN, item.shop_location)
print(Fore.RESET, "-" * 32)
print()

selected_model = 0
if len(item.models) > 1:
    print(INFO, "Pilih model/variasi")
    print(Fore.RESET, "-" * 32)
    for index, model in enumerate(item.models):
        print(Fore.GREEN + '[' + str(index+1) + ']' + Fore.BLUE, model.name)
        print('\t', Fore.LIGHTBLUE_EX, "Harga:", Fore.GREEN, item.get_price(model.price))
        print('\t', Fore.LIGHTBLUE_EX, "Stok:", Fore.GREEN, model.stock)
        print('\t', Fore.LIGHTBLUE_EX, "ID Model:", Fore.GREEN, model.model_id)
        print(Fore.RESET, "-" * 32)
    print()
    selected_model = int_input("Pilihan: ", len(item.models))-1
    print()

print(INFO, "Pilih metode pembayaran")
payment_channels = dict(enumerate(PaymentChannel))
for index, channel in payment_channels.items():
    print(Fore.GREEN + '[' + str(index+1) + ']' + Fore.BLUE, channel.name)
print()
selected_payment_channel = payment_channels[int_input("Pilihan: ", len(payment_channels))-1]
print()

selected_option_info = PaymentChannelOptionInfo.NONE
if selected_payment_channel is PaymentChannel.TRANSFER_BANK or \
        selected_payment_channel is PaymentChannel.AKULAKU:
    options_info = dict(enumerate(list(PaymentChannelOptionInfo)[1 if selected_payment_channel is
                        PaymentChannel.TRANSFER_BANK else 7:None if selected_payment_channel is
                        PaymentChannel.AKULAKU else 7]))
    for index, option_info in options_info.items():
        print(Fore.GREEN + '[' + str(index+1) + ']' + Fore.BLUE, option_info.name)
    print()
    selected_option_info = options_info[int_input("Pilihan: ", len(options_info))-1]

if not item.is_flash_sale:
    if item.upcoming_flash_sale is not None:
        flash_sale_start = datetime.fromtimestamp(item.upcoming_flash_sale.start_time)
        print(INFO, "Waktu Flash Sale: ", flash_sale_start.strftime("%H:%M:%S"))
        print(INFO, "Menunggu Flash Sale...", end='\r')
        sleep((datetime.fromtimestamp(item.upcoming_flash_sale.start_time) - datetime.now())
              .total_seconds() - 2)
        print(INFO, "Bersiap siap...", end='\r')
        while not item.is_flash_sale:
            item = bot.fetch_item(item.item_id, item.shop_id)
    else:
        print(PROMPT, "Flash Sale telah Lewat!")
        exit(1)

print(INFO, "Flash Sale telah tiba")
start = datetime.now()
print(INFO, "Menambah item ke cart...")
cart_item = bot.add_to_cart(item, selected_model)
print(INFO, "Checkout item...")
bot.checkout(PaymentInfo(
    channel=selected_payment_channel,
    option_info=selected_option_info
), cart_item)
end = datetime.now() - start
print(INFO, "Item berhasil dibeli dalam waktu", Fore.YELLOW, end.seconds, "detik", end.microseconds // 1000,
      "milis")
print(Fore.GREEN + "[*]", "Sukses")
