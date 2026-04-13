from flask import Flask, request
import stripe
from supabase import create_client

app = Flask(__name__)

# KEYS
stripe.api_key = "SUA_STRIPE_SECRET_KEY"

supabase = create_client(
    "SUA_SUPABASE_URL",
    "SUA_SUPABASE_KEY"
)

# WEBHOOK SECRET
endpoint_secret = "SEU_WEBHOOK_SECRET"

@app.route('/webhook', methods=['POST'])
def webhook():
    payload = request.data
    sig_header = request.headers.get('stripe-signature')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except Exception as e:
        return str(e), 400

    # PAGAMENTO CONCLUÍDO
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        email = session['customer_details']['email']

        # DEFINE CRÉDITOS
        amount = session['amount_total']

        if amount == 399:
            credits = 10
        elif amount == 799:
            credits = 50
        else:
            credits = 9999

        # ATUALIZA NO BANCO
        user = supabase.table("users").select("*").eq("email", email).execute().data

        if user:
            current = user[0]["credits"]

            supabase.table("users").update({
                "credits": current + credits
            }).eq("email", email).execute()

    return "OK", 200

if __name__ == "__main__":
    app.run(port=4242)
