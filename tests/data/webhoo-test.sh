curl -X POST https://groupb-project-3a82e1f0.fastapicloud.dev/webhook \
  -H "Content-Type: application/json" \
  -d '{"Records":[{"s3":{"object":{"key":"data/csv/review_chart_data_2026-09-24_22-00-00.csv"}}}]}'