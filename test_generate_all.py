"""
测试脚本：直接生成所有4种视频
用于验证video_generator.py是否正常工作
"""

import cv2
import os
from video_generator import VideoGenerator
from sequence_analyzer import SequenceAnalyzer
from pose_detector import PoseDetector

def test_generate_all_videos():
    print("=" * 60)
    print("🎬 测试：生成所有4种视频")
    print("=" * 60)
    
    # 检查是否有测试视频
    test_videos = [f for f in os.listdir('.') if f.endswith(('.mp4', '.avi', '.mov'))]
    if not test_videos:
        print("❌ 错误：当前目录没有找到测试视频")
        print("💡 请将一个视频文件放在项目根目录")
        return
    
    test_video = test_videos[0]
    print(f"📹 使用测试视频: {test_video}")
    print()
    
    # 初始化
    print("初始化组件...")
    detector = PoseDetector()
    analyzer = SequenceAnalyzer(detector)
    video_gen = VideoGenerator()
    
    # 读取视频
    print(f"读取视频: {test_video}...")
    cap = cv2.VideoCapture(test_video)
    
    frames = []
    frame_count = 0
    max_frames = 25  # 只取前25帧用于测试
    
    while True:
        ret, frame = cap.read()
        if not ret or frame_count >= max_frames:
            break
        frames.append(frame)
        frame_count += 1
    
    cap.release()
    print(f"✅ 成功读取 {len(frames)} 帧")
    print()
    
    # 分析序列
    print("分析动作序列...")
    sequence_result = analyzer.analyze_sequence(frames)
    print(f"✅ 分析完成，最佳帧: {sequence_result['best_frame_idx']}")
    print()
    
    # 生成所有视频
    output_dir = 'output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    print("=" * 60)
    print("开始生成所有视频...")
    print("=" * 60)
    print()
    
    # 1. 骨架叠加视频
    print("1/4 生成骨架叠加视频...")
    try:
        video_path = video_gen.create_overlay_video(frames, sequence_result)
        file_size = os.path.getsize(video_path) / 1024  # KB
        print(f"✅ 成功: {video_path} ({file_size:.1f} KB)")
    except Exception as e:
        print(f"❌ 失败: {e}")
    print()
    
    # 2. 纯骨架动画
    print("2/4 生成纯骨架动画...")
    try:
        video_path = video_gen.create_skeleton_video(sequence_result)
        file_size = os.path.getsize(video_path) / 1024  # KB
        print(f"✅ 成功: {video_path} ({file_size:.1f} KB)")
    except Exception as e:
        print(f"❌ 失败: {e}")
    print()
    
    # 3. 左右对比视频
    print("3/4 生成左右对比视频...")
    try:
        video_path = video_gen.create_side_by_side_video(frames, sequence_result)
        file_size = os.path.getsize(video_path) / 1024  # KB
        print(f"✅ 成功: {video_path} ({file_size:.1f} KB)")
    except Exception as e:
        print(f"❌ 失败: {e}")
    print()
    
    # 4. 轨迹追踪视频
    print("4/4 生成轨迹追踪视频...")
    try:
        video_path = video_gen.create_trajectory_video(frames, sequence_result)
        file_size = os.path.getsize(video_path) / 1024  # KB
        print(f"✅ 成功: {video_path} ({file_size:.1f} KB)")
    except Exception as e:
        print(f"❌ 失败: {e}")
    print()
    
    # 显示最终结果
    print("=" * 60)
    print("🎉 生成完成！查看output文件夹")
    print("=" * 60)
    print()
    
    # 列出所有生成的视频
    video_files = sorted([f for f in os.listdir(output_dir) if f.endswith('.mp4')])
    print(f"📂 output文件夹包含 {len(video_files)} 个视频:")
    for i, video_file in enumerate(video_files, 1):
        file_path = os.path.join(output_dir, video_file)
        file_size = os.path.getsize(file_path) / 1024  # KB
        video_type = "未知"
        if 'overlay' in video_file:
            video_type = "骨架叠加"
        elif 'skeleton' in video_file:
            video_type = "纯骨架动画"
        elif 'comparison' in video_file:
            video_type = "左右对比"
        elif 'trajectory' in video_file:
            video_type = "轨迹追踪"
        print(f"  {i}. {video_type:10s} - {video_file} ({file_size:.1f} KB)")
    
    print()
    print(f"💡 文件位置: {os.path.abspath(output_dir)}")
    print()

if __name__ == "__main__":
    test_generate_all_videos()


