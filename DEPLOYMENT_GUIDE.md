# SIRIUS - Guia de Deploy

**Sistema:** Strategic Intelligence Relationship & Interactive Universal System  
**Versão:** 2.0.0  
**Última atualização:** Janeiro 2025  

---

## 📋 Visão Geral

Este guia fornece instruções completas para fazer deploy do SIRIUS em diferentes ambientes de produção.

## 🎯 Ambientes Suportados

- **Heroku** (Recomendado para início)
- **DigitalOcean App Platform**
- **AWS Elastic Beanstalk**
- **VPS/Servidor Dedicado**

## 🚀 Deploy no Heroku

### Pré-requisitos

- Conta no Heroku
- Heroku CLI instalado
- Git configurado

### Passo a Passo

```bash
# 1. Login no Heroku
heroku login

# 2. Criar aplicação
heroku create nome-da-sua-app

# 3. Configurar variáveis de ambiente
heroku config:set DEBUG=False
heroku config:set SECRET_KEY=sua-chave-secreta-super-segura
heroku config:set ALLOWED_HOSTS=nome-da-sua-app.herokuapp.com

# 4. Adicionar PostgreSQL
heroku addons:create heroku-postgresql:mini

# 5. Deploy
git push heroku main

# 6. Executar migrações
heroku run python manage.py migrate

# 7. Criar superusuário
heroku run python manage.py createsuperuser

# 8. Coletar arquivos estáticos
heroku run python manage.py collectstatic --noinput
```

### Configuração Heroku

O projeto já inclui:
- `Procfile` configurado
- `requirements.txt` atualizado
- Configurações de produção no `settings.py`

## 🌊 Deploy no DigitalOcean App Platform

### Configuração via Interface Web

1. **Conectar Repositório**
   - Acesse DigitalOcean App Platform
   - Conecte seu repositório GitHub
   - Selecione a branch `main`

2. **Configurar Aplicação**
   ```yaml
   # app.yaml (opcional)
   name: sirius-system
   services:
   - name: web
     source_dir: /
     github:
       repo: seu-usuario/sirius-system
       branch: main
     run_command: gunicorn sirius_project.wsgi:application
     environment_slug: python
     instance_count: 1
     instance_size_slug: basic-xxs
     
   databases:
   - name: sirius-db
     engine: PG
     version: "13"
   ```

3. **Variáveis de Ambiente**
   ```bash
   DEBUG=False
   SECRET_KEY=sua-chave-secreta
   ALLOWED_HOSTS=sua-app.ondigitalocean.app
   DATABASE_URL=${sirius-db.DATABASE_URL}
   ```

## ☁️ Deploy no AWS Elastic Beanstalk

### Preparação

```bash
# 1. Instalar EB CLI
pip install awsebcli

# 2. Inicializar aplicação
eb init

# 3. Criar ambiente
eb create production

# 4. Configurar variáveis
eb setenv DEBUG=False
eb setenv SECRET_KEY=sua-chave-secreta
eb setenv ALLOWED_HOSTS=sua-app.elasticbeanstalk.com

# 5. Deploy
eb deploy
```

### Configuração AWS

Criar arquivo `.ebextensions/django.config`:

```yaml
option_settings:
  aws:elasticbeanstalk:container:python:
    WSGIPath: sirius_project.wsgi:application
  aws:elasticbeanstalk:application:environment:
    DJANGO_SETTINGS_MODULE: sirius_project.settings
```

## 🖥️ Deploy em VPS/Servidor Dedicado

### Configuração do Servidor (Ubuntu 22.04)

