FROM rent_golem/backend

USER dev

# Installing Golem requestor only to have gftp in this container
RUN mkdir -p /home/dev/.local/share/ya-installer/terms
RUN touch /home/dev/.local/share/ya-installer/terms/testnet-01.tag
RUN curl -sSf https://join.golem.network/as-requestor | bash - || echo "Nothing to see here"
ENV PATH=${PATH}:/home/dev/.local/bin/:/home/dev/.local/
