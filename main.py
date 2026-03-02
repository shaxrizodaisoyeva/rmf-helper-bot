from keep_alive import keep_alive
import os
from telegram import (
    ReplyKeyboardMarkup, 
    Update, 
    KeyboardButton, 
    InlineKeyboardButton, 
    InlineKeyboardMarkup,
    ReplyKeyboardRemove
)
from telegram.ext import (
    Application, 
    CommandHandler, 
    MessageHandler, 
    filters, 
    ContextTypes, 
    CallbackQueryHandler
)

# --- CONFIGURATION ---
TOKEN = os.environ['TELEGRAM_TOKEN']
ADMIN_ID = -5134870846 
user_orders = {}
user_states = {} 

# --- DATA LISTS ---
leaflets_med_list = [
    "Акваципро-Д", "Ангиотрен 200мл", "Ангисем 100мл", "Броникс 5мл", "Доунарин 100мл", "Зотокам 1.125г",
    "Исофлокс №10", "Кардисем 100мл", "Ландиос 100мл", "Мексибел №10", "Миранол 50мл", "Неодексон 100мл",
    "Рангор 5мл", "Рогинолит 200мл", "Семпер 200мл", "Синаперазон С", "Софин 100мл", "Форкард 5мл",
    "Эвотрон 100мл", "Экситен 100мл", "Элоксилит 250мл", "Эпсол 50мл", "Эльфор 5мл", "Элгинарин 100мл"
]

cert_medicine_list = [
    "Акваципро-Д", "Адинтан 200мл", "Ангиотрен 200мл", "Ангисем 100мл", "Ангисем 250мл", 
    "Броникс 5мл", "Доунарин 100мл", "Зотокам 1.125г", "Исофлокс №10", "Кардисем 100мл", 
    "Ландиос 100мл", "Ликрузен №6", "Мексибел №10", "Миранол 50мл", "Неодексон 100мл", 
    "Рангор 5мл", "Рогинолит 100мл", "Рогинолит 200мл", "Семпер 200мл", "Элгинарин 100мл", 
    "Эльфор 5мл", "Эпсол 50мл", "Экситен 100мл", "Экситен 200мл"
]

qty_list = ["20", "30", "40", "50", "100"]
warehouse_list = ["Самарканд", "Ташкент"]

# --- KEYBOARDS ---
main_menu_keyboard = [
    ["Прайс-Листы", "Лифлеты"],
    ["Информация лекарствах", "Контакты"],
    ["Документы", "Отзывы и предложения"]
]

contacts_submenu = [
    ["Ассистент Регионального Менеджера", "Финансовый Аналитик"],
    ["Оператор", "Логистика Самарканд"],
    ["Логистика Ташкент", "Логистика Водий"],
    ["Зав. склад Самарканд", "Зав. склад Ташкент"],
    ["Зав. склад Водий", "Консультант по онлайн документам"],
    ["Бухгалтерия", "Больничные Договора"],
    ["Отдел Дебиторов"],
    ["Вернуться в главное меню"]
]

# --- CONTACTS DATA ---
contacts_data = {
    "Ассистент Регионального Менеджера": {"phone": "+998772715160", "first_name": "Бехзод"},
    "Финансовый Аналитик": {"phone": "+998772715160", "first_name": "Бехзод"},
    "Оператор": {"phone": "+998955683837", "first_name": "Бехруз"},
    "Логистика Самарканд": {"phone": "+998915571881", "first_name": "Бахром"},
    "Логистика Ташкент": {"phone": "+998933018885", "first_name": "Бобур"},
    "Логистика Водий": {"phone": "+998977253966", "first_name": "Шавкат"},
    "Зав. склад Самарканд": {"phone": "+998933472537", "first_name": "Дустмурод"},
    "Зав. склад Ташкент": {"phone": "+998990039320", "first_name": "Бобомурод"},
    "Зав. склад Водий": {"phone": "+998886650203", "first_name": "Аброр"},
    "Консультант по онлайн документам": {"phone": "+998908752752", "first_name": "Акобирхон"},
    "Бухгалтерия": {"phone": "+998998228852", "first_name": "Дилфуза"},
    "Больничные Договора": {"phone": "+998983018184", "first_name": "Наима"},
    "Отдел Дебиторов": {"phone": "+998936050009", "first_name": "Феруза"}
}

