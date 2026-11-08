curl -X POST http://127.0.0.1:8000/webhook \
  -H "Content-Type: application/json" \
  -d '{"Records":[{"s3":{"object":{"key":"data/csv/review_chart_data_2026-09-24_22-00-00.csv"}}}]}'