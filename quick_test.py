"""
快速测试：直接从output文件夹读取一个视频，生成所有4种格式
"""

import cv2
import os
import sys

# 设置输出编码
sys.stdout.reconfigure(encoding='utf-8')

from video_generator import VideoGenerator
from sequence_analyzer import SequenceAnalyzer
from pose_detector import PoseDetector

def quick_test():
    print("=" * 70)
    print("[TEST] 快速测试：生成所有4种视频")
    print("=" * 70)
    
    # 查找output文件夹中的视频
    output_dir = 'output'
    if not os.path.exists(output_dir):
        print("[ERROR] output文件夹不存在")
        return
    
    video_files = [f for f in os.listdir(output_dir) if f.endswith('.mp4')]
    if not video_files:
        print("[ERROR] output文件夹中没有视频文件")
        return
    
    # 使用第一个视频文件
    test_video = os.path.join(output_dir, video_files[0])
    print(f"[VIDEO] 使用测试视频: {test_video}")
    print()
    
    # 初始化
    print("[INIT] 初始化组件...")
    detector = PoseDetector()
    analyzer = SequenceAnalyzer(detector)
    video_gen = VideoGenerator()
    print("[OK] 组件初始化完成")
    print()
    
    # 读取视频帧
    print("[READ] 读取视频帧...")
    cap = cv2.VideoCapture(test_video)
    
    frames = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
    
    cap.release()
    print(f"[OK] 成功读取 {len(frames)} 帧")
    print()
    
    # 分析序列
    print("[ANALYZE] 分析动作序列...")
    sequence_result = analyzer.analyze_sequence(frames)
    print(f"[OK] 分析完成，最佳帧索引: {sequence_result['best_frame_idx']}")
    print()
    
    # 生成所有视频
    print("=" * 70)
    print("[GENERATE] 开始生成所有视频...")
    print("=" * 70)
    print()
    
    results = []
    
    # 1. 骨架叠加视频
    print("[1/4] 生成骨架叠加视频...")
    try:
        video_path = video_gen.create_overlay_video(frames, sequence_result)
        if os.path.exists(video_path):
            file_size = os.path.getsize(video_path) / 1024
            print(f"  [OK] 成功: {os.path.basename(video_path)} ({file_size:.1f} KB)")
            results.append(("骨架叠加", video_path, file_size))
        else:
            print(f"  [ERROR] 文件不存在: {video_path}")
    except Exception as e:
        print(f"  [ERROR] 失败: {e}")
    print()
    
    # 2. 纯骨架动画
    print("[2/4] 生成纯骨架动画...")
    try:
        video_path = video_gen.create_skeleton_video(sequence_result)
        if os.path.exists(video_path):
            file_size = os.path.getsize(video_path) / 1024
            print(f"  [OK] 成功: {os.path.basename(video_path)} ({file_size:.1f} KB)")
            results.append(("纯骨架动画", video_path, file_size))
        else:
            print(f"  [ERROR] 文件不存在: {video_path}")
    except Exception as e:
        print(f"  [ERROR] 失败: {e}")
    print()
    
    # 3. 左右对比视频
    print("[3/4] 生成左右对比视频...")
    try:
        video_path = video_gen.create_side_by_side_video(frames, sequence_result)
        if os.path.exists(video_path):
            file_size = os.path.getsize(video_path) / 1024
            print(f"  [OK] 成功: {os.path.basename(video_path)} ({file_size:.1f} KB)")
            results.append(("左右对比", video_path, file_size))
        else:
            print(f"  [ERROR] 文件不存在: {video_path}")
    except Exception as e:
        print(f"  [ERROR] 失败: {e}")
    print()
    
    # 4. 轨迹追踪视频
    print("[4/4] 生成轨迹追踪视频...")
    try:
        video_path = video_gen.create_trajectory_video(frames, sequence_result)
        if os.path.exists(video_path):
            file_size = os.path.getsize(video_path) / 1024
            print(f"  [OK] 成功: {os.path.basename(video_path)} ({file_size:.1f} KB)")
            results.append(("轨迹追踪", video_path, file_size))
        else:
            print(f"  [ERROR] 文件不存在: {video_path}")
    except Exception as e:
        print(f"  [ERROR] 失败: {e}")
    print()
    
    # 显示结果摘要
    print("=" * 70)
    print("[SUMMARY] 生成结果摘要")
    print("=" * 70)
    print(f"[OK] 成功生成: {len(results)}/4 个视频")
    print()
    
    if results:
        print("成功生成的视频:")
        for i, (video_type, video_path, file_size) in enumerate(results, 1):
            print(f"  {i}. {video_type:12s} - {os.path.basename(video_path)} ({file_size:.1f} KB)")
        print()
    
    # 列出output文件夹所有视频
    print("=" * 70)
    print("[FILES] output文件夹所有视频文件")
    print("=" * 70)
    
    all_videos = sorted([f for f in os.listdir(output_dir) if f.endswith('.mp4')])
    
    # 统计各类型视频数量
    overlay_count = sum(1 for f in all_videos if 'overlay' in f)
    skeleton_count = sum(1 for f in all_videos if 'skeleton' in f)
    comparison_count = sum(1 for f in all_videos if 'comparison' in f)
    trajectory_count = sum(1 for f in all_videos if 'trajectory' in f)
    
    print(f"总计: {len(all_videos)} 个视频文件")
    print(f"  - 骨架叠加 (overlay):    {overlay_count} 个")
    print(f"  - 纯骨架 (skeleton):     {skeleton_count} 个")
    print(f"  - 左右对比 (comparison): {comparison_count} 个")
    print(f"  - 轨迹追踪 (trajectory): {trajectory_count} 个")
    print()
    
    print("所有文件列表:")
    for i, video_file in enumerate(all_videos, 1):
        file_path = os.path.join(output_dir, video_file)
        file_size = os.path.getsize(file_path) / 1024
        
        # 识别视频类型
        if 'overlay' in video_file:
            video_type = "骨架叠加"
        elif 'skeleton' in video_file:
            video_type = "纯骨架动画"
        elif 'comparison' in video_file:
            video_type = "左右对比"
        elif 'trajectory' in video_file:
            video_type = "轨迹追踪"
        else:
            video_type = "未知"
        
        print(f"  {i:2d}. {video_type:12s} - {video_file} ({file_size:.1f} KB)")
    
    print()
    print(f"[PATH] 文件位置: {os.path.abspath(output_dir)}")
    print()
    
    # 检查是否生成了所有类型
    print("=" * 70)
    if skeleton_count > 0 and comparison_count > 0 and trajectory_count > 0:
        print("[SUCCESS] 太好了！所有4种类型的视频都已生成！")
    else:
        print("[WARNING] 警告：还有视频类型未生成！")
        if skeleton_count == 0:
            print("  [MISSING] 缺少：纯骨架动画 (skeleton)")
        if comparison_count == 0:
            print("  [MISSING] 缺少：左右对比视频 (comparison)")
        if trajectory_count == 0:
            print("  [MISSING] 缺少：轨迹追踪视频 (trajectory)")
    print("=" * 70)

if __name__ == "__main__":
    quick_test()