teams_by_region = {
    "Андижон": ["Андижон_Жонибек ака"],
    "Кукон": ["Кукон_Бахромжон ака", "Кукон_Баходирхон ака"],
    "Фаргона": ["Фаргона_Гулбахор опа", "Фаргона_Зафаржон ака", "Фаргона_Хасанхон ака","Фаргона_Умар ака Сух"],
    "Наманган": ["Наманган_Солихон ака", "Наманган_Равшан ака"],
    "Таш.Обл": ["Таш.Обл_Рустам ака", "Таш.Обл_Ноила опа"],
    "Сирдарьё": ["Сирдарё_Фотима опа"],
    "Самарканд": ["Самарканд_Хуршед ака", "Самарканд_Хуршед ака 2"],
    "Карши": ["Карши_Абдуахад ака", "Карши_Дилсўз опа", "Карши_Хусан ака"],
    "Шахрисабз": ["Шахрисабз_Хуршид ака"],
    "Сурхондарьё": ["Сурхондарьё_Анвар ака"],
    "Навоий": ["Навоий_Дилафруз опа", "Навоий_Гулшода опа", "Навоий_Анвар ака","Навоий_Хуршед ака"],
    "Бухоро": ["Бухоро_Нафосат опа"],
    "Хоразм": ["Хоразм_Улугбек ака", "Хоразм_Дилмурод ака"],
    "Нукус": ["Нукус_Мехрибон опа"]
}

# --- HELPERS ---
def build_indexed_grid(items, callback_prefix, cols=2):
    keyboard = []
    row = []
    for i, item in enumerate(items):
        row.append(InlineKeyboardButton(item, callback_data=f"{callback_prefix}:{i}"))
        if len(row) == cols:
            keyboard.append(row)
            row = []
    if row: keyboard.append(row)
    return InlineKeyboardMarkup(keyboard)

    # --- HANDLERS ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Turn the ID into a string so Python can compare it to the file text
    user_id = str(update.effective_user.id) 

    # --- SIMPLE COUNTER ---
    with open("users.txt", "a+") as f:
        f.seek(0)
        if user_id not in f.read():
            f.write(user_id + "\n")

        # --- UPDATED WELCOME MESSAGE ---
        welcome_text = (
            "<b>Добро пожаловать в Reflektiv Med Farm Bot!</b>\n\n"
            "Этот бот — ваш цифровой помощник. Здесь вы можете:\n"
            "💰 Получить актуальные прайс-листы\n"
            "💊 Найти и заказать лифлеты\n"
            "📄 Скачать сертификаты и реквизиты\n"
            "📞 Быстро связаться с логистикой и складом\n"
            "✍️ Оставить предложение или жалобу\n\n"
            "<b>Выберите нужный раздел👇</b>"
        )

        await update.message.reply_text(
            welcome_text, 
            parse_mode='HTML', 
            reply_markup=ReplyKeyboardMarkup(main_menu_keyboard, resize_keyboard=True)
        )

