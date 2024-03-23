import torch
import pandas
import pandas as pd
from transformers import T5ForConditionalGeneration, T5Tokenizer

# Load pre-trained model and tokenizer
model = T5ForConditionalGeneration.from_pretrained("t5-small")
tokenizer = T5Tokenizer.from_pretrained("t5-small")

# Data from the provided JSON
data = pd.read_json('data/diurnal.json')
#data = pd.DataFrame.from_dict(df)
print (data)
# Extract relevant data for the report
diurnal_data = data['airquality']['diurnal']
city = data['airquality']['city']
start_time = data['airquality']['start_time']
end_time = data['airquality']['end_time']
mean_pm_data = data["airquality"]["mean_pm_by_day_hour"]

# Generate introduction dynamically
introduction_template = "Introduction:\n\nAir quality report for {city} from {start_time} to {end_time}.\n\n"
introduction = introduction_template.format(city=city, start_time=start_time, end_time=end_time)

# Generating report
report = introduction + "Air Quality Report:\n\n"

# Diurnal Data
report += "Diurnal PM Data (Hourly):\n"
hourly_pm2_5_values = [entry['pm2_5_raw_value'] for entry in diurnal_data]
max_pm2_5 = max(hourly_pm2_5_values)
min_pm2_5 = min(hourly_pm2_5_values)
peak_hours = [entry['hour'] for entry in diurnal_data if entry['pm2_5_raw_value'] == max_pm2_5]
valley_hours = [entry['hour'] for entry in diurnal_data if entry['pm2_5_raw_value'] == min_pm2_5]

for entry in diurnal_data:
    report += f"Hour {entry['hour']}: PM10 - {entry['pm10_raw_value']} µg/m³, PM2.5 - {entry['pm2_5_raw_value']} µg/m³\n"

# Explain peaks and dips
report += "\n\n"
report += f"Peak PM2.5 levels observed at hour(s): {', '.join(map(str, peak_hours))}\n"
report += f"Valley PM2.5 levels observed at hour(s): {', '.join(map(str, valley_hours))}\n"

# Prompt for the transformer
prompt = "Summarize the diurnal variation of PM2.5 levels in {{city}}."

# Tokenize and generate summary
inputs = tokenizer.encode(prompt + report, return_tensors="pt", max_length=512, truncation=True)
summary_ids = model.generate(inputs, max_length=150, min_length=50, length_penalty=2.0, num_beams=4, early_stopping=True, num_return_sequences=1, use_cache=True)
summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

print(summary)
