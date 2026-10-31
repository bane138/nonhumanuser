# NonHumanUser

Stories, articles, a resource library and actual-play recordings for Call of Cthulhu and related games.

## Stack
- Python 3.14, Django 6.1, Gunicorn, WhiteNoise for static files
- PostgreSQL 18 in its own container
- Uploaded media (images, PDFs, audio) in an AWS S3 bucket; older actual-play audio links point at the `nonhumanuser` bucket directly
- Caddy for automatic HTTPS

## Local development
```bash
docker compose -f docker-compose.dev.yml up --build     # http://localhost:8001
docker compose -f docker-compose.dev.yml exec web python manage.py createsuperuser
docker compose -f docker-compose.dev.yml run --rm web pytest
```
Without `AWS_*` settings, uploads are stored in `./media`.

## Deploying to a DigitalOcean droplet

### 1. AWS S3 bucket (for media)
1. Create a bucket, e.g. `nonhumanuser-media`, in `us-east-2` (any region works; set `AWS_S3_REGION_NAME` to match).
2. Under **Permissions → Block public access**, turn off "Block public access to buckets and objects granted through *new/any public bucket policies*". Leave the ACL blocks on.
3. Add this bucket policy so media can be viewed publicly:
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [{
       "Sid": "PublicReadMedia",
       "Effect": "Allow",
       "Principal": "*",
       "Action": "s3:GetObject",
       "Resource": "arn:aws:s3:::nonhumanuser-media/media/*"
     }]
   }
   ```
4. Create an IAM user with an access key and attach this policy, which only allows access to that bucket:
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {"Effect": "Allow", "Action": ["s3:ListBucket"], "Resource": "arn:aws:s3:::nonhumanuser-media"},
       {"Effect": "Allow", "Action": ["s3:GetObject", "s3:PutObject", "s3:DeleteObject"],
        "Resource": "arn:aws:s3:::nonhumanuser-media/media/*"}
     ]
   }
   ```
5. Copy existing media into the bucket under the same names (safe to re-run; it skips files already there):
   ```bash
   docker compose exec web python manage.py upload_media /path/to/media --only-referenced
   ```

### 2. Server
On a fresh Ubuntu 24.04 droplet, run the one-time setup as root (Docker, firewall, swap, a `deploy` user):
```bash
ssh root@<droplet-ip> 'sh -s' < deploy/setup-server.sh
```
Point A records for `nonhumanuser.com` and `www.nonhumanuser.com` at the droplet.

### 3. Configure and start the site
As the `deploy` user:
```bash
git clone <your-repo-url> /opt/nonhumanuser
cd /opt/nonhumanuser
cp .env.example .env
nano .env        # set SECRET_KEY, POSTGRES_PASSWORD, AWS_*, EMAIL_*
docker compose up -d --build
docker compose exec web python manage.py createsuperuser
```
Caddy obtains the HTTPS certificate automatically. Once HTTPS works, raise `SECURE_HSTS_SECONDS` to `31536000` in `.env` and run `docker compose up -d`.

### 4. Updating
```bash
cd /opt/nonhumanuser && git pull && docker compose up -d --build
```
Migrations run automatically when the container starts.

### 5. Database backups
A nightly cron job for the `deploy` user (`crontab -e`) that keeps 14 days of backups:
```cron
30 3 * * * cd /opt/nonhumanuser && docker compose exec -T db sh -c 'pg_dump -U "$POSTGRES_USER" "$POSTGRES_DB"' | gzip > /opt/backups/db-$(date +\%F).sql.gz && find /opt/backups -name 'db-*.sql.gz' -mtime +14 -delete
```
Restore a backup:
```bash
gunzip -c /opt/backups/db-YYYY-MM-DD.sql.gz | docker compose exec -T db sh -c 'psql -U "$POSTGRES_USER" "$POSTGRES_DB"'
```

### Useful commands
```bash
docker compose logs -f web      # application logs
docker compose logs -f caddy    # HTTPS / proxy logs
docker compose exec web python manage.py check --deploy
docker compose exec web python manage.py check_storage
```
