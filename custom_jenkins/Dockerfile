# Use the Jenkins image as the base image
FROM jenkins/jenkins:lts

# Switch to root user to install dependencies
USER root

# Install prerequisites and Docker (use Debian's docker.io to avoid repo/codename issues)
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
      ca-certificates curl gnupg docker.io && \
    rm -rf /var/lib/apt/lists/*

# Add Jenkins user to the Docker group (create if it doesn't exist)
RUN groupadd -f docker && \
    usermod -aG docker jenkins

# Switch back to the Jenkins user
USER jenkins
