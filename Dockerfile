FROM nginx:1.31.8-alpine3.24@sha256:1ef7ca94d7879df82421428ce13bd1eaa412404953859cf7a5b6512c25e67a60

COPY nginx.conf /etc/nginx/nginx.conf
COPY site/ /usr/share/nginx/html/

RUN chmod 0644 /etc/nginx/nginx.conf \
    && chmod -R a=rX /usr/share/nginx/html

USER 101:101

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget -q -O - http://127.0.0.1:8080/health >/dev/null || exit 1

ENTRYPOINT ["nginx", "-g", "daemon off;"]
