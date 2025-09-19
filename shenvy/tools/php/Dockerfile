ARG VERSION=${VERSION:-8}

FROM php:${VERSION}-cli AS php-base

RUN apt-get update && apt-get install -y git zip unzip

# install ext installer
ADD --chmod=0755 https://github.com/mlocati/docker-php-extension-installer/releases/latest/download/install-php-extensions /usr/local/bin/

# install php extensions
RUN install-php-extensions \
    @composer \
    ctype \
    iconv \
    xml \
    zlib \
    bz2 \
    zip

# install symfony cli
RUN curl -sS https://get.symfony.com/cli/installer | bash \
    && mv /root/.symfony5/bin/symfony /usr/local/bin/symfony

# Create a non-root user (php)
RUN useradd -m -s /bin/bash php \
    && mkdir -p /srv /home/php/.composer \
    && chown -R php:php /srv /home/php/.composer

WORKDIR /srv

# Switch to non-root user
USER php