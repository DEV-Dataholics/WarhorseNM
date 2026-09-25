import os
import sys
import ftplib

FTP_SERVER = os.getenv("FTP_SERVER", "ftp.dataholics.com.mx")
FTP_USERNAME = os.getenv("FTP_USERNAME", "dev-WNM@warhorsenm.dataholics.com.mx")
FTP_PASSWORD = os.getenv("FTP_PASSWORD", "UILHDA=iDiaJ")

# HARD GUARDRAIL: Strict Project Isolation
if "warhorsenm" not in FTP_USERNAME.lower() and "dev-wnm" not in FTP_USERNAME.lower():
    raise SystemExit(
        f"FATAL SECURITY VIOLATION: WarhorseNM attempted to deploy using unauthorized FTP account '{FTP_USERNAME}'! "
        f"WarhorseNM is strictly isolated to 'dev-WNM@warhorsenm.dataholics.com.mx'. Deployment aborted immediately."
    )

def ensure_remote_dir(ftp, remote_dir):
    """Ensures a remote directory exists by creating nested parts if necessary."""
    parts = remote_dir.strip("/").split("/")
    cur = ""
    for p in parts:
        if not p:
            continue
        cur += "/" + p
        try:
            ftp.mkd(cur)
        except Exception:
            pass

def upload_dir_recursive(ftp, local_dir, remote_base):
    """Recursively uploads local directory contents to remote base."""
    for root, dirs, files in os.walk(local_dir):
        rel_path = os.path.relpath(root, local_dir).replace("\\", "/")
        target_dir = remote_base if rel_path == "." else f"{remote_base}/{rel_path}".replace("//", "/")
        ensure_remote_dir(ftp, target_dir)

        for file in files:
            local_file = os.path.join(root, file)
            remote_file = f"{target_dir}/{file}".replace("//", "/")
            print(f"Uploading: {remote_file}")
            with open(local_file, "rb") as f:
                ftp.storbinary(f"STOR {remote_file}", f)

def main():
    print(f"Connecting to {FTP_SERVER} as {FTP_USERNAME}...")
    ftp = ftplib.FTP()
    ftp.connect(FTP_SERVER, 21, timeout=60)
    ftp.login(FTP_USERNAME, FTP_PASSWORD)
    ftp.set_pasv(True)
    print("Connected successfully! Current remote directory:", ftp.pwd())

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    dist_dir = os.path.join(base_dir, "apps", "web", "dist")

    if not os.path.exists(dist_dir):
        print(f"Error: Dist directory not found at {dist_dir}")
        sys.exit(1)

    print(f"\n--- Uploading Frontend SPA ({dist_dir}) to / ---")
    upload_dir_recursive(ftp, dist_dir, "/")

    # Check if public_html exists as a subfolder and sync there as well
    remote_items = ftp.nlst()
    if "public_html" in remote_items:
        print(f"\n--- Syncing Frontend SPA to /public_html ---")
        upload_dir_recursive(ftp, dist_dir, "/public_html")

    ftp.quit()
    print("\n[SUCCESS] Deployment completed successfully!")

if __name__ == "__main__":
    main()
