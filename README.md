# web_yanoa

The public portal for the Yanoa product space. It separates Yanoa applications
from independent websites created or hosted by Yanoa Engineering.

## Architecture

The project is an immutable static site served by a pinned NGINX container. It
has no application runtime, database, secrets, writable storage, or external
frontend dependencies. The production Compose service joins only the shared
external `yanoa-edge` network and publishes no host port.

## Local verification

```sh
make validate
make test
```

The smoke test builds the production image, starts it temporarily on
`127.0.0.1:18080`, checks the page, security headers, and health endpoint, then
removes the test project.

## Production deployment

The repository is deployed to:

```text
/srv/yanoa/repositories/web_yanoa
```

Start it with:

```sh
docker compose -p web-yanoa up -d --build
```

Shared Caddy routes `yanoa.be` to `web-yanoa:8080`. `www.yanoa.be`
permanently redirects to the apex hostname. Deploy through `ubuntu@yanoa.be`.
