# SIRIUS Deployment Guide

## Production Deployment Options

### Option 1: Heroku Deployment

1. **Install Heroku CLI**
2. **Create Heroku App**
   ```bash
   heroku create sirius-legal-structures
   ```

3. **Configure Environment Variables**
   ```bash
   heroku config:set DEBUG=False
   heroku config:set SECRET_KEY=your-production-secret-key
   heroku config:set ALLOWED_HOSTS=sirius-legal-structures.herokuapp.com
   ```

4. **Add Procfile**
   ```
   web: gunicorn sirius_project.wsgi:application --log-file -
   release: python manage.py migrate
   ```

5. **Deploy**
   ```bash
   git push heroku main
   heroku run python manage.py populate_initial_data
   ```

### Option 2: DigitalOcean App Platform

1. **Connect GitHub Repository**
2. **Configure Build Settings**
   - Build Command: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
   - Run Command: `gunicorn sirius_project.wsgi:application`

3. **Set Environment Variables**
   - DEBUG=False
   - SECRET_KEY=your-production-secret-key
   - ALLOWED_HOSTS=your-app-domain.ondigitalocean.app

### Option 3: Traditional VPS

1. **Server Setup**
   ```bash
   sudo apt update
   sudo apt install python3.11 python3.11-venv nginx postgresql
   ```

2. **Application Setup**
   ```bash
   git clone https://github.com/carlossilvatbh/sirius-system.git
   cd sirius-system
   python3.11 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Database Setup**
   ```bash
   sudo -u postgres createdb sirius_db
   python manage.py migrate
   python manage.py populate_initial_data
   ```

4. **Nginx Configuration**
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location /static/ {
           alias /path/to/sirius-system/staticfiles/;
       }
       
       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

## Production Checklist

- [ ] Set DEBUG=False
- [ ] Configure proper SECRET_KEY
- [ ] Set ALLOWED_HOSTS
- [ ] Configure database (PostgreSQL recommended)
- [ ] Set up static file serving
- [ ] Configure SSL certificate
- [ ] Set up monitoring and logging
- [ ] Configure backup strategy
- [ ] Test all functionality
- [ ] Set up domain and DNS

## Security Considerations

1. **Environment Variables**: Never commit secrets to version control
2. **HTTPS**: Always use SSL in production
3. **Database Security**: Use strong passwords and restrict access
4. **Regular Updates**: Keep dependencies updated
5. **Monitoring**: Set up error tracking and monitoring

## Performance Optimization

1. **Static Files**: Use CDN for static file serving
2. **Database**: Optimize queries and add indexes
3. **Caching**: Implement Redis for caching
4. **Compression**: Enable gzip compression
5. **Monitoring**: Set up performance monitoring

