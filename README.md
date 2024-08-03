# AiHelper
Голосовой помощник в системе. Нейросеть, которая работает с помощью голоса.

> [!WARNING]  
> Приложение тестировалось только на Windows 11 23H2 (22631.3880) системе. По идее должно работать на всех Windows, Linux, MacOS: использовались кроссплатформенные функции.

<details>
<summary>Триггер команды</summary>

Для вопроса:
* Нейро [ваш вопрос]
* Вопрос [ваш вопрос]
* Окей [ваш вопрос]

Для выхода:
* Стоп
* Выход
* Выключить
* Остановка

</details>


<details>
<summary>Настройка, установка и запуск</summary>

Настройка:
```bash
cp .env.example .env
nano .env # или любой удобный вам редактор

Вместо GIGACHAT_AUTH_CREDENTIALS укажите авторизационные данные, полученные [здесь](https://developers.sber.ru/studio/workspaces/my-space/get/gigachat-api)
```

Установка:
```bash
pip install -r requirements.txt
# или
pip3 install -r requirements.txt
```

Запуск:
```bash
python main.py
# или
python3 main.py
```

Сборка в исполняемый файл:
```bash
pip install pyinstaller
# или
pip3 install pyinstaller

pyinstaller --onefile main.py
```

</details>
