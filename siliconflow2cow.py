import os
import time
import json
import base64
import threading
import requests
import random
from typing import Optional, Dict, Any
from PIL import Image
from io import BytesIO
from .base import Plugin

class Siliconflow2cowPlus(Plugin):
    def __init__(self):
        super().__init__()
        self.config = self._load_config()
        self._setup_timers()
        
    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        config_path = os.path.join(os.path.dirname(__file__), 'config.json')
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"加载配置文件失败: {e}")
            return {
                "auth_token": "",
                "drawing_prefixes": ["绘", "draw"],
                "image_output_dir": "images",
                "clean_interval": 3,
                "clean_check_interval": 3600,
                "supported_models": {
                    "flux.s": "FLUX.1-schnell"
                },
                "aspect_ratios": {
                    "1:1": "1024x1024"
                }
            }
            
    def _setup_timers(self):
        """设置定时器"""
        self.clean_timer = threading.Timer(
            self.config["clean_check_interval"],
            self._clean_images
        )
        self.clean_timer.start()
        
    def _clean_images(self):
        """清理过期图片"""
        try:
            image_dir = self.config["image_output_dir"]
            if not os.path.exists(image_dir):
                return
                
            current_time = time.time()
            for filename in os.listdir(image_dir):
                filepath = os.path.join(image_dir, filename)
                if os.path.getmtime(filepath) < current_time - self.config["clean_interval"] * 3600:
                    os.remove(filepath)
        except Exception as e:
            print(f"清理图片失败: {e}")
        finally:
            self._setup_timers()
            
    def generate_image(self, prompt: str, aspect_ratio: str = "1:1") -> Optional[str]:
        """生成图片"""
        try:
            if not self.config["auth_token"]:
                return "请先设置认证令牌"
                
            if aspect_ratio not in self.config["aspect_ratios"]:
                return f"不支持的图片比例: {aspect_ratio}"
                
            # 构建请求数据
            data = {
                "prompt": prompt,
                "model": self.config["supported_models"]["flux.s"],
                "size": self.config["aspect_ratios"][aspect_ratio],
                "n": 1
            }
            
            # 发送请求
            headers = {
                "Authorization": f"Bearer {self.config['auth_token']}",
                "Content-Type": "application/json"
            }
            
            response = requests.post(
                "https://api.openai.com/v1/images/generations",
                headers=headers,
                json=data
            )
            
            if response.status_code != 200:
                return f"生成图片失败: {response.text}"
                
            # 保存图片
            image_url = response.json()["data"][0]["url"]
            image_response = requests.get(image_url)
            if image_response.status_code != 200:
                return "下载图片失败"
                
            # 确保输出目录存在
            os.makedirs(self.config["image_output_dir"], exist_ok=True)
            
            # 保存图片
            filename = f"image_{int(time.time())}_{random.randint(1000, 9999)}.png"
            filepath = os.path.join(self.config["image_output_dir"], filename)
            
            with open(filepath, "wb") as f:
                f.write(image_response.content)
                
            return f"图片已保存: {filepath}"
            
        except Exception as e:
            return f"生成图片时发生错误: {e}"
            
    def handle_message(self, message: str) -> Optional[str]:
        """处理消息"""
        for prefix in self.config["drawing_prefixes"]:
            if message.startswith(prefix):
                prompt = message[len(prefix):].strip()
                if not prompt:
                    return "请输入要生成的图片描述"
                return self.generate_image(prompt)
        return None
 