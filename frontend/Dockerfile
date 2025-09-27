# Use official Nginx image
FROM nginx:alpine

# Set working directory
WORKDIR /usr/share/nginx/html

# Remove default Nginx static files
RUN rm -rf ./*

# Copy frontend files
COPY . .

# Expose Nginx default port
EXPOSE 80

# Run nginx
CMD ["nginx", "-g", "daemon off;"]
