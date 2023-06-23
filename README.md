## Краткое описание проекта
Проект предсатавляет собой базу данных центра телемаркетинга коммерческого банка с которой по средством API ODBC взаимодействуют веб-приложение и desktop клиент.
Для защиты базы данных применено прозрачное шифрование, которое обеспечивает целостность фалов базы на устройстве расположения.

Для защиты данных передаваемых по открытым каналам связи предпологается использования ssl/tls.

### Web
- Веб-приложение создано на микрофреймворке Flask
- Для CSS использовался Bootstrap, а также был взят шаблон для панели авторизации.
- Приложение - отсебятина автора. Автор не использовал стандарт REST при разработке.
- Учитывая предыдущий пункт. URL указывает не на физическую директорию, а на эмулируемую в контексте функции.
- Blueprints не были использованы для увеличения гибкости, оптимизованности и общего качества приложения.
- Приложение в основном статическое не учитывая live-чат, который использует вебсокеты.
- Приложение не использует AJAX.
- Приложениие собираллсь в `app` остальные `.py` файлы использовались как модули/библиотеки для доступа к классу выполняющего определенный функционал.
- Файл `Encrypt` предназанчен для эмуляции хеширования пароля пользователя при регистрации, полученный хеш заносится вручную в DB. В последствии веб-приложение будет проверять при входе пользователя в систему старый хеш из дб с новым от вводимого пароля пользователя.
- Предназначено для использованием клиентами для получения услуг банка, а также работниками низшего звена для обслуживания клиентов в чат команатах.
- В `db` осуществляется подключение к SQL серверу и получение массивов строк таблиц с занесением в словари для дальнейшей удобной обработки.
- В `db_check`осуществляется идентификация и аутентификация пользователя.
- `Cookie_check` проверяет наличие кук в браузере, если они есть то сравнивает с куками в бд(эти куки были занесены при успешном первом входе пользователя), при совпадении кук пользователь проходит авторизацию и получает права иначе нет.

### Desktop
- Разрабатовалось с использованием стандартной графической библиотке tkinter
- Представляет собой GUI для продукт менеджера банка
- Авторизации совершается через SQL Server Authentication с использованием API ODBC

## Даталогическая модель базы данных

![datalog2](https://github.com/LegendaryVasya/Telemarketing_system/assets/46849169/8228f7f1-5ed0-4966-ae36-02136b6a5f41)

## Связи
- Связь «Клиенты» – «Сообщения» (1: М)

  Один клиент может получить несколько персонализированных сообщений. Несколько персонализированных сообщений принадлежат к одному конкретному клиенту.

- Связь «Аккаунты» – «Клиенты» (М:1)

  Аккаунт выдается пользователю для управления своим счетом и получения услуг банка, не выходя из дома. К аккаунту привязан конкретный счет, клиент может оформить несколько счетов в банке для которых потребуются несколько аккаунтов.
  
- Связь «Аккаунты» – «Детали счета» (1: М)

  Аккаунт может иметь счет с различной валютой
  
- Связь «Детали счета» – «Чеки» (1: М)

  Используя один счет можно совершить несколько операций. Несколько операций могут быть совершены на одном счете.
  
- Связь «Аккаунты» – «Новости банка» (1: М)

  К одному аккаунты могут относиться несколько персонализированных новостей. Несколько персонализированных новостей относятся к одному аккаунтов.

- Связь «Клиенты» – «Опросы» (1: M)

  Одному клиенту советует несколько персонализированных опросов. Несколько персонализированных опросов относятся к одному клиенту.
  
- Связь «Аккаунты» – «Работники» (М: 1)

  Аккаунт выдается работник для оказания услуг клиентам через веб-приложение банка. Из-за расширения функционала банка сотруднику могут принадлежать несколько аккаунтов с разным функционалом.
  
- Связь «Работники» – «Компании» (1: M)

  Один работник на одну кампанию. Обычно выбирается профессионал области для удачного осуществления поставленной задачи. Один работник может участвовать в нескольких компаниях.
  
- Связь «Лиды» – «Сообщения» (1: М)

  Один лид может получить несколько персонализированных сообщений. Несколько персонализированных сообщений могут относиться к одному лиду.
  
- Связь «Компания» – «Лид» (М: 1)

  В нескольких компаниях может участвовать один лид. Один лид может участвовать в нескольких копаниях.
  
- Связь «Компании» – «Продукты»

  Одна компания может продвигать несколько продуктов. 


## Демонстрация работы разлинчых функций ИС

### Функционал web

| ![fail_log](https://github.com/LegendaryVasya/Telemarketing_system/assets/46849169/123e0383-9240-489d-bc2f-6d1ca7cc4106) |
|:--:| 
| *Демонстрация провальной авторизации* |


| ![true_log](https://github.com/LegendaryVasya/Telemarketing_system/assets/46849169/d2bc678b-be42-4215-b0ee-8031f73f9f78) |
|:--:|
| *Демонстрация успешной авторизации* |


| ![live_chat](https://github.com/LegendaryVasya/Telemarketing_system/assets/46849169/89ed5a01-326f-4fd5-98cc-bbcf38011835) |
|:--:| 
| *Демонстрация live-чата* |


| ![make_pay](https://github.com/LegendaryVasya/Telemarketing_system/assets/46849169/ef0a942f-f3f1-4f41-8664-52d576c67b47) |
|:--:|
| *Демонстрация совершения платежа* |


| ![reviews](https://github.com/LegendaryVasya/Telemarketing_system/assets/46849169/66bdd749-5dfc-41b9-89e3-e50e499e7c8e) |
|:--:|
| *Демонстрация составления отзыва* |

---
### Функционал десктопного приложения

| ![fail_log_tkinter](https://github.com/LegendaryVasya/Telemarketing_system/assets/46849169/a92bfc21-8501-4084-90ab-c9cf922a5b7d) | 
|:--:|
| *Демонстрация провальной авторизации* |


| ![log_tkinter](https://github.com/LegendaryVasya/Telemarketing_system/assets/46849169/a446b348-e34e-4b60-9f1f-eeba14ca30b6) |
|:--:|
| *Демонстрация успешной авторизации* |


| ![revie_tkinter](https://github.com/LegendaryVasya/Telemarketing_system/assets/46849169/b2e1f3ed-4e8e-48a4-94b7-d65a324fe720) |
|:--:|
| *Демонстрация сбора данных о опросах* |


| [![Survays](https://img.youtube.com/vi/rv8fs02tihU/maxresdefault.jpg)](https://www.youtube.com/watch?v=rv8fs02tihU) |
|:--:|
| *Демонстрация работы с опросами* 
  *Чтобы посмотреть нажми на изображение*|


| [![News](https://img.youtube.com/vi/DyOgZ7HSzc0/maxresdefault.jpg)](https://www.youtube.com/watch?v=DyOgZ7HSzc0) |
|:--:|
| *Демонстрация работы с новостями* 
  *Чтобы посмотреть нажми на изображение*|
