FROM python:3.7

RUN mkdir /code
WORKDIR /code
COPY . .

RUN pip install pipenv
RUN pipenv install --system

CMD ["python", "manage.py", "keep-sleeping"]
