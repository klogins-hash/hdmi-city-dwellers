FROM node:18.19-alpine

# Set environment variables
ENV NODE_ENV=development \
    CHOKIDAR_USEPOLLING=true

# Install system dependencies for Alpine
RUN apk add --no-cache curl && rm -rf /var/cache/apk/*

# Create non-root user for security
RUN addgroup -g 1001 -S nodejs && \
    adduser -S reactuser -u 1001

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci && npm cache clean --force

# Copy application code
COPY . .

# Change ownership to non-root user
RUN chown -R reactuser:nodejs /app

# Switch to non-root user
USER reactuser

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:3000 || exit 1

CMD ["npm", "start"]
