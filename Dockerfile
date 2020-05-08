FROM python:3.7.7-alpine3.11

WORKDIR /usr/src/app

EXPOSE 80

ENV PYTHONPATH "${PYTHONPATH}:/usr/src/app"

COPY ./ ./

CMD [ "python", "-u", "./main_server.py" ]
