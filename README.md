# application_of_goals 
(продукт, который позволит работать с целями и отслеживать прогресс по ним)

Установил Django последней версии (Django==4.0.1)

Создал проект (todolist)

Подключил контроль версий, создал репозиторий в GITHUB(https://github.com/Kirill-oss67/application_of_goals.git),
связал с текущим проектом

Добавил файл ".gitignore" в репозиторий, использовал готовый шаблон для python: https://github.com/github/gitignore/blob/main/Python.gitignore

Создал виртуальное окружение.

Добавил созданное виртуальное окружение в проект.

Активировал виртуальное окружение.

Добавил requirement.txt в корень проекта

Создал первое приложение "core"

Создал модель User в core.models

## run database
docker run --name "postgresql" -e POSTGRES_PASSWORD="1q2w3e4r5t" -e POSTGRES_USER="admin" -e POSTGRES_DB="todolist_db" -p 5432:5432 -d postgres:13.0-alpine










