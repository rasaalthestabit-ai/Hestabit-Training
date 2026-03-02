FROM node:20-alpine

# Create app directory
WORKDIR /app

# Copy package.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy rest of app
COPY . .

# Create non-root user
RUN addgroup appgroup && adduser -S appuser -G appgroup

USER appuser

EXPOSE 3000

CMD ["node", "index.js"]
