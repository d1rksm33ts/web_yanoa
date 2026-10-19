FROM nginx:1.31.7-alpine3.24@sha256:892bb2152464f0c5d8972593a5f5afaf8054552580b699d95f8ff4af08c2d33d

COPY nginx.conf /etc/nginx/nginx.conf
COPY site/ /usr/share/nginx/html/

RUN chmod 0644 /etc/nginx/nginx.conf \
    && chmod -R a=rX /usr/share/nginx/html

USER 101:101

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget -q -O - http://127.0.0.1:8080/health >/dev/null || exit 1

ENTRYPOINT ["nginx", "-g", "daemon off;"]
