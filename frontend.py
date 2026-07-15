import gradio as gr
import requests
import os
# Backend URL
API_URL =  "https://ai-product-description-backend-1.onrender.com/generate"
# Function to call backend
def generate_description(product_name):

    if not product_name.strip():
        return "Please enter a product name."

    payload = {
        "product_name": product_name
    }

    try:
        response = requests.post(API_URL, json=payload)

        if response.status_code == 200:

            data = response.json()["data"]

            output = f"""
# 🛍️ Product Title

{data['title']}

---

# 📝 Product Description

{data['description']}

---

# ⭐ Key Features

"""

            for feature in data["features"]:
                output += f"• {feature}\n"

            output += "\n---\n"

            output += "# 🎯 Benefits\n\n"

            for benefit in data["benefits"]:
                output += f"• {benefit}\n"

            output += "\n---\n"

            output += "# 🔍 SEO Keywords\n\n"

            output += ", ".join(data["seo_keywords"])

            output += "\n\n---\n"

            output += "# 📢 Call To Action\n\n"

            output += data["call_to_action"]

            return output

        else:
            return response.json()["detail"]

    except Exception as e:
        return str(e)


# Gradio UI
with gr.Blocks(title="AI Product Description Generator") as demo:

    gr.Markdown(
        """
# 🤖 AI Product Description Generator

Generate professional product descriptions using Gemini AI.
"""
    )

    product = gr.Textbox(
        label="Product Name",
        placeholder="Example: Wireless Bluetooth Earbuds"
    )

    generate = gr.Button("🚀 Generate Description")

    output = gr.Markdown()

    generate.click(
        fn=generate_description,
        inputs=product,
        outputs=output
    )
if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=int(os.environ.get("PORT", 7860))
    )
