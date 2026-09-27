# BlackCat's Jailbreak Repository

A personal Cydia/APT repository for jailbreak tweaks and apps, hosted on GitHub Pages.

## Repository URL

```
https://blackcatofficialytb.github.io/jbrepo/
```

## Adding the Repository

Add this repository to your preferred package manager:

| Package Manager | Method |
|----------------|--------|
| **Cydia** | `cydia://url/https://cydia.saurik.com/api/share#?source=https://blackcatofficialytb.github.io/jbrepo/` |
| **Installer** | `installer://add/repo=https://blackcatofficialytb.github.io/jbrepo/` |
| **Sileo** | `sileo://source/https://blackcatofficialytb.github.io/jbrepo/` |
| **Zebra** | `zbra://sources/add/https://blackcatofficialytb.github.io/jbrepo/` |

Or manually add the URL: `https://blackcatofficialytb.github.io/jbrepo/`

## Repository Structure

```
jbrepo/
├── deb/                    # .deb packages
├── metadata/               # Package metadata (TOML)
│   ├── appsync_rootful.toml
│   ├── appsync_rootless.toml
│   ├── esign_jb.toml
│   └── example.toml.example
├── assets/                 # Web assets (CSS/JS)
├── web/                    # Package icons/screenshots
├── Packages                # APT package index (generated)
├── Packages.bz2            # Compressed package index
├── Release                 # Repository Release file
├── generate_repo.py        # Package index generator
└── index.html              # Repository landing page
```

## For Developers

### Adding a New Package

1. Place your `.deb` file in the `deb/` directory
2. Create a `.toml` metadata file in `metadata/` (see `example.toml.example` for format)
3. Run the generator:

```bash
python generate_repo.py
```

4. Compress the Packages file (required for APT):
```bash
# Linux/macOS
bzip2 -f -k Packages
zstd -q -c19 Packages > Packages.zst

# Windows (using 7-Zip)
7z a Packages.bz2 Packages
```

5. Commit and push - GitHub Pages will auto-deploy

### Metadata Format (TOML)

```toml
Package = "com.example.package"
Name = "Example Package"
Version = "1.0.0"
Architecture = "iphoneos-arm64"
Description = "A brief description of the package"
Maintainer = "Your Name <email@example.com>"
Author = "Author Name"
Section = "Tweaks"
Depends = "firmware (>= 14.0), mobilesubstrate"
Filename = "deb/com.example.package_1.0.0_iphoneos-arm64.deb"
Icon = "https://example.com/icon.png"
SileoDepiction = "https://example.com/depiction.json"
```

The generator automatically calculates `Size`, `MD5sum`, `SHA1`, and `SHA256` from the `.deb` file.

## License

See [LICENSE](LICENSE) for details.

---

*Based on [PoomSmart's repository template](https://github.com/PoomSmart/PoomSmart.github.io)*
