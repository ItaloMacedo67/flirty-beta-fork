#ifndef FLIRTY_BETA_GENERAL_GLSL
#define FLIRTY_BETA_GENERAL_GLSL

/*
 * Beta's light brightness table. light_level goes from 0 to 1, ambient is the darkest it gets.
 */
float flirty_beta_light(float light_level, float ambient) {
    float darkness = 1.0 - light_level;
    float lit_amount = 1.0 - darkness;
    float falloff = darkness * 3.0 + 1.0;
    return lit_amount / falloff * (1.0 - ambient) + ambient;
}

/*
 * Beta's skylightSubtracted: how many whole sky light levels the time of day takes away.
 */
float flirty_beta_sky_subtracted(float sky_factor) {
    return floor((1.0 - clamp(sky_factor, 0.0, 1.0)) * 15.0);
}

#endif
