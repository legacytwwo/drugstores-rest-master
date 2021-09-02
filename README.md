Ваша задача - разработать на python REST API сервис, который сохраняет
переданные ему наборы данных c аптеками, позволяет их
просматривать, редактировать информацию отдельных аптек, а также
производить выборку по городам, регионами или ближайших
на основе заданных координат и радиусу.

## Описание обработчиков REST API
------

### 1. Создание аптеки

Принимает на вход набор с данными аптеки в формате `json`
(поля не могут быть пустыми) и сохраняет его.

`drugstore_id` уникален и не может повторяться у разных аптек.
При создании необходимо обогатить данные полями:
- `created_at` дата создания (в формате ISO 8601);
- `updated_at` дата изменения (в формате ISO 8601);
- `schedule_representation` представление расписания;

`schedule_representation` формируется следующим образом:
- если по времени есть 23:59 то формируем как "круглосуточно";
- если у всех дней совпадает время то формируем как "ежедневно 10:00-21:00";
- если есть время совпадает у 2х и меньше выводим через запятую - "сб, вс 10:00-21:00";
- если есть время совпадает у 3х подрят и больше выводим через тире - "пн-пт 08:00-22:00";

примеры:
- "круглосуточно";
- "ежедневно 09:00-21:00";
- "пн-пт 08:00-22:00 сб, вс 09:00-22:00";

`POST /`
```json
{
    "drugstore_id": "d4b7b8d0-322b-45a7-8b5a-a697d8418ffc",
    "geo": {
        "address": "Мостовая ул, 88",
        "city_id": "c8ef279e-f476-11e8-9d1f-ec0d9ac026a5",
        "city_name": "Алексеевка",
        "region_id": "6c11e6bf-5649-11eb-9d79-00155d0c026e",
        "region_name": "Белгородская область",
        "location": {
            "lat": 50.631692,
            "lon": 38.691661
        }
    },
    "phone": "8-800-2005-400",
    "schedule": [
        {
            "day": 1,
            "day_name": "Пн",
            "start": "08:00",
            "end": "20:00"
        },
        {
            "day": 2,
            "day_name": "Вт",
            "start": "08:00",
            "end": "20:00"
        },
        {
            "day": 3,
            "day_name": "Ср",
            "start": "08:00",
            "end": "20:00"
        },
        {
            "day": 4,
            "day_name": "Чт",
            "start": "08:00",
            "end": "20:00"
        },
        {
            "day": 5,
            "day_name": "Пт",
            "start": "08:00",
            "end": "20:00"
        },
        {
            "day": 6,
            "day_name": "Сб",
            "start": "08:00",
            "end": "20:00"
        },
        {
            "day": 7,
            "day_name": "Вс",
            "start": "08:00",
            "end": "20:00"
        }
    ]
}
```

В случае успеха возвращается ответ с HTTP статусом 201 Created и
идентификатором аптеки:

```json
HTTP 201

{
    "status": true,
    "detail": "successfully",
    "payload": {
        "drugstore_id": "d4b7b8d0-322b-45a7-8b5a-a697d8418ffc"
    }
}
```

### 2. Изменение или создание аптеки

Изменяет информацию в указанной аптеке или создает аптеку в случае ее отсутствия

`PUT /{drugstore_id}`
```json
{
    "drugstore_id": "d4b7b8d0-322b-45a7-8b5a-a697d8418ffc",
    "geo": {
        "address": "Мостовая ул, 88",
        "city_id": "c8ef279e-f476-11e8-9d1f-ec0d9ac026a5",
        "city_name": "Алексеевка",
        "region_id": "6c11e6bf-5649-11eb-9d79-00155d0c026e",
        "region_name": "Белгородская область",
        "location": {
            "lat": 50.631692,
            "lon": 38.691661
        }
    },
    "phone": "8-800-2005-400",
    "schedule": [
        {
            "day": 1,
            "day_name": "Пн",
            "start": "08:00",
            "end": "20:00"
        },
        {
            "day": 2,
            "day_name": "Вт",
            "start": "08:00",
            "end": "20:00"
        },
        {
            "day": 3,
            "day_name": "Ср",
            "start": "08:00",
            "end": "20:00"
        },
        {
            "day": 4,
            "day_name": "Чт",
            "start": "08:00",
            "end": "20:00"
        },
        {
            "day": 5,
            "day_name": "Пт",
            "start": "08:00",
            "end": "20:00"
        },
        {
            "day": 6,
            "day_name": "Сб",
            "start": "08:00",
            "end": "20:00"
        },
        {
            "day": 7,
            "day_name": "Вс",
            "start": "08:00",
            "end": "20:00"
        }
    ]
}
```

