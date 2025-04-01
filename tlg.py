import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, ForceReply
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
import logging
import os
import sys

# Bot configuration
TOKEN = "7755049307:AAEq18jZdgqk12Sl06EF0Xz4fwJpTe4fKrU"
WELCOME_MESSAGE = "🎉 Xush kelibsiz! Bu psixologik test bot. Iltimos, ismingizni kiriting:"
COMPLETION_MESSAGE = "✅ Test yakunlandi! Javoblaringiz saqlandi."
TEACHER_PASSWORD = "secret123"  # Change this to your desired password

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Psychological questions
questions = [
    {
        "text": "Tasavvur qiling, sizning bir do’stingiz ustozingiz bilan tortishib qoldi. Siz bu vaziyatda qanday yo’l tutasiz?",
        "options": [
            "Do’stimga xato ish qilayotganini tushuntiraman.",
            "Oxiri nima bo’lishini kuzatib turaman.",
            "Javob berishim qiyin."
        ]
    },
    {
        "text": "Senga maktab yoqadimi yoki unchalik yoqmaydimi?",
        "options": [
            "Unchalik yoqmaydi.",
            "Yoqadi.",
            "Hecham yoqmaydi."
        ]
    },
    {
        "text": "Biror bir dars bo‘lmasligi senga yoqadimi?",
        "options": [
            "Yoqmaydi.",
            "Ba’zida yoqadi ba’zan esa yoq.",
            "Yoqadi."
        ]
    },
    {
        "text": "Ertalab uyg’onib doim xursandchilik bilan maktabga borasizmi yoki ko‘pincha uyda qolishni xohlaysanmi?",
        "options": [
            "Ko‘pincha uyda qolishni istayman.",
            "Har qanday vaziyatda ham maktabga borishni xohlayman.",
            "Ba’zida borishni ba’zan esa qolishni istayman."
        ]
    },
    {
        "text": "Yaqin do‘stingiz nimadandir xafa bo‘ldi. Siz nima qilgan bo‘lardingiz?",
        "options": [
            "Undan nimaga yig’layotganini so‘rardim.",
            "E’tibor bermasdim.",
            "Battar bo‘l degan bo‘lardim."
        ]
    },
    {
        "text": "Tasavvur qiling sinfdoshingiz bir o‘rtog’i bilan urushyabdi. Siz qanday ish tutardingiz?",
        "options": [
            "Borib sinfdoshimga yordam berardim.",
            "Orqadan turib kuzatib turardim.",
            "E’tibor bermaslikka harakat qilardim."
        ]
    },
    {
        "text": "Sinfda o‘rtoqlariz ko‘pmi?",
        "options": [
            "Kam.",
            "Ko‘p.",
            "Umuman yo‘q."
        ]
    },
    {
        "text": "Bir do‘stingiz juda urushqoq. U ustozingiz bilan ko‘p tortishadi. Siz bu vaziyatga qanday qaraysiz?",
        "options": [
            "Ustozni hurmat qilishini aytardim.",
            "Vaziyatni kuzatib turardim.",
            "Menga farqi yo‘q urushsa ham, urushmasa ham."
        ]
    },
    {
        "text": "Bir o‘rtog’ingiz sizning daftaringizga chizdi. Siz do‘stingiz bilan urush qilarmidingiz?",
        "options": [
            "Yoq urush qilmasdim.",
            "Men ham uni daftariga qaytarib chizardim.",
            "Ustozga aytib berardim."
        ]
    },
    {
        "text": "Yuqori sinf o‘quvchisi ukangizni uryabdi. Siz qanday yo‘l tutardingiz?",
        "options": [
            "Albatta borib o‘sha bolani urardim.",
            "Ustozga aytardim.",
            "Ukamni himoya qilardim."
        ]
    },
    {
        "text": "Senga sinfdoshlaringiz yoqadimi?",
        "options": [
            "Yoqmaydi.",
            "Yoqadi.",
            "Unchalik yoqmaydi."
        ]
    },
    {
        "text": "O’z vazifalaringizni bajarish muhimroqmi yoki huquqlaringizga rioya qilishni talab qilish muhimroqmi?",
        "options": [
            "O’z vazifalarini bajarish.",
            "O’z huquqlariga rioya qilishni talab qilish.",
            "Ikkalasi ham bir xil darajada muhimdir."
        ]
    },
    {
        "text": "Siz huquqlaringiz va majburiyatlaringiz haqida kimdan bilib olasiz?",
        "options": [
            "Ota-onadan.",
            "O’qituvchilardan.",
            "Do’stlardan."
        ]
    },
    {
        "text": "Oilada, maktabda, sizga nizolar salbiy oqibatlarga olib kelishi aytiladimi?",
        "options": [
            "Ko’pincha.",
            "Kamdan-kam hollarda.",
            "Umuman eslatmaydi."
        ]
    },
    {
        "text": "Sizning huquqlaringiz va majburiyatlaringizni eslatib o’tadigan qonunlarni bilasizmi?",
        "options": [
            "Ha, bilaman.",
            "Yo’q.",
            "Bilmayman."
        ]
    },
    {
        "text": "Uyda, oilada bola sifatida sizning huquqlaringiz hurmat qilinadimi?",
        "options": [
            "Ha.",
            "Yo’q.",
            "Javob berishim qiyin."
        ]
    },
    {
        "text": "Ota-onangiz va yaqinlaringiz bilan maroqli dam olishga bormoqchisiz, ammo sizning dars mashg’ulotlaringiz bor. Shunday vaziyatda siz qanday yo’l tutasiz?",
        "options": [
            "Darsga bormayman.",
            "Men uchun darsga borish muhim.",
            "Javob berish qiyin."
        ]
    },
    {
        "text": "Ota-onalar siz bilan bahslashishda agarda noto'g'ri ekanliklarini bilishsa tan olishadimi?",
        "options": [
            "Ha, har doim.",
            "Faqat ba’zan.",
            "Yo’q, hech qachon."
        ]
    },
    {
        "text": "Sizning sirlaringizni ochgan do’stingizga nisbatan munosabatingiz?",
        "options": [
            "Men uni yomon ko’raman.",
            "Borib sochini yulib, janjal qilib kelaman.",
            "Javob berish qiyin."
        ]
    },
    {
        "text": "Sizningcha, maktab o’quvchilari o’z vazifalarini bajaradimi?",
        "options": [
            "Har doim yoki deyarli har doim bajariladi.",
            "Hech qachon yoki deyarli hech qachon bajarilmaydi.",
            "Javob berish qiyin."
        ]
    },
    {
        "text": "Nima uchun maktab o’quvchilari o’z vazifalarini bajarmaydilar?",
        "options": [
            "Ular o'z vazifalarini bilishmaydi.",
            "Jazodan qo'rqmaydilar.",
            "Javob berish qiyin."
        ]
    },
    {
        "text": "Sizni do’stlaringiz  hurmat qilinadimi?",
        "options": [
            "Har doim.",
            "Hech qachon. ",
            "Javob berish qiyin."
        ]
    },
    {
        "text": "Maktabda ziddiyat yomon odat ekanligini aytadigan  biron bir faningiz bormi?",
        "options": [
            "Ha, bor-bu tarbiya fani.",
            "Maxsus mavzu yo'q-biz buni sinf soatlarida o'tkazamiz.",
            "Yo’q."
        ]
    },
    {
        "text": "Siz  ziddiyatli vaziyatlar to’g’risida ma'lumotlarni qayerdan olasiz?",
        "options": [
            "Darslarda.",
            "Internetdan.",
            "Ota-onadan ."
        ]
    },
    {
        "text": "Bizga boshqa odamlarning huquqlarini buzishga ruxsat beriladimi?",
        "options": [
            "Ha, albatta ruxsat berilgan. ",
            "Faqat kamdan-kam hollarda ruxsat etiladi.",
            "Mutlaqo ta’qiqlangan."
        ]
    },
    {
        "text": "Sizningcha, har bir bola oilada yashash va tarbiyalanish huquqiga egami?",
        "options": [
            "Yo’q, faqat ota-onasini sevadigan va hurmat qiladigan bolalar bu huquqqa ega.",
            "Ushbu huquq har bir bola uchun mavjud.",
            "Hech bir bola bunday huquqqa ega emas."
        ]
    },

]

