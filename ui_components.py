"""
Gradio UI 구성 요소들
"""
import gradio as gr
import os

def create_header():
    """헤더 HTML을 생성"""
    return gr.HTML("""
    <div style="text-align: center; padding: 30px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; margin-bottom: 20px;">
        <h1 style="color: white; font-size: 3em; margin: 0; font-weight: 300;">🖼️ Ovis Vision Model</h1>
        <p style="color: white; font-size: 1.3em; margin: 10px 0 0 0; opacity: 0.9;">AI가 이미지를 분석하고 설명해드립니다</p>
    </div>
    """)

def create_footer():
    """푸터 HTML을 생성"""
    return gr.HTML("""
    <div style="text-align: center; padding: 20px; margin-top: 30px; border-top: 1px solid #eee;">
        <p style="color: #666; margin: 0;">
            🚀 Powered by <strong>Ovis Vision Language Model</strong> | 
            ⚡ Built with <strong>Gradio</strong> | 
            🔧 Made with ❤️
        </p>
    </div>
    """)

def create_input_section():
    """입력 섹션을 생성"""
    with gr.Column(scale=1):
        gr.HTML("<h2 style='color: #333; margin-bottom: 20px;'>📤 입력</h2>")
        
        # 이미지 업로드
        image_input = gr.Image(
            label="이미지 업로드",
            type="pil",
            height=300,
            elem_id="image_upload"
        )
        
        # 텍스트 프롬프트
        text_input = gr.Textbox(
            label="질문 또는 요청사항",
            placeholder="이미지에 대해 묻고 싶은 것을 입력하세요...",
            value="이미지를 한국어로 자세히 설명해주세요.",
            lines=3,
            max_lines=5
        )
        
        # 고급 설정
        with gr.Accordion("🔧 고급 설정", open=False):
            max_tokens = gr.Slider(
                minimum=50,
                maximum=2048,
                value=1024,
                step=50,
                label="최대 토큰 수",
                info="생성할 최대 텍스트 길이"
            )
            
            temperature = gr.Slider(
                minimum=0.0,
                maximum=1.0,
                value=0.0,
                step=0.1,
                label="Temperature",
                info="0이면 결정적, 높을수록 창의적"
            )
            
            top_p = gr.Slider(
                minimum=0.1,
                maximum=1.0,
                value=0.9,
                step=0.1,
                label="Top-p",
                info="다양성 제어 (temperature > 0일 때만 적용)"
            )
        
        # 분석 버튼
        analyze_btn = gr.Button(
            "🔍 이미지 분석하기",
            variant="primary",
            size="lg"
        )
        
        # 예시 이미지들
        create_examples_section(image_input, text_input)
        
    return image_input, text_input, max_tokens, temperature, top_p, analyze_btn

def create_examples_section(image_input, text_input):
    """예시 섹션을 생성"""
    gr.HTML("<h3 style='color: #333; margin-top: 30px;'>📋 예시 이미지</h3>")
    
    # 예시 이미지들을 현재 디렉토리로 복사
    example_images = []
    
    # 원본 이미지 경로들
    source_examples = [
        ["/home/aisw/Project/UST-ETRI-2025/data/etri_char.png", "이 캐릭터의 특징을 설명해주세요."],
        ["/home/aisw/Project/UST-ETRI-2025/data/windows_xp.jpg", "이 이미지에서 무엇을 볼 수 있나요?"],
    ]
    
    # examples 폴더 생성
    examples_dir = os.path.join(os.path.dirname(__file__), "examples")
    os.makedirs(examples_dir, exist_ok=True)
    
    # 이미지 복사 및 유효한 예시 추가
    valid_examples = []
    for i, (img_path, prompt) in enumerate(source_examples):
        try:
            if os.path.exists(img_path):
                # 파일명 생성
                filename = f"example_{i+1}" + os.path.splitext(img_path)[1]
                dest_path = os.path.join(examples_dir, filename)
                
                # 파일이 없으면 복사
                if not os.path.exists(dest_path):
                    import shutil
                    shutil.copy2(img_path, dest_path)
                    print(f"Copied example image: {dest_path}")
                
                valid_examples.append([dest_path, prompt])
        except Exception as e:
            print(f"Failed to copy example image {img_path}: {e}")
            pass
    
    if valid_examples:
        gr.Examples(
            examples=valid_examples,
            inputs=[image_input, text_input],
            label="클릭하여 예시 사용"
        )

def create_output_section(system_info_text):
    """출력 섹션을 생성"""
    with gr.Column(scale=1):
        gr.HTML("<h2 style='color: #333; margin-bottom: 20px;'>📤 결과</h2>")
        
        # 결과 출력
        output_text = gr.Textbox(
            label="분석 결과",
            placeholder="여기에 AI의 분석 결과가 표시됩니다...",
            lines=15,
            max_lines=20,
            interactive=False,
            show_copy_button=True
        )
        
        # 시스템 정보
        with gr.Accordion("💻 시스템 정보", open=False):
            system_info = gr.Textbox(
                value=system_info_text,
                label="현재 시스템 상태",
                interactive=False,
                lines=8
            )
        
    return output_text
