# Сравниваем вакансии программистов.

Этот проект позволяет собрать и сравнить статистику зарплат программистов в Москве, используя данные с сайтов **HeadHunter** и **SuperJob**. Программа собирает вакансии по популярным языкам программирования, обрабатывает их и выводит статистику о средней зарплате по каждому языку в виде удобных таблиц.

## Установка зависимостей.

Список зависимостей содержится в файле requirements.txt. Для установки всех необходимых библиотек, выполните следующую команду:

```bash
pip install -r requirements.txt
```

## Получение супер-ключа.

Для работы с API SuperJob необходим ключ, который можно получить после регистрации на SuperJob API. Зарегистрируйтесь, создайте приложение и получите свой API_KEY_SUPERJOB. После этого cоздайте файл .env в корневой директории проекта и добавьте в него переменные окружения для работы с API SuperJob:

## Пример запуска.

1. Запустите программу командой:
```
python SuperJob_and_HH.ru_in_Moscow.py
```

2. Программа выведет в консоль две таблицы — по вакансиям с HeadHunter и SuperJob.

![Данные о зарплатах ](https://i.postimg.cc/fbtqsMV6/image.jpg)


## Цель проекта.

Цель проекта — предоставить пользователю актуальные данные о зарплатах программистов по основным языкам программирования в Москве, собранные с двух популярных сайтов по поиску работы: HeadHunter и SuperJob. Данные обрабатываются, а затем выводятся в виде таблиц с информацией о количестве найденных и обработанных вакансий, а также о средней зарплате по каждому языку.



