#!/bin/sh

set -eu

repo_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
project_name=web-yanoa-smoke-test

cleanup() {
    docker compose \
        -p "$project_name" \
        -f "$repo_dir/compose.yml" \
        -f "$repo_dir/compose.test.yml" \
        down --remove-orphans >/dev/null 2>&1 || true
}

trap cleanup EXIT INT TERM
cleanup

docker compose \
    -p "$project_name" \
    -f "$repo_dir/compose.yml" \
    -f "$repo_dir/compose.test.yml" \
    up -d --build --wait

curl --fail --silent --show-error http://127.0.0.1:18080/health | grep -qx ok
curl --fail --silent --show-error http://127.0.0.1:18080/ | grep -q "Your Yanoa"
curl --fail --silent --show-error --head http://127.0.0.1:18080/ \
    | grep -qi '^Content-Security-Policy:'

echo "Container smoke test passed."
