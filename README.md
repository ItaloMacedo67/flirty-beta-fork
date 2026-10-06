<div align="center">
  
# Flirty Beta

Flirty Beta brings back Beta Minecraft lighting into modern versions of the game.

  **DISABLE SMOOTH LIGHTING FOR BEST EXPERIENCE**


<img width="800" alt="mc" src="https://github.com/user-attachments/assets/1ed889b7-0379-4b16-ac68-8e6191a5e777"/>

</div>

## About this fork

This is a fork of [Blobosle/flirty-beta](https://github.com/Blobosle/flirty-beta) by Benjamin Lobos Lertpunyaroj, licensed under the [MIT License](LICENSE). All credit for the original pack goes to the original author.

Changes in this fork:

- **Minecraft 26.3 support** (resource pack format 97.1). The lightmap shader was ported to the new 26.3 shader pipeline (`#include`, explicit interface locations, 26.x `LightmapInfo` block).
- **Beta-style stepped sky light** on 26.3. Sky light is reduced in whole light levels, like Beta's `skylightSubtracted`, so dusk and dawn change in visible steps and shaded areas get as dark as in Beta at night. Set `STEPPED_SKY_LIGHT` to `0` in `lightmap.fsh` to use the smooth behavior instead.
- Older versions (1.21 to 26.1.2) keep the original shader from `variants/legacy`.

## Download

Check out the [releases](https://github.com/ItaloMacedo67/flirty-beta-rust/releases) to download the resource pack for Minecraft 26.3. For older versions, use the [original releases](https://github.com/Blobosle/flirty-beta/releases).

## Building

```sh
./build.sh
```

The zips for every supported version are written to `dist/`.
