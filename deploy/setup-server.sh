#!/bin/sh
# One-time setup for a fresh Ubuntu 24.04 droplet. Run as root:
#   ssh root@<droplet-ip> 'sh -s' < deploy/setup-server.sh
# Safe to re-run. Installs Docker, enables the firewall (SSH, HTTP, HTTPS only),
# adds 2 GB of swap, and creates a "deploy" user (same SSH keys as root) that owns /opt/nonhumanuser.
set -e
export DEBIAN_FRONTEND=noninteractive

# Swap: builds can run out of memory on a 1 GB droplet.
if [ ! -f /swapfile ]; then
  fallocate -l 2G /swapfile
  chmod 600 /swapfile
  mkswap /swapfile >/dev/null
  swapon /swapfile
  echo "/swapfile none swap sw 0 0" >> /etc/fstab
fi
echo vm.swappiness=10 > /etc/sysctl.d/99-swappiness.conf
sysctl -q -p /etc/sysctl.d/99-swappiness.conf

apt-get update -qq
apt-get upgrade -y -qq >/dev/null
apt-get install -y -qq ca-certificates curl git ufw unattended-upgrades >/dev/null

# Docker Engine and the compose plugin from Docker's own repository.
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" \
  > /etc/apt/sources.list.d/docker.list
apt-get update -qq
apt-get install -y -qq docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin >/dev/null
systemctl enable --now docker >/dev/null 2>&1

ufw allow OpenSSH >/dev/null
ufw allow 80/tcp >/dev/null
ufw allow 443/tcp >/dev/null
ufw allow 443/udp >/dev/null
ufw --force enable >/dev/null

id deploy >/dev/null 2>&1 || adduser --disabled-password --gecos "" deploy >/dev/null
usermod -aG docker deploy
install -d -m 700 -o deploy -g deploy /home/deploy/.ssh
install -m 600 -o deploy -g deploy /root/.ssh/authorized_keys /home/deploy/.ssh/authorized_keys
install -d -o deploy -g deploy /opt/nonhumanuser /opt/backups

echo
docker --version
docker compose version
free -h | grep -i swap
ufw status | head -8
if [ -f /var/run/reboot-required ]; then echo "Reboot recommended: run 'reboot'"; fi
