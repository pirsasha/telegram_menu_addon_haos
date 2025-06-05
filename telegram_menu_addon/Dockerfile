FROM python:3.10-slim

WORKDIR /app

# Копируем весь код, включая web
COPY . /app/

# Отдельно копируем скрипт запуска (если он выше уровнем)
COPY run.sh /run.sh

# Установка зависимостей
RUN pip install flask pyyaml
RUN chmod +x /run.sh

EXPOSE 8123

CMD ["/run.sh"]

