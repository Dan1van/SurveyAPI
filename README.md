# SurveyAPI

API разработанное для системы опросов пользователей

**Функционал для администраторов системы**:

- авторизация в системе (регистрация не нужна)
- добавление/изменение/удаление опросов. Атрибуты опроса: название, дата старта, дата окончания, описание. После создания поле "дата старта" у опроса менять нельзя
- добавление/изменение/удаление вопросов в опросе. Атрибуты вопросов: текст вопроса, тип вопроса (ответ текстом, ответ с выбором одного варианта, ответ с выбором нескольких вариантов)

**Функционал для пользователей системы**:

- получение списка активных опросов
- прохождение опроса: опросы можно проходить анонимно, в качестве идентификатора пользователя в API передаётся числовой ID, по которому сохраняются ответы пользователя на вопросы; один пользователь может участвовать в любом количестве опросов
- получение пройденных пользователем опросов с детализацией по ответам (что выбрано) по ID уникальному пользователя

## Установка

Склонируйте git-репозиторий и установите зависимости.

```bash
git clone https://github.com/Dan1van/technical-inspection-website.git
pip install -r requirements.txt
```

## Использование

Запустить скрипт **manage.py**

```bash
python manage.py runserver
```

### Страницы API:

Документация, выполненная при помощи библиотеки yasg: 

- http://127.0.0.1:8000/swagger/


Страница для администратора: http://127.0.0.1:8000/admin/ 

Логин: **admin**
Пароль: **admin**

Страница с активными опросами: http://127.0.0.1:8000/api/survey/

Страница с определенным опросом: http://127.0.0.1:8000/api/survey/*survey-id*/

На страницах с определенным опросом можно послать ответ в виде JSON. 
Формат для отправки ответа:


```json
{
    "data": {
        "user-id": 1,
        "survey-id": 1,
        "answers": {
            "1": [1],         
            "2": [5, 6],                    
            "3": ["Example of answer"]   
         }
     }
}
```


Страница с опросами пройденными пользователем: http://127.0.0.1:8000/api/answer/*user-id*/
