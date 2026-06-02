from rag_fir_engine import retrieve_sections
from langdetect import detect
from deep_translator import GoogleTranslator

def preprocess_fir(fir_text):
    try:
        lang = detect(fir_text)
    except:
        lang = "en"

    if lang == "hi":
        fir_text = GoogleTranslator(source="hi", target="en").translate(fir_text)

    return fir_text, lang


def fir_chatbot(fir_text):
    processed_text, detected_lang = preprocess_fir(fir_text)

    # retrieve_sections returns a mixed list; split here for chatbot formatting
    sections = retrieve_sections(processed_text)
    ipc = [s["section_text"] for s in sections if "IPC" in s["section_text"]]
    crpc = [s["section_text"] for s in sections if "CrPC" in s["section_text"]]

    response = ""
    response += "🧾 FIR EXPLANATION (SIMPLIFIED)\n"
    response += "=" * 50 + "\n\n"

    response += f"🌐 Detected Language: {'Hindi' if detected_lang == 'hi' else 'English'}\n\n"

    response += "📌 FIR SUMMARY:\n"
    response += (
        "The FIR describes an alleged incident involving the accused. "
        "Based on the description, the following legal provisions may apply.\n\n"
    )

    if ipc:
        response += "⚖️ APPLICABLE IPC SECTIONS:\n"
        for sec in ipc:
            response += f"\n{sec}\n"

    if crpc:
        response += "\n📜 RELEVANT CrPC PROCEDURES:\n"
        for sec in crpc:
            response += f"\n{sec}\n"

    response += "\n⚠️ DISCLAIMER:\n"
    response += (
        "This information is for legal awareness only and does not constitute legal advice."
    )

    return response