Возвращается актуальная информация о аптеке

```json
HTTP 200

{
    "status": true,
    "detail": "successfully",
    "payload": {
        "created_at": "2021-03-24T08:24:54.693+00:00",
        "updated_at": "2021-03-28T12:30:21.453+00:00",
        "drugstore_id": "d4b7b8d0-322b-45a7-8b5a-a697d8418ffc",
        "geo": {
            "address": "Мостовая ул, 88",
            "city_id": "c8ef279e-f476-11e8-9d1f-ec0d9ac026a5",
            "city_name": "Алексеевка",
            "region_id": "6c11e6bf-5649-11eb-9d79-00155d0c026e",
            "region_name": "Белгородская область",
            "location": {
                "lat": 50.631692,
                "lon": 38.691661
            }
        },
        "phone": "8-800-2005-400",
        "schedule_representation": "ежедневно 08:00-20:00",
        "schedule": [
            {
                "day": 1,
                "day_name": "Пн",
                "start": "08:00",
                "end": "20:00"
            },
            {
                "day": 2,
                "day_name": "Вт",
                "start": "08:00",
                "end": "20:00"
            },
            {
                "day": 3,
                "day_name": "Ср",
                "start": "08:00",
                "end": "20:00"
            },
            {
                "day": 4,
                "day_name": "Чт",
                "start": "08:00",
                "end": "20:00"
            },
            {
                "day": 5,
                "day_name": "Пт",
                "start": "08:00",
                "end": "20:00"
            },
            {
                "day": 6,
                "day_name": "Сб",
                "start": "08:00",
                "end": "20:00"
            },
            {
                "day": 7,
                "day_name": "Вс",
                "start": "08:00",
                "end": "20:00"
            }
        ]
    }
}
```

### 3. Удаление указанной аптеки

`DELETE /{drugstore_id}`

В случае успеха возвращается ответ с HTTP статусом 204 No Content

```json
HTTP 204
```

### 4. Получение списка аптек

Возвращать список с возможностью пагинации и фильтрацией

| query params  | type | default |
| :------------ |:----:| -------:|
| limit         | int  | 10      |
| offset        | int  | 0       |
| city_id       | str  |         |
| region_id     | str  |         |


`GET /`

```json
HTTP 200

{
    "status": true,
    "detail": "successfully",
    "payload": {
        "count": 100,
        "limit": 10,
        "offset": 0,
        "result": [
            {
                "drugstore_id": "d4b7b8d0-322b-45a7-8b5a-a697d8418ffc",
                "geo": {
                    "address": "Мостовая ул, 88",
                    "city_id": "c8ef279e-f476-11e8-9d1f-ec0d9ac026a5",
                    "city_name": "Алексеевка",
                    "region_id": "6c11e6bf-5649-11eb-9d79-00155d0c026e",
                    "region_name": "Белгородская область",
                    "location": {
                        "lat": 50.631692,
                        "lon": 38.691661
                    }
                },
                "phone": "8-800-2005-400",
                "schedule_representation": "ежедневно 08:00-20:00",
                "schedule": [
                    {
                        "day": 1,
                        "day_name": "Пн",
                        "start": "08:00",
                        "end": "20:00"
                    },
                    {
                        "day": 2,
                        "day_name": "Вт",
                        "start": "08:00",
                        "end": "20:00"
                    },
                    {
                        "day": 3,
                        "day_name": "Ср",
                        "start": "08:00",
                        "end": "20:00"
                    },
                    {
                        "day": 4,
                        "day_name": "Чт",
                        "start": "08:00",
                        "end": "20:00"
                    },
                    {
                        "day": 5,
                        "day_name": "Пт",
                        "start": "08:00",
                        "end": "20:00"
                    },
                    {
                        "day": 6,
                        "day_name": "Сб",
                        "start": "08:00",
                        "end": "20:00"
                    },
                    {
                        "day": 7,
                        "day_name": "Вс",
                        "start": "08:00",
                        "end": "20:00"
                    }
                ]
            },
            ...
        ]
    }
}
```

### 4. Получение указанной аптеки

`GET /{drugstore_id}`

