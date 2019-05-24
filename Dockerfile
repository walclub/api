FROM python
COPY . /project
RUN cd /project \
	&& pip install -r requirements.txt \
    && pip install -U --force-reinstall --no-binary :all: gevent \
    && rm -rf requirements.txt README.md Dockerfile \
    && chmod +x entrypoint.sh \
    # Reduce image size
    && apt-get remove --purge -y build-essential git curl wget gzip --allow-remove-essential \
    && apt-get autoremove -y \
    && apt-get clean \
    && apt-get autoclean \
    && apt-get autoremove -y \
    && rm -rf /var/cache/debconf/*-old \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /usr/share/doc/* /usr/share/locale/* \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /var/cache/apt/archives/*.deb /var/cache/apt/archives/partial/*.deb /var/cache/apt/*.bin
ENTRYPOINT ["/project/entrypoint.sh"]