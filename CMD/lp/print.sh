#!/bin/bash

# Имя файла для печати
FILE_TO_PRINT="\$1"

# Проверяем, существует ли файл
if [ ! -f "$FILE_TO_PRINT" ]; then
    echo "Ошибка: Файл '$FILE_TO_PRINT' не найден!"
    exit 1
fi

# Отправляем файл на печать
lp "$FILE_TO_PRINT"