```json
HTTP 200

{
    "status": true,
    "detail": "successfully",
    "payload": {
        "drugstore_id": "d4b7b8d0-322b-45a7-8b5a-a697d8418ffc",
        "geo": {
            "address": "Мостовая ул, 88",
            "city_id": "c8ef279e-f476-11e8-9d1f-ec0d9ac026a5",
            "city_name": "Алексеевка",
            "region_id": "6c11e6bf-5649-11eb-9d79-00155d0c026e",
            "region_name": "Белгородская область",
            "location": {
                "lat": 50.631692,
                "lon": 38.691661
            }
        },
        "phone": "8-800-2005-400",
        "schedule_representation": "ежедневно 08:00-20:00",
        "schedule": [
            {
                "day": 1,
                "day_name": "Пн",
                "start": "08:00",
                "end": "20:00"
            },
            {
                "day": 2,
                "day_name": "Вт",
                "start": "08:00",
                "end": "20:00"
            },
            {
                "day": 3,
                "day_name": "Ср",
                "start": "08:00",
                "end": "20:00"
            },
            {
                "day": 4,
                "day_name": "Чт",
                "start": "08:00",
                "end": "20:00"
            },
            {
                "day": 5,
                "day_name": "Пт",
                "start": "08:00",
                "end": "20:00"
            },
            {
                "day": 6,
                "day_name": "Сб",
                "start": "08:00",
                "end": "20:00"
            },
            {
                "day": 7,
                "day_name": "Вс",
                "start": "08:00",
                "end": "20:00"
            }
        ]
    }
}
```

## Дополнительное задание
------

### Получение списка ближайших аптек

| query params  | type       |
| :------------ |:----------:|
| lat           | int, float |
| lon           | int, float |
| radius        | int, float |

Возвращать список аптек в указанном радиусе
Значение радиуса в километрах

`GET /near?lat=50.63&lon=38.40&radius=0.5`

Возвращать список с возможностью пагинации

```json
HTTP 200

{
    "status": true,
    "detail": "successfully",
    "payload": {
        "count": 100,
        "limit": 10,
        "offset": 0,
        "result": [
            {
                "drugstore_id": "d4b7b8d0-322b-45a7-8b5a-a697d8418ffc",
                "geo": {
                    "address": "Мостовая ул, 88",
                    "city_id": "c8ef279e-f476-11e8-9d1f-ec0d9ac026a5",
                    "city_name": "Алексеевка",
                    "region_id": "6c11e6bf-5649-11eb-9d79-00155d0c026e",
                    "region_name": "Белгородская область",
                    "location": {
                        "lat": 50.631692,
                        "lon": 38.691661
                    }
                },
                "phone": "8-800-2005-400",
                "schedule_representation": "ежедневно 08:00-20:00",
                "schedule": [
                    {
                        "day": 1,
                        "day_name": "Пн",
                        "start": "08:00",
                        "end": "20:00"
                    },
                    {
                        "day": 2,
                        "day_name": "Вт",
                        "start": "08:00",
                        "end": "20:00"
                    },
                    {
                        "day": 3,
                        "day_name": "Ср",
                        "start": "08:00",
                        "end": "20:00"
                    },
                    {
                        "day": 4,
                        "day_name": "Чт",
                        "start": "08:00",
                        "end": "20:00"
                    },
                    {
                        "day": 5,
                        "day_name": "Пт",
                        "start": "08:00",
                        "end": "20:00"
                    },
                    {
                        "day": 6,
                        "day_name": "Сб",
                        "start": "08:00",
                        "end": "20:00"
                    },
                    {
                        "day": 7,
                        "day_name": "Вс",
                        "start": "08:00",
                        "end": "20:00"
                    }
                ]
            },
            ...
        ]
    }
}
```


## На что обратить внимание
------

Для прохождения проверки обратите внимание на следующее:
- Статусы HTTP ответов;
- Структура json на входе и выходе;
- Типы данных (строки, числа);
- Формат даты;


## Как производится оценка задания
------
Задание считается выполненным, если в REST API реализован и проходит валидацию

Также учитывается:
- Наличие валидации входных данных;
- Наличие файла README в корне репозитория с инструкциями по установке;
- развертыванию и запуску тестов;
- Явно описанные внешние python-библиотеки (зависимости);
- Наличие тестов;
- Автоматическое возобновление работы REST API после перезагрузки виртуальной машины;
