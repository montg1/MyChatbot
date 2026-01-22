# Build Stage
FROM node:20-alpine AS builder
WORKDIR /app

# Install build dependencies (if needed)
RUN apk add --no-cache --virtual .build-deps build-base python3

COPY package*.json ./
RUN npm ci
COPY . .

# Build the app
RUN npm run build

# Remove build dependencies to reduce image size
RUN apk del .build-deps

# Production Stage
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
RUN chown -R nginx:nginx /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
