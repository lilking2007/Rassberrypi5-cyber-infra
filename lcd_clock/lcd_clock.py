#!/usr/bin/env python3
"""
LCD Clock Display - Runs a 24/7 digital clock on small TFT LCD
Designed for 3.5" 480x320 displays connected via GPIO pins
"""

import os
import time
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

# LCD framebuffer device (usually /dev/fb1 for secondary display)
FRAMEBUFFER = "/dev/fb1"

# Display dimensions for 3.5" LCD (adjust if different)
WIDTH = 480
HEIGHT = 320

# Clock appearance
BG_COLOR = (0, 0, 0)  # Black background
CLOCK_COLOR = (255, 255, 255)  # White text
DATE_COLOR = (200, 200, 200)  # Light gray for date

def get_framebuffer_size():
    """Detect actual framebuffer size"""
    try:
        with open('/sys/class/graphics/fb1/virtual_size', 'r') as f:
            size = f.read().strip().split(',')
            return int(size[0]), int(size[1])
    except:
        return WIDTH, HEIGHT

def create_clock_image(width, height):
    """Create the clock display image"""
    img = Image.new('RGB', (width, height), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    # Get current time
    now = datetime.now()
    time_str = now.strftime("%H:%M:%S")
    date_str = now.strftime("%A, %B %d, %Y")
    
    # Try to load a large font for the time
    try:
        # Try different font sizes to fit the screen
        time_font_size = int(height * 0.25)  # 25% of screen height
        date_font_size = int(height * 0.08)  # 8% of screen height
        
        time_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", time_font_size)
        date_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", date_font_size)
    except:
        # Fallback to default font
        time_font = ImageFont.load_default()
        date_font = ImageFont.load_default()
    
    # Get text bounding boxes for centering
    time_bbox = draw.textbbox((0, 0), time_str, font=time_font)
    time_width = time_bbox[2] - time_bbox[0]
    time_height = time_bbox[3] - time_bbox[1]
    
    date_bbox = draw.textbbox((0, 0), date_str, font=date_font)
    date_width = date_bbox[2] - date_bbox[0]
    date_height = date_bbox[3] - date_bbox[1]
    
    # Center the time
    time_x = (width - time_width) // 2
    time_y = (height - time_height) // 2 - date_height
    
    # Center the date below the time
    date_x = (width - date_width) // 2
    date_y = time_y + time_height + 20
    
    # Draw the time and date
    draw.text((time_x, time_y), time_str, fill=CLOCK_COLOR, font=time_font)
    draw.text((date_x, date_y), date_str, fill=DATE_COLOR, font=date_font)
    
    return img

def write_to_framebuffer(img, fb_path):
    """Write image directly to framebuffer"""
    try:
        with open(fb_path, 'wb') as fb:
            fb.write(img.tobytes())
    except Exception as e:
        print(f"Error writing to framebuffer: {e}")

def main():
    """Main clock loop"""
    print("LCD Clock starting...")
    print(f"Using framebuffer: {FRAMEBUFFER}")
    
    # Detect actual screen size
    width, height = get_framebuffer_size()
    print(f"Display size: {width}x{height}")
    
    # Check if framebuffer exists
    if not os.path.exists(FRAMEBUFFER):
        print(f"ERROR: Framebuffer {FRAMEBUFFER} not found!")
        print("Make sure your LCD drivers are installed correctly.")
        return
    
    last_second = -1
    
    try:
        while True:
            now = datetime.now()
            current_second = now.second
            
            # Only update display when second changes (reduce CPU usage)
            if current_second != last_second:
                img = create_clock_image(width, height)
                write_to_framebuffer(img, FRAMEBUFFER)
                last_second = current_second
            
            # Sleep for a short time to avoid busy waiting
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\nClock stopped by user")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
