# Docker Compose — patterns comuns

## Pattern 1: App web + DB + reverse proxy (Traefik)

```yaml
services:
  app:
    image: my/app:latest
    restart: unless-stopped
    environment:
      DATABASE_URL: postgres://user:pass@db:5432/myapp
    depends_on:
      db:
        condition: service_healthy
    networks:
      - traefik
      - internal
    labels:
      - traefik.enable=true
      - traefik.docker.network=traefik
      - traefik.http.routers.myapp.rule=Host(`myapp.example.com`)
      - traefik.http.routers.myapp.tls.certresolver=letsencrypt
      - traefik.http.services.myapp.loadbalancer.server.port=3000

  db:
    image: postgres:16-alpine
    restart: unless-stopped
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    volumes:
      - dbdata:/var/lib/postgresql/data
    networks:
      - internal
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user"]
      interval: 5s
      timeout: 3s
      retries: 5

networks:
  traefik:
    external: true
  internal:

volumes:
  dbdata:
```

## Pattern 2: Healthcheck robusto

```yaml
services:
  api:
    image: my/api
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 10s
      timeout: 3s
      retries: 3
      start_period: 30s    # importante para apps que demoram para subir
```

## Pattern 3: Resource limits (essencial em produção)

```yaml
services:
  app:
    image: my/app
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 256M
```

`deploy.resources` funciona em Compose >= 1.27 (com `--compatibility`) ou Swarm.

## Pattern 4: Logs rotativos (não encher disco)

```yaml
services:
  app:
    image: my/app
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"
```

## Pattern 5: .env file pattern (segredos fora do compose)

```yaml
# docker-compose.yml
services:
  app:
    image: my/app
    environment:
      DATABASE_URL: ${DATABASE_URL}
      SECRET_KEY: ${SECRET_KEY}
```

```bash
# .env (gitignored!)
DATABASE_URL=postgres://...
SECRET_KEY=super-secret
```

## Pattern 6: Override files (dev vs prod)

```bash
# docker-compose.yml         (base, prod-ready)
# docker-compose.override.yml (dev — auto-loaded)
# docker-compose.prod.yml    (prod-specific overrides)

# Em dev:
docker compose up -d   # carrega base + override

# Em prod:
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

## Pattern 7: Watchtower (auto-update — usar com cuidado)

```yaml
services:
  watchtower:
    image: containrrr/watchtower
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    environment:
      WATCHTOWER_LABEL_ENABLE: "true"
      WATCHTOWER_CLEANUP: "true"
      WATCHTOWER_SCHEDULE: "0 0 4 * * *"  # 4 AM
    restart: unless-stopped

  app:
    image: my/app:latest
    labels:
      com.centurylinklabs.watchtower.enable: "true"
```

⚠️ Watchtower em produção pode quebrar coisas. Prefira CI/CD pipeline com tags fixas.

## Pattern 8: Volume backup automatizado

```yaml
services:
  db:
    image: postgres:16
    volumes:
      - dbdata:/var/lib/postgresql/data

  backup:
    image: prodrigestivill/postgres-backup-local
    restart: always
    volumes:
      - ./backups:/backups
    environment:
      POSTGRES_HOST: db
      POSTGRES_DB: myapp
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      SCHEDULE: '@daily'
      BACKUP_KEEP_DAYS: 7
      BACKUP_KEEP_WEEKS: 4
      BACKUP_KEEP_MONTHS: 6
    depends_on:
      - db
```

## Pattern 9: Init container (one-shot tarefa antes de subir app)

```yaml
services:
  migrate:
    image: my/app
    command: npm run db:migrate
    environment:
      DATABASE_URL: ${DATABASE_URL}
    depends_on:
      db:
        condition: service_healthy
    restart: "no"

  app:
    image: my/app
    depends_on:
      migrate:
        condition: service_completed_successfully
```

## Pattern 10: Network isolation (3-tier)

```yaml
services:
  proxy:
    image: traefik
    networks:
      - public
      - frontend

  app:
    image: my/app
    networks:
      - frontend
      - backend

  db:
    image: postgres
    networks:
      - backend          # SÓ backend — nunca exposto

networks:
  public:
    external: true       # rede compartilhada com Traefik externo
  frontend:
  backend:
    internal: true       # impossível sair pra fora
```
