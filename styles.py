"""
CSS 스타일 정의
"""

def get_custom_css():
    """커스텀 CSS를 반환"""
    return """
    .gradio-container {
        max-width: 1200px !important;
    }
    .gr-button-primary {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        border: none !important;
        color: white !important;
        border-radius: 25px !important;
        font-weight: 500 !important;
    }
    .gr-button-primary:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3) !important;
    }
    .gr-textbox {
        border-radius: 15px !important;
        border: 2px solid #e1e5e9 !important;
    }
    .gr-textbox:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 15px rgba(102, 126, 234, 0.2) !important;
    }
    """

def get_theme():
    """Gradio 테마를 반환"""
    import gradio as gr
    
    return gr.themes.Soft(
        primary_hue="blue",
        secondary_hue="cyan",
        neutral_hue="slate"
    )
