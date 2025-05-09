from textblob import TextBlob
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# ✅ New model name for grammar correction
model_name = "pszemraj/grammar-synthesis-small"

# Load the tokenizer and model
print(f"Loading model: {model_name}...")
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# Function for basic spelling correction using TextBlob
def correct_spelling(text: str) -> str:
    """
    This function uses TextBlob for spelling correction.
    """
    print("Correcting spelling...")
    blob = TextBlob(text)
    corrected_text = blob.correct()
    return str(corrected_text)

# Function for grammar correction using the transformer model
def correct_grammar(text: str) -> str:
    """
    This function uses the pre-trained transformer model for grammar correction.
    """
    print("Correcting grammar...")
    # Encode the input text using the tokenizer
    inputs = tokenizer(text, return_tensors="pt")
    
    # Generate the corrected output
    outputs = model.generate(
        inputs["input_ids"],
        max_length=256,
        num_beams=5,
        early_stopping=True
    )
    
    # Decode the generated output and return the corrected sentence
    corrected_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return corrected_text

# Main function to apply both spelling and grammar correction
def correct_transcript(transcription: str) -> str:
    """
    This function first corrects spelling using TextBlob, and then applies grammar correction using the transformer model.
    """
    # First correct spelling
    spelling_corrected_text = correct_spelling(transcription)
    
    # Then correct grammar on the already corrected text
    grammar_corrected_text = correct_grammar(spelling_corrected_text)
    
    return grammar_corrected_text

# Example usage
if __name__ == "__main__":
    test_input = "this are the example which have bad grammar"
    corrected_transcription = correct_transcription(test_input)
    print("Original:", test_input)
    print("Corrected:", corrected_transcription)
