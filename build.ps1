$key = -Join (
    (0x30..0x39) + (0x41..0x5A) + (0x61..0x7A) + '!@#$%^&*()-=_+[]{};:",.<>/?\|`~'.ToCharArray() |
    Get-Random -Count 16 |
    ForEach-Object { [Char]$_ }
)

try {
    $commitHash = (git rev-parse HEAD)
} catch {
    $commitHash = '????????????????????????????????????????'
}
$buildTime = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
Set-Content 'build-info.txt' (($commitHash, $buildTime) -join "`n") -NoNewline

pyinstaller `
    --name striker `
    --icon icon.ico `
    --onefile `
    --noconsole `
    --clean `
    --log-level WARN `
    --key $key `
    --add-data "assets;assets" `
    --add-data "font/SourceHanSerifSC-Medium.otf;font" `
    --add-data "scriptfiles;scriptfiles" `
    --add-data "sound;sound" `
    --add-data "build-info.txt;." `
    --collect-submodules lib `
    main.py