async def handle_contact_share(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in user_orders:
        data = user_orders[user_id]
        c = update.message.contact

        # This creates the vertical list using \n (new line)
        vertical_items = "\n".join(data.get('items', []))

        summary = (
            f"<b>{data.get('team')}</b>\n\n"
            f"Лифлеты:\n{vertical_items}\n\n" # Medicines now appear on new lines
            f"Количество: {data.get('amount')}\n"
            f"Склад: #{data.get('region')}\n\n"
            f"Заказчик:\n"
            f"{c.first_name}\n"
            f"+{c.phone_number}"
        )
        await context.bot.send_message(chat_id=ADMIN_ID, text=summary, parse_mode='HTML')
        await update.message.reply_text("Спасибо! Ваш заказ успешно отправлен.", reply_markup=ReplyKeyboardMarkup(main_menu_keyboard, resize_keyboard=True))
        del user_orders[user_id]

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id
    data_parts = query.data.split(":")
    action, val = data_parts[0], data_parts[1]

    if action == "order_team":
        all_teams = [t for sub in teams_by_region.values() for t in sub]
        team_name = all_teams[int(val)]
        user_orders[user_id] = {"team": team_name, "items": []}
        await query.edit_message_text(f"Команда: {team_name}\nВыберите препараты:", reply_markup=build_indexed_grid(leaflets_med_list, "order_med", cols=2))
    elif action == "order_med":
        name = leaflets_med_list[int(val)]
        if name not in user_orders[user_id]["items"]: user_orders[user_id]["items"].append(name)
        current = ", ".join(user_orders[user_id]["items"])
        kb = build_indexed_grid(leaflets_med_list, "order_med", cols=2).inline_keyboard
        keyboard = [list(row) for row in kb]
        keyboard.append([InlineKeyboardButton("✅ ПОДТВЕРДИТЬ", callback_data="confirm:done")])
        await query.edit_message_text(f"Выбрано: {current}\nВыберите еще или подтвердите:", reply_markup=InlineKeyboardMarkup(keyboard))
    elif action == "confirm":
        await query.edit_message_text("Выберите количество:", reply_markup=build_indexed_grid(qty_list, "qty", cols=3))
    elif action == "qty":
        user_orders[user_id]["amount"] = qty_list[int(val)]
        await query.edit_message_text("Выберите склад получения:", reply_markup=build_indexed_grid(warehouse_list, "reg", cols=2))
    elif action == "reg":
        user_orders[user_id]["region"] = warehouse_list[int(val)]
        await query.message.reply_text("Завершите заказ, отправив контакт 👇", reply_markup=ReplyKeyboardMarkup([[KeyboardButton("Отправить контакт 📞", request_contact=True)]], resize_keyboard=True, one_time_keyboard=True))
    elif action == "view":
        name = leaflets_med_list[int(val)]
        try: await query.message.reply_document(document=open(f"{name}.pdf", "rb"), caption=f"📄 {name}")
        except: await query.message.reply_text(f"❌ Файл {name}.pdf не найден.")
    elif action == "cert":
        name = cert_medicine_list[int(val)]
        try: await query.message.reply_document(document=open(f"{name}.pdf", "rb"), caption=f"📜 {name}")
        except: await query.message.reply_text(f"❌ Файл {name}.pdf не найден.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.effective_user.id

    # 1. HANDLE RETURN FIRST (Priority)
    if text == "Вернуться в главное меню":
        user_states[user_id] = None 
        await update.message.reply_text(
            "<b>Главное меню</b>", 
            parse_mode='HTML', 
            reply_markup=ReplyKeyboardMarkup(main_menu_keyboard, resize_keyboard=True)
        )
        return # Important: Stop here so it doesn't process feedback logic

    # 2. FEEDBACK LOGIC
    if user_states.get(user_id) == "waiting_for_feedback":
        feedback = f"💡 <b>НОВЫЙ ОТЗЫВ</b>\n👤 От: {update.effective_user.first_name}\n📝: {text}"
        await context.bot.send_message(chat_id=ADMIN_ID, text=feedback, parse_mode='HTML')
        user_states[user_id] = None
        await update.message.reply_text("Спасибо за отзыв!", reply_markup=ReplyKeyboardMarkup(main_menu_keyboard, resize_keyboard=True))
        return

    # 3. CONTACTS
    if text in contacts_data:
        person = contacts_data[text]
        await update.message.reply_contact(phone_number=person['phone'], first_name=person['first_name'])
        return

    if text == "Контакты":
        try: await update.message.reply_photo(photo=open("contacts_image.jpg", "rb"), caption="Выберите нужный контакт!")
        except: await update.message.reply_text("Выберите нужный контакт!")
        await update.message.reply_text("👇", reply_markup=ReplyKeyboardMarkup(contacts_submenu, resize_keyboard=True))

    # 4. PRICE LISTS
    elif text == "Прайс-Листы":
        await update.message.reply_text("Выберите раздел👇", reply_markup=ReplyKeyboardMarkup([["Общий Прайс-лист RMF"], ["Прайс по командам"], ["Вернуться в главное меню"]], resize_keyboard=True))
    elif text == "Общий Прайс-лист RMF":
        try: await update.message.reply_document(document=open('Общий Прайс Лист RMF.xlsx', 'rb'), caption="📂 Общий Прайс-лист")
        except: await update.message.reply_text("❌ Файл 'Общий Прайс Лист RMF.xlsx' не найден.")
    elif text == "Прайс по командам":
        await update.message.reply_text("Выберите регион👇", reply_markup=ReplyKeyboardMarkup([["Андижон", "Кукон", "Фаргона"], ["Наманган", "Таш.Обл", "Сирдарьё"], ["Самарканд", "Карши", "Шахрисабз"], ["Сурхондарьё", "Навоий", "Бухоро"], ["Хоразм", "Нукус"], ["Вернуться в главное меню"]], resize_keyboard=True))
    elif text in teams_by_region:
        teams = [[t] for t in teams_by_region[text]] + [["Вернуться в главное меню"]]
        await update.message.reply_text("Выберите команду👇", reply_markup=ReplyKeyboardMarkup(teams, resize_keyboard=True))

    # 5. DOCUMENTS
    elif text == "Документы":
        await update.message.reply_text("Выберите нужный раздел👇", reply_markup=ReplyKeyboardMarkup([["Папка документов", "Реквизиты"], ["Вернуться в главное меню"]], resize_keyboard=True))
    elif text == "Папка документов":
        try: await update.message.reply_document(document=open("Папка документов.docx", "rb"), caption="📄 Папка документов")
        except: await update.message.reply_text("❌ Файл 'Папка документов.docx' не найден.")
    elif text == "Реквизиты":
        rek = (
            "<b>OOO «REFLECTIVE MED PHARM»</b>\n"
            "Адрес: 111801, РУз, Ташкентская обл, Зангиотинский р-н, Катта Чинор МФЙ, 1А.\n"
            "Р/с 20208000905364813002 \n" 
            "в «УЗСАНОАТКУРИЛИШБАНКИ»\n"
            "МФО 00440 \n"
            "ИНН 308321773 \n"
            "ОКЭД 46460"
        )
        await update.message.reply_text(rek, parse_mode="HTML")

    # 6. MEDICINE INFO
    elif text == "Информация лекарствах":
        await update.message.reply_text("Выберите раздел👇", reply_markup=ReplyKeyboardMarkup([["Сертификаты"], ["Вернуться в главное меню"]], resize_keyboard=True))
    elif text == "Сертификаты":
        await update.message.reply_text("Выберите препарат:", reply_markup=build_indexed_grid(cert_medicine_list, "cert", cols=2))

    # 7. LEAFLETS
    elif text == "Лифлеты":
        await update.message.reply_text("Выберите раздел👇", reply_markup=ReplyKeyboardMarkup([["Посмотреть Лифлеты"], ["Заказать лифлеты"], ["Вернуться в главное меню"]], resize_keyboard=True))
    elif text == "Посмотреть Лифлеты":
        await update.message.reply_text("Выберите препарат:", reply_markup=build_indexed_grid(leaflets_med_list, "view", cols=2))
    elif text == "Заказать лифлеты":
        all_teams = [t for sub in teams_by_region.values() for t in sub]
        await update.message.reply_text("Выберите вашу команду:", reply_markup=build_indexed_grid(all_teams, "order_team", cols=1))

    # 8. FEEDBACK TRIGGER
    elif text == "Отзывы и предложения":
        user_states[user_id] = "waiting_for_feedback"
        await update.message.reply_text("Напишите ваш отзыв или предложение:", reply_markup=ReplyKeyboardRemove())

    # 9. TEAM XLSX DELIVERY
    else:
        for t_list in teams_by_region.values():
            if text in t_list:
                try: await update.message.reply_document(document=open(f"{text}.xlsx", 'rb'), caption=f"📊 Прайс: {text}")
                except: await update.message.reply_text(f"❌ Файл {text}.xlsx не найден.")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_handler(MessageHandler(filters.CONTACT, handle_contact_share))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot is 100% active and monitoring sections...")
    app.run_polling()

if __name__ == "__main__":
    keep_alive()  # <--- Add this line here
    main()