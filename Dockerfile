FROM python:3.11-slim

# Install SSH server and required tools
RUN apt-get update \
    && apt-get install -y --no-install-recommends openssh-server \
    && rm -rf /var/lib/apt/lists/*

# Set root password to "Docker!" — required by Azure App Service for SSH console access
RUN echo "root:Docker!" | chpasswd

# Copy custom SSH daemon configuration
COPY sshd_config /etc/ssh/sshd_config

# Ensure SSH host keys are generated
RUN ssh-keygen -A

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY . .

# Copy and prepare the startup script
COPY init.sh /init.sh
RUN chmod +x /init.sh

# Expose web app port and SSH port
EXPOSE 8000 2222

# Start SSH and the web server
CMD ["/init.sh"]
