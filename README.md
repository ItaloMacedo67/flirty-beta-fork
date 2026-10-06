<div align="center">
  
# Flirty Beta

Flirty Beta brings back Beta Minecraft lighting into modern versions of the game.

  **DISABLE SMOOTH LIGHTING FOR BEST EXPERIENCE**


<img width="800" alt="mc" src="https://github.com/user-attachments/assets/1ed889b7-0379-4b16-ac68-8e6191a5e777"/>

</div>

## About this fork

This is my fork of [Blobosle/flirty-beta](https://github.com/Blobosle/flirty-beta). The pack is theirs (MIT, see [LICENSE](LICENSE)), I just got it running on 26.3 because I wanted it in my modpack.

What's different:

- It works on 26.3. Mojang changed how shaders load in this version and the old lightmap wouldn't even compile, so I wanted to port it.
- Sky light now drops in steps at sunset and sunrise like it did in beta, instead of fading smoothly. Shadows at night get properly dark too. If you prefer the old smooth fade, change `STEPPED_SKY_LIGHT` to `0` in `lightmap.fsh`.
- 1.21 up to 26.1.2 still use the original shader, nothing changed there.

## Download

Grab the 26.3 zip from the [releases](https://github.com/ItaloMacedo67/flirty-beta-rust/releases). For older versions get it from the [original repo](https://github.com/Blobosle/flirty-beta/releases).

## Building

Run `./build.sh` and the zips end up in `dist/`.
