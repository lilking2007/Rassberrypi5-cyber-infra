#!/bin/bash
# LCD Clock Setup Script
# This configures your LCD screen as a dedicated clock display
# while keeping HDMI as your main monitor

set -e

echo "========================================="
echo "LCD Clock Display Setup"
echo "========================================="
echo ""

# Install required packages
echo "[1/5] Installing required packages..."
sudo apt update
sudo apt install -y python3-pip python3-pil git

# Install PIL if not already available
pip3 install Pillow --break-system-packages 2>/dev/null || pip3 install Pillow

# Clone LCD-show repository if not present
if [ ! -d "LCD-show" ]; then
    echo "[2/5] Downloading LCD drivers..."
    git clone https://github.com/goodtft/LCD-show.git
    chmod -R 755 LCD-show
fi

# Install LCD drivers WITHOUT making it the primary display
echo "[3/5] Installing LCD drivers..."
cd LCD-show

# Install the driver but don't reboot or switch displays
# We'll manually configure it to work alongside HDMI
sudo apt-mark hold raspberrypi-kernel
sudo dpkg -i -B ./usr/tft35a-overlay.deb

# Configure config.txt to enable LCD as secondary display
echo "[4/5] Configuring displays..."

# Backup original config
sudo cp /boot/firmware/config.txt /boot/firmware/config.txt.backup 2>/dev/null || \
sudo cp /boot/config.txt /boot/config.txt.backup 2>/dev/null || true

# Add LCD configuration (keeping HDMI as primary)
CONFIG_FILE="/boot/firmware/config.txt"
[ ! -f "$CONFIG_FILE" ] && CONFIG_FILE="/boot/config.txt"

# Add LCD overlay if not already present
if ! grep -q "dtoverlay=tft35a" "$CONFIG_FILE"; then
    echo "" | sudo tee -a "$CONFIG_FILE"
    echo "# LCD Display Configuration" | sudo tee -a "$CONFIG_FILE"
    echo "dtoverlay=tft35a:rotate=180" | sudo tee -a "$CONFIG_FILE"
    echo "hdmi_force_hotplug=1" | sudo tee -a "$CONFIG_FILE"
fi

cd ..

# Copy clock script to /usr/local/bin
echo "[5/5] Installing clock script..."
sudo cp lcd_clock.py /usr/local/bin/lcd_clock.py
sudo chmod +x /usr/local/bin/lcd_clock.py

# Create systemd service to run clock at startup
sudo tee /etc/systemd/system/lcd-clock.service > /dev/null <<EOF
[Unit]
Description=LCD Clock Display
After=network.target

[Service]
Type=simple
User=pi
ExecStart=/usr/bin/python3 /usr/local/bin/lcd_clock.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Enable the service
sudo systemctl daemon-reload
sudo systemctl enable lcd-clock.service

echo ""
echo "========================================="
echo "Setup Complete!"
echo "========================================="
echo ""
echo "Your LCD will display a clock after reboot."
echo "HDMI will remain your main display."
echo ""
echo "To start the clock now (after reboot):"
echo "  sudo systemctl start lcd-clock"
echo ""
echo "To view clock status:"
echo "  sudo systemctl status lcd-clock"
echo ""
echo "REBOOT NOW? (y/n)"
read -r response
if [[ "$response" =~ ^[Yy]$ ]]; then
    sudo reboot
else
    echo "Reboot manually when ready: sudo reboot"
fi
