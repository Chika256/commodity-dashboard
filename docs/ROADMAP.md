# Roadmap

## Near term
- Capture real screenshot assets for README once connected to live data.
- Add CI pipeline (GitHub Actions) to run linting, formatting, and tests on every push.
- Package Streamlit app with Docker for reproducible deployment.

## Mid term
- Deploy to AWS (e.g., ECS or App Runner) with scheduled cache warmers.
- Introduce alert microservice to send emails/SMS when thresholds are breached.
- Integrate Kafka for streaming price ingestion to reduce reliance on yfinance polling.

## Long term
- Expand coverage to power and emissions markets, including spread analytics.
- Implement user authentication and per-trader watchlists.
- Add scenario analysis with Monte Carlo simulations for risk teams.
