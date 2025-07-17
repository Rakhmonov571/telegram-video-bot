from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import logging

API_TOKEN = '7461127833:AAEscfu7JCsNLEsFTo9mEeDW-UfS9viDoH0'
CHANNEL_USERNAME = '@oliy_stavka_betvinner_1xbet'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

check_button = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton("✅ Obuna bo‘ldim", callback_data="check_subs")
)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    member = await bot.get_chat_member(CHANNEL_USERNAME, user_id)
    if member.status not in ['member', 'creator', 'administrator']:
        await message.answer("❗️Iltimos, quyidagi kanalga obuna bo‘ling:", reply_markup=check_button)
    else:
        await message.answer("🎉 Xush kelibsiz! Kod kiriting:")

@dp.callback_query_handler(lambda c: c.data == 'check_subs')
async def check_subscription(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    member = await bot.get_chat_member(CHANNEL_USERNAME, user_id)
    if member.status in ['member', 'creator', 'administrator']:
        await bot.send_message(user_id, "✅ Obuna tasdiqlandi. Kod kiriting:")
    else:
        await bot.send_message(user_id, "❗️Hali ham obuna bo‘lmagansiz.", reply_markup=check_button)

@dp.message_handler()
async def handle_code(message: types.Message):
    code = message.text.strip()
    video_dict = {
        "1234": "BAACAgQAAxkBAAIBOWZq7ZsU7eEvQnJKoAmwl9fCQ5CD_AAC9x8AAl4oUVEovSQUk1np6zQE",
        "5678": "BAACAgQAAxkBAAIBPmZq7d2MZXYMf8YuzV3YxgN8aW9jAAKAAQACtY6NUd4eey6WVUakNQQ"
    }
    if code in video_dict:
        await message.answer_video(video_dict[code])
    else:
        await message.answer("❌ Noto‘g‘ri kod!")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
