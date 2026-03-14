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

```yaml
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

```yaml
sudo raspi-config
```

Navigate to:

```
Advanced Options → Expand Filesystem → Finish → Reboot
```

## Step 1.2 – Install Docker

```yaml
sudo apt update && sudo apt upgrade -y
curl -sSL https://get.docker.com | sh
sudo usermod -aG docker $USER
newgrp docker
```

## Step 1.3 – Test Docker

```yaml
docker run hello-world
```

---

# Phase 2 – Portainer Dashboard (5 mins)

## Step 2.1 – Deploy Portainer

```yaml
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

```yaml
mkdir -p ~/pihole/{etc-pihole,etc-dnsmasq.d}
```

## Step 3.2 – Deploy in Portainer

**Container Name:** pihole  
**Image:** pihole/pihole:latest  
**Network Mode:** host  

### Volumes

```
CONTINER:/etc/pihole                                        # BIND
HOST: /home/lilking/pihole/etc-pihole:/etc/pihole         # Writable

CONTINER: /etc/dnsmasq.d                                    #BIND
HOST: /home/lilking/pihole/etc-dnsmasq.d:/etc/dnsmasq.d   # Writable
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

**Passwrod reset/set** `docker exec -it pihole pihole setpassword
`

## Step 3.4 – Router Configuration & Redundancy

To apply ad-blocking to your entire network, update your Router's LAN/DNS settings with the following:

**Primary DNS:** YOUR_PI_IP

**Secondary DNS:** 8.8.8.8 or 8.8.4.4 (Google Backup)

> **Why use a Secondary DNS?**  
> Provides a fallback (`8.8.8.8` / `8.8.4.4`) if the Raspberry Pi or Pi-hole container goes offline. Your network keeps internet access, but ads will not be blocked during that time.
---

# Phase 4 – n8n Automation (5 mins)

## Step 4.1 – Prepare Data

```yaml
mkdir -p ~/n8n_data
sudo chown -R 1000:1000 ~/n8n_data
```

## Step 4.2 – Deploy n8n

```yaml
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

## step 5.1- Prepare Folders

**create a directory**: `mkdir -p /home/USER/filebrowser_data`

## step 5.2.1 - Deploy via Portainer

**Container Name:** filebrowser  
**Image:** filebrowser/filebrowser:latest  
**Ports:** 8082:80  
**1Volume:** `/srv #(Bind) is the "Work Office" host: /`
**2Volume:** `/database #(Bind) is the "Personal Safe" host:/home/USERNAME/filebrowser_data`   
**Environment:** name`FB_DATABASE` value`/database/filebrowser.db`  
**Restart Policy:** Always  

## step 5.2.2 - Deployment via potainer using stacks 

Delet the brocken container: `docker rm -f filebrowser`

```yaml
version: '3'
services:
  filebrowser:
    image: filebrowser/filebrowser:latest
    container_name: filebrowser
    user: "0:0"  # This forces ROOT access for your cyber tools
    ports:
      - "8082:80"
    volumes:
      - /:/srv  # Full SD Card access
      - /home/lilking/filebrowser_data:/database
    environment:
      - FB_DATABASE=/database/filebrowser.db
      - FB_ROOT=/srv
    restart: always
```

## step 5.3 - Access

```
http://YOUR_PI_IP:8082
```
login:
- Go to Portainer -> Containers.
- Click the Logs icon (the little document page) next to filebrowser.
- Look for a line that says:
- User 'admin' initialized with randomly generated password: [YOUR_PASSWORD]
- Copy that password and use it to log in.

⚠ Change this immediately in production.

---

# Phase 6 – ntopng Network Monitor (5 mins)

## Option A Pro INSTALLATION "Recommended" Step 6.1 – Prepare Data

``` yaml

wget https://packages.ntop.org/RaspberryPI/apt-ntop.deb
sudo apt install ./apt-ntop.deb
sudo apt update

```
## Step 6.2 – Install ntopng & Redis

``` yaml

sudo apt install ntopng nprobe redis-server -y

```
## Step 6.3 – Enable and Start Services

``` yaml
sudo systemctl enable redis-server ntopng
sudo systemctl start redis-server ntopng

```

## Option B INSTALLATION VIA DOCKER DEPLOYMENT Step 6.1 – Prepare Data

```yaml
mkdir -p ~/ntopng_data
```

## Step 6.2 – Deploy via Portainer

**Container Name:** ntopng  
**Image:** lucasheld/ntopng:latest

### Volumes

```
CONTAINER: /var/lib/ntopng               # BIND
HOST:      /home/lilking/ntopng_data     # Writable

CONTAINER: /host/proc                    # BIND
HOST:      /proc                         # Read-only
```

**Network Mode:** host  
**Runtime & resources:** Privileged mode = true  
**Restart Policy:** Always  

## Step 6.3/4 – Access

```
http://YOUR_PI_IP:3000
```

---

# Phase 7 – Tor Anonymity Proxy (3 mins)

---

## Step 7.1 – Prepare Data Folder

Create a persistent data directory for the Tor proxy container.

```yaml
mkdir -p ~/tor_proxy_data
```

```yaml
sudo chown -R 1000:1000 ~/tor_proxy_data
```

---

## Step 7.2 – Deploy via Portainer (Stacks)

Create a new **Portainer Stack** named:

```
tor-proxy
```

Paste the following configuration.

