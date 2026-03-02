# Rassberrypi5-cyber-infra
Raspberry Pi 5 cybersecurity infrastructure: Docker-based Pi-hole DNS security, ntopng network monitoring, n8n automation, Portainer dashboard. Blue-team foundation for attack/defense homelab (Pi 5 → Dell Kali → Surface Pro 7 victim). Reproducible via docker-compose.yml.

# 🚀 My Raspberry Pi 5 Home Lab – Cybersecurity Infrastructure

**I built this self-hosted lab on my Raspberry Pi 5** to create a professional-grade monitoring, DNS security, and automation environment for my cybersecurity studies.

---

## 🛠 My Hardware Setup

Raspberry Pi 5 (8GB)
- ├── 1TB microSD card (Class 10 A2)
- ├── A compatible 5v USB-C power supply
- ├── Ethernet cable (monitoring accuracy)
- ├── Mini LCD touchscreen (visual aesthetic)
    - ├── Driver: LCD-show
    - ├── Resolution: 480x320
    - └── Interface: SPI
- └── Heatsink + fan (24/7 stability)

 

**Base OS:** Raspberry Pi OS 64-bit (Lite)

---

## 📋 My Complete Step-by-Step Setup

### **Phase 1: Fresh OS → Docker (10 mins)**

**Step 1.1 - First boot setup:**
sudo raspi-config

→ Advanced Options → Expand Filesystem → Finish → Reboot
 

**Step 1.2 - Install Docker:**
- sudo apt update && sudo apt upgrade -y
- curl -sSL https://get.docker.com | sh
- sudo usermod -aG docker $USER
- newgrp docker

 

**Step 1.3 - Test Docker:**
docker run hello-world

 

---

### **Phase 2: Portainer Dashboard (5 mins)**

**Step 2.1 - Create Portainer:**
- docker volume create portainer_data
- docker run -d
- --name portainer
- -p 9443:9443
- --restart=always
- -v /var/run/docker.sock:/var/run/docker.sock
- -v portainer_data:/data
- portainer/portainer-ce:latest

 

**Step 2.2 - Access dashboard:**
https://YOUR_PI_IP:9443

 
*Accept self-signed certificate → Create admin account → Connect Local Docker*

---

### **Phase 3: Pi-hole DNS Security (5 mins)**

**Step 3.1 - Prepare folders:**
mkdir -p ~/pihole/{etc-pihole,etc-dnsmasq.d}

 

**Step 3.2 - Portainer deployment:**
- Portainer → Containers → Add container
- Name: pihole
- Image: pihole/pihole:latest
- Network Mode: host
- Volumes:

/home/lilking/pihole/etc-pihole:/etc/pihole

/home/lilking/pihole/etc-dnsmasq.d:/etc/dnsmasq.d
Environment:

TZ=Australia/Sydney

WEBPASSWORD=SecurePiHole2026!

- PIHOLE_DNS_=8.8.8.8
- Capabilities: NET_ADMIN
- Restart Policy: Always

 

**Step 3.3 - Access:**
http://YOUR_PI_IP/admin

 

---

### **Phase 4: n8n Automation (5 mins)**

**Step 4.1 - Prepare data:**
- mkdir -p ~/n8n_data
- sudo chown -R 1000:1000 ~/n8n_data

 

**Step 4.2 - Deploy n8n:**
- docker run -d
- --name n8n
- -p 5678:5678
- --restart unless-stopped
- -v ~/n8n_data:/home/node/.n8n
- -e N8N_BASIC_AUTH_ACTIVE=true
- -e N8N_BASIC_AUTH_USER=ryan
- -e N8N_BASIC_AUTH_PASSWORD=SecureN8N2026!
- -e TZ=Australia/Sydney
- n8nio/n8n:latest

 

**Step 4.3 - Access:**
http://YOUR_PI_IP:5678

 

---

### **Phase 5: Filebrowser (3 mins)**

