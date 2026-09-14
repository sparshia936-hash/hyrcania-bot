import telebot
from telebot import types
import random
from flask import Flask
from threading import Thread

# ==============================================================================
#                 سند ساختار و منطق جامع بازی بزرگ هیرکانیا (HYRCANIA)
# ==============================================================================

# ساخت یک سرور وب الکی برای دور زدن و راضی نگه داشتن رندر
app = Flask('')

@app.route('/')
def home():
    return "Hyrcania Bot is Running Live!"

def run_web_server():
    app.run(host='0.0.0.0', port=8080)

BOT_TOKEN = "8871506098:AAFi6PFTH1gUpInr0N7Br7OY3mTlv0OXbBs"
bot = telebot.TeleBot(BOT_TOKEN)

users_db = {}
VIP_CODES = ["VIP_CODE_A1B2", "VIP_CODE_C3D4", "VIP_CODE_E5F6", "VIP_CODE_G7H8", "VIP_CODE_I9J0"]
OWNER_CODE = "HYRCANIA_ETERNAL_OWNER_2026"

CLASSES_INFO = {
    "healer": {"name": "🩺 درمانگر", "hp": 140, "dmg": 18, "def": 0, "mp": 300, "speed": 12, "luck": 18, "gold": 75, "m_name": "سِینا", "f_name": "پَری", "desc_m": "سینا با الهام از حکیم بزرگ، ابوعلی سینا، دانای اسرار و طبیب نامدار هیرکانیا است.", "desc_f": "پَری با الهام از سکینه پری، نخستین پزشک جراح زن ایران، شفادهنده‌ای بی‌باک در مرزها است."},
    "mage": {"name": "🔮 جادوگر عناصر", "hp": 90, "dmg": 36, "def": 0, "mp": 240, "speed": 15, "luck": 10, "gold": 40, "m_name": "آتَر", "f_name": "وازیسْت", "desc_m": "آتَر جادوگر ارشد کائنات و نگهبان آتش زنده در مرزهای هیرکانیا است.", "desc_f": "وازیسْت ساحره‌ای مقتدر و احضارکننده‌ی آتش صاعقه از دل ابرهای باستانی است."},
    "necro": {"name": "💀 سایه‌افسون", "hp": 110, "dmg": 24, "def": 0, "mp": 220, "speed": 11, "luck": 12, "gold": 30, "m_name": "رِیوَند", "f_name": "ریما", "desc_m": "رِیوَند جادوگر مطرود کائنات و استاد جادوی سیاه و ارتش سایه‌ها است.", "desc_f": "ریما افسونگر تاریکی و ملکه سایه‌های سرگردان در نقاط مخوف هیرکانیا است."},
    "paladin": {"name": "🛡️ دادخواه", "hp": 130, "dmg": 22, "def": 2, "mp": 200, "speed": 10, "luck": 15, "gold": 40, "m_name": "هِیراد", "f_name": "دِلسا", "desc_m": "هِیراد جنگجوی زره‌پوش، مدافع نور و شوالیه پاک‌سرشت نیایشگاه کهن است.", "desc_f": "دِلسا بانوی شوالیه و نگهبان پاک‌سرشت یک نیایشگاه کهن و مقدس است."},
    "berserker": {"name": "🪓 پیلتن", "hp": 100, "dmg": 32, "def": 4, "mp": 180, "speed": 8, "luck": 8, "gold": 30, "m_name": "رُسْتَم", "f_name": "گُردیه", "desc_m": "رُسْتَم جنگجویی تنومند، پیلتن و بی‌باک است که با تبر بزرگ خود دل به دریا می‌زند.", "desc_f": "گُردیه بانوی پهلوان از تبار جنگجویان کهن با خشم طوفانی و تبر تیز است."},
    "ronin": {"name": "⚔️ تک‌رو", "hp": 115, "dmg": 25, "def": 1, "mp": 190, "speed": 18, "luck": 14, "gold": 35, "m_name": "سُهْراب", "f_name": "سایه", "desc_m": "سُهْراب شمشیرزنی ماهر در مهدهای تاریک است که به دنبال انتقام است.", "desc_f": "سایه بانویی مبارز و منزوی است که در میدان نبرد مثل شبح حرکت می‌کند."},
    "assassin": {"name": "🗡️ آدم‌کش", "hp": 95, "dmg": 34, "def": 0, "mp": 175, "speed": 25, "luck": 12, "gold": 60, "m_name": "شاهین", "f_name": "غَزال", "desc_m": "شاهین تیزدست‌ترین قاتل مه است که پیش از دیدن، جان از بدن می‌درد.", "desc_f": "غَزال قاتلی فرز است که مثل شبح حرکت کرده و با سرعت باد جابه‌جا می‌شود."},
    "beast": {"name": "🐺 گرگ‌زاده", "hp": 120, "dmg": 22, "def": 1, "mp": 185, "speed": 16, "luck": 11, "gold": 35, "m_name": "هیرْکان", "f_name": "تارا", "desc_m": "هیرْکان بزرگ‌شده در آغوش گرگ‌هاست که خوی گرگینه و انتقام‌جو دارد.", "desc_f": "تارا بانویی است که با قدرت یک گرگینه در خونش، به همراه گله خود می‌جنگد."},
    "vip": {"name": "👑 امپراتور / آرتمیس (VIP) 💎", "hp": 500, "dmg": 50, "def": 10, "mp": 500, "speed": 22, "luck": 15, "gold": 250, "m_name": "اِمپَراتور", "f_name": "آرْتِمیس", "desc_m": "طبقه شاهانه و حاکم قلمرو با دقت بالاتر و شانس لوت دوبرابر.", "desc_f": "بانوی اول قلمرو و آرتمیس بزرگ، شکارچی افسانه‌ای با لوت دوبرابر."}
}