```yaml
version: '3.8'
services:
  tor:
    image: dperson/torproxy:latest
    container_name: tor-proxy
    restart: unless-stopped
    ports:
      - "9050:9050"  # SOCKS5 Proxy
      - "9051:9051"  # Control Port
    environment:
      - TZ=Australia/Sydney
      - SOCKS_POLICY=accept 192.168.0.0/16
    volumes:
      - /home/lilking/tor_proxy_data:/var/lib/tor
```

Deploy the stack to start the Tor proxy service.

---

## Step 7.3 – Verify Connection

Run the following command to confirm your Raspberry Pi is routing traffic through Tor.

```yaml
curl --socks5-hostname localhost:9050 https://check.torproject.org/api/ip
```

If successful, the response will show a **Tor exit node IP address**.

## Step 7.4 – Activation on the browser 

> installation of "proxy switch omega" extension 
---

# Phase 8 – OpenClaw AI Agent (The Brain)

> **Note:**  
> OpenClaw replaces NanoBot.  
> It runs on **Bare Metal** to ensure direct terminal access for managing Docker, ntopng, and system services.

---

## Step 8.1 – Install Requirements

Install **Node.js 22+**, which is required by OpenClaw.

```yaml
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
```

```yaml
sudo apt install -y nodejs
```

---

## Step 8.2 – Install OpenClaw

Install the OpenClaw AI agent.

```yaml
curl -fsSL https://openclaw.ai/install.sh | bash
```

---

## Step 8.3 – Configuration (Onboarding)

Run the interactive onboarding wizard.

```yaml
openclaw onboard
```

Follow the prompts to configure your AI provider and communication channel.

---

# 🔧 Service Access Summary

| Service | URL / Access | Default Credentials |
|--------|--------------|--------------------|
| Tor Proxy | SOCKS5: `PI_IP:9050` | No UI (Proxy only) |
| OpenClaw | http://PI_IP:18789 | Web Dashboard |
| Portainer | https://PI_IP:9443 | Admin setup |
| Pi-hole | http://PI_IP/admin | SecurePiHole2026! |
| ntopng | http://PI_IP:3000 | admin / admin |
| n8n | http://PI_IP:5678 | ryan / SecureN8N2026! |
| Filebrowser | http://PI_IP:8082 | admin (check logs) |

---

# 🔧 Issues I Fixed

| Problem | Solution |
|--------|----------|
| Tor Permission Denied | Created `~/tor_proxy_data` and applied `chown -R 1000:1000` before deployment |
| Portainer Permission Denied | Applied `newgrp docker` and `sudo chmod 666 /var/run/docker.sock` |
| Pi-hole Locked Dashboard | Reset password using `docker exec -it pihole pihole setpassword` |
| ntopng No Traffic | Enabled `network_mode: host` and `privileged: true` |
| OpenClaw File Access | Moved to **Bare Metal installation** for full system control |

---

# 🧠 Production Usage

This is my **real production cybersecurity lab**.

I use it to:

- **Monitor Attacks:** Capture traffic from Dell Kali VMs  
- **Target Simulation:** Analyze a Surface Pro 7 victim machine  
- **AI Analysis:** Use OpenClaw to summarize ntopng traffic and Pi-hole DNS logs via WhatsApp / Telegram  
- **Automated Defense:** Build advanced automation workflows in n8n to trigger alerts  

---

# 📦 Full Stack Export (Optional)

Generate a `docker-compose.yml` file from running containers to back up your stack.

```yaml
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  ghcr.io/red5d/docker-autocompose $(docker ps -q) > docker-compose.yml
```

---

# 🚀 My TRUE One-Shot Rebuild Command

After flashing **Raspberry Pi OS**, run the following commands to rebuild the entire infrastructure.

```yaml
###############################################################################
# 1. SYSTEM PREP & CORE TOOLS
###############################################################################
sudo apt update && sudo apt upgrade -y
sudo apt install git wget curl nodejs npm -y
curl -sSL https://get.docker.com | sh
sudo usermod -aG docker $USER

###############################################################################
# 2. OPENCLAW AI INSTALL (BARE METAL)
###############################################################################
# Ensure Node 22+ for OpenClaw
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt install -y nodejs
curl -fsSL https://openclaw.ai/install.sh | bash

###############################################################################
# 3. PROJECT CLONE & DIRECTORY SETUP
###############################################################################
git clone https://github.com/lilking2007/Rassberrypi5-cyber-infra.git
cd Rassberrypi5-cyber-infra
mkdir -p data/{pihole/etc-pihole,pihole/etc-dnsmasq.d,n8n,filebrowser}
sudo chown -R 1000:1000 data/n8n

###############################################################################
# 4. NTOPNG INSTALL (BARE METAL)
###############################################################################
wget https://packages.ntop.org/RaspberryPI/apt-ntop.deb
sudo apt install ./apt-ntop.deb -y
sudo apt update
sudo apt install ntopng nprobe redis-server -y
sudo systemctl enable --now redis-server ntopng

###############################################################################
# 5. LAUNCH DOCKER STACK
###############################################################################
newgrp docker <<EONG
docker compose up -d
EONG

echo "-----------------------------------------------------------------------"
echo "🚀 INFRASTRUCTURE REBUILT!"
echo "AI SETUP: Run 'openclaw onboard' to link WhatsApp."
echo "-----------------------------------------------------------------------"
```

---

🔥 Built for cybersecurity practice.  
🛡 Fully self-hosted.  
🤖 OpenClaw AI-assisted monitoring.

---