**Step 5.1 - Portainer deployment:**
- Portainer → Add container
- Name: filebrowser
- Image: filebrowser/filebrowser:latest
- Ports: 8082:80
- Volumes: /:/srv
- Environment: FB_DATABASE=/database/filebrowser.db
- Restart Policy: Always

 

**Step 5.2 - Access:**
http://YOUR_PI_IP:8082

 
*Username: admin / Password: admin*

---

### **Phase 6: ntopng Network Monitor (5 mins)**

**Step 6.1 - Prepare data:**
mkdir -p ~/ntopng_data

 

**Step 6.2 - Portainer deployment:**
- Portainer → Add container
- Name: ntopng
- Image: ntop/ntopng:latest
- Ports: 3000:3000
- Volumes:

~/ntopng_data:/var/lib/ntopng

- /proc:/host/proc:ro
- Network Mode: host
- Privileged Mode: true
- Restart Policy: Always

 

**Step 6.3 - Access:**
http://YOUR_PI_IP:3000

 

---

## 🎯 Service Access Summary

| Service      | URL                    | Username | Password            |
|--------------|-----------------------|----------|---------------------|
| Portainer    | `https://PI_IP:9443`  | admin    | (your choice)       |
| Pi-hole      | `http://PI_IP/admin`  | -        | `SecurePiHole2026!` |
| n8n          | `http://PI_IP:5678`   | ryan     | `SecureN8N2026!`    |
| Filebrowser  | `http://PI_IP:8082`   | admin    | admin               |
| ntopng       | `http://PI_IP:3000`   | admin    | admin               |

**Get PI_IP:** `hostname -I | awk '{print $1}'`

---

## ✅ My Progress Checklist

### **Phase 1: Base System**
- [ ] OS flashed + expanded
- [ ] Docker installed + tested
- [ ] Docker group access

### **Phase 2: Portainer** ⏳
- [ ] Portainer running
- [ ] Dashboard accessible
- [ ] **Recipe:** `docker run --rm -v /var/run/docker.sock:/var/run/docker.sock ghcr.io/red5d/docker-autocompose portainer`

### **Phase 3: Pi-hole** ⏳
- [ ] Folders created
- [ ] Container deployed
- [ ] Admin panel working
- [ ] **Recipe:** `docker run --rm -v /var/run/docker.sock:/var/run/docker.sock ghcr.io/red5d/docker-autocompose pihole`

### **Phase 4: n8n** ⏳
- [ ] Data folder ready
- [ ] n8n accessible
- [ ] **Recipe:** `docker run --rm -v /var/run/docker.sock:/var/run/docker.sock ghcr.io/red5d/docker-autocompose n8n`

### **Phase 5: Filebrowser** ⏳
- [ ] File manager working
- [ ] **Recipe:** `docker run --rm -v /var/run/docker.sock:/var/run/docker.sock ghcr.io/red5d/docker-autocompose filebrowser`

### **Phase 6: ntopng** ⏳
- [ ] Traffic monitoring live
- [ ] **Recipe:** `docker run --rm -v /var/run/docker.sock:/var/run/docker.sock ghcr.io/red5d/docker-autocompose ntopng`

### **FINAL: Full Stack Recipe**
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock
ghcr.io/red5d/docker-autocompose $(docker ps -q) > docker-compose.yml

 

---

## 🔧 Issues I've Fixed

| Problem                | Solution                           |
|------------------------|------------------------------------|
| Docker permissions     | `newgrp docker`                    |
| Pi-hole DNS            | Router DNS → PI_IP                 |
| n8n folder permissions | `sudo chown -R 1000:1000 ~/n8n_data` |
| ntopng no traffic      | Network `host` + Privileged `true` |

---

> **This is my real production lab.** I use it to monitor attacks from my Dell Kali VMs → Surface Pro 7 victim machine. Every single command above is exactly what I ran to build it.
