import json
import gradio as gr

from main import agent
from services.review_service import save_review
from services.product_service import get_all_products, get_product


# Get product names from MySQL
products = get_all_products()


def process_review(product_name, review_title, rating, category, comments):

    # Send review to MoodMate agent
    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": f"""
                    Analyze this customer review and provide
                    alternative phone recommendations.

                    Product Name: {product_name}
                    Review Title: {review_title}
                    Rating: {rating}
                    Category: {category}
                    Comments: {comments}
                    """
                }
            ]
        }
    )

    # Get final JSON from agent
    final_response = result["messages"][-1].content
    analysis = json.loads(final_response)

    # Save review and AI results to MySQL
    save_review(
        product_name=product_name,
        review_title=review_title,
        rating=rating,
        category=category,
        comments=comments,
        sentiment=analysis["sentiment"],
        emotion=analysis["emotion"],
        suggestion_1=analysis["suggestion_1"],
        suggestion_2=analysis["suggestion_2"],
        message=analysis["message"]
    )

    # Get current phone details
    current_product = get_product(product_name)

    recommendation_data = {
        "suggestion_1": analysis["suggestion_1"],
        "suggestion_2": analysis["suggestion_2"],
        "message": analysis["message"]
    }

    result_text = f"""
## ✓ Review Submitted

**Product:** {product_name}

**Rating:** ⭐ {rating}

**Category:** {category}

**Price:** ₹{current_product['price']}
"""

    return result_text, recommendation_data


def show_recommendation(data):

    suggestion_1 = get_product(data["suggestion_1"])
    suggestion_2 = get_product(data["suggestion_2"])

    def product_card(product):

        return f"""
        <div class="product-card">

            <div class="product-title">
                📱 {product['product_name']}
            </div>

            <div class="product-price">
                ₹{product['price']}
            </div>

            <div class="spec-row">
                <span>Display</span>
                <b>{product['display']}</b>
            </div>

            <div class="spec-row">
                <span>Battery</span>
                <b>{product['battery']} mAh</b>
            </div>

            <div class="spec-row">
                <span>Camera</span>
                <b>{product['camera']}</b>
            </div>

            <div class="spec-row">
                <span>Processor</span>
                <b>{product['processor']}</b>
            </div>

            <div class="spec-row">
                <span>RAM</span>
                <b>{product['ram']}</b>
            </div>

            <div class="spec-row">
                <span>Storage</span>
                <b>{product['storage']}</b>
            </div>

            <div class="spec-row">
                <span>Charging</span>
                <b>{product['charging']}</b>
            </div>

            <div class="spec-row">
                <span>Network</span>
                <b>{product['network']}</b>
            </div>

        </div>
        """

    moodmate_message = f"""
    <div class="moodmate-message">

        <div class="message-title">
            💬 MoodMate
        </div>

        <div class="message-text">
            {data['message']}
        </div>

    </div>
    """

    return (
        moodmate_message,
        product_card(suggestion_1),
        product_card(suggestion_2)
    )


# Custom styling
custom_css = """

/* ---------- Overall font ---------- */

.gradio-container {
    font-family: Inter, ui-sans-serif, system-ui, -apple-system,
                 BlinkMacSystemFont, "Segoe UI", sans-serif !important;
}


/* ---------- Background ---------- */

html,
body,
.gradio-container {
    background:
        radial-gradient(
            circle at 10% 15%,
            #151b38 0%,
            transparent 35%
        ),
        radial-gradient(
            circle at 90% 20%,
            #241532 0%,
            transparent 38%
        ),
        radial-gradient(
            circle at 75% 90%,
            #102d32 0%,
            transparent 40%
        ),
        linear-gradient(
            135deg,
            #090d18 0%,
            #121526 35%,
            #180f24 68%,
            #09151b 100%
        ) !important;

    background-attachment: fixed !important;
}


/* ---------- Header ---------- */

#header {
    text-align: center;
    padding: 35px 0 5px 0;
}

#header h1 {
    font-size: 44px;
    font-weight: 800;
    letter-spacing: -1.5px;
}

#subtitle {
    text-align: center;
    font-size: 17px;
    opacity: 0.7;
    margin-bottom: 35px;
}


/* ---------- Form card ---------- */

.card {
    border-radius: 20px !important;
    padding: 28px !important;
}


/* ---------- Buttons ---------- */

#submit-btn,
#recommend-btn {
    border-radius: 12px !important;
    font-weight: 700 !important;
    min-height: 50px !important;
}


