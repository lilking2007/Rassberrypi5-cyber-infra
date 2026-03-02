# Rassberrypi5-cyber-infra
Raspberry Pi 5 cybersecurity infrastructure: Docker-based Pi-hole DNS security, ntopng network monitoring, n8n automation, Portainer dashboard. Blue-team foundation for attack/defense homelab (Pi 5 → Dell Kali → Surface Pro 7 victim). Reproducible via docker-compose.yml.

# 🚀 My Raspberry Pi 5 Home Lab – Cybersecurity Infrastructure

**I built this self-hosted lab on my Raspberry Pi 5** to create a professional-grade monitoring, DNS security, and automation environment for my cybersecurity studies. Everything runs in Docker containers managed through Portainer – accessible from any device on my network.

This is the **foundation** for my attack/defense lab:
- **Pi 5**: Monitoring, DNS filtering, automation hub  
- **Dell Latitude i7**: Kali VMs (attacker)  
- **Surface Pro 7**: Windows victim machine

---

## 🛠 **My Hardware Setup**

Raspberry Pi 5 (8GB)
├── 256GB microSD card (Class 10 A2)
├── Official 27W USB-C power supply
├── Ethernet cable (monitoring accuracy)
└── Heatsink + fan (24/7 stability)

text

**Base OS:** Raspberry Pi OS 64-bit (Lite) – flashed with Raspberry Pi Imager

---

## 📋 **My Step-by-Step Setup Process**

### **Phase 1: Fresh OS → Docker (10 mins)**
```bash
# First boot - expand filesystem + update
sudo raspi-config  # Advanced → Expand Filesystem → Reboot

# Install Docker
curl -sSL https://get.docker.com | sh
sudo usermod -aG docker $USER
newgrp docker  # or reboot
Test: docker run hello-world ✅

Phase 2: Portainer Dashboard (My Control Center)
bash
docker volume create portainer_data
docker run -d \
  --name portainer \
  -p 9443:9443 \
  --restart=always \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v portainer_data:/data \
  portainer/portainer-ce:latest
Access: https://192.168.20.13:9443

Create admin account

Connect local Docker

Browser control ready

Phase 3: Pi-hole (Network Protection)
bash
mkdir -p ~/pihole/{etc-pihole,etc-dnsmasq.d}
Portainer → Add container:

text
Name: pihole
Image: pihole/pihole:latest
Network: host
Volumes: ~/pihole/etc-pihole:/etc/pihole, ~/pihole/etc-dnsmasq.d:/etc/dnsmasq.d
Env: TZ=Australia/Sydney, WEBPASSWORD=SecurePiHole2026!
Cap_add: NET_ADMIN
Access: http://192.168.20.13/admin

Phase 4: n8n Automation
bash
mkdir -p ~/n8n_data && sudo chown -R 1000:1000 ~/n8n_data
bash
docker run -d \
  --name n8n \
  -p 5678:5678 \
  -v ~/n8n_data:/home/node/.n8n \
  -e N8N_BASIC_AUTH_ACTIVE=true \
  -e N8N_BASIC_AUTH_USER=ryan \
  -e N8N_BASIC_AUTH_PASSWORD=SecureN8N2026! \
  n8nio/n8n:latest
Access: http://192.168.20.13:5678

Phase 5: Filebrowser
Portainer → Add:

text
Name: filebrowser
Image: filebrowser/filebrowser:latest
Ports: 8082:80
Volumes: /:/srv
Access: http://192.168.20.13:8082 (admin/admin)

Phase 6: ntopng Monitoring
bash
mkdir -p ~/ntopng_data
Portainer → Add:

text
Name: ntopng
Image: ntop/ntopng:latest
Ports: 3000:3000
Volumes: ~/ntopng_data:/var/lib/ntopng, /proc:/host/proc:ro
Network: host
Privileged: true
Access: http://192.168.20.13:3000

🎯 Service Access
Service	URL	Username	Password
Portainer	https://PI_IP:9443	admin	(your choice)
Pi-hole	http://PI_IP/admin	-	SecurePiHole2026!
n8n	http://PI_IP:5678	ryan	SecureN8N2026!
Filebrowser	http://PI_IP:8082	admin	admin
ntopng	http://PI_IP:3000	admin	admin
PI_IP: hostname -I | awk '{print $1}'

🔧 My Troubleshooting Notes
Issue	My Fix
Docker permissions	newgrp docker
Pi-hole DNS	Router DNS → PI_IP
n8n permissions	sudo chown -R 1000:1000 ~/n8n_data
ntopng no traffic	Network host + Privileged true
📁 Repository Structure
text
├── docker-compose.yml
├── README.md (this file)
├── setup-guide.md (detailed notes)
├── services/ (per-service docs + screenshots)
├── scripts/
│   ├── install-all.sh
│   └── backup-config.sh
└── config/
    └── .env.example
✅ My Progress Checklist
Phase 1: Base System
 Raspberry Pi OS 64-bit flashed

 System updated (sudo apt upgrade)

 Docker installed and tested (docker run hello-world)

 User added to docker group (newgrp docker)

Phase 2: Portainer
 Portainer container running

 Dashboard accessible (https://PI_IP:9443)

 Local Docker environment connected

 Screenshot saved: services/portainer/screenshots/portainer-dashboard.png

Phase 3: Pi-hole
 Config folders created (~/pihole/)

 Pi-hole deployed via Portainer

 Admin interface accessible (http://PI_IP/admin)

 Router DNS points to Pi IP

 Screenshot saved: services/pihole/screenshots/pihole-stats.png

 Recipe generated: docker run --rm -v /var/run/docker.sock:/var/run/docker.sock ghcr.io/red5d/docker-autocompose pihole

Phase 4: n8n
 Data folder prepared (~/n8n_data)

 n8n container running

 Web UI accessible (http://PI_IP:5678)

 First workflow created

 Screenshot saved: services/n8n/screenshots/n8n-workflows.png

 Recipe generated: docker run --rm -v /var/run/docker.sock:/var/run/docker.sock ghcr.io/red5d/docker-autocompose n8n

Phase 5: Filebrowser
 Container deployed

 File manager accessible (http://PI_IP:8082)

 Screenshot saved: services/filebrowser/screenshots/filebrowser.png

 Recipe generated: docker run --rm -v /var/run/docker.sock:/var/run/docker.sock ghcr.io/red5d/docker-autocompose filebrowser

Phase 6: ntopng
 Data folder created (~/ntopng_data)

 Monitoring running

 Traffic visible (http://PI_IP:3000)

 Screenshot saved: services/ntopng/screenshots/ntopng-traffic.png

 Recipe generated: docker run --rm -v /var/run/docker.sock:/var/run/docker.sock ghcr.io/red5d/docker-autocompose ntopng

Final Step: FULL Stack Recipe
bash
# Generate COMPLETE docker-compose.yml for ALL containers
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  ghcr.io/red5d/docker-autocompose $(docker ps -q) > docker-compose.yml
🎓 My Learning Goals
Bachelor of Cybersecurity (Western Sydney University):

✅ Docker orchestration + container security

✅ Network defense (Pi-hole deployment)

⏳ Blue team monitoring (ntopng traffic analysis)

⏳ Security automation (n8n workflows)

⏳ Portfolio-ready documentation

🚀 Reproduce My Lab
bash
git clone https://github.com/lilking2007/raspberry-pi-home-lab
cd raspberry-pi-home-lab
cp config/.env.example config/.env  # Edit passwords
docker compose up -d
35 minutes from fresh SD card → production cybersecurity lab.
