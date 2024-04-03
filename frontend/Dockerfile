FROM node:19.5.0-alpine

RUN mkdir -p /usr/src/frontend/

WORKDIR /usr/src/frontend/
COPY package*.json .
RUN npm install
COPY . .

EXPOSE 3000