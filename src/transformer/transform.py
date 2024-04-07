import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer

# Load pre-trained model and tokenizer
model = T5ForConditionalGeneration.from_pretrained("t5-small")
tokenizer = T5Tokenizer.from_pretrained("t5-small")

# Data from the provided JSON
data = [{
    "airquality": {
        "city": "Gulu city",
        "start_time": "2024-01-01",
        "end_time": "2024-01-07",
        "diurnal": [
            {"hour": 0, "pm10_raw_value": 37.3108, "pm2_5_raw_value": 31.1102},
            {"hour": 1, "pm10_raw_value": 43.0327, "pm2_5_raw_value": 36.0745},
            # More data...
        ],
        "mean_pm_by_day_hour": [
            {"day": "Friday", "hour": 7, "pm10_raw_value": 161.5766, "pm2_5_raw_value": 154.4954},
            {"day": "Monday", "hour": 8, "pm10_raw_value": 53.5215, "pm2_5_raw_value": 49.8414},
            # More data...
        ],
        "sites": {
            "grid name": ["Gulu", "Unyama"],
            "number_of_sites": 5,
            # More data...
        },
        "status": "success"
    }
}]

# Extract relevant data for the report
diurnal_data = data[0]["airquality"]["diurnal"]
mean_pm_data = data[0]["airquality"]["mean_pm_by_day_hour"]
city = data[0]["airquality"]["city"]
start_time = data[0]["airquality"]["start_time"]
end_time = data[0]["airquality"]["end_time"]

# Generate introduction dynamically
introduction_template = "Introduction:\n\nAir quality report for {city} from {start_time} to {end_time}.\n\n"
introduction = introduction_template.format(city=city, start_time=start_time, end_time=end_time)

# Generating report
report = introduction + "Air Quality Report:\n\n"

# Diurnal Data
report += "Diurnal PM Data:\n"
for entry in diurnal_data:
    report += f"Hour {entry['hour']}: PM10 - {entry['pm10_raw_value']}, PM2.5 - {entry['pm2_5_raw_value']}\n"

# Mean PM Data
report += "\nMean PM Data by Day and Hour:\n"
for entry in mean_pm_data:
    report += f"Day: {entry['day']}, Hour: {entry['hour']}: PM10 - {entry['pm10_raw_value']}, PM2.5 - {entry['pm2_5_raw_value']}\n"

# Tokenize and generate summary
inputs = tokenizer.encode("summarize: " + report, return_tensors="pt", max_length=512, truncation=True)
summary_ids = model.generate(inputs, max_length=150, min_length=50, length_penalty=2.0, num_beams=4, early_stopping=True, num_return_sequences=1, use_cache=True)
summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

print(summary)
