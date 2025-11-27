# Official image
FROM cowrie/cowrie:latest

# Copy the modified cofig file to the default one
COPY --chown=cowrie:cowrie cowrie.cfg /cowrie/cowrie-git/etc/cowrie.cfg

# Switch back to cowrie user
USER cowrie