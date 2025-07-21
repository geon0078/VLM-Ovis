"""
메인 애플리케이션 실행 파일
"""
import gradio as gr
from model import OvisModel
from ui_components import (
    create_header, 
    create_footer, 
    create_input_section, 
    create_output_section
)
from styles import get_custom_css, get_theme

def create_app():
    """Gradio 애플리케이션을 생성"""
    # 모델 초기화 및 로딩
    ovis_model = OvisModel()
    ovis_model.load_model()
    
    # Gradio 인터페이스 생성
    with gr.Blocks(
        title="🖼️ Ovis Vision Language Model",
        theme=get_theme(),
        css=get_custom_css()
    ) as iface:
        
        # 헤더
        create_header()
        
        with gr.Row():
            # 입력 섹션
            image_input, text_input, max_tokens, temperature, top_p, analyze_btn = create_input_section()
            
            # 출력 섹션
            output_text = create_output_section(ovis_model.get_system_info())
        
        # 푸터
        create_footer()
        
        # 이벤트 처리
        analyze_btn.click(
            fn=ovis_model.analyze_image,
            inputs=[image_input, text_input, max_tokens, temperature, top_p],
            outputs=output_text,
            show_progress=True
        )
        
    return iface

def main():
    """메인 실행 함수"""
    print("\n" + "="*60)
    print("🚀 Ovis Vision Model Gradio App Starting...")
    print("📍 Gradio will provide the URL once started")
    print("💡 Upload images and get AI-powered descriptions!")
    print("="*60 + "\n")
    
    # 앱 생성 및 실행
    app = create_app()
    app.launch(
        server_name="0.0.0.0",  # 외부 접속 허용
        server_port=7860,       # 포트 설정
        share=False,            # 공개 링크 생성 (필요시 True로 변경)
        debug=False,
        show_error=True,
        quiet=False
    )

if __name__ == "__main__":
    main()
