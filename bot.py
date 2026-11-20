import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = "حط_التوكن_الجديد_هنا"
ADMIN_ID = 123456789

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("اهلا بيك في منصة عبدالرحمن السيد 👋\nدوس /code عشان يجيلك كود التأكيد")

async def code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    otp = random.randint(100000, 999999)
    context.user_data['otp'] = otp
    await update.message.reply_text(f"كود التأكيد بتاعك هو: {otp}\nاكتبه هنا عشان نأكده ✅")

async def handle_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    user = update.effective_user
    if 'otp' in context.user_data and text == str(context.user_data['otp']):
        await update.message.reply_text("✅ الكود صح، تم التأكيد بنجاح")
        del context.user_data['otp']
        return
    await update.message.reply_text("وصلتني رسالتك ✅ هرد عليك في اقرب وقت")
    try:
        await context.bot.send_message(chat_id=ADMIN_ID, text=f"📩 رسالة من @{user.username}\nالاي دي: {user.id}\nالرسالة: {text}")
    except:
        pass

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    if len(context.args) < 2:
        await update.message.reply_text("اكتب: /reply اي_دي_الشخص الرسالة")
        return
    await context.bot.send_message(chat_id=int(context.args[0]), text="رد من المنصة: " + " ".join(context.args[1:]))
    await update.message.reply_text("تم ارسال الرد ✅")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("code", code))
app.add_handler(CommandHandler("reply", reply))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_msg))
print("البوت اشتغل...")
app.run_polling()