/* ---------- Result ---------- */

#result {
    border-radius: 18px !important;
    padding: 22px !important;
    margin-top: 20px;
}


/* ---------- MoodMate message ---------- */

.moodmate-message {
    margin-top: 30px;
    margin-bottom: 25px;
    padding: 22px 25px;
    border-radius: 18px;
    border: 1px solid var(--border-color-primary);
    background: var(--background-fill-secondary);
}

.message-title {
    font-size: 20px;
    font-weight: 750;
    margin-bottom: 8px;
}

.message-text {
    font-size: 16px;
    line-height: 1.6;
    opacity: 0.85;
}


/* ---------- Product cards ---------- */

.product-card {
    border: 1px solid var(--border-color-primary);
    border-radius: 20px;
    padding: 25px;
    height: 100%;
    box-sizing: border-box;
    background: var(--background-fill-secondary);
}

.product-title {
    font-size: 23px;
    font-weight: 750;
    margin-bottom: 10px;
}

.product-price {
    font-size: 25px;
    font-weight: 800;
    margin-bottom: 22px;
}


/* ---------- Specification rows ---------- */

.spec-row {
    display: flex;
    justify-content: space-between;
    gap: 20px;
    padding: 12px 0;
    border-bottom: 1px solid var(--border-color-primary);
    font-size: 14px;
}

.spec-row span {
    opacity: 0.65;
}

.spec-row b {
    text-align: right;
    font-weight: 600;
}


/* ---------- Hide Gradio footer ---------- */

footer {
    display: none !important;
}

"""


with gr.Blocks(
    theme=gr.themes.Soft(),
    css=custom_css,
    title="MoodMate"
) as app:

    # Header
    gr.Markdown(
        """
        <div id="header">
            <h1>📱 MoodMate</h1>
        </div>
        """,
        elem_id="header"
    )

    gr.Markdown(
        "Understand your experience. Discover what might suit you better.",
        elem_id="subtitle"
    )

    # Review form
    with gr.Group(elem_classes="card"):

        gr.Markdown("## 📝 Share Your Experience")

        with gr.Row():

            with gr.Column():

                product = gr.Dropdown(
                    choices=products,
                    label="Product Name",
                    info="Which phone are you reviewing?"
                )

                review_title = gr.Textbox(
                    label="Review Title",
                    placeholder="e.g. Great camera but battery could be better"
                )

            with gr.Column():

                rating = gr.Number(
                    label="Rating",
                    minimum=1,
                    maximum=5,
                    step=0.5,
                    info="Rate your phone from 1 to 5"
                )

                category = gr.Dropdown(
                    choices=[
                        "Display",
                        "Battery",
                        "Camera",
                        "Performance",
                        "Design",
                        "Price",
                        "Software",
                        "Others"
                    ],
                    label="Category"
                )

        comments = gr.Textbox(
            label="Your Comments",
            placeholder="Tell us about your experience...",
            lines=5
        )

        submit = gr.Button(
            "✨ Analyze Review",
            variant="primary",
            elem_id="submit-btn"
        )

    # Review result
    result = gr.Markdown(
        visible=False,
        elem_id="result"
    )

    # Keep recommendation data hidden
    recommendation_data = gr.State()

    show_button = gr.Button(
        "🔍 Show Recommendation",
        visible=False,
        variant="secondary",
        elem_id="recommend-btn"
    )

    # MoodMate message
    recommendation_message = gr.HTML(
        visible=False
    )

    # Two recommendation cards side-by-side
    with gr.Row(
        visible=False
    ) as recommendation_row:

        recommendation_1 = gr.HTML()

        recommendation_2 = gr.HTML()

    # Submit review
    submit.click(
        process_review,
        inputs=[
            product,
            review_title,
            rating,
            category,
            comments
        ],
        outputs=[
            result,
            recommendation_data
        ]
    ).then(
        lambda: gr.update(visible=True),
        outputs=result
    ).then(
        lambda: gr.update(visible=True),
        outputs=show_button
    )

    # Show recommendations
    show_button.click(
        show_recommendation,
        inputs=recommendation_data,
        outputs=[
            recommendation_message,
            recommendation_1,
            recommendation_2
        ]
    ).then(
        lambda: gr.update(visible=True),
        outputs=recommendation_message
    ).then(
        lambda: gr.update(visible=True),
        outputs=recommendation_row
    )


app.launch()