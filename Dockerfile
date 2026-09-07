FROM nginx:1.31.5-alpine3.24@sha256:72ba65eb42c10344912a84ff42408db7d34f2feb642204570ab8fc5ffd29f1d3

COPY nginx.conf /etc/nginx/nginx.conf
COPY site/ /usr/share/nginx/html/

RUN chmod 0644 /etc/nginx/nginx.conf \
    && chmod -R a=rX /usr/share/nginx/html

USER 101:101

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget -q -O - http://127.0.0.1:8080/health >/dev/null || exit 1

ENTRYPOINT ["nginx", "-g", "daemon off;"]