# User data storage
user_data = {}  # {user_id: {"name": str, "answers": list, "current_question": int}}
all_results = {}  # {name: [answers]}


# Helper functions
def create_question_keyboard(options):
    builder = ReplyKeyboardBuilder()
    for option in options:
        builder.button(text=option)
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)


def format_all_results():
    option_letters = ['A', 'B', 'C']
    result = "📋 Barcha talabalar javoblari:\n\n"

    for name, answers in all_results.items():
        result += f"👤 {name}:\n"
        for i, answer in enumerate(answers, 1):
            question = questions[i - 1]
            option_index = question["options"].index(answer)
            result += f"{i}. {option_letters[option_index]}\n"
        result += "\n"

    return result if all_results else "Hozircha javoblar yo'q."


# Command handlers
@dp.message(Command("start"))
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    user_data[user_id] = {"name": None, "answers": [], "current_question": 0}
    await message.answer(WELCOME_MESSAGE)


@dp.message(Command("stats"))
async def stats_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_data or not user_data[user_id]["name"]:
        await message.answer("Avval ismingizni kiriting!")
        return

    completed = len(user_data[user_id]["answers"])
    total = len(questions)
    await message.answer(f"📊 Progress: {completed}/{total} savol javob berildi")


@dp.message(Command("teacher"))
async def teacher_handler(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔐 Natijalarni ko'rish", callback_data="view_results")]
    ])
    await message.answer("O'qituvchi rejimi: Parolni kiritish uchun tugmani bosing.", reply_markup=keyboard)


