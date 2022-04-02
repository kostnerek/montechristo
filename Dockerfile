FROM python:3.6
COPY .  /montechristo
WORKDIR /montechristo
RUN pip install -r requirements.txt
EXPOSE  80
CMD ["python", "app.py"]