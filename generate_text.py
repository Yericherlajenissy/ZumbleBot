from huggingface_hub import InferenceClient

# Initialize the InferenceClient with your API token
client = InferenceClient(
    "Qwen/Qwen2.5-1.5B-Instruct",
    token="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",  # Replace with your actual Hugging Face token
)

def generate_text(prompt):
    # Send the prompt to the model using chat completion
    result = ""
    for message in client.chat_completion(
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1500,
        stream=True
    ):
        result += message.choices[0].delta.content

    return result


