from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
import json
import asyncio

API_TOKEN = "7461127833:AAEscfu7JCsNLEsFTo9mEeDW-UfS9viDoH0"
CHANNEL_USERNAME = "@oliy_stavka_betvinner_1xbet"

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

async def is_subscribed(user_id):
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        return member.status in ["member", "creator", "administrator"]
    except:
        return False

subscribe_btn = InlineKeyboardMarkup(row_width=1)
subscribe_btn.add(
    InlineKeyboardButton("🔔 Kanalga obuna bo‘lish", url=f"https://t.me/{CHANNEL_USERNAME.strip('@')}"),
    InlineKeyboardButton("✅ Tekshirish", callback_data="check_sub")
)

with open("videos.json", "r") as f:
    video_data = json.load(f)

@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    if not await is_subscribed(user_id):
        await message.answer("👋 Avvalo kanalga obuna bo‘ling:", reply_markup=subscribe_btn)
        return
    await message.answer("✅ Kodni kiriting (masalan: 1, 456...)")

@dp.callback_query_handler(lambda c: c.data == "check_sub")
async def check_subscription(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    if await is_subscribed(user_id):
        await callback.message.edit_text("✅ Rahmat! Endi kodni yuboring.")
    else:
        await callback.answer("⛔ Hali obuna bo‘lmagansiz.", show_alert=True)

@dp.message_handler()
async def send_video(message: types.Message):
    user_id = message.from_user.id
    if not await is_subscribed(user_id):
        await message.answer("⛔ Iltimos, avval kanalga obuna bo‘ling.", reply_markup=subscribe_btn)
        return
    code = message.text.strip()
    if code in video_data:
        await message.answer_video(video_data[code])
    else:
        await message.answer("❌ Bunday kod mavjud emas.")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)