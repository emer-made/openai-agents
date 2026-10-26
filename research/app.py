import asyncio
import planner
import searcher
import writer
from agents import trace, gen_trace_id
from pathlib import Path
import gradio as gr
from dotenv import load_dotenv

load_dotenv(override=True)

PLACEHOLDER_MD = ""

async def run(query: str):
    trace_id = gen_trace_id()
    yield f"Starting research. Trace: https://platform.openai.com/traces/trace?trace_id={trace_id}"
    search_plan = await planner.plan_search(query)
    yield f"Searches planned, starting {len(search_plan.searches)} searches..."     
    search_results = await searcher.process(search_plan)
    yield "Searches complete, writing report..."
    report = await writer.write_report(query, search_results)
    yield "Report written..."
    PLACEHOLDER_MD = report.markdown_report
    yield PLACEHOLDER_MD


EXAMPLES = [
    "What is the most popular Agentic frameworks today.",
    "The economy of Indonesia.",
    "Why immigration is not popular in Japan."
]
async def on_research(query: str):
    query = (query or "").strip()
    if not query:
        yield "> ⚠️ Please enter a research topic first."
        return
    yield f"> 🔎 Researching **{query}** …"
    
    async for item in run(query):
        yield item


CSS = (Path(__file__).parent / "style.css").read_text()


def build_ui() -> gr.Blocks:
    with gr.Blocks(title="Personal Research Agent") as demo:
        gr.HTML(
            '<div id="header"><h1>Personal Research Agent</h1>'
            "<p>Ask a question. Get a structured, sourced report.</p></div>"
        )

        with gr.Row(equal_height=False):
            # Left: input
            with gr.Column(scale=2, min_width=320, elem_classes="card"):
                gr.HTML('<div class="section-label">Research topic</div>')
                query = gr.Textbox(
                    elem_id="query",
                    placeholder="e.g. Find the most popular AI Agent frameworks in 2026",
                    lines=5,
                    show_label=False,
                )
                run_btn = gr.Button("Start Research  →", elem_id="run-btn")

                gr.HTML('<div class="section-label" style="margin-top:18px">Try an example</div>')
                for ex in EXAMPLES:
                    gr.Button(ex, elem_classes="chip", size="sm").click(
                        lambda e=ex: e, outputs=query
                    )

            # Right: markdown report
            with gr.Column(scale=3, min_width=420, elem_classes="card"):
                gr.HTML('<div class="section-label">Report</div>')
                report = gr.Markdown(PLACEHOLDER_MD, elem_id="report")

        run_btn.click(on_research, inputs=query, outputs=report)
        query.submit(on_research, inputs=query, outputs=report)

    return demo


if __name__ == "__main__":
    theme = gr.themes.Base(primary_hue="violet", neutral_hue="slate")
    build_ui().launch(css=CSS, theme=theme)