set -e

CC="${CXX:-gcc}"
CXX="${CXX:-g++}"
libExtension="${libExtension:-.so}"

$CXX \
    -std=c++17 \
    -Wall \
    -O3 \
    -flto \
    -fPIC \
    -s \
    -shared \
    ${useStatic:+-static} \
    -fvisibility=hidden \
    -o libstgnative${libExtension} \
    native/xbrz/xbrz.h \
    native/xbrz/xbrz.cpp \
    -x c native/effects/effects.c
upx --ultra-brute libstgnative${libExtension} || true