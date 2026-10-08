#version 330
#extension GL_ARB_separate_shader_objects : require

#define QUANTIZE_LIGHT 0
#define OVERRIDE_AMBIENT 0
#define STEPPED_SKY_LIGHT 1

#include <flirty_beta:general.glsl>

layout(std140) uniform LightmapInfo {
    float SkyFactor;
    float BlockFactor;
    float NightVisionFactor;
    float DarknessScale;
    float BossOverlayWorldDarkeningFactor;
    float BrightnessFactor;
    vec3 BlockLightTint;
    vec3 SkyLightColor;
    vec3 AmbientColor;
    vec3 NightVisionColor;
} lightmapInfo;

layout(location = 0) in vec2 texCoord;

layout(location = 0) out vec4 fragColor;

/*
 * Brightness slider curve. Vanilla raises it to the 4th power now, this keeps the old cube.
 */
vec3 notGamma(vec3 color) {
    float max_component = max(max(color.x, color.y), color.z);
    float max_inverted = 1.0f - max_component;
    float max_scaled = 1.0f - max_inverted * max_inverted * max_inverted;
    return color * (max_scaled / max_component);
}

void main() {
    float block_level = floor(texCoord.x * 16) / 15;

    #if STEPPED_SKY_LIGHT == 1
        float sky_subtracted = flirty_beta_sky_subtracted(lightmapInfo.SkyFactor);
        float sky_level = max(floor(texCoord.y * 16) - sky_subtracted, 0.0) / 15;
    #else
        float sky_level = floor(texCoord.y * 16) * lightmapInfo.SkyFactor / 15;
    #endif

    float light_level = max(block_level, sky_level);
    light_level = clamp(light_level, 0.0, 1.0);

    #if QUANTIZE_LIGHT == 1
        light_level = floor(light_level * 15 + 0.5) / 15;
    #endif

    #if OVERRIDE_AMBIENT == 1
        float ambient = 0.05;
    #else
        float ambient = (lightmapInfo.AmbientColor.r + lightmapInfo.AmbientColor.g + lightmapInfo.AmbientColor.b) / 3;
    #endif

    vec3 color = vec3(flirty_beta_light(light_level, max(ambient, 0.05)));

    color = mix(color, color * max(light_level, 0.4), lightmapInfo.BossOverlayWorldDarkeningFactor);

    color = color - vec3(lightmapInfo.DarknessScale);

    color = clamp(color, 0.0, 1.0);
    vec3 gamma_color = notGamma(color);
    color = mix(color, gamma_color, lightmapInfo.BrightnessFactor);

    if (lightmapInfo.NightVisionFactor > 0.0) {
        color = color + vec3(1.0) * lightmapInfo.NightVisionFactor;
    }

    fragColor = vec4(color, 1.0);
}
