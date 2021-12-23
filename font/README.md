主要使用的字体为[思源宋体](https://github.com/adobe-fonts/source-han-serif)的 Medium 字重。

由于完整的字体文件大小较大（单个字重的 OTF 大小在 20 MB），因此并没有上传到仓库中，需要从以下链接之一下载 `SourceHanSerifSC-Medium.otf`，保存到这个目录：

* https://raw.githubusercontent.com/adobe-fonts/source-han-serif/release/OTF/SimplifiedChinese/SourceHanSerifSC-Medium.otf
* https://mirrors.cloud.tencent.com/adobe-fonts/source-han-serif/OTF/SimplifiedChinese/SourceHanSerifSC-Medium.otf
* https://mirrors.tuna.tsinghua.edu.cn/adobe-fonts/source-han-serif/OTF/SimplifiedChinese/SourceHanSerifSC-Medium.otf
* https://mirrors.sustech.edu.cn/adobe-fonts/source-han-serif/OTF/SimplifiedChinese/SourceHanSerifSC-Medium.otf
* （其他 Adobe 开源字体的镜像）

打包时使用的的是经过字体子集化处理、只保留了实际使用的字形的文件（可以减小到 300 KB 左右）。如果需要生成这个文件，可以在下载字体到任意位置后在项目根目录运行 `tool/generate-font-subset.py "**/*.py" /path/to/SourceHanSerifSC-Medium.otf font/SourceHanSerifSC-Medium.otf`。