```bash
# 1. Atualizar sistema
sudo apt update && sudo apt upgrade -y

# 2. Instalar dependências
sudo apt install python3 python3-pip python3-venv nginx postgresql postgresql-contrib

# 3. Configurar PostgreSQL
sudo -u postgres createuser --interactive
sudo -u postgres createdb sirius_db

# 4. Configurar usuário
sudo adduser sirius
sudo usermod -aG sudo sirius
su - sirius

# 5. Clonar projeto
git clone https://github.com/seu-usuario/sirius-system.git
cd sirius-system

# 6. Configurar ambiente virtual
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 7. Configurar variáveis de ambiente
cp .env.example .env
# Editar .env com configurações de produção

# 8. Executar migrações
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

### Configuração Nginx

```nginx
# /etc/nginx/sites-available/sirius
server {
    listen 80;
    server_name seu-dominio.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /home/sirius/sirius-system;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
```

### Configuração Gunicorn

```bash
# /etc/systemd/system/gunicorn.service
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=sirius
Group=www-data
WorkingDirectory=/home/sirius/sirius-system
ExecStart=/home/sirius/sirius-system/venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          sirius_project.wsgi:application

[Install]
WantedBy=multi-user.target
```

```bash
# Ativar serviços
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket
sudo systemctl start nginx
sudo systemctl enable nginx

# Configurar firewall
sudo ufw allow 'Nginx Full'
```

## 🔧 Configurações de Produção

### Variáveis de Ambiente Obrigatórias

```bash
# Segurança
DEBUG=False
SECRET_KEY=chave-super-secreta-com-50-caracteres-minimo
ALLOWED_HOSTS=seudominio.com,www.seudominio.com

# Banco de dados
DATABASE_URL=postgres://usuario:senha@host:porta/nome_db

# Email (opcional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=seu-email@gmail.com
EMAIL_HOST_PASSWORD=sua-senha-app

# Arquivos estáticos (se usando CDN)
STATIC_URL=/static/
STATIC_ROOT=/caminho/para/static/
```

### Configurações de Segurança

```python
# settings.py (já configurado)
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000 if not DEBUG else 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

## 📊 Monitoramento

### Logs de Aplicação

```bash
# Heroku
heroku logs --tail

# DigitalOcean
doctl apps logs nome-da-app

# VPS
sudo journalctl -u gunicorn
sudo tail -f /var/log/nginx/access.log
```

### Métricas Importantes

- **Tempo de resposta** < 500ms
- **Uso de memória** < 80%
- **Uso de CPU** < 70%
- **Disponibilidade** > 99.9%

## 🔄 Atualizações

### Deploy de Novas Versões

```bash
# Heroku
git push heroku main
heroku run python manage.py migrate

# DigitalOcean
git push origin main
# Deploy automático configurado

# VPS
cd /home/sirius/sirius-system
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart gunicorn
```

## 🛡️ Backup

### Backup do Banco de Dados

```bash
# Heroku
heroku pg:backups:capture
heroku pg:backups:download

# PostgreSQL local
pg_dump sirius_db > backup_$(date +%Y%m%d_%H%M%S).sql

# Restaurar backup
psql sirius_db < backup_20250109_120000.sql
```

### Backup de Arquivos

```bash
# Arquivos estáticos e media
tar -czf backup_files_$(date +%Y%m%d).tar.gz static/ media/

# Código fonte (já no Git)
git archive --format=tar.gz --output=sirius_$(date +%Y%m%d).tar.gz HEAD
```

## 🚨 Troubleshooting

### Problemas Comuns

**1. Erro 500 - Internal Server Error**
```bash
# Verificar logs
heroku logs --tail
# ou
sudo journalctl -u gunicorn

# Verificar configuração
python manage.py check --deploy
```

**2. Arquivos estáticos não carregam**
```bash
# Coletar novamente
python manage.py collectstatic --noinput

# Verificar configuração Nginx
sudo nginx -t
sudo systemctl reload nginx
```

**3. Erro de conexão com banco**
```bash
# Verificar variável DATABASE_URL
echo $DATABASE_URL

# Testar conexão
python manage.py dbshell
```

## 📞 Suporte

Para problemas de deploy:
1. Verificar logs de erro
2. Consultar documentação da plataforma
3. Abrir issue no repositório
4. Contatar suporte técnico

---

**Sucesso no seu deploy!** 🚀

