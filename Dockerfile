FROM python:3.9-slim

WORKDIR /home/app_user

COPY cryptopt.py /home/app_user

ENV API_KEY=""

RUN chmod +x cryptopt.py

CMD [ "bash", "-c", "read -p 'Please enter your CoinMarketcap API key: ' API_KEY && export API_KEY=$API_KEY && bash" ]
