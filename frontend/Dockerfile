# Use an official Node.js image to build the frontend
FROM node:18 as build

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json
COPY package.json package-lock.json ./

# Install dependencies using npm
RUN npm install --legacy-peer-deps

# Copy the rest of the application code
COPY . .

# Build the frontend
RUN npm run build

# Use Nginx to serve the built frontend
FROM nginx:alpine

# Copy built frontend to Nginx web server
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

# Start Nginx server
CMD ["nginx", "-g", "daemon off;"]
