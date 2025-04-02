# Use Node.js official image
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package.json and install dependencies
COPY package.json package-lock.json ./
RUN npm install

# Copy frontend source code
COPY . .

# Expose frontend port
EXPOSE 5173

# Start React app
CMD ["npm", "run", "dev"]
