import os
from src.f1002packet import FPacket
from src.hex2Ascii import Converter


def file_name(file_dir):
    files = []
    count = 1
    child_path = []
    for root, dirs, file_names in os.walk(file_dir):
        # print(root)  # 当前目录路径

        if count == 1:
            files.extend(file_names)
            child_path = dirs
        else:
            files.extend([(child_path[count - 2] + '/' + x) for x in file_names])
            # files.extend([os.path.join(child_path[count - 2], x) for x in file_names])
        count += 1
    return files


if __name__ == '__main__':
    # ans = file_name('C:\\Users\\23303\\Desktop\\电表项目\\集中器U盘安装包\\install\sge800app')
    # ans = file_name('C:\\Users\\23303\\Desktop\\电表项目\\5.项目文档\\集中器程序目标码')
    ans = file_name('C:\\Users\\23303\\Desktop\\集中器U盘安装包20190520\\集中器U盘安装包20190520\\install\\sge800app')
    print(ans)
    file_list = ['/mnt/local/' + x for x in ans]
    print(file_list)
    for x in file_list:
        path = Converter.str2reversed_space_hex(x)
        print(FPacket(path).get_assemble_packet(), '  path: ' + path, x)
