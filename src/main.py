import argparse
import os
import sys
import logging
from datetime import datetime
import shutil  # 👈 NAYA TOOLBOX ADD KIYA
import subprocess  # 👈 NAYA TOOLBOX YAHAN ADD KARNA

# 1. Diary Setup
logging.basicConfig(
    filename="/home/sandeep-yaduvanshi/Desktop/cloud_school_mlops/logs/backup.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# 2. Terminal form (Sandeep ki machine)
parser = argparse.ArgumentParser(description="SafeGuard Backup Tool")
parser.add_argument("--path", required=True, help="Folder ka rasta do")
args = parser.parse_args()

print(f"🚀 SafeGuard Initialized at {datetime.now().strftime('%H:%M:%S')}")

# 3. Rasta Check karo
if not os.path.exists(args.path):
    print(f"❌ ERROR: Folder '{args.path}' nahi mila!")
    logging.error(f"Folder not found: {args.path}")
    sys.exit(1)

# --- 🚨 SECURITY CHECK (Point 10) ---
# Jasoos ko bolo folder ke andar .env file dhundhe
env_file_rasta = os.path.join(args.path, ".env")

if os.path.exists(env_file_rasta):
    print(f"❌ SECURITY ALERT: '{args.path}' me .env file mil gayi!")
    print("⚠️ Passwords leak hone ka khatra hai. Backup Cancelled.")
    logging.critical(f"Security violation! .env file found in {args.path}. Aborting.")
    sys.exit(1) # Emergency Brake lagao!

# 4. Agar rasta mil gaya, toh BACKUP shuru karo!
print(f"✅ Folder mil gaya: {args.path}. Zipping started...")
logging.info(f"Starting backup for: {args.path}")

# Backup file ka naam aaj ki date aur time se banayenge
# Example: backup_2026-03-02_15-30-00
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
backup_filename = f"/home/sandeep-yaduvanshi/Desktop/cloud_school_mlops/backup_files/backup_{timestamp}"

# shutil function ko 3 cheezein chahiye: 
# 1. Zip file ka naam kya rakhna hai?
# 2. Format kya hoga? ("zip" ya "tar")
# 3. Kis folder ko zip karna hai? (args.path)
shutil.make_archive(backup_filename, "zip", args.path)

print(f"🎉 SUCCESS: Backup saved as {backup_filename}.zip")
logging.info(f"Backup completed successfully: {backup_filename}.zip")


print("---------------------------------")
print("🚀 Pushing backup to GitHub...")
logging.info("Starting Git auto-push...")

# Hum 'try' aur 'except' use karte hain taaki agar internet na ho 
# ya git fail ho jaye, toh script crash na ho, balki ek clean error de.
try:
    
    # 1. Git Add (Cart me daalo)
    subprocess.run(["git", "add", "."], check=True)
    
    # 2. Git Commit (Bill banao - hum isme aaj ki date bhi daal rahe hain!)
    commit_msg = f"Automated Backup: {backup_filename}"
    subprocess.run(["git", "commit", "-m", commit_msg], check=True)
    
    # 3. Git Push (Live kar do)
    subprocess.run(["git", "push"], check=True)
    
    print("✅ SUCCESS: Backup automatically pushed to GitHub!")
    logging.info("Git push completed successfully.")

except subprocess.CalledProcessError as e:
    # Agar upar teeno me se koi bhi command fail hui, toh script yahan aa jayegi
    print("❌ ERROR: Git push failed!")
    logging.error(f"Git command failed: {e}")
