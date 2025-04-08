# Этап сборки
FROM node:20-alpine AS build

WORKDIR /app

COPY package*.json ./
RUN npm install

# Копируем всё, включая src и public
COPY . . 
RUN npm run build

# Этап сервера
FROM nginx:alpine

# Удалим стандартный конфиг (по желанию)
RUN rm -rf /usr/share/nginx/html/*

# Копируем собранный билд в папку nginx
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
