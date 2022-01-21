#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
#include <math.h>

// Doing an SNES Mode 7 (affine transform) effect in pygame
// https://gamedev.stackexchange.com/questions/24957#answer-28764
__attribute__((visibility("default")))
void perspective_blit(
    const uint32_t *src,
    size_t srcWidth, size_t srcHeight,
    uint32_t *dest,
    size_t destWidth, size_t destHeight,
    float horizon, float fov, float scaling,
    float offsetX, float offsetY, float rotate,
    bool repeat
) {
    float sr = sin(rotate);
    float cr = cos(rotate);
    int32_t sw = srcWidth;
    int32_t sh = srcHeight;
    int32_t dw = destWidth;
    // int32_t dh = destHeight;
    int32_t sw2 = srcWidth / 2;
    int32_t sh2 = srcHeight / 2;
    int32_t dw2 = destWidth / 2;
    int32_t dh2 = destHeight / 2;

    for (int32_t y = -dh2; y < dh2; y++) {
        if (y + dh2 < horizon) {
            continue;
        }
        for (int32_t x = -dw2; x < dw2; x++) {
            float px = x;
            float py = -fov;
            float pz = y + dh2 + horizon;
            float sx = px / pz * scaling;
            float sy = py / pz * scaling;
            float rx = sx * cr - sy * sr;
            float ry = sx * sr + sy * cr;

            size_t srx = rx + sw2 + offsetX;
            size_t sry = ry + sh2 + offsetY;
            if (repeat) {
                srx %= sw;
                sry %= sh;
            } else if (srx >= srcWidth || sry >= srcHeight) {
                continue;
            }
            dest[(x + dw2) + (y + dh2) * dw] = src[srx + sry * sw];
        }
    }
}