# Question handling
async def send_question(user_id):
    current = user_data[user_id]["current_question"]
    if current < len(questions):
        question = questions[current]
        keyboard = create_question_keyboard(question["options"])
        await bot.send_message(
            user_id,
            f"❓ {current + 1}/{len(questions)}: {question['text']}",
            reply_markup=keyboard
        )
    else:
        # Save results and show completion
        name = user_data[user_id]["name"]
        all_results[name] = user_data[user_id]["answers"]
        await bot.send_message(user_id, COMPLETION_MESSAGE, reply_markup=types.ReplyKeyboardRemove())


# Message handlers with priority
# Teacher password handler (highest priority)
@dp.message(lambda message: message.reply_to_message and "Parolni kiriting" in message.reply_to_message.text)
async def handle_teacher_password(message: types.Message):
    if message.text == TEACHER_PASSWORD:
        results_text = format_all_results()
        await message.answer(results_text)
    else:
        await message.answer("Noto'g'ri parol! Qayta urinib ko'ring.")
        await bot.send_message(message.chat.id, "Parolni kiriting:", reply_markup=ForceReply())
    await message.delete()  # Delete password message for security


# Regular message handler for name and answers
@dp.message()
async def handle_message(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_data:
        await message.answer("Iltimos, /start bilan boshlang!")
        return

    # Handle name input
    if user_data[user_id]["name"] is None:
        user_data[user_id]["name"] = message.text.strip()
        await message.answer(f"Salom, {user_data[user_id]['name']}! Testni boshlaymiz.")
        await send_question(user_id)
        return

    # Handle answers
    current = user_data[user_id]["current_question"]
    if current >= len(questions):
        await message.answer("Test allaqachon tugagan!")
        return

    question = questions[current]
    if message.text in question["options"]:
        user_data[user_id]["answers"].append(message.text)
        user_data[user_id]["current_question"] += 1
        await send_question(user_id)
    else:
        await message.answer("Iltimos, berilgan variantlardan birini tanlang!")


# Callback handlers
@dp.callback_query()
async def process_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    if callback.data == "view_results":
        await bot.send_message(user_id, "Parolni kiriting:", reply_markup=ForceReply())
        await callback.answer()


# Main function
async def main():
    try:
        logger.info("Bot ishga tushdi...")
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Xatolik yuz berdi: {e}")


if __name__ == "__main__":
    asyncio.run(main())
