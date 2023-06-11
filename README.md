## Краткое описание проекта
Проект предсатавляет себой базу данных центра телемаркетинга коммерческого банка с которой по средством API ODBC взаимодействуют веб-приложение и desktop клиент.
Для защиты базы данных применено прозрачное шифрование, которое обеспечивает целостность фалов базы на устройстве расположения.

Для защиты данных передаваемых по открытым каналам связи предпологается использования ssl/tls.

### Web
- Веб-приложение создано на микрофреймворке Flask
- Приложение - отсебятина автора. Автор не использовал стандарт REST при разработке.
- Учитывая предыдущий пункт. URL указывает не на физическую директорию, а на эмулируемую в контексте функции.
- Blueprints не были использованы для увеличения гибкости, оптимизованности и общего качества приложения.
- Приложениие собираллсь в `app` остальные `.py` файлы использовались как модули/библиотеки для доступа к классу выполняющего определенный функционал.
- Файл `Encrypt` предназанчен для эмуляции хеширования пароля пользователя при регистрации, полученный хеш заносится вручную в DB. В последствии веб-приложение будет проверять при входе пользователя в систему старый хеш из дб с новым от вводимого пароля пользователя.
- Предназначено для использованием клиентами для получения услуг банка, а также работниками низшего звена для обслуживания клиентов в чат команатах.
- В `db` осуществляется подключение к SQL серверу и получение массивов строк таблиц с занесением в словари для дальнейшей удобной обработки.
- В `db_check`

### Desktop
- Разрабатовалось с использованием стандартной графической библиотке tkinter
- Представляет собой GUI для продукт менеджера банка
