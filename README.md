# Pavlov_server_statistic
Супер сырой код

### Файлы (папки) проекта:
* **Logs** - Логи
* **templates** - Шаблоны WEB страниц для Flask
* **парсинг лога для сайта.jpynb** - Ноутбук с тестами
* **Preview.PNG** - Пример отображения WEB страницы
* **site_1.py** - Серверная часть сайта на Flask

### Что реализовано:
При обновлении страницы Flask:
* парсит конкретный файл с логами
* находит все jason с результатами и статистикой матчей,
* разбирает данные на 2 Dataframe (имитация SQL)
* собирает из 2 Dataframe нужный Json (имитация SQL)
* отправляет данные на сайт, используя шаблон

### Что необходимо доделать, изменить
* Вынести загрузчик логов в отдельный процесс и загружать уже в SQL
* Переделать работу Flask на SQL
* Добавить оформление
