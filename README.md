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

### Запуск

Компилируем и запускаем сервер:
```commandline
gcc main.c
./a.out
```

> Либо python-вариант
> `python udp_server.py`

Запуск программы:
```commandline
python main.py
```
> [!NOTE]
> Программа может быть запущена с другими параметрами, подробнее - `python main.py -h`.

Вывод программы содержит координаты только последнего сочленения (кисти) манипулятора:
```
                координата      координата      координата      поворот вокруг  поворот вокруг  поворот вокруг
номер пакета    x (м)           y (м)           z (м)           оси x (град)    оси y (град)    оси z (град)
timestamp: 0    x: -0.6856      y: 0.9401       z: 1.2636       ax: 3.5836      ay -0.3937      az 49.9638
timestamp: 1    x: -0.0000      y: 1.3541       z: 1.2786       ax: 3.1416      ay 0.0000       az -180.0000       
timestamp: 2    x: 1.1279       y: 0.5154       z: 1.1503       ax: -0.7857     ay 1.3601       az 60.0280
timestamp: 3    x: -1.3980      y: -0.0555      z: 1.2013       ax: 3.1416      ay 0.0000       az -0.0000
timestamp: 4    x: 1.1108       y: 0.2159       z: 1.2032       ax: -0.9567     ay 1.3637       az -113.0080
```

Но можно получить позицию любого сочленения с помощью методов `Manipulator.get_decart_by_joint_number(joint_number)` 
и `Manipulator.get_euler_by_joint_number(joint_number)`
