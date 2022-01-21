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

tar cf resources.tar assets font/SourceHanSerifSC-Medium.otf scriptfiles sound

pyiSeparator="${pyiSeparator:-:}"
libExtension="${libExtension:-.so}"

pyinstaller \
    --name striker \
    --icon icon.ico \
    --onefile \
    --noconsole \
    --clean \
    --key $key \
    --log-level WARN \
    --add-data "build-info.txt${pyiSeparator}." \
    --add-data "resources.tar${pyiSeparator}." \
    --add-data "libstgnative${libExtension}${pyiSeparator}." \
    main.py