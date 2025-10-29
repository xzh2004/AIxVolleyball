"""
视频生成模块 - 生成骨架叠加视频和纯骨架动画
"""
import cv2
import numpy as np
import tempfile
import os
from pose_detector import PoseDetector


class VideoGenerator:
    """生成骨架视频的类"""
    
    def __init__(self):
        self.detector = PoseDetector()
        # MediaPipe 骨架连接定义
        self.connections = [
            # 躯干
            (11, 12),  # 左肩-右肩
            (11, 23),  # 左肩-左髋
            (12, 24),  # 右肩-右髋
            (23, 24),  # 左髋-右髋
            
            # 左臂
            (11, 13),  # 左肩-左肘
            (13, 15),  # 左肘-左腕
            
            # 右臂
            (12, 14),  # 右肩-右肘
            (14, 16),  # 右肘-右腕
            
            # 左腿
            (23, 25),  # 左髋-左膝
            (25, 27),  # 左膝-左踝
            
            # 右腿
            (24, 26),  # 右髋-右膝
            (26, 28),  # 右膝-右踝
        ]
        
        # 关键点索引映射
        self.landmark_map = {
            'left_shoulder': 11,
            'right_shoulder': 12,
            'left_elbow': 13,
            'right_elbow': 14,
            'left_wrist': 15,
            'right_wrist': 16,
            'left_hip': 23,
            'right_hip': 24,
            'left_knee': 25,
            'right_knee': 26,
            'left_ankle': 27,
            'right_ankle': 28,
        }
    
    def create_overlay_video(self, frames, sequence_result, output_path=None, fps=10):
        """
        创建骨架叠加视频（方案1）
        
        Args:
            frames: 原始视频帧列表
            sequence_result: 序列分析结果（包含每帧的landmarks）
            output_path: 输出视频路径（如果为None则创建临时文件）
            fps: 输出视频帧率
            
        Returns:
            output_path: 生成的视频文件路径
        """
        if output_path is None:
            # 使用项目目录下的output文件夹
            output_dir = 'output'
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            output_path = os.path.join(output_dir, f'volleyball_overlay_{id(sequence_result)}.mp4')
        
        # 获取视频参数
        height, width = frames[0].shape[:2]
        
        # 尝试多种编码格式，确保兼容性
        fourcc_list = [
            cv2.VideoWriter_fourcc(*'mp4v'),  # MPEG-4
            cv2.VideoWriter_fourcc(*'avc1'),  # H.264
            cv2.VideoWriter_fourcc(*'XVID'),  # Xvid
        ]
        
        out = None
        for fourcc in fourcc_list:
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
            if out.isOpened():
                break
        
        if not out or not out.isOpened():
            raise RuntimeError("无法创建视频写入器，请检查OpenCV安装")
        
        # 处理每一帧
        for idx, frame in enumerate(frames):
            try:
                # 获取该帧的landmarks
                frame_data = sequence_result['frames_data'][idx]
                landmarks = frame_data['landmarks']
                
                # 复制帧，确保是正确的数据类型
                overlay_frame = frame.copy()
                
                # 确保帧是BGR格式，uint8类型
                if overlay_frame.dtype != np.uint8:
                    overlay_frame = overlay_frame.astype(np.uint8)
                
                if landmarks:
                    # 绘制骨架
                    overlay_frame = self._draw_skeleton(overlay_frame, landmarks)
                    
                    # 添加帧信息文字
                    cv2.putText(overlay_frame, f"Frame {idx + 1}/{len(frames)}", 
                               (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                else:
                    # 未检测到姿态
                    cv2.putText(overlay_frame, f"Frame {idx + 1}/{len(frames)} - No Pose Detected", 
                               (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                
                # 写入帧（不检查返回值，因为OpenCV在Windows上返回值不可靠）
                out.write(overlay_frame)
                
            except Exception as e:
                # 如果单帧处理失败，记录但继续
                print(f"警告：处理第{idx+1}帧时出错: {str(e)}")
        
        # 释放资源
        out.release()
        
        # 验证文件是否生成
        if not os.path.exists(output_path) or os.path.getsize(output_path) == 0:
            raise RuntimeError(f"视频文件生成失败: {output_path}")
        
        return output_path
    
    def create_skeleton_video(self, sequence_result, output_path=None, fps=10, 
                             width=640, height=480, bg_color=(255, 255, 255)):
        """
        创建纯骨架动画视频（方案2）
        
        Args:
            sequence_result: 序列分析结果
            output_path: 输出视频路径
            fps: 输出视频帧率
            width: 视频宽度
            height: 视频高度
            bg_color: 背景颜色 (B, G, R)
            
        Returns:
            output_path: 生成的视频文件路径
        """
        if output_path is None:
            # 使用项目目录下的output文件夹
            output_dir = 'output'
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            output_path = os.path.join(output_dir, f'volleyball_skeleton_{id(sequence_result)}.mp4')
        
        # 尝试多种编码格式
        fourcc_list = [
            cv2.VideoWriter_fourcc(*'mp4v'),
            cv2.VideoWriter_fourcc(*'avc1'),
            cv2.VideoWriter_fourcc(*'XVID'),
        ]
        
        out = None
        for fourcc in fourcc_list:
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
            if out.isOpened():
                break
        
        if not out or not out.isOpened():
            raise RuntimeError("无法创建视频写入器")
        
        frames_data = sequence_result['frames_data']
        
        # 处理每一帧
        for idx, frame_data in enumerate(frames_data):
            try:
                # 创建白色背景
                skeleton_frame = np.ones((height, width, 3), dtype=np.uint8) * np.array(bg_color, dtype=np.uint8)
                
                landmarks = frame_data['landmarks']
                
                if landmarks:
                    # 绘制骨架（黑色，更清晰）
                    skeleton_frame = self._draw_skeleton(
                        skeleton_frame, 
                        landmarks,
                        point_color=(0, 0, 255),      # 红色关键点
                        line_color=(0, 0, 0),         # 黑色骨架线
                        point_radius=8,
                        line_thickness=3
                    )
                    
                    # 添加标题和帧信息
                    cv2.putText(skeleton_frame, "Skeleton Animation", 
                               (width//2 - 120, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), 2)
                    cv2.putText(skeleton_frame, f"Frame {idx + 1}/{len(frames_data)}", 
                               (10, height - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (100, 100, 100), 2)
                else:
                    # 未检测到姿态
                    cv2.putText(skeleton_frame, "No Pose Detected", 
                               (width//2 - 100, height//2), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)
                    cv2.putText(skeleton_frame, f"Frame {idx + 1}/{len(frames_data)}", 
                               (10, height - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (100, 100, 100), 2)
                
                # 写入帧（不检查返回值）
                out.write(skeleton_frame)
                
            except Exception as e:
                print(f"警告：处理第{idx+1}帧时出错: {str(e)}")
        
        # 释放资源
        out.release()
        
        # 验证文件
        if not os.path.exists(output_path) or os.path.getsize(output_path) == 0:
            raise RuntimeError(f"视频文件生成失败: {output_path}")
        
        return output_path
    
    def create_side_by_side_video(self, frames, sequence_result, output_path=None, fps=10):
        """
        创建左右对比视频：左侧原视频，右侧纯骨架
        
        Args:
            frames: 原始视频帧列表
            sequence_result: 序列分析结果
            output_path: 输出视频路径
            fps: 输出视频帧率
            
        Returns:
            output_path: 生成的视频文件路径
        """
        if output_path is None:
            # 使用项目目录下的output文件夹
            output_dir = 'output'
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            output_path = os.path.join(output_dir, f'volleyball_comparison_{id(sequence_result)}.mp4')
        
        # 获取视频参数
        height, width = frames[0].shape[:2]
        
        # 尝试多种编码格式
        fourcc_list = [
            cv2.VideoWriter_fourcc(*'mp4v'),
            cv2.VideoWriter_fourcc(*'avc1'),
            cv2.VideoWriter_fourcc(*'XVID'),
        ]
        
        out = None
        for fourcc in fourcc_list:
            out = cv2.VideoWriter(output_path, fourcc, fps, (width * 2, height))
            if out.isOpened():
                break
        
        if not out or not out.isOpened():
            raise RuntimeError("无法创建视频写入器")
        
        frames_data = sequence_result['frames_data']
        
        # 处理每一帧
        for idx, frame in enumerate(frames):
            landmarks = frames_data[idx]['landmarks']
            
            # 左侧：原视频 + 骨架
            left_frame = frame.copy()
            if landmarks:
                left_frame = self._draw_skeleton(left_frame, landmarks)
            cv2.putText(left_frame, "Original + Skeleton", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # 右侧：纯骨架
            right_frame = np.ones((height, width, 3), dtype=np.uint8) * 255
            if landmarks:
                right_frame = self._draw_skeleton(
                    right_frame, 
                    landmarks,
                    point_color=(0, 0, 255),
                    line_color=(0, 0, 0),
                    point_radius=8,
                    line_thickness=3
                )
            cv2.putText(right_frame, "Skeleton Only", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
            
            # 合并左右画面
            combined_frame = np.hstack([left_frame, right_frame])
            
            # 添加帧信息
            cv2.putText(combined_frame, f"Frame {idx + 1}/{len(frames)}", 
                       (width - 150, height - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            # 写入帧（不检查返回值）
            out.write(combined_frame)
        
        # 释放资源
        out.release()
        
        # 验证文件
        if not os.path.exists(output_path) or os.path.getsize(output_path) == 0:
            raise RuntimeError(f"视频文件生成失败: {output_path}")
        
        return output_path
    
    def _draw_skeleton(self, frame, landmarks, point_color=(0, 255, 0), 
                      line_color=(0, 255, 0), point_radius=5, line_thickness=2):
        """
        在帧上绘制骨架
        
        Args:
            frame: 要绘制的帧
            landmarks: 关键点字典
            point_color: 关键点颜色
            line_color: 骨架线颜色
            point_radius: 关键点半径
            line_thickness: 骨架线粗细
            
        Returns:
            绘制后的帧
        """
        height, width = frame.shape[:2]
        
        # 创建关键点位置数组（用于连线）
        points = {}
        for name, idx in self.landmark_map.items():
            if name in landmarks:
                lm = landmarks[name]
                x = int(lm['x'] * width)
                y = int(lm['y'] * height)
                visibility = lm.get('visibility', 1.0)
                
                # 只绘制可见度高的点
                if visibility > 0.5:
                    points[idx] = (x, y)
        
        # 绘制连接线
        for connection in self.connections:
            start_idx, end_idx = connection
            if start_idx in points and end_idx in points:
                cv2.line(frame, points[start_idx], points[end_idx], 
                        line_color, line_thickness)
        
        # 绘制关键点
        for idx, point in points.items():
            cv2.circle(frame, point, point_radius, point_color, -1)
            # 添加点的标注（可选）
            # cv2.putText(frame, str(idx), point, cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 255, 255), 1)
        
        return frame
    
    def create_trajectory_video(self, frames, sequence_result, output_path=None, fps=10):
        """
        创建轨迹追踪视频：显示关键点的运动轨迹
        
        Args:
            frames: 原始视频帧列表
            sequence_result: 序列分析结果
            output_path: 输出视频路径
            fps: 输出视频帧率
            
        Returns:
            output_path: 生成的视频文件路径
        """
        if output_path is None:
            # 使用项目目录下的output文件夹
            output_dir = 'output'
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            output_path = os.path.join(output_dir, f'volleyball_trajectory_{id(sequence_result)}.mp4')
        
        # 获取视频参数
        height, width = frames[0].shape[:2]
        
        # 尝试多种编码格式
        fourcc_list = [
            cv2.VideoWriter_fourcc(*'mp4v'),
            cv2.VideoWriter_fourcc(*'avc1'),
            cv2.VideoWriter_fourcc(*'XVID'),
        ]
        
        out = None
        for fourcc in fourcc_list:
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
            if out.isOpened():
                break
        
        if not out or not out.isOpened():
            raise RuntimeError("无法创建视频写入器")
        
        # 收集轨迹点
        trajectories = sequence_result['trajectories']
        
        # 处理每一帧
        for idx, frame in enumerate(frames):
            trajectory_frame = frame.copy()
            
            # 绘制当前帧之前的轨迹
            for point_name in ['left_wrist', 'right_wrist']:
                if point_name not in trajectories:
                    continue
                
                traj = trajectories[point_name]
                color = (255, 0, 0) if 'left' in point_name else (0, 0, 255)
                
                # 绘制轨迹线
                points_to_draw = []
                for i in range(min(idx + 1, len(traj['x']))):
                    x = traj['x'][i]
                    y = traj['y'][i]
                    vis = traj['visibility'][i]
                    
                    if x is not None and y is not None and vis > 0.5:
                        px = int(x * width)
                        py = int(y * height)
                        points_to_draw.append((px, py))
                
                # 绘制轨迹点和连线
                for i in range(1, len(points_to_draw)):
                    # 线条透明度渐变
                    alpha = 0.3 + 0.7 * (i / max(1, len(points_to_draw) - 1))
                    cv2.line(trajectory_frame, points_to_draw[i-1], points_to_draw[i], 
                            color, 2)
                
                # 当前点加粗显示
                if len(points_to_draw) > 0:
                    cv2.circle(trajectory_frame, points_to_draw[-1], 8, color, -1)
            
            # 绘制当前骨架
            landmarks = sequence_result['frames_data'][idx]['landmarks']
            if landmarks:
                trajectory_frame = self._draw_skeleton(trajectory_frame, landmarks, 
                                                      point_color=(0, 255, 0),
                                                      line_color=(0, 255, 0),
                                                      point_radius=5,
                                                      line_thickness=2)
            
            # 添加标题和说明
            cv2.putText(trajectory_frame, "Motion Trajectory", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
            cv2.putText(trajectory_frame, f"Frame {idx + 1}/{len(frames)}", 
                       (10, height - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            # 图例
            cv2.rectangle(trajectory_frame, (width - 150, 10), (width - 10, 80), (0, 0, 0), -1)
            cv2.putText(trajectory_frame, "Left Wrist", (width - 140, 35), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
            cv2.putText(trajectory_frame, "Right Wrist", (width - 140, 60), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
            
            # 写入帧（不检查返回值）
            out.write(trajectory_frame)
        
        # 释放资源
        out.release()
        
        # 验证文件
        if not os.path.exists(output_path) or os.path.getsize(output_path) == 0:
            raise RuntimeError(f"视频文件生成失败: {output_path}")
        
        return output_path

