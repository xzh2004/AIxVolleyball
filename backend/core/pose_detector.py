"""
姿态识别模块 - 使用MediaPipe提取人体关键点
"""
import cv2
import mediapipe as mp
import numpy as np


class PoseDetector:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            smooth_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
    
    def detect_pose(self, image):
        """
        检测图像中的人体姿态
        
        Args:
            image: BGR格式的图像
            
        Returns:
            landmarks: 关键点坐标字典
            annotated_image: 标注后的图像
        """
        # 转换为RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # 检测姿态
        results = self.pose.process(image_rgb)
        
        # 绘制骨架
        annotated_image = image.copy()
        if results.pose_landmarks:
            self.mp_drawing.draw_landmarks(
                annotated_image,
                results.pose_landmarks,
                self.mp_pose.POSE_CONNECTIONS,
                self.mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                self.mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2)
            )
        
        # 提取关键点
        landmarks = self._extract_landmarks(results)
        
        return landmarks, annotated_image
    
    def _extract_landmarks(self, results):
        """提取关键点坐标"""
        if not results.pose_landmarks:
            return None
        
        landmarks = {}
        h, w = 1.0, 1.0  # 归一化坐标
        
        # 提取关键点
        lm = results.pose_landmarks.landmark
        
        landmarks = {
            # 躯干
            'nose': {'x': lm[0].x, 'y': lm[0].y, 'z': lm[0].z, 'visibility': lm[0].visibility},
            'left_shoulder': {'x': lm[11].x, 'y': lm[11].y, 'z': lm[11].z, 'visibility': lm[11].visibility},
            'right_shoulder': {'x': lm[12].x, 'y': lm[12].y, 'z': lm[12].z, 'visibility': lm[12].visibility},
            
            # 手臂
            'left_elbow': {'x': lm[13].x, 'y': lm[13].y, 'z': lm[13].z, 'visibility': lm[13].visibility},
            'right_elbow': {'x': lm[14].x, 'y': lm[14].y, 'z': lm[14].z, 'visibility': lm[14].visibility},
            'left_wrist': {'x': lm[15].x, 'y': lm[15].y, 'z': lm[15].z, 'visibility': lm[15].visibility},
            'right_wrist': {'x': lm[16].x, 'y': lm[16].y, 'z': lm[16].z, 'visibility': lm[16].visibility},
            
            # 髋部
            'left_hip': {'x': lm[23].x, 'y': lm[23].y, 'z': lm[23].z, 'visibility': lm[23].visibility},
            'right_hip': {'x': lm[24].x, 'y': lm[24].y, 'z': lm[24].z, 'visibility': lm[24].visibility},
            
            # 腿部
            'left_knee': {'x': lm[25].x, 'y': lm[25].y, 'z': lm[25].z, 'visibility': lm[25].visibility},
            'right_knee': {'x': lm[26].x, 'y': lm[26].y, 'z': lm[26].z, 'visibility': lm[26].visibility},
            'left_ankle': {'x': lm[27].x, 'y': lm[27].y, 'z': lm[27].z, 'visibility': lm[27].visibility},
            'right_ankle': {'x': lm[28].x, 'y': lm[28].y, 'z': lm[28].z, 'visibility': lm[28].visibility},
        }
        
        return landmarks
    
    @staticmethod
    def calculate_angle(point1, point2, point3):
        """
        计算三点之间的角度
        
        Args:
            point1, point2, point3: 字典格式 {'x': x, 'y': y}
            point2为顶点
            
        Returns:
            角度 (度)
        """
        # 转换为numpy数组
        p1 = np.array([point1['x'], point1['y']])
        p2 = np.array([point2['x'], point2['y']])
        p3 = np.array([point3['x'], point3['y']])
        
        # 计算向量
        v1 = p1 - p2
        v2 = p3 - p2
        
        # 计算角度
        cos_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2) + 1e-6)
        angle = np.arccos(np.clip(cos_angle, -1.0, 1.0))
        
        return np.degrees(angle)
    
    def __del__(self):
        self.pose.close()

