$key = -Join (
    (0x30..0x39) + (0x41..0x5A) + (0x61..0x7A) + '!@#$%^&*()-=_+[]{};:",.<>/?\|`~'.ToCharArray() |
    Get-Random -Count 16 |
    ForEach-Object { [Char]$_ }
)

$upxDir = Split-Path ((Get-Command upx).Source)
Write-Host 'UPX dir:' $upxdir

try {
    $commitHash = (git rev-parse HEAD)
} catch {
    $commitHash = '????????????????????????????????????????'
}
$buildTime = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
Set-Content 'build-info.txt' (($commitHash, $buildTime) -join "`n") -NoNewline

pyinstaller `
    --name striker `
    --icon NONE `
    --onefile `
    --noconsole `
    --clean `
    --log-level WARN `
    --upx-dir $upxDir `
    --key $key `
    --add-data "assets;assets" `
    --add-data "font;font" `
    --add-data "scriptfiles;scriptfiles" `
    --add-data "sound;sound" `
    --add-data "build-info.txt;." `
    --collect-submodules lib `
    main.py