MARKET_ITEMS = {
    "1": {"name": "چماقِ جنگلی [رتبه E]", "price": 45, "dmg": 15, "def": 0, "hp": 0, "speed": 0, "durability": 50, "slot": "weapon", "tier": "E", "desc": "از تنه درختان خشک هیرکانیا؛ ساده اما خردکننده."},
    "2": {"name": "سپرِ ترکه‌ای [رتبه E]", "price": 30, "def": 2, "dmg": 0, "hp": 0, "speed": 0, "durability": 50, "slot": "shield", "tier": "E", "desc": "بافته شده از ترکه‌های درخت انار برای دفع ضربات اولیه."},
    "3": {"name": "قبایِ نخی [رتبه E]", "price": 25, "hp": 15, "def": 1, "dmg": 0, "speed": 0, "durability": 50, "slot": "armor", "tier": "E", "desc": "پوششی سبک و ارزان‌قیمت بدون لایه‌های سنگین."},
    "4": {"name": "تبرِ برنزی [رتبه D]", "price": 120, "dmg": 30, "def": 0, "hp": 0, "speed": 0, "durability": 80, "slot": "weapon", "tier": "D", "desc": "تسلیحات برنزی مستحکم برای مبارزان نوپا."},
    "5": {"name": "جوشنِ چرمی [رتبه D]", "price": 60, "hp": 35, "def": 3, "dmg": 0, "speed": 0, "durability": 80, "slot": "armor", "tier": "D", "desc": "زره ساخته شده از پوست دباغی شده شیاطین."},
    "6": {"name": "کمانِ آرش [رتبه C]", "price": 350, "dmg": 55, "def": 0, "hp": 0, "speed": 0, "durability": 120, "slot": "weapon", "tier": "C", "desc": "کمانی مرغوب با زه کشیده و برد بالا."},
    "7": {"name": "فرجامِ جهان [رتبه SSS]", "price": 55000, "dmg": 350, "def": 0, "hp": 0, "speed": 0, "durability": 800, "slot": "weapon", "tier": "SSS", "desc": "⚡ قابلیت مخصوص [شکاف زمان]: کاهش ۱۰ واحد از سرعت مدافع در محاسبات."},
    "8": {"name": "پوششِ کیهانی [رتبه SSS]", "price": 45000, "hp": 750, "def": 60, "dmg": 0, "speed": 0, "durability": 800, "slot": "armor", "tier": "SSS", "desc": "🩸 قابلیت مخصوص [پناه آخر]: دوبرابر شدن دفاع زره تن زیر ۲۰٪ خون."}
}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    if user_id in users_db:
        main_menu(message)
        return
    markup = types.InlineKeyboardMarkup(row_width=2)
    buttons = [types.InlineKeyboardButton(info["name"], callback_data=f"sel_{k}") for k, info in CLASSES_INFO.items() if k != "vip"]
    buttons.append(types.InlineKeyboardButton("👑 امپراتور / آرتمیس (VIP) 💎", callback_data="sel_vip"))
    markup.add(*buttons)
    bot.send_message(message.chat.id, "⚔️ **به جهان حماسی بازی بزرگ هیرکانیا خوش آمدید!**\n\nکلاس قهرمان خود را انتخاب کنید:", reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data.startswith("sel_"))
