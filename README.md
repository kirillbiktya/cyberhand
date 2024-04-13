# cyberhand

### Установка

Для начала - склонируйте репозиторий, создайте виртуальную среду и установите зависимости:
```commandline
git clone https://github.com/kirillbiktya/cyberhand
cd cyberhand
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Следующим шагом компилируем и запускаем сервер:
```commandline
gcc main.c
./a.out
```

И, наконец, запускаем клиента:
```commandline
python main.py
```