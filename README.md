# Student Registration App (Flask + SQLite)

## Как запустить
```bash
cd student_reg_app
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
python app.py
```

Открой: http://127.0.0.1:5000/

## Структура
```
student_reg_app/
│  app.py
│  requirements.txt
│
├─templates/
│      Reg.html
│      success.html
│      students.html
│      error.html
└─static/
       Reg.css
       Reg.js
       alert_5610989.png
```

## Заметки
- База создастся автоматически: `students.db`.
- От спама: простая защита — не чаще 1 запроса в 30 сек с одного IP.
- На Windows уведомления через win10toast. Если не установлено — приложение всё равно работает.
