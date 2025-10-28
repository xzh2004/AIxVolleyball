"""
评分算法模块 - 评估排球垫球动作标准度
"""
import numpy as np
import json
from pose_detector import PoseDetector


class VolleyballScorer:
    def __init__(self, template_path='template.json'):
        """初始化评分器"""
        self.template = self._load_template(template_path)
        self.detector = PoseDetector()
    
    def _load_template(self, path):
        """加载标准动作模板"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            # 返回默认模板
            return {
                "arm_angle": 165,  # 手臂伸直角度
                "arm_gap_angle": 25,  # 双臂夹角
                "knee_angle": 75,  # 膝盖弯曲角度
                "hip_height": 0.55,  # 髋部相对高度
                "arm_height": 0.45,  # 手臂触球高度
            }
    
    def score_pose(self, landmarks):
        """
        对姿态进行评分
        
        Args:
            landmarks: 姿态关键点字典
            
        Returns:
            dict: 包含总分和各项得分的字典
        """
        if landmarks is None:
            return {
                'total_score': 0,
                'arm_score': 0,
                'body_score': 0,
                'position_score': 0,
                'stability_score': 0,
                'feedback': ['未检测到人体姿态，请确保全身入镜']
            }
        
        scores = {}
        feedback = []
        
        # 1. 手臂评分 (40分)
        arm_score, arm_feedback = self._score_arms(landmarks)
        scores['arm_score'] = arm_score
        feedback.extend(arm_feedback)
        
        # 2. 身体重心评分 (30分)
        body_score, body_feedback = self._score_body(landmarks)
        scores['body_score'] = body_score
        feedback.extend(body_feedback)
        
        # 3. 触球位置评分 (20分)
        position_score, position_feedback = self._score_position(landmarks)
        scores['position_score'] = position_score
        feedback.extend(position_feedback)
        
        # 4. 整体稳定性评分 (10分)
        stability_score, stability_feedback = self._score_stability(landmarks)
        scores['stability_score'] = stability_score
        feedback.extend(stability_feedback)
        
        # 计算总分
        scores['total_score'] = int(arm_score + body_score + position_score + stability_score)
        scores['feedback'] = feedback
        
        return scores
    
    def _score_arms(self, landmarks):
        """评分手臂姿态"""
        feedback = []
        
        try:
            # 左臂角度（肩-肘-腕）
            left_angle = self.detector.calculate_angle(
                landmarks['left_shoulder'],
                landmarks['left_elbow'],
                landmarks['left_wrist']
            )
            
            # 右臂角度
            right_angle = self.detector.calculate_angle(
                landmarks['right_shoulder'],
                landmarks['right_elbow'],
                landmarks['right_wrist']
            )
            
            # 双臂夹角（左腕-左肩-右腕）
            arm_gap = self.detector.calculate_angle(
                landmarks['left_wrist'],
                {'x': (landmarks['left_shoulder']['x'] + landmarks['right_shoulder']['x']) / 2,
                 'y': (landmarks['left_shoulder']['y'] + landmarks['right_shoulder']['y']) / 2},
                landmarks['right_wrist']
            )
            
            # 计算得分
            arm_straight_score = 0
            template_arm = self.template['arm_angle']
            
            # 左臂得分
            left_error = abs(left_angle - template_arm)
            left_score = max(0, 10 - left_error / 3)
            
            # 右臂得分
            right_error = abs(right_angle - template_arm)
            right_score = max(0, 10 - right_error / 3)
            
            # 双臂夹角得分
            gap_error = abs(arm_gap - self.template['arm_gap_angle'])
            gap_score = max(0, 20 - gap_error / 2)
            
            total_arm_score = left_score + right_score + gap_score
            
            # 生成反馈
            if left_angle < 140:
                feedback.append('❌ 左臂弯曲过多，应该更伸直')
            elif left_angle > 175:
                feedback.append('✅ 左臂姿势标准')
            
            if right_angle < 140:
                feedback.append('❌ 右臂弯曲过多，应该更伸直')
            elif right_angle > 175:
                feedback.append('✅ 右臂姿势标准')
            
            if arm_gap < 15:
                feedback.append('❌ 双臂距离太近，应该打开与肩同宽')
            elif arm_gap > 40:
                feedback.append('❌ 双臂距离太宽，应该收拢')
            else:
                feedback.append('✅ 双臂间距合适')
            
            return total_arm_score, feedback
            
        except Exception as e:
            return 0, [f'手臂姿态识别异常: {str(e)}']
    
    def _score_body(self, landmarks):
        """评分身体重心"""
        feedback = []
        
        try:
            # 左膝角度（髋-膝-踝）
            left_knee_angle = self.detector.calculate_angle(
                landmarks['left_hip'],
                landmarks['left_knee'],
                landmarks['left_ankle']
            )
            
            # 右膝角度
            right_knee_angle = self.detector.calculate_angle(
                landmarks['right_hip'],
                landmarks['right_knee'],
                landmarks['right_ankle']
            )
            
            # 髋部高度（相对身高）
            hip_height = (landmarks['left_hip']['y'] + landmarks['right_hip']['y']) / 2
            shoulder_height = (landmarks['left_shoulder']['y'] + landmarks['right_shoulder']['y']) / 2
            relative_hip = hip_height - shoulder_height
            
            # 膝盖弯曲度评分
            knee_score = 0
            template_knee = self.template['knee_angle']
            
            left_knee_error = abs(left_knee_angle - template_knee)
            knee_score += max(0, 10 - left_knee_error / 5)
            
            right_knee_error = abs(right_knee_angle - template_knee)
            knee_score += max(0, 10 - right_knee_error / 5)
            
            # 重心高度评分
            hip_score = 10 if 0.15 < relative_hip < 0.25 else 5
            
            total_body_score = knee_score + hip_score
            
            # 生成反馈
            if left_knee_angle > 160:
                feedback.append('❌ 左腿太直，膝盖应该弯曲')
            elif left_knee_angle < 60:
                feedback.append('❌ 左腿弯曲过多，重心过低')
            else:
                feedback.append('✅ 左腿弯曲适中')
            
            if right_knee_angle > 160:
                feedback.append('❌ 右腿太直，膝盖应该弯曲')
            elif right_knee_angle < 60:
                feedback.append('❌ 右腿弯曲过多，重心过低')
            else:
                feedback.append('✅ 右腿弯曲适中')
            
            return total_body_score, feedback
            
        except Exception as e:
            return 0, [f'身体重心识别异常: {str(e)}']
    
    def _score_position(self, landmarks):
        """评分触球位置"""
        feedback = []
        
        try:
            # 手腕平均高度
            wrist_y = (landmarks['left_wrist']['y'] + landmarks['right_wrist']['y']) / 2
            
            # 髋部高度
            hip_y = (landmarks['left_hip']['y'] + landmarks['right_hip']['y']) / 2
            
            # 肩部高度
            shoulder_y = (landmarks['left_shoulder']['y'] + landmarks['right_shoulder']['y']) / 2
            
            # 相对位置
            relative_wrist = (wrist_y - shoulder_y) / (hip_y - shoulder_y + 1e-6)
            
            # 评分
            if 1.2 < relative_wrist < 2.0:
                position_score = 20
                feedback.append('✅ 触球位置标准（腰腹前方）')
            elif 0.8 < relative_wrist < 2.5:
                position_score = 12
                feedback.append('⚠️ 触球位置偏高/偏低')
            else:
                position_score = 5
                feedback.append('❌ 触球位置不正确')
            
            return position_score, feedback
            
        except Exception as e:
            return 0, [f'触球位置识别异常: {str(e)}']
    
    def _score_stability(self, landmarks):
        """评分整体稳定性（根据关键点置信度）"""
        feedback = []
        
        try:
            # 计算关键点平均可见度
            key_points = ['left_shoulder', 'right_shoulder', 'left_elbow', 'right_elbow',
                         'left_wrist', 'right_wrist', 'left_hip', 'right_hip',
                         'left_knee', 'right_knee']
            
            visibilities = [landmarks[point]['visibility'] for point in key_points]
            avg_visibility = np.mean(visibilities)
            
            # 评分
            stability_score = avg_visibility * 10
            
            if avg_visibility > 0.8:
                feedback.append('✅ 姿态识别清晰稳定')
            elif avg_visibility > 0.6:
                feedback.append('⚠️ 姿态识别一般，建议改善拍摄角度')
            else:
                feedback.append('❌ 姿态识别不清晰，请确保全身入镜且光线充足')
            
            return stability_score, feedback
            
        except Exception as e:
            return 0, [f'稳定性评估异常: {str(e)}']
    
    def get_grade(self, score):
        """根据分数返回等级"""
        if score >= 90:
            return 'S', '完美！职业级水准！🏆'
        elif score >= 80:
            return 'A', '优秀！继续保持！⭐'
        elif score >= 70:
            return 'B', '良好！还有进步空间！👍'
        elif score >= 60:
            return 'C', '及格！加油练习！💪'
        else:
            return 'D', '需要改进！多看教学视频！📚'

