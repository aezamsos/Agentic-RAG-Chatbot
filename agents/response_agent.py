from transformers import pipeline
import torch

class LLMResponseAgent:
    def __init__(self):
        self.generator = pipeline(
            "text-generation",
            model="distilgpt2",
            tokenizer="distilgpt2",
            torch_dtype=torch.float32,
            device=0 if torch.cuda.is_available() else -1
        )

    def generate_answer(self, mcp_message):
        chunks = mcp_message["payload"]["top_chunks"]
        query = mcp_message["payload"]["query"]
        context = "\n".join(chunks)
        prompt = f"Context:\n{context}\n\nQuestion: {query}\nAnswer:"
        output = self.generator(prompt, max_length=300, num_return_sequences=1)[0]["generated_text"]
        answer_start = output.find("Answer:")
        return output[answer_start + len("Answer:"):].strip()