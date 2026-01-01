# FFMPEG Instructions for Logo Resizing (Qwen3-Coder)

The following commands were used to standardize the site's logo and favicon assets. Use these as a reference for any future image manipulation tasks.

### 1. Standardize Header Logo (60px height)
This maintains the aspect ratio while ensuring the header doesn't become "fat".
```bash
ffmpeg -y -i "public/TSTR-Logo-New.png" -vf "scale=-1:60" -frames:v 1 "public/TSTR-Logo-60px.png"
```

### 2. Create Square Dashboard Icon (128x128 with padding)
Useful for square containers where cropping is undesirable.
```bash
ffmpeg -y -i "public/TSTR-Logo-New.png" -vf "scale=128:128:force_original_aspect_ratio=decrease,pad=128:128:(128-iw)/2:(128-ih)/2:color=0x000000@0" -frames:v 1 "public/TSTR-Logo-Square-128.png"
```

### 3. Fix Oversized Favicon
Standardizes a (potentially huge) image to a proper 32x32 favicon.
```bash
ffmpeg -y -i "logo.png" -vf "scale=32:32" -frames:v 1 "public/favicon-32x32.png"
```

### 4. Create Standard 64px Logo
```bash
ffmpeg -y -i "logo.png" -vf "scale=64:64" -frames:v 1 "logo-64px.png"
```

> [!TIP]
> Always use `-vframes 1` or `-frames:v 1` when outputting single images to avoid `ffmpeg` attempting to create an image sequence.
