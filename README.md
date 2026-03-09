# 🚀 My Raspberry Pi Home Lab – Cybersecurity Infrastructure

I built this self-hosted lab on my Raspberry Pi 5 to create a professional-grade monitoring, DNS security, automation, and AI-assisted analysis environment for my cybersecurity studies.

---

# 🛠 Hardware Setup

**Device:** Raspberry Pi 5 (8GB)

- 64gb microSD card (Class 10 A2)
- Official 5V USB-C power supply
- Ethernet connection (for monitoring accuracy)
- Mini LCD touchscreen (visual aesthetic)
- Heatsink + fan (24/7 stability)

### LCD Setup Commands

```bash
sudo rm -rf LCD-show
git clone https://github.com/goodtft/LCD-show.git
chmod -R 755 LCD-show
cd LCD-show/
sudo ./LCD35-show 180 # orientation based on screeen preference 
```

**Base OS:** Raspberry Pi OS 64-bit (Lite)  
**Core Stack:** Docker, Portainer, Pi-hole, ntopng, n8n, Filebrowser, NanoBot

---

# 📋 Complete Step-by-Step Setup

---

# Phase 1 – Fresh OS → Docker (10 mins)

## Step 1.1 – First Boot Setup

```bash
sudo raspi-config
```

Navigate to:

```
Advanced Options → Expand Filesystem → Finish → Reboot
```

## Step 1.2 – Install Docker

```bash
sudo apt update && sudo apt upgrade -y
curl -sSL https://get.docker.com | sh
sudo usermod -aG docker $USER
newgrp docker
```

## Step 1.3 – Test Docker

```bash
docker run hello-world
```

---

# Phase 2 – Portainer Dashboard (5 mins)

## Step 2.1 – Deploy Portainer

```bash
docker volume create portainer_data

docker run -d \
  --name portainer \
  -p 9443:9443 \
  --restart=always \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v portainer_data:/data \
  portainer/portainer-ce:latest
```

## Step 2.2 – Access

```
https://YOUR_PI_IP:9443
```

Accept the self-signed certificate → Create admin account → Connect Local Docker

---

# Phase 3 – Pi-hole DNS Security (5 mins)

## Step 3.1 – Prepare Folders

```bash
mkdir -p ~/pihole/{etc-pihole,etc-dnsmasq.d}
```

## Step 3.2 – Deploy in Portainer

**Container Name:** pihole  
**Image:** pihole/pihole:latest  
**Network Mode:** host  

### Volumes

```
/home/YOUR_USER/pihole/etc-pihole:/etc/pihole
/home/YOUR_USER/pihole/etc-dnsmasq.d:/etc/dnsmasq.d
```

### Environment Variables

```
TZ=Australia/Sydney
WEBPASSWORD=SecurePiHole2026!
PIHOLE_DNS_=8.8.8.8
```

**Capabilities:** NET_ADMIN  
**Restart Policy:** Always

## Step 3.3 – Access

```
http://YOUR_PI_IP/admin
```
## Step 3.4 – Router Configuration & Redundancy

To apply ad-blocking to your entire network, update your Router's LAN/DNS settings with the following:

**Primary DNS:** YOUR_PI_IP

**Secondary DNS:** 8.8.8.8 or 8.8.4.4 (Google Backup)

> **Why use a Secondary DNS?**  
> Provides a fallback (`8.8.8.8` / `8.8.4.4`) if the Raspberry Pi or Pi-hole container goes offline. Your network keeps internet access, but ads will not be blocked during that time.
---

# Phase 4 – n8n Automation (5 mins)

## Step 4.1 – Prepare Data

```bash
mkdir -p ~/n8n_data
sudo chown -R 1000:1000 ~/n8n_data
```

## Step 4.2 – Deploy n8n

```bash
version: '3.8'
services:
  n8n:
    image: n8nio/n8n:latest
    container_name: n8n
    restart: unless-stopped
    ports:
      - "5678:5678"
    volumes:
      - /home/lilking/n8n_data:/home/node/.n8n
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=ryan
      - N8N_BASIC_AUTH_PASSWORD=SecureN8N2026!
      - TZ=Australia/Sydney
      - N8N_SECURE_COOKIE=false
      - N8N_ENCRYPTION_KEY=rpi5-automation-secret-key-99
```

## Step 4.3 – Access

```
http://YOUR_PI_IP:5678
```

---

# Phase 5 – Filebrowser (3 mins)
##Prep installation

**create a directory**: `mkdir -p /home/USER/filebrowser_data`

## Deploy via Portainer

**Container Name:** filebrowser  
**Image:** filebrowser/filebrowser:latest  
**Ports:** 8082:80  
**1Volume:** `/srv #(Bind) is the "Work Office" host: /`
**2Volume:** `/database #(Bind) is the "Personal Safe" host:/home/USERNAME/filebrowser_data`   
**Environment:** name`FB_DATABASE` value`/database/filebrowser.db`  
**Restart Policy:** Always  

## Access

```
http://YOUR_PI_IP:8082
```

Default login:

```
Username: admin
Password: admin
```

⚠ Change this immediately in production.

---

# Phase 6 – ntopng Network Monitor (5 mins)

## Step 6.1 – Prepare Data

```bash
mkdir -p ~/ntopng_data
```

