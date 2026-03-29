# Telemetry Service
*Done by: Leheza Daniil IM-41*

## Prerequisites
- Python 3.10+

## Installation
Clone the repository:
```bash
git clone https://github.com/Tr1ggerbtw/telemetry-service.git
cd telemetry-service
```

Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux
venv\Scripts\activate     # Windows
# If you get execution policy error on WINDOWS run this:
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
```

Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration
Create a `.env` file in the root directory:
```
SECRET_KEY=your-secret-key-here
DATABASE_URI=sqlite:///app.db
```

## Running
```bash
python run.py
```

## Testing
```bash
pytest
```

