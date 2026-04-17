# Stage 1: Build the React Application
FROM node:18-alpine as builder

# Set the working directory
WORKDIR /app

# Copy package metadata
COPY package.json package-lock.json* ./

# Install dependencies
RUN npm install

# Copy all source files
COPY . .

# Capture the build arg and map it to an env var
ARG VITE_API_URL
ENV VITE_API_URL=${VITE_API_URL}

# Build the app to a static directory (usually /app/dist for Vite)
RUN npm run build

# Stage 2: Serve the App using Nginx
FROM nginx:alpine

# Copy custom Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy build artifacts to Nginx html directory
COPY --from=builder /app/dist /usr/share/nginx/html

# Expose Nginx on port 80 (we'll map it to 5173 externally)
EXPOSE 80

# Keep Nginx in the foreground
CMD ["nginx", "-g", "daemon off;"]
