import time
import telebot
from google import genai
from google.genai import types

TELEGRAM_BOT_TOKEN = "9198614146:AAEI0UXRzEK4MKZlyuuRSXlCKFTU6FkWxaY"
GEMINI_API_KEY = "AQ.Ab8RN6KwZ5FV_DK5tiA7a6m9kH6ZgekmSruTfPXvwu-Vqx4pfg"

client = genai.Client(api_key=GEMINI_API_KEY)
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

mening_qoidalarim = """
Sen professional o'zbek yozuvchisisansan. 
Sening yagona vazifang — foydalanuvchi yuborgan g'oya asosida badiiy, jonli va qiziqarli hikoya yaratish.
Hech qanday maslahat berma, kirish yoki xulosa so'zlari yozma, to'g'ridan-to'g'ri hikoyani boshla.
Personajlarning jinsiga va xarakteriga qat'iy rioya qil.
"""

def hikoya_generatsiya(goya):
    for urinish in range(5):
        try:
            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=goya,
                config=types.GenerateContentConfig(
                    system_instruction=mening_qoidalarim,
                    temperature=0.8,
                )
            )
            return response.text
        except Exception as e:
            if "503" in str(e) and urinish < 4:
                time.sleep(3)
                continue
            else:
                raise e

@bot.message_handler(func=lambda message: True)
def hikoya_yoz(message):
    bot.reply_to(message, "⏳ Hikoya yozilyapti, biroz kuting...")
    try:
        matn = hikoya_generatsiya(message.text)
        if len(matn) > 4000:
            for i in range(0, len(matn), 4000):
                bot.send_message(message.chat.id, matn[i:i+4000])
        else:
            bot.reply_to(message, matn)
    except Exception as e:
        bot.reply_to(message, f"Xatolik yuz berdi: {e}")

bot.infinity_polling()
