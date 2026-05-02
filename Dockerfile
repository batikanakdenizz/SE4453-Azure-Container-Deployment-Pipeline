FROM python:3.11-slim

# Install SSH server
RUN apt-get update \
    && apt-get install -y --no-install-recommends openssh-server \
    && rm -rf /var/lib/apt/lists/*

# Azure App Service requires root password "Docker!" for SSH console access
RUN echo "root:Docker!" | chpasswd

COPY sshd_config /etc/ssh/sshd_config
RUN ssh-keygen -A

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY init.sh /init.sh
RUN chmod +x /init.sh

# Port 8000: web app, Port 2222: SSH
EXPOSE 8000 2222

CMD ["/init.sh"]
