FROM nginx:1.31.4-alpine3.24@sha256:db35bfc6b2951e7f8a72db5db120288c127ffaeeb4a6d4b95a26fead017d5913

COPY nginx.conf /etc/nginx/nginx.conf
COPY site/ /usr/share/nginx/html/

RUN chmod 0644 /etc/nginx/nginx.conf \
    && chmod -R a=rX /usr/share/nginx/html

USER 101:101

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget -q -O - http://127.0.0.1:8080/health >/dev/null || exit 1

ENTRYPOINT ["nginx", "-g", "daemon off;"]
