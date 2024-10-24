# Weather Monitoring System

A real-time weather monitoring system that fetches and displays weather data for major Indian cities using the OpenWeatherMap API.

## Features

- Real-time weather data collection
- Support for multiple cities (Delhi, Mumbai, Chennai, Bangalore, Kolkata, Hyderabad)
- Temperature tracking (average, maximum, minimum, feels like)
- Weather condition monitoring
- Web interface for data visualization

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/roar3691/weather-monitoring-system.git
   ```

2. Install required packages:
   ```bash
   pip install requests flask schedule
   ```

3. Set up the database:
   ```bash
   python setup_database.py
   ```

4. Start the weather data collection:
   ```bash
   python rule_engine.py
   ```

5. Start the web interface:
   ```bash
   python app.py
   ```

6. Access the web interface at `http://127.0.0.1:5000`

## API Key

This project uses the OpenWeatherMap API with key: 6df9088b6249404f60dd52436845d94b

## File Structure

- `setup_database.py`: Database initialization and test data setup
- `rule_engine.py`: Weather data collection and processing
- `app.py`: Web interface implementation

## Dependencies

- Python 3.x
- Flask
- Requests
- Schedule
