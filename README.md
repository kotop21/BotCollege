# 📚 Telegram-бот для завантаження розкладів 📅

## 🛠 Як працює бот:

1. **Запуск бота**:
   - Користувач надсилає команду `/start`.
   - Бот відповідає привітанням і відображає меню з кнопками для вибору курсу (1–4).

2. **Вибір курсу**:
   - Користувач натискає на одну з кнопок, яка відповідає курсу:
     - `1 курс 👶🏻`
     - `2 курс 👦🏻`
     - `3 курс 👨🏻`
     - `4 курс 👴🏻`

3. **Пошук файлу розкладу**:
   - Бот формує запит на сервер за посиланням:  
     `https://ztk.org.ua/files/{номер_курсу}-{дата}.pdf`.
   - Перевіряє доступність файлу для сьогоднішньої дати та останніх 7 днів.

4. **Обробка результату**:
   - Якщо файл знайдено:
     - Якщо дата відповідає сьогоднішній, бот надсилає повідомлення:  
       `🎉 Завантаження розкладу для {курс} курсу завершено!`
     - Якщо сьогоднішній файл відсутній, бот надсилає:  
       `⚠️ Сьогоднішній розклад відсутній. Надсилаю розклад за {дата}.`
     - Бот відправляє файл PDF у чат.
   - Якщо файл не знайдено за останні 7 днів:  
     `⚠️ Ой! Не вдалося знайти розклад за останні 7 днів. Спробуйте ще раз пізніше.`

5. **Помилки**:
   - Якщо сталася помилка, бот повідомляє:  
     `⚠️ Виникла проблема при обробці запиту. Спробуйте пізніше.`

---

## 💻 Особливості:

- **Логування**: Бот фіксує всі події в логах для моніторингу.
- **Інтерактивність**: Зручні кнопки для швидкого вибору курсу.
- **Гнучкість**: Пошук розкладу за кілька днів, якщо файл недоступний для поточної дати.
- **Безпечність**: Файли надсилаються без збереження на сервері.

👾 *Автор бота: xxds🎀❤️‍🔥*