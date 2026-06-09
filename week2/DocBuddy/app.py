import gradio as gr

from rag import (
    index_docments,   # change to index_documents if you renamed it
    ask,
    load_existing_store
)

loaded = load_existing_store()

initial_status = (
    "✅ Existing ChromaDB loaded."
    if loaded
    else "⚠️ No documents indexed yet."
)


def handle_index(files):

    if not files:
        return "❌ No files uploaded."

    chunk_count = index_docments(files)

    return (
        f"✅ {len(files)} document(s) indexed — "
        f"{chunk_count} total chunks"
    )


def handle_question(question):

    if not question.strip():
        return "Please enter a question.", ""

    answer, context = ask(question)

    return answer, context


with gr.Blocks(title="DocBuddy Pro") as demo:

    gr.Markdown("# 📄 DocBuddy Pro")
    gr.Markdown(
        """
        Upload one or more PDFs, index them,
        and ask questions using RAG.
        """
    )

    pdf_files = gr.File(
        file_count="multiple",
        file_types=[".pdf"],
        label="Upload PDF Documents"
    )

    index_btn = gr.Button("Index Documents")

    status = gr.Textbox(
        value=initial_status,
        label="Status"
    )

    question = gr.Textbox(
        label="Ask a Question",
        placeholder="Example: How was Aron trapped?"
    )

    ask_btn = gr.Button("Ask")

    answer_box = gr.Markdown(
        label="Answer"
    )

    with gr.Accordion(
        "🔍 Retrieved Context",
        open=False
    ):
        context_md = gr.Markdown()

    index_btn.click(
        fn=handle_index,
        inputs=[pdf_files],
        outputs=[status]
    )

    ask_btn.click(
        fn=handle_question,
        inputs=[question],
        outputs=[answer_box, context_md]
    )

demo.launch()
