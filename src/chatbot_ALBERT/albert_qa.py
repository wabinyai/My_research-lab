from transformers import AlbertTokenizer, AlbertForQuestionAnswering
import torch
import streamlit as st

class AlbertQA:
    def __init__(self):
        # Load pre-trained ALBERT model and tokenizer
        self.tokenizer = AlbertTokenizer.from_pretrained('albert-base-v2')
        self.model = AlbertForQuestionAnswering.from_pretrained('twmkn9/albert-base-v2-squad2')

    def answer_question(self, question, context):
        if not context:
            return "No context provided for answering."

        max_length = 512  # ALBERT's max input length
        inputs = self.tokenizer.encode_plus(question, context, return_tensors='pt', truncation=True, max_length=max_length)
        input_ids = inputs['input_ids'].tolist()[0]
        
        # Check if context was truncated
        if len(input_ids) == max_length:
            st.warning("Context is too long and has been truncated.")
        
        # Get the output logits from the model
        outputs = self.model(**inputs)
        answer_start = torch.argmax(outputs.start_logits)
        answer_end = torch.argmax(outputs.end_logits) + 1

        # Convert tokens to the answer string
        answer = self.tokenizer.convert_tokens_to_string(self.tokenizer.convert_ids_to_tokens(input_ids[answer_start:answer_end]))
        return answer if answer.strip() else "No answer could be found in the context."

