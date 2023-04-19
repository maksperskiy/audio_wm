FROM nginx:alpine
COPY app/frontend /usr/share/nginx/html

RUN sed -i -e "s/'http:\/\/localhost:8081'/'http:\/\/optimizer:80'/" /usr/share/nginx/html/scripts/main.js