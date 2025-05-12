# pylint: disable=redefined-builtin,missing-module-docstring
from sys import exit, argv
from os import remove, system
from apt.cache import Cache
from apt.debfile import DebPackage
from requests import get

# pylint: enable=redefined-builtin

rel = "stable"
url = "https://discord.com/api/download?platform=linux&format=deb"
if len(argv) == 2:
    if argv[1] not in ["stable", "ptb", "canary"]:
        exit("Invalid release, select from None, 'stable', 'ptb', or 'canary'.")
    match argv[1]:
        case "stable":
            ...
        case "ptb":
            rel = "ptb"
            url = "https://discord.com/api/download/ptb?platform=linux&format=deb"
        case "canary":
            rel = "canary"
            url = "https://discord.com/api/download/canary?platform=linux&format=deb"
        case _:
            exit("Impossible Scenario.")
elif len(argv) > 2:
    exit("Too many arguments, expected 0-1 arguments")

resp = get(url, stream=True, timeout=60)

system("clear")

with open(f"discord-{rel}.deb", mode="wb") as file:
    fileSize = int(resp.headers["Content-length"])
    downloaded = 0
    chunkSize = 10 * 1024
    print(
        f"Downloading {resp.headers['Content-length']} byte file: discord-{rel}.deb\n0/{fileSize} bytes (0%)"
    )
    for chunk in resp.iter_content(chunk_size=chunkSize):
        file.write(chunk)
        downloaded += chunkSize
        downloaded = min(downloaded, fileSize)
        percent = round((downloaded / fileSize) * 100, 2)
        print(
            f"\x1b[HDownloading {resp.headers['Content-length']} byte file: discord-{rel}.deb\n{downloaded}/{fileSize} bytes downloaded ({percent}%)"
        )

cache = Cache()
cache.update()
cache.open()

pkg = DebPackage(f"discord-{rel}.deb", cache)

ver = pkg.compare_to_version_in_cache()

if ver in [0, 3] and pkg.check():
    print(f"{'Updat' if ver else 'Install'}ing discord {rel}...")
    pkg.install()
    print(f"{'Update' if ver else 'Install'} complete!")
else:
    print("Update was not needed.")

remove(f"discord-{rel}.deb")
