from telethon import TelegramClient
from telethon.errors import *
import asyncio
import random
from datetime import datetime, timedelta
import os

# ==========================
# ENV (RAILWAY SAFE)
# ==========================
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
phone_number = os.getenv("PHONE_NUMBER")

client = TelegramClient("session_name", api_id, api_hash)

# ==========================
# GROUPS
# ==========================
groups = {
-1001845591076: "LAPAK PROMOSI",
-1002339616541: "LPM MUTUALAN (G)",
-1001898336908: "MUTUALAN INSTAGRAM LPM",
-1002388849623: "MOOTS INSTAGRAM LPM",
-1003607205167: "LPM MUTUALAN IG",
-1002172302878: "MUTUALAN INSTAGRAM",
-1003326471965: "Mutualan 7",
-1001161461117: "SALING FOLLOW INSTAGRAM",
-1002098986854: "Lpm Mutualan Ig Tiktok",
-1003284219631: "Mutual Reborn",
-1002412598040: "LPM MUTUALAN ( V )",
-1001899902692: "LPMO MUTUALANI IGI 3",
-1003709824758: "MUTUALAN IG",
-1001556464205: "LPM MUTUALAN IG",
-1002782195695: "LPM MUTUALAN ( MI )",
-1003502050045: "LPM MUTUAL REBORN",
-1002419627184: "Mutualan 10",
-1002344370068: "MUTUALAN REBUILD",
-1003977600090: "MUTUALAN TIKTOK TT #2",
-1003949605674: "MUTUALAN TIKTOK TT #5",
-1003949575198: "MUTUALAN TIKTOK TT #3",
-1003967428513: "MUTUALAN TIKTOK TT #6",
-1003937807902: "MUTUALAN TIKTOK TT #4",
-1003810812095: "MOOTS TIKTOK MUTUALAN TT #14",
-1003604586876: "MOOTS TIKTOK MUTUALAN TT #01",
-1001865044003: "SALING FOLLOW TIKTOK 2026",
-1003631658232: "MOOTS TIKTOK MUTUALAN TT #18",
-1003510110937: "MOOTS TIKTOK MUTUALAN TT #16",
-1003687062207: "MOOTS TIKTOK MUTUALAN TT #06",
-1003773740442: "MOOTS TIKTOK MUTUALAN TT #20",
-1003591223965: "MOOTS TIKTOK MUTUALAN TT #19",
-1003118874591: "MOOTS TIKTOK MUTUALAN TT #03",
-1003934119291: "MUTUALAN TIKTOK TT #7",
-1003161902664: "MOOTS IG",
-1003993826825: "MOOTS TIKTOK",
-1002857426145: "Mutualan TIKTOK TT",
-1003789805526: "MOOTS TIKTOK MUTUALAN TT #10",
-1003627932685: "MUTUALAN INSTAGRAM MOOTS IG",
-1001258278417: "MUTUALAN INSTAGRAM | MOOTS IG | SALING FOLLOW INSTAGRAM",
-1001202141403: "MUTUAL INSTAGRAM OLD",
}

# ==========================
# MESSAGES (VARIATION)
# ==========================
messages = [
"""MUTUAL INSTAGRAM, RL ONLY, NO AKUN BANTU.
BACK? DM AJA
🔗 instagram.com/noctrxksa""",

"""MUTUAL INSTAGRAM RL ONLY.
NO BOT ❌ REAL USER
DM BACK 🔗 instagram.com/noctrxksa""",

"""INSTAGRAM MUTUAL 🔥
REAL ONLY USER
BACK DM 📩 instagram.com/noctrxksa"""
]

# ==========================
# SETTINGS
# ==========================
MIN_INTERVAL_MIN = 3
MAX_INTERVAL_MIN = 5

MIN_DELAY_SEC = 2
MAX_DELAY_SEC = 3

temporary_skip = set()
slowmode_groups = {}

def now():
    return datetime.now().strftime("%H:%M:%S")

# ==========================
# SEND CYCLE
# ==========================
async def send_cycle():

    print("\n" + "=" * 50)
    print(f"[{now()}] START CYCLE")
    print("=" * 50)

    success = []
    failed = []

    available_groups = []
    current_time = datetime.now()

    for gid, gname in groups.items():

        if gid in temporary_skip:
            continue

        if gid in slowmode_groups:
            if current_time < slowmode_groups[gid]:
                continue
            del slowmode_groups[gid]

        available_groups.append((gid, gname))

    random.shuffle(available_groups)

    for group_id, group_name in available_groups:

        try:
            # ==========================
            # RANDOM MESSAGE + LABEL
            # ==========================
            msg_index = random.randint(0, len(messages) - 1)
            msg = messages[msg_index]

            delay = random.randint(MIN_DELAY_SEC, MAX_DELAY_SEC)

            print(f"Delay {delay}s -> {group_name}")
            print(f"[MSG-{msg_index + 1}] -> Sending to {group_name}")

            await asyncio.sleep(delay)

            entity = await client.get_input_entity(group_id)
            await client.send_message(entity, msg)

            print(f"[OK] SENT MSG-{msg_index + 1} -> {group_name}")

            success.append(group_name)

        except SlowModeWaitError as e:
            slowmode_groups[group_id] = datetime.now() + timedelta(seconds=e.seconds)
            print(f"[SLOWMODE] {group_name} ({e.seconds}s)")
            continue

        except FloodWaitError as e:
            print(f"[FLOODWAIT] wait {e.seconds}s")
            await asyncio.sleep(e.seconds + 1)
            continue

        except UserBannedInChannelError:
            print(f"[BANNED] {group_name}")
            temporary_skip.add(group_id)
            failed.append(group_name)

        except ChatWriteForbiddenError:
            print(f"[NO PERMISSION] {group_name}")
            temporary_skip.add(group_id)
            failed.append(group_name)

        except Exception as e:
            print(f"[ERROR] {group_name} -> {type(e).__name__}")
            failed.append(group_name)

    print("\n" + "-" * 50)
    print(f"SUCCESS: {len(success)}")
    print(f"FAILED : {len(failed)}")
    print(f"SLOW   : {len(slowmode_groups)}")
    print("-" * 50)

# ==========================
# SCHEDULER
# ==========================
async def scheduler():

    while True:
        await send_cycle()

        wait_minutes = random.randint(MIN_INTERVAL_MIN, MAX_INTERVAL_MIN)

        print(f"\nNEXT CYCLE IN {wait_minutes} MINUTES\n")

        await asyncio.sleep(wait_minutes * 60)

# ==========================
# MAIN
# ==========================
async def main():

    await client.start(phone=PHONE_NUMBER)

    me = await client.get_me()

    print("=" * 40)
    print("BOT ACTIVE")
    print(f"LOGIN: {me.first_name}")
    print("=" * 40)

    await scheduler()

# ==========================
# RUN
# ==========================
with client:
    client.loop.run_until_complete(main())