def select_class(call):
    class_key = call.data.split("_")[1]
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(f"👨 مرد ({CLASSES_INFO[class_key]['m_name']})", callback_data=f"gen_{class_key}_m"),
        types.InlineKeyboardButton(f"👩 زن ({CLASSES_INFO[class_key]['f_name']})", callback_data=f"gen_{class_key}_f")
    )
    markup.add(types.InlineKeyboardButton("🔙 بازگشت", callback_data="back_classes"))
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="جنسیت قهرمان خود را انتخاب کنید:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "back_classes")
def back_classes(call):
    markup = types.InlineKeyboardMarkup(row_width=2)
    buttons = [types.InlineKeyboardButton(info["name"], callback_data=f"sel_{k}") for k, info in CLASSES_INFO.items() if k != "vip"]
    buttons.append(types.InlineKeyboardButton("👑 امپراتور / آرتمیس (VIP) 💎", callback_data="sel_vip"))
    markup.add(*buttons)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="کلاس قهرمان خود را انتخاب کنید:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("gen_"))
def select_gender(call):
    _, class_key, gender = call.data.split("_")
    info = CLASSES_INFO[class_key]
    name = info["m_name"] if gender == "m" else info["f_name"]
    desc = info["desc_m"] if gender == "m" else info["desc_f"]
    
    text = f"📜 **تاریخچه حماسی قهرمان:**\n{desc}\n\n📊 **آمار سطح ۱:**\n" \
           f"❤️ جون: {info['hp']} | ⚔️ دمیج: {info['dmg']} | 🛡️ دفاع: {info['def']}\n" \
           f"🔮 مانا: {info['mp']} | ⚡ سرعت: {info['speed']}\n\nآیا از انتخاب خود مطمئنید؟"
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("✅ بله، مطمئنم", callback_data=f"cfrm_{class_key}_{gender}"))
    markup.add(types.InlineKeyboardButton("🔙 بازگشت", callback_data="back_classes"))
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data.startswith("cfrm_"))
def confirm_hero(call):
    user_id = call.from_user.id
    _, class_key, gender = call.data.split("_")
    
    if class_key == "vip":
        msg = bot.send_message(call.message.chat.id, "🔑 لطفاً کد فعال‌سازی VIP خود را ارسال کنید:")
        bot.register_next_step_handler(msg, verify_vip, gender)
        return

    init_hero(user_id, class_key, gender)
    bot.send_message(call.message.chat.id, f"🎉 قهرمان شما **{users_db[user_id]['name']}** متولد شد!")
    show_main_menu_msg(call.message.chat.id)

def init_hero(user_id, class_key, gender):
    info = CLASSES_INFO[class_key]
    users_db[user_id] = {
        "name": info["m_name"] if gender == "m" else info["f_name"], "tier": class_key, "gender": gender,
        "level": 1, "xp": 0, "gold": info["gold"], "fatigue": 0, "stat_points": 0, "skill_points": 3,
        "max_hp": info["hp"], "hp": info["hp"], "dmg": info["dmg"], "base_def": info["def"], "max_mp": info["mp"], "mp": info["mp"], "speed": info["speed"], "luck": info["luck"],
        "weapon": None, "shield": None, "armor": None, "dur_w": 0, "dur_s": 0, "dur_a": 0,
        "ability_1_lvl": 1, "ability_2_lvl": 1
    }

def verify_vip(message, gender):
    user_id = message.from_user.id
    code = message.text.strip()
    if code in VIP_CODES:
        VIP_CODES.remove(code)
        init_hero(user_id, "vip", gender)
        bot.send_message(message.chat.id, "👑 حساب VIP با موفقیت تایید شد! خوش آمدید امپراتور.")
        show_main_menu_msg(message.chat.id)
    else:
        bot.send_message(message.chat.id, "❌ کد نامعتبر است. مجدداً /start را بزنید.")

