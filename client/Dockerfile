FROM node:18.19 AS installer
WORKDIR /app
COPY package*.json ./
RUN npm install
FROM node:18.19-alpine AS release
WORKDIR /app
COPY --from=installer /app/node_modules ./node_modules
COPY . .
EXPOSE 5173
CMD ["npm", "run", "dev"]
