# 项目二：文件批量归类工具
# 作用：把一个混放文件的文件夹，按文件类型自动分到 图片/文档/表格/压缩包/其他 子文件夹
# 用法：先在下面 TARGET 填要整理的文件夹；留空则整理脚本旁边的「演示文件夹」
# 运行：py 文件批量处理.py
import shutil
from pathlib import Path

# ===== 配置 =====
TARGET = ''   # 例：r'C:\Users\LENOVO\Desktop\散乱文件'

# 归类表：子文件夹名 -> 认哪些后缀（小写）
CATEGORY = {
    '图片': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'],
    '文档': ['.txt', '.doc', '.docx', '.pdf', '.md', '.ppt', '.pptx'],
    '电子书': ['.epub'],
    '音频': ['.mp3', '.wav'],
    '表格': ['.xls', '.xlsx', '.csv'],
    '压缩包': ['.zip', '.rar', '.7z'],
}


def pick_folder(ext):
    """根据后缀判断该进哪个文件夹，找不到就归到「其他」"""
    for folder, exts in CATEGORY.items():
        if ext.lower() in exts:
            return folder
    return '其他'


# 定位要整理的文件夹
base = Path(__file__).resolve().parent
target = Path(TARGET) if TARGET else base / '演示文件夹'
target.mkdir(exist_ok=True)

moved = []
# 遍历文件夹里的每一项（文件和子文件夹）
for item in target.iterdir():
    if item.is_dir():          # 子文件夹跳过，不动它
        continue
    folder = pick_folder(item.suffix)
    dest_dir = target / folder
    dest_dir.mkdir(exist_ok=True)

    dest = dest_dir / item.name
    # 重名不覆盖：自动在文件名后面加序号
    if dest.exists():
        stem, suf = item.stem, item.suffix
        n = 1
        while dest.exists():
            dest = dest_dir / f'{stem}_{n}{suf}'
            n += 1

    shutil.move(str(item), str(dest))
    moved.append(f'{item.name}  ->  {folder}/')

print(f'共整理 {len(moved)} 个文件：')
for m in moved:
    print(' ', m)
print('\n整理完成，打开「演示文件夹」即可看到分类结果。')
