import streamlit as st
import requests
import matplotlib.pyplot as plt

# Streamlit UI setup
st.set_page_config(page_title="EcoGPT-Lite", layout="wide")
st.title("🔋 EcoGPT-Lite: AI Token & Energy Tracker")

# User input for prompt & model selection
prompt = st.text_area("Enter your prompt:", height=150)
model = st.selectbox("Select Model:", ["gpt-3.5-turbo", "gpt-4","deepseek-chat(Not Available)","claude-3-5-sonnet-2024102","grok-2-1212"])

if st.button("Calculate Token & Energy Usage"):
    if prompt.strip():
        # API request to Flask backend
        api_url = "http://127.0.0.1:5000/process_prompt"
        response = requests.post(api_url, json={"prompt": prompt, "model": model})

        if response.status_code == 200:
            data = response.json()
            tokens_used = data["token_count"]
            carbon_emissions = data["carbon_emissions"]
            model_response = data["response"]
            model_selected = data["model"]
            inference_time_seconds = data["inference_time_seconds"]
            
            # Display results
            st.success(f"✅ Tokens Used: {tokens_used}")
            st.info(f"⚡ Carbon Emissions by {model_selected}: {carbon_emissions:.6f} kg")
            st.info(f"🕒 Inference Time: {inference_time_seconds:.4f} seconds")
            st.info(f"{model_selected} Response: {model_response}")


            # Energy comparison chart
            energy_per_model = {
                "GPT-3.5 Turbo": 0.3 * tokens_used / 1_000_000,
                "GPT-4": 0.3 * tokens_used / 1_000_000
            }

            fig, ax = plt.subplots()
            ax.bar(energy_per_model.keys(), energy_per_model.values(), color=["blue", "red"])
            ax.set_ylabel("Energy (kWh)")
            ax.set_title("🔋 Energy Consumption by Model")
            st.pyplot(fig)
        else:
            st.error("❌ Error processing your request. Please try again.")
    else:
        st.warning("⚠️ Please enter a prompt before calculating.")
