# FlyBudget - Intelligent Flight Monitor

## 🎯 Project Description  
Automated flight tracking system that monitors prices across multiple destinations and sends SMS alerts when deals fall below predefined thresholds.

## 📦 Deliverables  
- Dual API integration (Amadeus + Twilio)
- Dynamic price monitoring engine
- SMS notification system
- Modular configuration management

## 🚀 Key Features  
- ✈️ Multi-destination monitoring
- 💰 Smart price filtering
- 📱 Instant SMS alerts
- 🔗 Automatic booking link generation
- 📅 Date-range flexibility

## 🛠️ Technologies Used  
| Component              | Technology                          |
|------------------------|-------------------------------------|
| **Core Language**      | Python 3                            |
| **Flight API**         | Amadeus for Developers              |
| **SMS Gateway**        | Twilio                              |
| **Config Management**  | python-dotenv                       |

## 🔄 How It Works  
1. The system checks flight prices using the Amadeus API.
2. If a price drops below the predefined threshold, an SMS is triggered via Twilio. 
3. The user receives a message with flight details and a booking link.

## ⚙️ Installation & Setup  

### 1. Clone Repository  
```bash
git clone https://github.com/seu-usuario/fly-budget.git
cd fly-budget
```

### 2. Install Dependencies  
```bash
pip install requests python-dotenv twilio
```

### 3. Environment Configuration  
Create `.env` file with:

```ini
# Amadeus API
API_KEY=your_amadeus_key
API_SECRET=your_amadeus_secret

# Twilio API
TWILIO_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE=+15555555555

# User Phone Number (for alerts)
USER_PHONE=+15551234567
```

### 4. Customize Your Search  
Edit `data.py` to define your preferences:

```ini
# User-defined destinations and price limits
self.destinations = {
    "LHR": 500,   # IATA code: Max price in USD (you can change the currency in the api.py file)
    "CDG": 450,   # Example: Paris (CDG) @ $450 max
    "MAD": 400,   # Add/remove destinations
    "BKK": 600,
}

# Departure airport (user-defined)
self.origin = "JFK"  # IATA code

# Travel dates (user-defined)
self.dates = {
    "2025-06-15": "2025-06-25",  # Format: departure → return
    # "YYYY-MM-DD": "YYYY-MM-DD"
}
```

### 5. Run Application  
```bash
python main.py
```

```plaintext
✈️ Cheap Flight Alert! ✈️  
From: JFK → CDG  
Departure: 2025-06-15 | Return: 2025-06-25  
Price: $236.91  
🔗 Check it out: 'Booking Link'
```

**Important Notes:**  
```plaintext
1. Required API Accounts:
   - Amadeus: https://developers.amadeus.com
   - Twilio: https://www.twilio.com

2. Customization Points:
   - dates in data.py
   - SMS template in api.py
   - Price thresholds per destination
```
