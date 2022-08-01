FROM nginx
RUN mkdir /usr/share/nginx/html/blog
COPY ./public/ /usr/share/nginx/html/blog

