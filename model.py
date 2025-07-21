"""
Ovis 모델 로딩 및 추론 관련 함수들
"""
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import time
import os

class OvisModel:
    def __init__(self, model_path="AIDC-AI/Ovis2-8B"):
        self.model_path = model_path
        self.model = None
        self.tokenizer = None
        self.visual_tokenizer = None
        self.torch_dtype = torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16
        
        # hf_cache 경로 설정 (Ovis 폴더 내의 hf_cache 사용)
        self.cache_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "hf_cache")
        
    def load_model(self):
        """모델을 로딩합니다"""
        print(f"Loading Ovis model from {self.model_path}...")
        print(f"Using cache directory: {self.cache_dir}")
        
        # cache 디렉토리 존재 확인
        if not os.path.exists(self.cache_dir):
            print(f"Warning: Cache directory {self.cache_dir} does not exist. Creating it...")
            os.makedirs(self.cache_dir, exist_ok=True)
        
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_path,
            torch_dtype=self.torch_dtype,
            trust_remote_code=True,
            cache_dir=self.cache_dir,
            device_map="auto",
            low_cpu_mem_usage=True,
        )
        
        self.tokenizer = self.model.get_text_tokenizer()
        self.visual_tokenizer = self.model.get_visual_tokenizer()
        print("Model loaded successfully!")
        
    def analyze_image(self, image, text_prompt, max_tokens=1024, temperature=0.0, top_p=0.9):
        """이미지를 분석하는 함수"""
        if image is None:
            return "이미지를 업로드해주세요."
        
        if not text_prompt.strip():
            text_prompt = "이미지를 자세히 설명해주세요."
        
        try:
            # PIL Image로 변환
            if hasattr(image, 'convert'):
                if image.mode != 'RGB':
                    image = image.convert('RGB')
            
            # 모델 추론 준비
            images = [image]
            max_partition = 9
            query = f'<image>\n{text_prompt}'
            
            # 입력 데이터 전처리
            prompt, input_ids, pixel_values = self.model.preprocess_inputs(
                query, images, max_partition=max_partition
            )
            attention_mask = torch.ne(input_ids, self.tokenizer.pad_token_id)
            input_ids = input_ids.unsqueeze(0).to(device=self.model.device)
            attention_mask = attention_mask.unsqueeze(0).to(device=self.model.device)
            
            if pixel_values is not None:
                pixel_values = pixel_values.to(
                    dtype=self.visual_tokenizer.dtype, 
                    device=self.visual_tokenizer.device
                )
            pixel_values = [pixel_values]
            
            # 생성 파라미터 설정
            gen_kwargs = {
                'max_new_tokens': int(max_tokens),
                'do_sample': temperature > 0,
                'top_p': top_p if temperature > 0 else None,
                'temperature': temperature if temperature > 0 else None,
                'repetition_penalty': 1.1,
                'eos_token_id': self.model.generation_config.eos_token_id,
                'pad_token_id': self.tokenizer.pad_token_id,
                'use_cache': True
            }
            
            # 추론 실행
            start_time = time.time()
            with torch.inference_mode():
                output_ids = self.model.generate(
                    input_ids, 
                    pixel_values=pixel_values, 
                    attention_mask=attention_mask, 
                    **gen_kwargs
                )[0]
                output = self.tokenizer.decode(output_ids, skip_special_tokens=True)
            end_time = time.time()
            
            # 토큰 통계 계산
            input_tokens = input_ids.shape[1]
            output_tokens = len(output_ids) - input_tokens
            total_tokens = len(output_ids)
            processing_time = end_time - start_time
            
            # 처리 속도 계산
            tokens_per_second = output_tokens / processing_time if processing_time > 0 else 0
            
            # 결과 정리
            if query in output:
                result = output.replace(query, '').strip()
            else:
                result = output
            
            # 처리 통계 추가
            stats_info = f"""
⏱️ 처리 시간: {processing_time:.2f}초
🔢 입력 토큰: {input_tokens:,}개
📝 생성 토큰: {output_tokens:,}개
📊 총 토큰: {total_tokens:,}개
⚡ 생성 속도: {tokens_per_second:.1f} tokens/sec
💾 사용 메모리: {torch.cuda.memory_allocated() / 1024**3:.2f}GB (GPU)"""
            
            result += stats_info
            
            return result
            
        except Exception as e:
            return f"❌ 오류가 발생했습니다: {str(e)}"
    
    def get_system_info(self):
        """시스템 정보를 반환"""
        info = []
        info.append(f"🔧 PyTorch 버전: {torch.__version__}")
        info.append(f"🎮 CUDA 사용 가능: {'Yes' if torch.cuda.is_available() else 'No'}")
        
        if torch.cuda.is_available():
            info.append(f"📊 GPU 개수: {torch.cuda.device_count()}")
            for i in range(torch.cuda.device_count()):
                gpu_name = torch.cuda.get_device_properties(i).name
                gpu_memory = torch.cuda.get_device_properties(i).total_memory / 1024**3
                info.append(f"  - GPU {i}: {gpu_name} ({gpu_memory:.1f}GB)")
        
        info.append(f"💾 데이터 타입: {self.torch_dtype}")
        
        return "\n".join(info)
