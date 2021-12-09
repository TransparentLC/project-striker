key=$(cat /dev/urandom | tr -cd 'a-zA-Z0-9!@#$%^&*()-=_+[]{};:",.<>/?\|`~' | head -c 16)
commitHash=$(git rev-parse HEAD)
commitHash="${commitHash:-????????????????????????????????????????}"
buildTime=$(date +%Y%m%d-%H%M%S)
echo $commitHash > build-info.txt
echo -n $buildTime >> build-info.txt

python -O -m PyInstaller \
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