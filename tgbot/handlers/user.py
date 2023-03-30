import asyncio

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from tgbot.filters.back import BackFilter
from tgbot.keyboards.inline import category_btn, prod_btn, conf_btns, back_cb
from tgbot.keyboards.reply import contact_btn, remove_btn
from tgbot.misc.states import UserStartState, UserMenuState
from tgbot.db.db_api import get_category, get_prod, get_one_prod, create_order, get_order, create_user, get_video, \
    get_user


async def user_start(message: Message, config):
    res = await get_user(message.from_user.id, config)
    if "detail" in res:
        await message.answer("Assalomu aleykum 👋\nRo'yxatdan o'tish uchun ismingizni yuboring!")
        await UserStartState.get_name.set()
    else:
        res = await get_category(config)
        await message.answer("Mashina modelini tanlang 🚘", reply_markup=await category_btn(res))
        await UserMenuState.get_cat.set()


async def get_name(m: Message, state: FSMContext):
    await state.update_data(name=m.text)
    await m.answer("Iltimos telefon raqamingizni yuboring 📲",
                   reply_markup=contact_btn)
    await UserStartState.next()


async def get_contact(m: Message, state: FSMContext, config):
    data = await state.get_data()
    phone = m.contact.phone_number
    await create_user(m.from_user.id, data["name"], phone, config)
    await m.answer("Bosh menuga xush kelibsiz. Bo'limlar bilan tanishing! 👇",
                   reply_markup=remove_btn)
    res = await get_category(config)
    await m.answer("Mashina modelini tanlang 🚘", reply_markup=await category_btn(res))
    await UserMenuState.get_cat.set()


async def get_categorys(c: CallbackQuery, config):
    res = await get_prod(c.data, config)
    await c.message.edit_text("Chexollardan birini tanlang 👇", reply_markup=await prod_btn(res))
    await UserMenuState.next()


async def get_prod_type(c: CallbackQuery, state: FSMContext, config):
    res = await get_one_prod(c.data, config)
    if res["quan"] == 0:
        return await c.answer("Kechirasiz bu chexoldan qolmagan 😞")
    await state.update_data(prod_id=c.data, prod=f"{res['category']['name']} {res['price']}")
    await c.message.delete()
    await c.message.answer(text=f"{res['descr']}\n\n{res['price']} so'm", reply_markup=conf_btns)
    await state.update_data(video=res['video'])
    await UserMenuState.next()


async def get_prods(c: CallbackQuery, state: FSMContext, config):
    data = await state.get_data()
    if c.data == "buy":
        check = await get_order(config, c.from_user.id)
        if bool(check['status']):
            return await c.answer("Kechirasiz faqat bitta chexol mumkun 😞")
        await c.message.delete()
        order = await create_order(config, user_id=c.from_user.id, product_id=data['prod_id'])
        await c.message.answer(f"Sizning raqamingiz: {order['id']}\n"
                               f"Tovar: {data['prod']} so'm\n"
                               "tez orada sizga qayerdan qanday olib\n"
                               "ketishingiz haqida ma'lumot berib\n"
                               "yuboramiz 👨‍💻\n")
        await UserMenuState.get_cat.set()
    else:
        await c.message.delete()
        for video in data['video']:
            vid = await get_video(config, vd_id=video)
            await c.message.answer_video(video=vid['video'])
            await asyncio.sleep(0.5)
        await c.message.answer("Malumotlar 👆", reply_markup=back_cb)


async def back(c: CallbackQuery, config):
    await c.message.delete()
    res = await get_category(config)
    await c.message.answer("Mashina modelini tanlang 🚘", reply_markup=await category_btn(res))
    await UserMenuState.get_cat.set()


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
    dp.register_message_handler(get_name, state=UserStartState.get_name)
    dp.register_message_handler(get_contact, content_types="contact", state=UserStartState.get_contact)
    dp.register_callback_query_handler(get_categorys, state=UserMenuState.get_cat)
    dp.register_callback_query_handler(get_prod_type, BackFilter(), state=UserMenuState.get_prod_type)
    dp.register_callback_query_handler(get_prods, BackFilter(), state=UserMenuState.get_prod)
    dp.register_callback_query_handler(back, state="*")
