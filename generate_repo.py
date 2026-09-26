import os
import glob
import hashlib

try:
    import tomllib
except ImportError:
    import tomli as tomllib

DEB_DIR = "deb"
METADATA_DIR = "metadata"
OUTPUT_PACKAGES = "Packages"

def get_file_hashes(filepath):
    """Calculates Size, MD5, SHA1, and SHA256 for a given file."""
    md5 = hashlib.md5()
    sha1 = hashlib.sha1()
    sha256 = hashlib.sha256()
    size = os.path.getsize(filepath)

    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            md5.update(chunk)
            sha1.update(chunk)
            sha256.update(chunk)

    return size, md5.hexdigest(), sha1.hexdigest(), sha256.hexdigest()

def generate_packages_file():
    packages_entries = []

    # Find all .toml files in metadata directory, excluding *.example files
    toml_files = [f for f in glob.glob(os.path.join(METADATA_DIR, "*.toml")) if not f.endswith(".example")]

    for toml_path in toml_files:
        with open(toml_path, "r", encoding="utf-8") as f:
            data = tomllib.loads(f.read())

        deb_filename = data.get("Filename")
        deb_path = os.path.join(DEB_DIR, os.path.basename(deb_filename)) if deb_filename else None

        if not deb_path or not os.path.exists(deb_path):
            print(f"[Warning] Skipping {toml_path}: Linked DEB file '{deb_path}' not found.")
            continue

        # Calculate file hashes automatically
        size, md5, sha1, sha256 = get_file_hashes(deb_path)

        # Standard Cydia / APT Control Fields
        entry = []
        entry.append(f"Package: {data.get('Package')}")
        entry.append(f"Name: {data.get('Name')}")
        entry.append(f"Version: {data.get('Version')}")
        entry.append(f"Architecture: {data.get('Architecture', 'iphoneos-arm')}")
        entry.append(f"Description: {data.get('Description', '')}")

        if "Maintainer" in data:
            entry.append(f"Maintainer: {data['Maintainer']}")
        if "Author" in data:
            entry.append(f"Author: {data['Author']}")
        if "Section" in data:
            entry.append(f"Section: {data['Section']}")
        if "Depends" in data:
            entry.append(f"Depends: {data['Depends']}")
        if "Icon" in data:
            entry.append(f"Icon: {data['Icon']}")
        if "SileoDepiction" in data:
            entry.append(f"SileoDepiction: {data['SileoDepiction']}")

        # Ensure correct relative directory path for APT clients
        relative_filename = f"{DEB_DIR}/{os.path.basename(deb_path)}"
        entry.append(f"Filename: {relative_filename}")
        entry.append(f"Size: {size}")
        entry.append(f"MD5sum: {md5}")
        entry.append(f"SHA1: {sha1}")
        entry.append(f"SHA256: {sha256}")

        packages_entries.append("\n".join(entry))

    # Write output Packages file
    with open(OUTPUT_PACKAGES, "w", encoding="utf-8") as f:
        f.write("\n\n".join(packages_entries) + "\n")

    print(f"[Success] Generated '{OUTPUT_PACKAGES}' with {len(packages_entries)} packages.")
    print("Use `bzip2 -f -k Packages` and `zstd -q -c19 Packages > Packages.zst` in Linux/MacOS")
    print("Or `7z a Packages.bz2 Packages` in Windows")

if __name__ == "__main__":
    generate_packages_file()