## Step 6.2 – Deploy via Portainer

**Container Name:** ntopng  
**Image:** ntop/ntopng:latest  
**Ports:** 3000:3000  

### Volumes

```
~/ntopng_data:/var/lib/ntopng
/proc:/host/proc:ro
```

**Network Mode:** host  
**Privileged Mode:** true  
**Restart Policy:** Always  

## Step 6.3 – Access

```
http://YOUR_PI_IP:3000
```

---

# Phase 7 – NanoBot AI Agent (5 mins)

## Step 7.1 – Prepare Data

```bash
mkdir -p ~/nanobot_data
sudo chown -R 1000:1000 ~/nanobot_data
```

## Step 7.2 – Deploy NanoBot

```bash
docker run -d \
  --name nanobot \
  -p 8085:8085 \
  --restart unless-stopped \
  -v ~/nanobot_data:/app/data \
  -e TZ=Australia/Sydney \
  -e NANO_API_KEY=YOUR_NANOBOT_KEY_HERE \
  nanobot/your-image:latest
```

## Step 7.3 – Access

```
http://YOUR_PI_IP:8085
```

NanoBot summarizes Pi-hole and ntopng logs, generates reports, and helps design new n8n automations.

---

# 🎯 Service Access Summary

| Service     | URL                     | Username | Password / Notes |
|------------|--------------------------|----------|------------------|
| Portainer  | https://PI_IP:9443       | admin    | Your choice |
| Pi-hole    | http://PI_IP/admin       | -        | SecurePiHole2026! |
| n8n        | http://PI_IP:5678        | ryan     | SecureN8N2026! |
| Filebrowser| http://PI_IP:8082        | admin    | admin (change) |
| ntopng     | http://PI_IP:3000        | admin    | admin |
| NanoBot    | http://PI_IP:8085        | -        | Requires API key |

Get your PI IP:

```bash
hostname -I | awk '{print $1}'
```

---

# 🔧 Issues I Fixed

| Problem | Solution |
|----------|----------|
| Portainer Permission Denied | Applied `newgrp docker` and `sudo chmod 666 /var/run/docker.sock` to allow the user to manage the Docker engine |
| Portainer Repository Error | Fixed the **Trixie vs Bookworm** mismatch in `/etc/apt/sources.list.d/docker.list` to allow clean updates on the Pi 5 |
| Pi-hole Locked Dashboard | Reset the forgotten admin password using `docker exec -it pihole pihole setpassword` |
| n8n Login "Cannot GET" | Added `N8N_SECURE_COOKIE=false` to the stack environment to allow access via local IP (`192.168.x.x`) |
| n8n YAML Format Error | Converted the terminal `docker run` script into a properly indented **Docker Compose stack** for the Web Editor |
| n8n Permissions | Fixed the internal `node` user access with `sudo chown -R 1000:1000 ~/n8n_data` |
| n8n Path Persistence | Updated the stack to use absolute path `/home/lilking/n8n_data` so workflows persist after reboot |
| ntopng No Traffic | Enabled `network_mode: host` and `privileged: true` so the container can see the Pi network interface |
| NanoBot File Access | Corrected directory ownership using `sudo chown -R 1000:1000 ~/nanobot_data` |

---

# 🧠 Production Usage

This is my real production cybersecurity lab.

I use it to:

- Monitor attacks from Dell Kali VMs  
- Target a Surface Pro 7 victim machine  
- Analyze logs with NanoBot  
- Generate automated reports  
- Build advanced automation workflows in n8n  

Every command above is exactly what I ran to build this stack.

---

# 📦 Full Stack Export (Optional)

Generate a docker-compose file from running containers:

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  ghcr.io/red5d/docker-autocompose $(docker ps -q) > docker-compose.yml
```

---

🔥 Built for cybersecurity practice.  
⚡ Runs 24/7.  
🛡 Fully self-hosted.  
🤖 AI-assisted monitoring.

---

# 🚀 3️⃣ My TRUE One-Shot Rebuild Command in seconds

After flashing **Raspberry Pi OS**, I can rebuild the entire infrastructure with a few commands.  
Feel free to clone and explore it in seconds.

```bash
sudo apt update && sudo apt upgrade -y

sudo apt install git -y

curl -sSL https://get.docker.com | sh

sudo usermod -aG docker $USER

newgrp docker

git clone https://github.com/lilking2007/Rassberrypi5-cyber-infra.git

cd Rassberrypi5-cyber-infra

cp .env.example .env

mkdir -p data/{pihole/etc-pihole,pihole/etc-dnsmasq.d,n8n,filebrowser,ntopng,nanobot}

sudo chown -R 1000:1000 data/n8n data/nanobot

docker compose up -d
```
**Before you run this stack**

1. Copy the template and edit your own secrets:
    ```bash
    cp .env.example .env
    nano .env
    ```
2. In `.env`, change:
    - `PIHOLE_PASSWORD=` → set your own strong Pi-hole admin password  
    - `N8N_USER=` and `N8N_PASSWORD=` → your own n8n login  
    - `NANOBOT_API_KEY=` → your own AI API key (OpenRouter or other)  
3. Save the file, then start the stack:
    ```bash
    docker compose up -d
    ```
4. **Never** commit your real `.env` back to GitHub – only `.env.example` stays in the repo.
