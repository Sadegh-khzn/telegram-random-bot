from aiogram import filters , F , Dispatcher ,Bot
from aiogram.types import ReplyKeyboardMarkup , InlineKeyboardButton , KeyboardButton , InlineKeyboardMarkup , Message , CallbackQuery
from aiogram.types import InlineQuery,InlineQueryResultArticle,InputTextMessageContent
import asyncio
import os
import random
from middleware import Requirmenets
from models import create_table
from filters import is_admin
from aiogram.fsm.state import State,StatesGroup
from aiogram.fsm.context import FSMContext
from models import User,get_user,change_max,change_min



#config
#TOKEN = os.environ["BOT_TOKEN"]
TOKEN = ""
admins = []
#default
max_number = 100
min_number = 0
randomNUmber = 0
message_for_take_newNumber = None


dp = Dispatcher()
dp.message.outer_middleware(Requirmenets())

class UserState(StatesGroup):
    max_state = State()
    min_state = State()

#keyboard
reply_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="عدد شانسی"),
        KeyboardButton(text="راهنمای ربات")
    ]
],resize_keyboard=True)
def set_inline_keyboard_setNumber(max_number , min_number):
    inline_keyboard_setNumber = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="حداکثر مقدار:" , callback_data="change_max_number"),
            InlineKeyboardButton(text=f"{max_number}" , callback_data="change_max_number")
        ],
        [
            InlineKeyboardButton(text="حداقل مقدار:" , callback_data="change_min_number"),
            InlineKeyboardButton(text=f"{min_number}" , callback_data="change_min_number")
        ],
        [
            InlineKeyboardButton(text="انتخاب عدد شانسی" , callback_data="set_random")
        ]
    ]
)
    return inline_keyboard_setNumber
def inline_keyboard_again(randomNUmber:int)->None:
    inline_keyboard_again = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=f"عدد انتخا شده:  {randomNUmber} ",callback_data="nothing")
        ],
        [
            InlineKeyboardButton(text="انتخاب مجدد",callback_data="set_random")
        ]
    ]
)
    return inline_keyboard_again

@dp.message(filters.CommandStart() , F.chat.type.in_(["private"]))
async def start_handler(message: Message):
    await message.answer("به ربات خوش اومدی \n از منوی زیر انتخاب کن " , reply_markup=reply_keyboard)
@dp.message(F.text == "راهنمای ربات")
async def info_handler(message : Message):
    await message.answer("این بخش راهنمای رباته هنوز تکمیل نشده عجله نکن ")
@dp.message(F.text == "عدد شانسی")
async def random_handler(message : Message):
    user = await get_user(message.from_user.id)
    max_number=user.max_number
    min_number=user.min_number
    await message.answer("از منو زیر برای انتخاب عدد در بازه مشخص شده استفاده کنین برای تغییر بازه روی عددها کلیک کنید " , reply_markup=set_inline_keyboard_setNumber(max_number, min_number))


@dp.callback_query(F.data == "change_max_number")
async def change_max_number_handler(callback : CallbackQuery , state: FSMContext):    
    await state.set_state(UserState.max_state)
    if callback.message:
        await callback.message.edit_text("مقدار جدید برای حداکثر عدد وارد کنید\nحتما روی این پیام ریپلای بزنید")
    elif callback.inline_message_id:
        await state.update_data(inline_message_id=callback.inline_message_id)
        await callback.bot.edit_message_text(text="مقدار جدید برای حداکثر عدد وارد کنید\nحتما روی این پیام ریپلای بزنید",inline_message_id=callback.inline_message_id)



@dp.message(UserState.max_state)
async def take_max_number(message : Message,state : FSMContext):
    if message.reply_to_message :
        if message.text.isdigit():
            user = await get_user(message.from_user.id)
            min_number=user.min_number
            max_number = message.text
            await change_max(message.from_user.id,max_number)
            data =  await state.get_data()
            if "inline_message_id" in data:
                await message.bot.edit_message_text("از منو زیر برای انتخاب عدد در بازه مشخص شده استفاده کنین برای تغییر بازه روی عددها کلیک کنید ",inline_message_id=data["inline_message_id"],reply_markup=set_inline_keyboard_setNumber(max_number ,min_number))
            else:
                await message.reply_to_message.edit_text("از منو زیر برای انتخاب عدد در بازه مشخص شده استفاده کنین برای تغییر بازه روی عددها کلیک کنید ",reply_markup=set_inline_keyboard_setNumber(max_number ,min_number))
            await state.clear()


@dp.callback_query(F.data == "change_min_number")
async def change_min_number_handler(callback : CallbackQuery , state: FSMContext):    
    await state.set_state(UserState.min_state)
    if callback.message:
        await callback.message.edit_text("مقدار جدید برای حداکثر عدد وارد کنید\nحتما روی این پیام ریپلای بزنید")
    elif callback.inline_message_id:
        await state.update_data(inline_message_id=callback.inline_message_id)
        await callback.bot.edit_message_text(text="مقدار جدید برای حداکثر عدد وارد کنید\nحتما روی این پیام ریپلای بزنید",inline_message_id=callback.inline_message_id)



@dp.message(UserState.min_state)
async def take_min_number(message : Message,state : FSMContext):
    if message.reply_to_message :
        if message.text.isdigit():
            user = await get_user(message.from_user.id)
            max_number=user.max_number
            min_number = message.text
            await change_min(message.from_user.id,min_number)
            data = await state.get_data()
            if "inline_message_id" in data:
                await message.bot.edit_message_text("از منو زیر برای انتخاب عدد در بازه مشخص شده استفاده کنین برای تغییر بازه روی عددها کلیک کنید ",inline_message_id=data["inline_message_id"],reply_markup=set_inline_keyboard_setNumber(max_number ,min_number))
            else:
                await message.reply_to_message.edit_text(text="از منو زیر برای انتخاب عدد در بازه مشخص شده استفاده کنین برای تغییر بازه روی عددها کلیک کنید ",reply_markup=set_inline_keyboard_setNumber(max_number ,min_number))
            await state.clear()




@dp.callback_query(F.data == "set_random")
async def generate_random_number(callback: CallbackQuery):
    user = await get_user(callback.from_user.id)
    max_number=user.max_number
    min_number=user.min_number
    randomNUmber = random.randint(min_number,max_number)
    if callback.message:
        await callback.message.edit_text(f"عدد جدید شما:{randomNUmber}",reply_markup=inline_keyboard_again(randomNUmber))
    elif callback.inline_message_id:
        await callback.bot.edit_message_text(text=f"عدد جدید شما: {randomNUmber}",reply_markup=inline_keyboard_again(randomNUmber),inline_message_id=callback.inline_message_id)

    
@dp.inline_query()
async def inline_mode_handler(inline_query:InlineQuery):
    user =await get_user(inline_query.from_user.id)
    max_number=user.max_number
    min_number=user.min_number
    result = InlineQueryResultArticle(
        id="inline_handler",
        title="عدد شانسی",
        input_message_content=InputTextMessageContent(message_text="salam"),
        reply_markup=set_inline_keyboard_setNumber(max_number,min_number),
        description="انتخاب عدد از بازه ی انتخابی",

        )
    await inline_query.answer(
        results=[result],
        cache_time=1
    )

async def main():
    await create_table()
    bot = Bot(TOKEN)
    await dp.start_polling(bot)
if __name__ == "__main__": 
    asyncio.run(main())