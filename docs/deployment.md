# Deployment: Production Hardening

MetaOpenCoach apps are designed for performance and reliability. Following these procedures ensures a secure and stable production environment.

## TL;DR
Production deployment requires specific environment variables, a process manager like PM2, a reverse proxy like NGINX for SSL termination, and a robust logging and backup strategy.

## Prerequisites
- **Node.js**: Version 18.x or higher (LTS recommended).
- **Process Manager**: PM2 is highly recommended for uptime.
- **Web Server**: NGINX for handling HTTPS and load balancing.

## 1. Environment Configuration
Create a `.env` file in the application root with the following variables:

```env
PORT=3000
NODE_ENV=production
DB_SECRET=your_super_secret_AES_key_here
AI_API_KEY=your_optional_api_key
AI_MODEL=qwen3.5-2b
AI_BASE_URL=http://localhost:1234/v1
```
> [!IMPORTANT]
> Change the `DB_SECRET` before the first run. If changed later, existing data in the encrypted database will become unreadable.

## 2. Running in Production
While `npm run dev` is suitable for testing, use the production start command for deployment:

```bash
# Using npm
npm start

# Using PM2 (Recommended)
pm2 start server.js --name "metaopencoach-app"
```

## 3. Production Hardening

### NGINX Reverse Proxy
Use NGINX to handle SSL and proxy requests to your Node.js application.
```nginx
server {
    listen 443 ssl;
    server_name coaching.yourdomain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

### SSL Termination
Always use HTTPS. The use of **Let's Encrypt** via Certbot is recommended for automated certificate management.

### Logging & Backups
- **PM2 Logs**: Monitor your app with `pm2 logs`.
- **Database Backup**: Regularly backup the `database.json` file. Since it is encrypted with `AES-256`, backups can be safely stored on cloud storage.

---
← [Back: Documentation Index](./Documentation_Index.md) | [Next: Contributing →](./contributing.md)
