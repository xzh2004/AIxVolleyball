# 📦 FFmpeg 安装指南

## 为什么需要FFmpeg？

FFmpeg用于将生成的视频转换为**H.264编码**的MP4格式，这是浏览器播放的标准格式。

**有FFmpeg**: ✅ 视频可以直接在浏览器中播放  
**无FFmpeg**: ⚠️ 视频需要下载后才能查看

---

## Windows 安装

### 方法1: 使用Conda（推荐）

如果你使用Anaconda或Miniconda：

```bash
conda install ffmpeg
```

### 方法2: 使用包管理器

```bash
# 使用Chocolatey
choco install ffmpeg

# 使用Scoop
scoop install ffmpeg
```

### 方法3: 手动安装

1. 访问 https://ffmpeg.org/download.html
2. 下载Windows构建版本
3. 解压到文件夹（如 `C:\ffmpeg`）
4. 添加到系统PATH：
   - 右键"此电脑" → 属性 → 高级系统设置
   - 环境变量 → 系统变量 → Path → 编辑
   - 添加 `C:\ffmpeg\bin`
5. 重启命令行窗口

### 验证安装

```bash
ffmpeg -version
```

应该看到FFmpeg的版本信息。

---

## Linux 安装

### Ubuntu/Debian

```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

### CentOS/RHEL

```bash
# 启用EPEL仓库
sudo yum install epel-release
sudo yum install ffmpeg
```

### Fedora

```bash
sudo dnf install ffmpeg
```

### 验证安装

```bash
ffmpeg -version
```

---

## macOS 安装

### 使用Homebrew（推荐）

```bash
brew install ffmpeg
```

### 使用MacPorts

```bash
sudo port install ffmpeg
```

### 验证安装

```bash
ffmpeg -version
```

---

## 验证安装成功

安装完成后，重启终端/命令行，运行：

```bash
ffmpeg -version
```

你应该看到类似输出：

```
ffmpeg version 4.4.2 Copyright (c) 2000-2021 the FFmpeg developers
built with gcc 9.3.0 (Ubuntu 9.3.0-17ubuntu1~20.04)
configuration: --prefix=/usr ...
```

---

## 在项目中测试

1. 重启你的Python环境
2. 重新启动应用：`streamlit run app.py`
3. 生成一个测试视频
4. 查看控制台，应该看到：

```
🔄 转换为浏览器兼容格式...
使用FFmpeg转换...
✅ 转换完成
```

---

## 常见问题

### Q: 安装后仍然无法找到FFmpeg？

**A**: 
1. 确保重启了终端/命令行
2. 检查PATH环境变量
3. 尝试完整路径：`C:\ffmpeg\bin\ffmpeg.exe`

### Q: conda install ffmpeg 失败？

**A**: 尝试指定channel：
```bash
conda install -c conda-forge ffmpeg
```

### Q: 权限错误？

**A**: 
- Linux/Mac: 使用sudo
- Windows: 以管理员身份运行

### Q: 不想安装FFmpeg，视频还能用吗？

**A**: 可以，但：
- ✅ 视频会生成
- ⚠️ 需要下载后用VLC等播放器查看
- ❌ 无法在浏览器中直接播放

---

## 推荐配置

安装完FFmpeg后，生成的视频将具有：

✅ **H.264编码** - 所有浏览器支持  
✅ **yuv420p像素格式** - 最佳兼容性  
✅ **faststart优化** - 更快的网络播放  
✅ **合理的文件大小** - 平衡质量和大小  

---

## 替代方案

如果实在无法安装FFmpeg，可以：

1. **手动转换**：
   - 下载生成的视频
   - 使用在线工具转换（如CloudConvert）
   - 转换为H.264编码的MP4

2. **使用VLC播放器**：
   - 下载VLC: https://www.videolan.org/
   - VLC可以播放任何格式的视频

3. **使用其他转换工具**：
   - HandBrake
   - Format Factory
   - 在线视频转换网站

---

## 总结

**强烈建议安装FFmpeg**，这样可以：
- 🎬 视频在浏览器中直接播放
- ⚡ 更好的视频质量
- 📱 更好的兼容性
- 🚀 更优化的文件

**安装只需几分钟，但能大大提升使用体验！**

---

**安装后请重启应用以使更改生效。**

