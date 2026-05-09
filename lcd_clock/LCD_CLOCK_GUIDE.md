# LCD Clock Display - Setup Guide

## What This Does

Instead of using your 3.5" LCD as a full desktop (which breaks boot), this turns it into a **dedicated 24/7 clock display**:

- ✅ HDMI monitor works normally for your desktop
- ✅ LCD shows a big digital clock (white text on black background)
- ✅ No more boot sequence issues
- ✅ Clock runs automatically at startup
- ✅ Updates every second

## Installation

### Step 1: Copy files to your Raspberry Pi

```bash
# Copy lcd_clock.py and setup_lcd_clock.sh to your Pi
# You can use USB drive, scp, or recreate them on the Pi
```

### Step 2: Run the setup script

```bash
chmod +x setup_lcd_clock.sh
./setup_lcd_clock.sh
```

The script will:
1. Install required packages (Python, PIL)
2. Download LCD drivers
3. Install drivers WITHOUT breaking HDMI
4. Configure the LCD as a secondary display
5. Install the clock script
6. Set up auto-start service
7. Ask if you want to reboot

### Step 3: Reboot

```bash
sudo reboot
```

After reboot:
- Your HDMI monitor will show the desktop normally
- Your LCD will show a big digital clock

## Manual Control

### Start the clock manually:
```bash
sudo systemctl start lcd-clock
```

### Stop the clock:
```bash
sudo systemctl stop lcd-clock
```

### Check if it's running:
```bash
sudo systemctl status lcd-clock
```

### Disable auto-start:
```bash
sudo systemctl disable lcd-clock
```

### Enable auto-start:
```bash
sudo systemctl enable lcd-clock
```

## Customization

Edit `/usr/local/bin/lcd_clock.py` to customize:

### Change colors:
```python
BG_COLOR = (0, 0, 0)        # Black background (R,G,B)
CLOCK_COLOR = (255, 255, 255)  # White text
DATE_COLOR = (200, 200, 200)   # Gray date
```

### Examples:
- Blue background: `BG_COLOR = (0, 0, 50)`
- Red text: `CLOCK_COLOR = (255, 0, 0)`
- Green text: `CLOCK_COLOR = (0, 255, 0)`

### Change time format:
```python
time_str = now.strftime("%H:%M:%S")  # 24-hour with seconds
# Change to:
time_str = now.strftime("%I:%M %p")  # 12-hour AM/PM
```

### Hide the date:
Comment out the date drawing lines:
```python
# draw.text((date_x, date_y), date_str, fill=DATE_COLOR, font=date_font)
```

After making changes, restart the service:
```bash
sudo systemctl restart lcd-clock
```

## Troubleshooting

### LCD stays black after reboot:

1. Check if the service is running:
```bash
sudo systemctl status lcd-clock
```

2. Check the framebuffer:
```bash
ls -l /dev/fb*
# You should see /dev/fb0 (HDMI) and /dev/fb1 (LCD)
```

3. Test manually:
```bash
sudo python3 /usr/local/bin/lcd_clock.py
# Watch for error messages
```

### LCD shows garbled display:

The orientation might be wrong. Edit `/boot/firmware/config.txt` (or `/boot/config.txt`):

```bash
sudo nano /boot/firmware/config.txt
```

Find the line:
```
dtoverlay=tft35a:rotate=180
```

Try different values: 0, 90, 180, or 270

```bash
sudo reboot
```

### HDMI stops working:

Restore the backup config:
```bash
sudo cp /boot/firmware/config.txt.backup /boot/firmware/config.txt
sudo reboot
```

### Want to go back to using LCD-show normally:

```bash
sudo systemctl disable lcd-clock
sudo systemctl stop lcd-clock
cd LCD-show
sudo ./LCD35-show 180
```

## Display Information

The clock shows:
- **Large centered time** in HH:MM:SS format
- **Date below** showing day, month, and year
- **Updates every second**
- **Minimal CPU usage** (only redraws when time changes)

## Technical Details

- Script: `/usr/local/bin/lcd_clock.py`
- Service: `/etc/systemd/system/lcd-clock.service`
- Framebuffer: `/dev/fb1` (LCD), `/dev/fb0` (HDMI)
- Display: 480x320 or auto-detected
- Update rate: 1 Hz (every second)

## Uninstall

To remove everything:

```bash
# Stop and disable service
sudo systemctl stop lcd-clock
sudo systemctl disable lcd-clock
sudo rm /etc/systemd/system/lcd-clock.service

# Remove script
sudo rm /usr/local/bin/lcd_clock.py

# Restore original config
sudo cp /boot/firmware/config.txt.backup /boot/firmware/config.txt

# Reboot
sudo reboot
```
