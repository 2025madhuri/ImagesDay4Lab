import os
import json
import base64
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

products = [
    {"name": "Product 1", "image": "product_images/product1.jpg"},
    {"name": "Product 2", "image": "product_images/product2.jpg"},
    {"name": "Product 3", "image": "product_images/product3.jpg"},
]


def encode_image(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def build_prompt(product_name: str) -> str:
    return f"""
You are an expert e-commerce copywriter.

Create a product listing for the item named: {product_name}

Return valid JSON only with keys:
- title
- description
- features
- keywords
"""


def main() -> None:
    results = []

    for product in products:
        print(f"Processing {product['name']}...")

        base64_img = encode_image(product["image"])
        prompt = build_prompt(product["name"])

        response = client.responses.create(
            model="gpt-4.1-mini",
            input=[
                {
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": prompt},
                        {
                            "type": "input_image",
                            "image_url": f"data:image/jpeg;base64,{base64_img}",
                        },
                    ],
                }
            ],
        )

        results.append({
            "product": product["name"],
            "output": response.output_text,
        })

    os.makedirs("output", exist_ok=True)
    with open("output/generated_listings.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print("✅ All products processed & saved!")


if __name__ == "__main__":
    main()