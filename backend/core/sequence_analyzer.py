"""
序列分析模块 - 连续帧动作分析
"""
import numpy as np
import cv2
from .pose_detector import PoseDetector


class SequenceAnalyzer:
    """分析视频序列中的动作连贯性和轨迹"""
    
    def __init__(self):
        self.detector = PoseDetector()
    
    def analyze_sequence(self, video_path_or_frames):
        """
        分析连续帧序列
        
        Args:
            video_path_or_frames: 视频文件路径(str) 或 视频帧列表(list)
            
        Returns:
            dict: 包含所有帧的分析结果
        """
        # 判断输入类型
        if isinstance(video_path_or_frames, str):
            # 如果是字符串，认为是视频路径
            frames = self._extract_frames_from_video(video_path_or_frames)
            if frames is None or len(frames) == 0:
                return {
                    "success": False,
                    "error": "无法从视频中提取帧"
                }
        else:
            # 否则认为是帧列表
            frames = video_path_or_frames
        results = {
            'frames_data': [],  # 每帧的姿态数据
            'trajectories': {},  # 关键点轨迹
            'smoothness_score': 0,  # 流畅度得分
            'completeness_score': 0,  # 完整性得分
            'consistency_score': 0,  # 一致性得分
            'best_frame_idx': 0,  # 最佳帧索引
        }
        
        # 分析每一帧
        all_landmarks = []
        annotated_frames = []
        
        for idx, frame in enumerate(frames):
            landmarks, annotated = self.detector.detect_pose(frame)
            results['frames_data'].append({
                'frame_idx': idx,
                'landmarks': landmarks,
                'has_pose': landmarks is not None
            })
            all_landmarks.append(landmarks)
            annotated_frames.append(annotated)
        
        # 计算轨迹
        results['trajectories'] = self._calculate_trajectories(all_landmarks)
        
        # 计算流畅度
        results['smoothness_score'] = self._calculate_smoothness(all_landmarks)
        
        # 计算完整性
        results['completeness_score'] = self._calculate_completeness(all_landmarks)
        
        # 计算一致性
        results['consistency_score'] = self._calculate_consistency(all_landmarks)
        
        # 找到最佳帧（用于主要评分）
        results['best_frame_idx'] = self._find_best_frame(all_landmarks)
        
        results['annotated_frames'] = annotated_frames
        results['success'] = True  # 添加成功标志
        
        return results
    
    def _calculate_trajectories(self, landmarks_list):
        """计算关键点的运动轨迹"""
        trajectories = {}
        
        # 关键点列表
        key_points = ['left_wrist', 'right_wrist', 'left_elbow', 'right_elbow',
                     'left_shoulder', 'right_shoulder', 'left_hip', 'right_hip',
                     'left_knee', 'right_knee']
        
        for point in key_points:
            trajectory = {
                'x': [],
                'y': [],
                'visibility': []
            }
            
            for landmarks in landmarks_list:
                if landmarks and point in landmarks:
                    trajectory['x'].append(landmarks[point]['x'])
                    trajectory['y'].append(landmarks[point]['y'])
                    trajectory['visibility'].append(landmarks[point].get('visibility', 0))
                else:
                    trajectory['x'].append(None)
                    trajectory['y'].append(None)
                    trajectory['visibility'].append(0)
            
            trajectories[point] = trajectory
        
        return trajectories
    
    def _calculate_smoothness(self, landmarks_list):
        """
        计算动作流畅度
        基于关键点移动的平滑程度
        """
        if len(landmarks_list) < 3:
            return 50.0  # 帧数太少，给个中等分
        
        # 计算手腕的加速度变化（衡量流畅度）
        smoothness_scores = []
        
        for point in ['left_wrist', 'right_wrist']:
            positions = []
            for landmarks in landmarks_list:
                if landmarks and point in landmarks:
                    positions.append([landmarks[point]['x'], landmarks[point]['y']])
                else:
                    positions.append(None)
            
            # 过滤None值
            valid_positions = [p for p in positions if p is not None]
            
            if len(valid_positions) < 3:
                continue
            
            # 计算速度变化
            velocities = []
            for i in range(1, len(valid_positions)):
                dx = valid_positions[i][0] - valid_positions[i-1][0]
                dy = valid_positions[i][1] - valid_positions[i-1][1]
                velocity = np.sqrt(dx**2 + dy**2)
                velocities.append(velocity)
            
            if len(velocities) < 2:
                continue
            
            # 计算加速度变化（越小越流畅）
            accelerations = []
            for i in range(1, len(velocities)):
                acc = abs(velocities[i] - velocities[i-1])
                accelerations.append(acc)
            
            # 标准差越小越流畅
            if len(accelerations) > 0:
                std = np.std(accelerations)
                # 转换为0-100分（标准差越小分数越高）
                score = max(0, 100 - std * 1000)
                smoothness_scores.append(score)
        
        if len(smoothness_scores) == 0:
            return 50.0
        
        return np.mean(smoothness_scores)
    
    def _calculate_completeness(self, landmarks_list):
        """
        计算动作完整性
        检查是否有完整的动作序列
        """
        if len(landmarks_list) == 0:
            return 0.0
        
        # 统计有效帧的比例
        valid_frames = sum(1 for lm in landmarks_list if lm is not None)
        completeness = (valid_frames / len(landmarks_list)) * 100
        
        # 检查关键点的可见度
        if valid_frames > 0:
            avg_visibility = []
            for landmarks in landmarks_list:
                if landmarks:
                    visibilities = [landmarks[point].get('visibility', 0) 
                                  for point in ['left_wrist', 'right_wrist', 'left_shoulder', 'right_shoulder']
                                  if point in landmarks]
                    if visibilities:
                        avg_visibility.append(np.mean(visibilities))
            
            if avg_visibility:
                visibility_score = np.mean(avg_visibility) * 100
                completeness = (completeness + visibility_score) / 2
        
        return completeness
    
    def _calculate_consistency(self, landmarks_list):
        """
        计算动作一致性
        检查整个动作过程中姿态的一致性
        """
        if len(landmarks_list) < 2:
            return 50.0
        
        # 计算双臂对称性（左右手腕的相对位置）
        symmetry_scores = []
        
        for landmarks in landmarks_list:
            if not landmarks:
                continue
            
            if 'left_wrist' in landmarks and 'right_wrist' in landmarks:
                # 计算双手高度差
                height_diff = abs(landmarks['left_wrist']['y'] - landmarks['right_wrist']['y'])
                # 转换为分数（差异越小越好）
                score = max(0, 100 - height_diff * 200)
                symmetry_scores.append(score)
        
        if len(symmetry_scores) == 0:
            return 50.0
        
        # 一致性 = 对称性的稳定程度
        mean_symmetry = np.mean(symmetry_scores)
        std_symmetry = np.std(symmetry_scores)
        
        # 标准差越小说明越一致
        consistency = mean_symmetry - std_symmetry * 0.5
        
        return max(0, min(100, consistency))
    
    def _find_best_frame(self, landmarks_list):
        """
        找到最佳帧（用于主要评分）
        选择姿态最标准、最清晰的一帧
        """
        if len(landmarks_list) == 0:
            return 0
        
        best_score = -1
        best_idx = 0
        
        for idx, landmarks in enumerate(landmarks_list):
            if landmarks is None:
                continue
            
            # 评估标准：关键点可见度
            key_points = ['left_wrist', 'right_wrist', 'left_elbow', 'right_elbow',
                         'left_shoulder', 'right_shoulder', 'left_knee', 'right_knee']
            
            visibilities = [landmarks[point].get('visibility', 0) 
                          for point in key_points if point in landmarks]
            
            if len(visibilities) > 0:
                score = np.mean(visibilities)
                
                # 偏好中间帧（避免开始和结束的不稳定帧）
                middle_bonus = 1.0 - abs(idx - len(landmarks_list) / 2) / (len(landmarks_list) / 2) * 0.2
                score *= middle_bonus
                
                if score > best_score:
                    best_score = score
                    best_idx = idx
        
        return best_idx
    
    def get_sequence_summary(self, sequence_result):
        """
        生成序列分析摘要
        
        Returns:
            dict: 包含总分和反馈的字典
        """
        total_frames = len(sequence_result['frames_data'])
        valid_frames = sum(1 for f in sequence_result['frames_data'] if f['has_pose'])
        
        # 计算序列总分（新增维度）
        smoothness = sequence_result['smoothness_score']
        completeness = sequence_result['completeness_score']
        consistency = sequence_result['consistency_score']
        
        # 加权平均
        sequence_score = (smoothness * 0.4 + completeness * 0.3 + consistency * 0.3)
        
        # 生成反馈
        feedback = []
        
        feedback.append(f"📹 分析了 {total_frames} 帧，{valid_frames} 帧有效")
        
        if smoothness >= 80:
            feedback.append("✅ 动作流畅度优秀")
        elif smoothness >= 60:
            feedback.append("⚠️ 动作有些不够流畅，注意保持连贯")
        else:
            feedback.append("❌ 动作不够流畅，建议多练习基本功")
        
        if completeness >= 80:
            feedback.append("✅ 动作完整性很好")
        elif completeness >= 60:
            feedback.append("⚠️ 部分帧识别不清晰")
        else:
            feedback.append("❌ 动作不完整，请确保全程全身入镜")
        
        if consistency >= 80:
            feedback.append("✅ 动作一致性优秀")
        elif consistency >= 60:
            feedback.append("⚠️ 动作稳定性还需加强")
        else:
            feedback.append("❌ 动作不够稳定，注意保持对称")
        
        return {
            'sequence_score': sequence_score,
            'smoothness_score': smoothness,
            'completeness_score': completeness,
            'consistency_score': consistency,
            'feedback': feedback,
            'total_frames': total_frames,
            'valid_frames': valid_frames
        }
    
    def _extract_frames_from_video(self, video_path):
        """
        从视频文件中提取帧
        
        Args:
            video_path: 视频文件路径
            
        Returns:
            list: 提取的帧列表
        """
        try:
            cap = cv2.VideoCapture(video_path)
            
            if not cap.isOpened():
                return None
            
            frames = []
            fps = cap.get(cv2.CAP_PROP_FPS)
            
            # 每秒提取2帧
            frame_interval = max(1, int(fps / 2))
            frame_count = 0
            
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                
                if frame_count % frame_interval == 0:
                    # 确保帧是有效的numpy数组
                    if frame is not None and isinstance(frame, np.ndarray):
                        frames.append(frame)
                
                frame_count += 1
            
            cap.release()
            return frames
            
        except Exception as e:
            print(f"提取视频帧失败: {str(e)}")
            return None

