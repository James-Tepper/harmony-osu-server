FROM python:3.11
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "app/main.py"]
RUN apt update && apt install postgresql

EXPOSE 80

# ENTRYPOINT [ "/scripts/bootstrap.sh" ]
