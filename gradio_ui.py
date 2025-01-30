from browser_agent.agent_for_ui import run_browser_agent
from browser_agent.output_summarizer import output_summarizer
from typing import List, Optional
from dataclasses import dataclass
import gradio as gr
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

custom_css = """
/* Base Dark Theme */
body {
    background-color: #1a1a1a !important;
    color: #e0e0e0 !important;
}

#title {
    text-align: center;
    font-size: 2.5em !important;
    font-weight: bold;
    background: linear-gradient(45deg, #5a7bff, #8a63d2);
    -webkit-background-clip: text;
    color: transparent;
    margin-bottom: 0.5em;
}

.logo {
    height: 80px;
    border-radius: 10px;
    margin: 0 auto;
    display: block;
    border: 2px solid #5a7bff;
    filter: drop-shadow(0 0 8px rgba(90, 123, 255, 0.2));
}

.subtitle {
    text-align: center;
    color: #a88dff !important;
    font-size: 1.2em !important;
    margin-bottom: 2em !important;
    opacity: 0.9;
}

.input-section {
    background: #2d2d2d !important;
    padding: 20px;
    border-radius: 10px;
    border: 1px solid #404040 !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.output-box {
    background: #252525 !important;
    border-radius: 10px;
    padding: 15px;
    border: 1px solid #404040 !important;
    color: #d0d0d0 !important;
}

.custom-button {
    background: linear-gradient(45deg, #1f3a4b 0%, #382a4a 100%) !important;
    color: #d0d0ff !important;
    font-weight: bold !important;
    border: none !important;
    padding: 15px 30px !important;
    border-radius: 8px !important;
    transition: all 0.3s ease !important;
}

.custom-button:hover {
    transform: scale(1.02);
    box-shadow: 0 0 15px rgba(90, 123, 255, 0.3);
    filter: brightness(1.1);
}

/* Dark Scrollbar */
::-webkit-scrollbar {
    width: 8px;
    background: #1a1a1a;
}

::-webkit-scrollbar-thumb {
    background: #5a7bff;
    border-radius: 4px;
}

/* Form Elements */
label {
    color: #a88dff !important;
    font-weight: 500 !important;
}

textarea, input {
    background: #333333 !important;
    border: 1px solid #404040 !important;
    color: #e0e0e0 !important;
}

/* Accordion Styling */
.accordion {
    background: #2d2d2d !important;
    border: 1px solid #404040 !important;
}

/* Footer Styling */
footer {
    color: #888 !important;
    border-top: 1px solid #404040 !important;
}

/* JSON Viewer Styling */
.json-viewer {
    background: #252525 !important;
    color: #8a63d2 !important;
}

/* Error Console */
.error-console {
    background: #2d2d2d !important;
    color: #ff6666 !important;
    border-color: #ff4444 !important;
}
"""

@dataclass
class ActionResult:
    is_done: bool
    extracted_content: Optional[str]
    error: Optional[str]
    include_in_memory: bool

@dataclass
class AgentHistoryList:
    all_results: List[ActionResult]
    all_model_outputs: List[dict]

def parse_agent_history(history_str: str) -> None:
    console = Console()
    sections = history_str.split('ActionResult(')

    for i, section in enumerate(sections[1:], 1):
        content = ''
        if 'extracted_content=' in section:
            content = section.split('extracted_content=')[1].split(',')[0].strip("'")

        if content:
            header = Text(f'Step {i}', style='bold blue')
            panel = Panel(content, title=header, border_style='blue')
            console.print(panel)
            console.print()

def create_ui():
    with gr.Blocks(
        title="Browser Use Agent - Razi AI&You",
        css=custom_css,
        theme=gr.themes.Soft()
    ) as interface:
        
        # Header Section
        with gr.Column(elem_id="header"):
            gr.Markdown("""
            <div id="title">
                <span style="background: linear-gradient(45deg, #2B5876, #4E4376); -webkit-background-clip: text; color: transparent;">
                    Browser Use Agent
                </span>
            </div>
            <div class="subtitle">
                AI-Powered Browser Use Platform
            </div>
            """)
        
        # Main Content
        with gr.Row():
            # Input Column
            with gr.Column(scale=1, elem_classes="input-section"):
                task = gr.Textbox(
                    label="📝 Task Description",
                    placeholder="Enter your browser automation task...\nExample: 'Research latest AI trends and summarize key findings'",
                    lines=4,
                    max_lines=6,
                    elem_id="task-input"
                )
                with gr.Row():
                    submit_btn = gr.Button(
                        "🚀 Execute Task",
                        elem_classes="custom-button",
                        scale=2
                    )
                    clear_btn = gr.Button("🧹 Clear", scale=1)
                
                gr.Markdown("""
                **Tips:**
                - Be specific with your instructions
                - Include target websites if needed
                - Use natural language commands
                """)

            # Output Column
            with gr.Column(scale=1, elem_classes="output-section"):
                with gr.Tabs():
                    with gr.Tab("📋 Results", elem_classes="output-box"):
                        output = gr.Textbox(
                            label="🧠 AI Analysis Report",
                            lines=12,
                            interactive=False,
                            elem_id="output-box"
                        )
                    with gr.Tab("⚙️ Raw Data"):
                        raw_data = gr.Textbox(
                            label="Technical Details",
                            lines=12,
                            interactive=False,
                            elem_id="output-box"
                        )
                
                with gr.Accordion("⚠️ Error Console", open=False):
                    error_console = gr.Textbox(
                        lines=2,
                        interactive=False,
                        visible=False
                    )

        # Footer
        gr.Markdown("""
        <div style="text-align: center; margin-top: 20px; color: #666;">
            🛡️ Powered by AI&You Research and Development | v0.1 |
        </div>
        """)

        # Interactive Functions
        async def run_and_summarize(query):
            try:
                raw_output = await run_browser_agent(query)
                summarized = output_summarizer(raw_output)
                return {output: summarized, raw_data: raw_output}
            except Exception as e:
                return {output: f"❌ Error: {str(e)}", error_console: str(e)}

        def clear_inputs():
            return {task: "", output: "", raw_data: None, error_console: ""}

        submit_btn.click(
            fn=run_and_summarize,
            inputs=task,
            outputs=[output, raw_data, error_console]
        )
        clear_btn.click(
            fn=clear_inputs,
            outputs=[task, output, raw_data, error_console]
        )

    return interface

if __name__ == "__main__":
    demo = create_ui()
    demo.launch()