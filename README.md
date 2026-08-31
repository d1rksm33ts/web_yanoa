# web_yanoa

The public portal for the Yanoa product space. It links to Yanoa applications
while deliberately excluding unrelated sites that merely share the same host.

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

## Greenfield deployment

The repository is deployed to:

```text
/srv/yanoa/repositories/web_yanoa
```

Start it with:

```sh
docker compose -p web-yanoa up -d --build
```

Shared Caddy routes `greenfield.yanoa.be` to `web-yanoa:8080` during
acceptance. Production `yanoa.be` DNS and routing remain unchanged until the
documented cutover gates have passed.
