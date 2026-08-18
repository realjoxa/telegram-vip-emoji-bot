import os
import math
import random
import shutil
import asyncio
import subprocess
from PIL import Image, ImageDraw, ImageFont
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import InputSticker, FSInputFile
from aiohttp import web

BOT_TOKEN = os.getenv("BOT_TOKEN", "7094292090:AAFKXD4K-OHIQE5NAvGrFqt5dNAdBivDs-4")
PORT = int(os.getenv("PORT", 8000))

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

TEMP_DIR = "temp_emoji"
os.makedirs(TEMP_DIR, exist_ok=True)

ANIMATION_TYPES = [
      "hacker", "millionaire", "fire", "ice", "cyberpunk",
      "blood_vip", "galaxy", "pulse", "rainbow", "electric",
      "wave", "typing", "shake", "ghost", "target",
      "money", "retrowave", "disco", "spin", "toxic"
]

def get_font(size=64):
      font_paths = [
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf",
                "arial.ttf",
                "DejaVuSans.ttf"
      ]
      for path in font_paths:
                if os.path.exists(path):
                              try:
                                                return ImageFont.truetype(path, size)
except Exception:
                continue
    return ImageFont.load_default()

def render_effect(draw, anim_type, t, frame_idx, total_frames, text, font, size):
      W, H = size
      color = (255, 255, 255, 255)
      offset_x, offset_y = 0, 0
      display_text = text
      scale_x = 1.0

    if anim_type == "hacker":
              color = (0, 255, 70, 255)
              for _ in range(8):
                            rx = random.randint(10, W - 10)
                            ry = (int(t * H * 1.5) + random.randint(0, H)) % H
                            draw.text((rx, ry), random.choice(["0", "1", "X", "Z"]), font=font, fill=(0, 255, 70, 90))

elif anim_type == "millionaire":
          gold_val = int(200 + 55 * math.sin(2 * math.pi * t))
          color = (255, gold_val, 0, 255)
          for _ in range(5):
                        px = random.randint(20, W - 20)
                        py = random.randint(20, H - 20)
                        draw.text((px, py), "✦", font=font, fill=(255, 255, 180, 180))

elif anim_type == "fire":
          color = (255, int(100 + 80 * math.sin(4 * math.pi * t)), 0, 255)
          offset_y = int(6 * math.sin(6 * math.pi * t))
          for _ in range(6):
                        fx = random.randint(40, W - 40)
                        fy = H - int((t * H * 1.2 + random.randint(0, 100)) % H)
                        draw.ellipse([fx, fy, fx + 6, fy + 6], fill=(255, 69, 0, 160))

elif anim_type == "ice":
          color = (180, 230, 255, 255)
          for _ in range(6):
                        sx = (random.randint(0, W) + int(t * 30)) % W
                        sy = (random.randint(0, H) + int(t * H)) % H
                        draw.text((sx, sy), "❄", font=font, fill=(255, 255, 255, 140))

elif anim_type == "cyberpunk":
          if frame_idx % 6 == 0:
                        offset_x = random.randint(-8, 8)
                        color = (255, 0, 128, 255)
    elif frame_idx % 6 == 1:
                  offset_x = random.randint(-4, 4)
                  color = (0, 255, 255, 255)
else:
              color = (255, 255, 0, 255)

elif anim_type == "blood_vip":
        color = (200, 0, 30, 255)
        for _ in range(4):
                      bx = random.randint(30, W - 30)
                      by = int(t * H * 1.5) % H
                      draw.ellipse([bx, by, bx + 5, by + 12], fill=(160, 0, 0, 180))

elif anim_type == "galaxy":
        color = (220, 150, 255, 255)
        angle = 2 * math.pi * t
        for r in [60, 120]:
                      gx = int(W / 2 + r * math.cos(angle))
                      gy = int(H / 2 + r * math.sin(angle))
                      draw.ellipse([gx - 3, gy - 3, gx + 3, gy + 3], fill=(255, 255, 255, 200))

elif anim_type == "pulse":
        color = (255, 50, 100, 255)
        scale_x = 0.85 + 0.25 * math.sin(2 * math.pi * t)

elif anim_type == "rainbow":
        hue = (t * 360) % 360
        r = int(127 * (1 + math.sin(math.radians(hue))))
        g = int(127 * (1 + math.sin(math.radians(hue + 120))))
        b = int(127 * (1 + math.sin(math.radians(hue + 240))))
        color = (r, g, b, 255)

elif anim_type == "electric":
        color = (130, 220, 255, 255)
        offset_x = random.randint(-3, 3)
        offset_y = random.randint(-3, 3)
        if frame_idx % 4 == 0:
                      color = (255, 255, 255, 255)

elif anim_type == "wave":
          color = (0, 200, 255, 255)
          offset_y = int(20 * math.sin(2 * math.pi * t))

elif anim_type == "typing":
          color = (240, 240, 240, 255)
          visible_len = max(1, int(len(text) * (t * 1.4)))
          display_text = text[:visible_len]
          if int(t * 8) % 2 == 0:
                        display_text += "|"

elif anim_type == "shake":
          color = (255, 140, 0, 255)
          offset_x = random.randint(-7, 7)
          offset_y = random.randint(-7, 7)

elif anim_type == "ghost":
          alpha = int(128 + 127 * math.sin(2 * math.pi * t))
          color = (200, 200, 255, alpha)

