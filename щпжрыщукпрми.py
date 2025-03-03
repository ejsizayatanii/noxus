import requests 
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram import Update
import datetime

# Токен вашего бота
TOKEN = "7939322115:AAG8aeDTDyRBydVxS9hWg-o2SZ-v8RmP9OY"
# Ваш API ключ от OpenWeatherMap
WEATHER_API_KEY = "045b403e9b66344be43e8b555c472b2a"  # замените на свой API ключ

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я бот programming camp.")

# Обработчик команды /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Доступные команды:\n/start\n/help\n/time\n/weather")

# Обработчик текстовых сообщений
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(update.message.text)

# Обработчик команды /time
async def time_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    await update.message.reply_text(f"Текущее время: {current_time}")

# Обработчик команды /weather
async def weather_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lat = 51.169392 # Город для получения погоды
    lon = 71.449074
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if data["cod"] == 200:
            weather_description = data["weather"][0]["description"]
            temperature = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]

            weather_info = (
                f"Погода в Астане:\n"
                f"Описание: {weather_description}\n"
                f"Температура: {temperature}°C\n"
                f"Влажность: {humidity}%\n"
                f"Скорость ветра: {wind_speed} м/с"
            )
            await update.message.reply_text(weather_info)
        else:
            await update.message.reply_text("Не удалось получить данные о погоде.")
    except Exception as e:
        await update.message.reply_text(f"Произошла ошибка: {e}")

def main():
    # Создаем приложение
    app = Application.builder().token(TOKEN).build()

    # Добавляем обработчики
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("time", time_command))
    app.add_handler(CommandHandler("weather", weather_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    print("Бот запущен...")
    
    # Запускаем бота
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
