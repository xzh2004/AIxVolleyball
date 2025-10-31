"""
轨迹可视化模块 - 绘制动作轨迹
"""
import cv2
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm
import io
from PIL import Image


class TrajectoryVisualizer:
    """可视化关键点运动轨迹"""
    
    def __init__(self):
        self.colors = {
            'left_wrist': (255, 0, 0),    # 红色
            'right_wrist': (0, 0, 255),   # 蓝色
            'left_elbow': (255, 100, 0),
            'right_elbow': (0, 100, 255),
        }
    
    def draw_trajectory_on_frame(self, frame, trajectories, current_idx=None):
        """
        在视频帧上绘制轨迹
        
        Args:
            frame: 原始帧
            trajectories: 轨迹数据
            current_idx: 当前帧索引
            
        Returns:
            绘制了轨迹的帧
        """
        result = frame.copy()
        h, w = frame.shape[:2]
        
        # 绘制主要关键点的轨迹
        key_points = ['left_wrist', 'right_wrist']
        
        for point in key_points:
            if point not in trajectories:
                continue
            
            traj = trajectories[point]
            color = self.colors.get(point, (0, 255, 0))
            
            # 转换归一化坐标到像素坐标
            points = []
            for i, (x, y, vis) in enumerate(zip(traj['x'], traj['y'], traj['visibility'])):
                if x is not None and y is not None and vis > 0.5:
                    px = int(x * w)
                    py = int(y * h)
                    points.append((px, py))
                    
                    # 绘制轨迹点
                    if current_idx is not None and i <= current_idx:
                        # 当前帧之前的点
                        alpha = 0.3 + 0.7 * (i / max(1, current_idx))
                        radius = 2 if i < current_idx else 4
                        cv2.circle(result, (px, py), radius, color, -1)
            
            # 连接轨迹线
            if len(points) > 1:
                for i in range(1, len(points)):
                    if current_idx is None or i <= current_idx:
                        cv2.line(result, points[i-1], points[i], color, 2)
        
        return result
    
    def create_trajectory_plot(self, trajectories, frame_width=640, frame_height=480):
        """
        创建2D轨迹图
        
        Args:
            trajectories: 轨迹数据
            frame_width: 视频宽度
            frame_height: 视频高度
            
        Returns:
            PIL Image对象
        """
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # 设置坐标轴
        ax.set_xlim(0, 1)
        ax.set_ylim(1, 0)  # Y轴翻转（图像坐标系）
        ax.set_aspect('equal')
        ax.set_title('关键点运动轨迹', fontsize=16, fontproperties='SimHei')
        ax.set_xlabel('水平位置', fontproperties='SimHei')
        ax.set_ylabel('垂直位置', fontproperties='SimHei')
        ax.grid(True, alpha=0.3)
        
        # 绘制主要关键点轨迹
        key_points = {
            'left_wrist': '左手腕',
            'right_wrist': '右手腕',
            'left_elbow': '左肘',
            'right_elbow': '右肘',
        }
        
        for point, label in key_points.items():
            if point not in trajectories:
                continue
            
            traj = trajectories[point]
            
            # 过滤有效点
            valid_points = [(x, y) for x, y, vis in zip(traj['x'], traj['y'], traj['visibility'])
                          if x is not None and y is not None and vis > 0.5]
            
            if len(valid_points) > 0:
                xs, ys = zip(*valid_points)
                
                # 使用颜色渐变表示时间
                colors_array = plt.cm.viridis(np.linspace(0, 1, len(xs)))
                
                # 绘制轨迹线
                ax.plot(xs, ys, '-', linewidth=2, alpha=0.6, label=label)
                
                # 绘制点（用颜色表示时间）
                ax.scatter(xs, ys, c=range(len(xs)), cmap='viridis', s=50, alpha=0.8)
                
                # 标记起点和终点
                ax.plot(xs[0], ys[0], 'go', markersize=10, label=f'{label}-起点')
                ax.plot(xs[-1], ys[-1], 'ro', markersize=10, label=f'{label}-终点')
        
        ax.legend(prop={'family': 'SimHei', 'size': 10})
        
        # 转换为图像
        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
        buf.seek(0)
        img = Image.open(buf)
        plt.close(fig)
        
        return img
    
    def create_angle_timeline(self, landmarks_list, angle_type='arm'):
        """
        创建角度时间轴图表
        
        Args:
            landmarks_list: 所有帧的关键点列表
            angle_type: 'arm' or 'knee'
            
        Returns:
            PIL Image对象
        """
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # 计算每帧的角度
        angles_left = []
        angles_right = []
        
        from .pose_detector import PoseDetector
        detector = PoseDetector()
        
        for landmarks in landmarks_list:
            if landmarks is None:
                angles_left.append(None)
                angles_right.append(None)
                continue
            
            try:
                if angle_type == 'arm':
                    # 手臂角度（肩-肘-腕）
                    left_angle = detector.calculate_angle(
                        landmarks['left_shoulder'],
                        landmarks['left_elbow'],
                        landmarks['left_wrist']
                    )
                    right_angle = detector.calculate_angle(
                        landmarks['right_shoulder'],
                        landmarks['right_elbow'],
                        landmarks['right_wrist']
                    )
                else:  # knee
                    # 膝盖角度（髋-膝-踝）
                    left_angle = detector.calculate_angle(
                        landmarks['left_hip'],
                        landmarks['left_knee'],
                        landmarks['left_ankle']
                    )
                    right_angle = detector.calculate_angle(
                        landmarks['right_hip'],
                        landmarks['right_knee'],
                        landmarks['right_ankle']
                    )
                
                angles_left.append(left_angle)
                angles_right.append(right_angle)
            except:
                angles_left.append(None)
                angles_right.append(None)
        
        # 过滤None
        frames = list(range(len(angles_left)))
        valid_left = [(i, a) for i, a in zip(frames, angles_left) if a is not None]
        valid_right = [(i, a) for i, a in zip(frames, angles_right) if a is not None]
        
        if valid_left:
            frames_left, angles_left_valid = zip(*valid_left)
            ax.plot(frames_left, angles_left_valid, 'b-o', linewidth=2, label='左侧', markersize=6)
        
        if valid_right:
            frames_right, angles_right_valid = zip(*valid_right)
            ax.plot(frames_right, angles_right_valid, 'r-o', linewidth=2, label='右侧', markersize=6)
        
        # 添加参考线（标准角度）
        if angle_type == 'arm':
            ax.axhline(y=165, color='g', linestyle='--', alpha=0.5, label='标准角度 (165°)')
            ax.set_ylabel('手臂角度 (度)', fontproperties='SimHei', fontsize=12)
            ax.set_title('手臂角度变化时间轴', fontproperties='SimHei', fontsize=14)
        else:
            ax.axhline(y=75, color='g', linestyle='--', alpha=0.5, label='标准角度 (75°)')
            ax.set_ylabel('膝盖角度 (度)', fontproperties='SimHei', fontsize=12)
            ax.set_title('膝盖角度变化时间轴', fontproperties='SimHei', fontsize=14)
        
        ax.set_xlabel('帧数', fontproperties='SimHei', fontsize=12)
        ax.legend(prop={'family': 'SimHei', 'size': 10})
        ax.grid(True, alpha=0.3)
        
        # 转换为图像
        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
        buf.seek(0)
        img = Image.open(buf)
        plt.close(fig)
        
        return img
    
    def create_comparison_view(self, frame1, frame2, title1="当前姿态", title2="标准姿态"):
        """
        创建对比视图
        
        Args:
            frame1: 第一个帧
            frame2: 第二个帧
            title1: 第一个标题
            title2: 第二个标题
            
        Returns:
            合并后的图像
        """
        h1, w1 = frame1.shape[:2]
        h2, w2 = frame2.shape[:2]
        
        # 调整尺寸一致
        target_h = max(h1, h2)
        target_w = max(w1, w2)
        
        frame1_resized = cv2.resize(frame1, (target_w, target_h))
        frame2_resized = cv2.resize(frame2, (target_w, target_h))
        
        # 添加标题
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame1_resized, title1, (10, 30), font, 1, (0, 255, 0), 2)
        cv2.putText(frame2_resized, title2, (10, 30), font, 1, (0, 255, 0), 2)
        
        # 横向拼接
        combined = np.hstack([frame1_resized, frame2_resized])
        
        return combined

