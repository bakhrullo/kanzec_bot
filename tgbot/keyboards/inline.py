from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

back_btn = InlineKeyboardButton("🔙 Orqaga", callback_data="back")

back_cb = InlineKeyboardMarkup().insert(back_btn)
conf_btns = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text="Xarid ✅", callback_data="buy"),
                                                  InlineKeyboardButton(text="Chexol haqida ma'lumot ℹ️", callback_data="info"),
                                                  back_btn)


async def category_btn(cars):
    car_btn = InlineKeyboardMarkup(row_width=1)
    for car in cars:
        car_btn.insert(InlineKeyboardButton(text=car["name"], callback_data=car["id"]))
    return car_btn


async def prod_btn(prods):
    prod_btn = InlineKeyboardMarkup(row_width=1)
    for prod in prods:
        prod_btn.insert(InlineKeyboardButton(text=f"{prod['price']} so'm", callback_data=prod["id"]))
    prod_btn.add(back_btn)
    return prod_btn
