FROM node:14

WORKDIR /app/frontend

COPY package*.json ./
RUN npm install

COPY . .
RUN quasar build

FROM nginx:stable-alpine
COPY --from=0 /app/frontend/dist/spa /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
