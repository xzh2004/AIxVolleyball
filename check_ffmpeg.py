#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
FFmpeg安装检查脚本
"""
import subprocess
import sys

def check_ffmpeg():
    """检查FFmpeg是否已安装"""
    print("\n" + "="*60)
    print("  🔍 FFmpeg 安装检查")
    print("="*60 + "\n")
    
    try:
        # 尝试运行ffmpeg
        result = subprocess.run(
            ['ffmpeg', '-version'], 
            capture_output=True, 
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            # 解析版本信息
            version_line = result.stdout.split('\n')[0]
            print("✅ FFmpeg 已安装！\n")
            print(f"📦 版本信息: {version_line}\n")
            print("="*60)
            print("  ✨ 太好了！现在可以生成浏览器兼容的视频了")
            print("="*60)
            print("\n🎯 下一步:")
            print("  1. 重启 Streamlit 应用")
            print("  2. 重新生成视频")
            print("  3. 视频将完美在浏览器中播放！\n")
            return True
        else:
            print("❌ FFmpeg 未正确安装\n")
            return False
            
    except FileNotFoundError:
        print("❌ FFmpeg 未安装\n")
        print("="*60)
        print("  📥 请使用以下命令安装:")
        print("="*60)
        print("\n方法1 (推荐):")
        print("  conda install ffmpeg\n")
        print("方法2:")
        print("  conda install -c conda-forge ffmpeg\n")
        print("方法3 (使用 Chocolatey):")
        print("  choco install ffmpeg\n")
        print("="*60)
        print("\n📖 详细安装指南: INSTALL_FFMPEG.md\n")
        return False
        
    except subprocess.TimeoutExpired:
        print("⚠️ FFmpeg 响应超时\n")
        return False
        
    except Exception as e:
        print(f"❌ 检查出错: {str(e)}\n")
        return False

def check_opencv_h264():
    """检查OpenCV的H.264支持"""
    print("\n" + "="*60)
    print("  🔍 OpenCV H.264 支持检查")
    print("="*60 + "\n")
    
    try:
        import cv2
        
        # 检查OpenCV版本
        print(f"📦 OpenCV 版本: {cv2.__version__}")
        
        # 检查可用的编码器
        fourcc_list = {
            'H264': cv2.VideoWriter_fourcc(*'H264'),
            'X264': cv2.VideoWriter_fourcc(*'X264'),
            'avc1': cv2.VideoWriter_fourcc(*'avc1'),
            'mp4v': cv2.VideoWriter_fourcc(*'mp4v'),
        }
        
        print("\n可用的编码器:")
        for name, fourcc in fourcc_list.items():
            print(f"  • {name}: {fourcc}")
        
        print("\n⚠️ 注意: OpenCV的H.264支持可能不完整")
        print("   推荐安装FFmpeg以获得最佳兼容性\n")
        
    except Exception as e:
        print(f"❌ 检查OpenCV出错: {str(e)}\n")

def main():
    """主函数"""
    has_ffmpeg = check_ffmpeg()
    
    if not has_ffmpeg:
        check_opencv_h264()
        print("\n" + "="*60)
        print("  ⚠️ 建议: 立即安装FFmpeg")
        print("="*60)
        print("\n没有FFmpeg的后果:")
        print("  ❌ 视频无法在浏览器中播放")
        print("  ❌ 需要下载后查看")
        print("  ⚠️ 可能出现编码警告")
        print("\n安装FFmpeg的好处:")
        print("  ✅ 完美的浏览器兼容性")
        print("  ✅ 更好的视频质量")
        print("  ✅ 更小的文件大小")
        print("  ✅ 无警告信息\n")
        
        print("🚀 立即安装:")
        print("  conda install ffmpeg\n")
    
    print("="*60 + "\n")

if __name__ == "__main__":
    main()

