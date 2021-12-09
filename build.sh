charset='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-=_+[]{};:",.<>/?\|`~'
key=""
for i in {0..15}; do
    key="${key}${charset:$(( RANDOM % ${#charset} )):1}"
done

commitHash=$(git rev-parse HEAD)
commitHash="${commitHash:-????????????????????????????????????????}"
buildTime=$(date +%Y%m%d-%H%M%S)
echo $commitHash > build-info.txt
echo -n $buildTime >> build-info.txt

pyinstaller \
    --name striker \
    --onefile \
    --noconsole \
    --clean \
    --log-level WARN \
    --key $key \
    --add-data "assets;assets" \
    --add-data "font/SourceHanSerifSC-Medium.otf;font" \
    --add-data "scriptfiles;scriptfiles" \
    --add-data "sound;sound" \
    --add-data "build-info.txt;." \
    --collect-submodules lib \
    main.py