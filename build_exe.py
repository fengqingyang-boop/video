import subprocess
import sys
import os


def check_pip():
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'pip', '--version'],
            capture_output=True,
            text=True
        )
        print(f"Pip版本: {result.stdout.strip()}")
        return True
    except Exception as e:
        print(f"检查Pip失败: {e}")
        return False


def upgrade_pip():
    print("正在升级pip...")
    try:
        subprocess.run(
            [sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip', '-i', 'https://pypi.tuna.tsinghua.edu.cn/simple'],
            check=True
        )
        print("pip升级成功")
    except subprocess.CalledProcessError as e:
        print(f"pip升级失败: {e}")


def install_dependencies():
    print("正在安装依赖包（使用清华镜像源）...")
    
    mirror_url = "https://pypi.tuna.tsinghua.edu.cn/simple"
    
    packages = [
        "PySide6",
        "pyinstaller"
    ]
    
    for package in packages:
        print(f"\n正在安装: {package}")
        try:
            result = subprocess.run(
                [sys.executable, '-m', 'pip', 'install', package, '-i', mirror_url, '--trusted-host', 'pypi.tuna.tsinghua.edu.cn'],
                check=True,
                capture_output=True,
                text=True
            )
            print(f"成功安装: {package}")
        except subprocess.CalledProcessError as e:
            print(f"安装 {package} 失败: {e}")
            print(f"错误信息: {e.stderr}")
            
            print(f"\n尝试使用阿里云镜像源安装 {package}...")
            try:
                result = subprocess.run(
                    [sys.executable, '-m', 'pip', 'install', package, '-i', 'https://mirrors.aliyun.com/pypi/simple/', '--trusted-host', 'mirrors.aliyun.com'],
                    check=True,
                    capture_output=True,
                    text=True
                )
                print(f"使用阿里云镜像成功安装: {package}")
            except subprocess.CalledProcessError as e2:
                print(f"使用阿里云镜像安装 {package} 也失败: {e2}")
                print(f"错误信息: {e2.stderr}")
                
                print(f"\n尝试使用默认源安装 {package}...")
                try:
                    result = subprocess.run(
                        [sys.executable, '-m', 'pip', 'install', package],
                        check=True,
                        capture_output=True,
                        text=True
                    )
                    print(f"使用默认源成功安装: {package}")
                except subprocess.CalledProcessError as e3:
                    print(f"所有镜像源都无法安装 {package}")
                    print(f"错误信息: {e3.stderr}")
                    return False
    return True


def build_exe():
    print("\n正在使用PyInstaller打包EXE文件...")
    
    pyinstaller_args = [
        sys.executable, '-m', 'PyInstaller',
        '--onefile',
        '--windowed',
        '--name=视频播放器',
        '--clean',
        'video_player.py'
    ]
    
    try:
        result = subprocess.run(
            pyinstaller_args,
            check=True,
            capture_output=True,
            text=True
        )
        print("打包成功！")
        return True
    except subprocess.CalledProcessError as e:
        print(f"打包失败: {e}")
        print(f"错误信息: {e.stderr}")
        return False


def main():
    print("=" * 60)
    print("视频播放器 - 环境配置与打包工具")
    print("=" * 60)
    
    print("\n步骤 1: 检查pip...")
    if not check_pip():
        print("未检测到pip，请确保Python安装正确")
        input("按回车键退出...")
        return
    
    print("\n步骤 2: 升级pip...")
    upgrade_pip()
    
    print("\n步骤 3: 安装依赖包...")
    if not install_dependencies():
        print("依赖安装失败，请检查网络连接或Python环境")
        input("按回车键退出...")
        return
    
    print("\n步骤 4: 打包EXE文件...")
    if build_exe():
        print("\n" + "=" * 60)
        print("打包完成！")
        print("EXE文件位于: dist/视频播放器.exe")
        print("=" * 60)
    else:
        print("打包失败，请检查错误信息")
    
    input("\n按回车键退出...")


if __name__ == '__main__':
    main()
