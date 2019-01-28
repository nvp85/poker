FROM python:3.7-stretch

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY forms.py tests.py the_best_hand.py ./
COPY templates templates

EXPOSE 5000

CMD ["python", "./the_best_hand.py"]