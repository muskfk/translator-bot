from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from deep_translator import GoogleTranslator
from langdetect import detect

API_TOKEN = '8001362405:AAFaKc8RK7XcoX8y4LaMQNnsfcEdppvvA80'  # Thay bằng token thực tế

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Danh sách 10 ngôn ngữ phổ biến
popular_languages = [
    ("🇺🇸 English", "en"),
    ("🇨🇳 Chinese", "zh-CN"),
    ("🇯🇵 Japanese", "ja"),
    ("🇰🇷 Korean", "ko"),
    ("🇫🇷 French", "fr"),
    ("🇩🇪 German", "de"),
    ("🇪🇸 Spanish", "es"),
    ("🇮🇹 Italian", "it"),
    ("🇵🇹 Portuguese", "pt"),
    ("🇷🇺 Russian", "ru"),
]

@dp.message_handler()
async def handle_message(message: types.Message):
    text = message.text
    src_lang = detect(text)

    # Nếu không phải tiếng Việt, tự động dịch sang tiếng Việt
    if src_lang != 'vi':
        translated = GoogleTranslator(source='auto', target='vi').translate(text)
        await message.reply(f"📘 Dịch sang Tiếng Việt:\n<b>{translated}</b>", parse_mode="HTML")
    else:
        # Nếu là tiếng Việt, hiển thị các nút dịch sang 10 ngôn ngữ khác
        buttons = [
            [InlineKeyboardButton(text=name, callback_data=f"{code}|{text}")]
            for name, code in popular_languages
        ]
        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
        await message.reply("🌍 Chọn ngôn ngữ để dịch:", reply_markup=keyboard)

@dp.callback_query_handler(lambda c: "|" in c.data)
async def handle_translation_callback(callback_query: types.CallbackQuery):
    code, original_text = callback_query.data.split("|", 1)
    translated = GoogleTranslator(source='vi', target=code).translate(original_text)
    await callback_query.message.reply(f"📘 Dịch sang {code.upper()}:\n<b>{translated}</b>", parse_mode="HTML")
    await callback_query.answer()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
