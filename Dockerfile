FROM python
LABEL authors="moritzslz"

WORKDIR /Users/moritzslz/PycharmProjects/Time-Series-Dash

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["top", "-b"]