elif anim_type == "target":
          color = (255, 0, 0, 255)
          laser_y = int(t * H)
          draw.line([(0, laser_y), (W, laser_y)], fill=(255, 0, 0, 150), width=3)

elif anim_type == "money":
          color = (50, 205, 50, 255)
          for _ in range(5):
                        mx = random.randint(20, W - 20)
                        my = int((t * H + random.randint(0, H)) % H)
                        draw.text((mx, my), "$", font=font, fill=(0, 255, 0, 120))

elif anim_type == "retrowave":
          color = (255, 0, 200, 255)
          scan_y = int((t * H * 2) % H)
          draw.line([(0, scan_y), (W, scan_y)], fill=(0, 255, 255, 180), width=2)

elif anim_type == "disco":
          color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255), 255)

elif anim_type == "spin":
          color = (255, 215, 0, 255)
          scale_x = abs(math.cos(2 * math.pi * t))

elif anim_type == "toxic":
          color = (127, 255, 0, 255)
          for _ in range(5):
                        bx = random.randint(30, W - 30)
                        by = H - int((t * H + random.randint(0, 50)) % H)
                        draw.ellipse([bx, by, bx + 8, by + 8], fill=(50, 205, 50, 140))

  bbox = draw.textbbox((0, 0), display_text, font=font)
tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
x = (W - tw) // 2 + offset_x
y = (H - th) // 2 + offset_y

draw.text((x, y), display_text, font=font, fill=color)

def generate_animated_emoji(text: str, anim_type: str, output_path: str):
      fps = 20
      duration = 2
      total_frames = fps * duration
      size = (512, 512)

    frame_dir = os.path.join(TEMP_DIR, f"frames_{os.getpid()}_{anim_type}_{random.randint(1000, 9999)}")
    os.makedirs(frame_dir, exist_ok=True)

    font = get_font(64)

    for i in range(total_frames):
              img = Image.new("RGBA", size, (0, 0, 0, 0))
              draw = ImageDraw.Draw(img)
              t = i / total_frames

        render_effect(draw, anim_type, t, i, total_frames, text, font, size)
        img.save(os.path.join(frame_dir, f"frame_{i:03d}.png"))

    ffmpeg_cmd = [
              "ffmpeg", "-y",
              "-framerate", str(fps),
              "-i", os.path.join(frame_dir, "frame_%03d.png"),
              "-c:v", "libvpx-vp9",
              "-pix_fmt", "yuva420p",
              "-b:v", "150k",
              "-an",
              "-auto-alt-ref", "0",
              output_path
    ]
    subprocess.run(ffmpeg_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    shutil.rmtree(frame_dir, ignore_errors=True)

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
      await message.answer(
                "👋 **Assalomu alaykum!**\n\n"
                "Menga ismingiz yoki so'z yuboring (maksimal 12 ta harf).\n"
                "Men sizga Telegram Premium statusi uchun **20 xil uslubdagi** animatsiyali Emoji Pack yaratib beraman!"
      )

@dp.message(F.text)
async def process_name(message: types.Message):
      name = message.text.strip()
      if len(name) > 12:
                await message.reply("⚠️ Ism juda uzun! 12 tagacha harf yozing.")
                return

      status_msg = await message.reply("⏳ 20 xil animatsiyali WEBM generatsiya qilinmoqda...")

    bot_info = await bot.get_me()
    pack_name = f"pack_{message.from_user.id}_{int(asyncio.get_event_loop().time())}_by_{bot_info.username}"
    pack_title = f"{name} VIP Status Set"

    stickers_list = []
    created_files = []

    try:
              for anim in ANIMATION_TYPES:
                            file_path = os.path.join(TEMP_DIR, f"{name}_{anim}_{message.from_user.id}_{random.randint(100, 999)}.webm")
                            await asyncio.to_thread(generate_animated_emoji, name, anim, file_path)
                            created_files.append(file_path)

                  stickers_list.append(
                                    InputSticker(
                                                          sticker=FSInputFile(file_path),
                                                          emoji_list=["⭐"],
                                                          format="video"
                                    )
                  )

        await bot.create_new_sticker_set(
                      user_id=message.from_user.id,
                      name=pack_name,
                      title=pack_title,
                      stickers=stickers_list,
                      sticker_type="custom_emoji"
        )

        pack_url = f"https://t.me/addemoji/{pack_name}"
        await status_msg.edit_text(
                      f"🎉 **{name}** uchun 20 xil animatsiyali Custom Emoji to'plami tayyor!\n\n"
                      f"🔗 **To'plamni o'rnatish:** [Emoji Packni qo'shish]({pack_url})\n\n"
                      f"O'rnatib bo'lgach, profilingiz tahrirlash bo'limidan ismingiz yonidagi **Emoji Status** ga qo'yishingiz mumkin.",
                      parse_mode="Markdown"
        )

except Exception as e:
        await status_msg.edit_text(f"❌ Xatolik yuz berdi: {str(e)}")

finally:
        for f in created_files:
                      if os.path.exists(f):
                                        os.remove(f)

          async def health_check(request):
                return web.Response(text="Bot is active and running 24/7!")

async def start_webserver():
      app = web.Application()
    app.router.add_get("/", health_check)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()

async def main():
      await start_webserver()
    await dp.start_polling(bot)

if __name__ == "__main__":
      asyncio.run(main())
