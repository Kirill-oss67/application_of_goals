# application_of_goals

(продукт, который позволит работать с целями и отслеживать прогресс по ним)

Установил Django последней версии (Django==4.0.1)

Создал проект (todolist)

Подключил контроль версий, создал репозиторий в GITHUB(https://github.com/Kirill-oss67/application_of_goals.git),
связал с текущим проектом


Добавил файл ".gitignore" в репозиторий, использовал готовый шаблон для
python: https://github.com/github/gitignore/blob/main/Python.gitignore

Создал виртуальное окружение.

Добавил созданное виртуальное окружение в проект.

Активировал виртуальное окружение.


Добавил requirement.txt в корень проекта

Создал первое приложение "core"

Создал модель User в core.models наследовавшись от AbstractUser

Собрал dockerfile, добавил файл .dockerignore

Собрал docker-compose.yaml и docker-compose.yaml-сi , создал директорию . github, в ней директорию workflows с файлом actions.yaml
настройка Continue Integration и Continue Deploy

Установил djangorestframework, social-auth-app-django

В todolist/urls.py добавил урлы из core/urls.py и social_django

Создал serializers.py в приложении core

Описал CreateUserSerializer для регистрации
Описал View для регистрации пользователя и добавил его в core/urls.py

Описал LoginSerializer для реализации входа по логину/паролю
Описал View и добавил его в core/urls.py

Описал ProfileSerializer для реализации получения/обновления текущего пользователя
Описал View и добавил его в core/urls.py

В предыдущий метод API /core/profile добавил реализацию HTTP метода DELETE

Описал UpdatePasswordSerializer для реализации смены пароля
Описал View и добавил его в core/urls.py

Добавил поддержку входа через социальные сети (VK)











