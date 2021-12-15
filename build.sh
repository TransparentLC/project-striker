set -e

charset='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-=_+[]{};:",.<>/?\|`~'
key=""
for i in {0..15}; do
    key="${key}${charset:$(( RANDOM % ${#charset} )):1}"
done

commitHash=$(git rev-parse HEAD)
commitHash="${commitHash:-????????????????????????????????????????}"
buildTime=$(date "+%Y-%m-%d %H:%M:%S")
echo $commitHash > build-info.txt
echo -n $buildTime >> build-info.txt

pyiSeparator="${pyiSeparator:-:}"

pyinstaller \
    --name striker \
    --icon icon.ico \
    --onefile \
    --noconsole \
    --clean \
    --key $key \
    --add-data "assets${pyiSeparator}assets" \
    --add-data "font/SourceHanSerifSC-Medium.otf${pyiSeparator}font" \
    --add-data "scriptfiles${pyiSeparator}scriptfiles" \
    --add-data "sound${pyiSeparator}sound" \
    --add-data "build-info.txt${pyiSeparator}." \
    --collect-submodules lib \
    main.py