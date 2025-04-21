# Flask Time API

This simple Flask service exposes three endpoints:

- **`GET /api/hello`** — public “hello world” check  
- **`GET /api/secure_data`** — token‑protected secret data  
- **`GET /api/time/<city>`** — token‑protected current local time + UTC offset for a world capital

## Installation and Running the API

1. **Clone** your repo
2. **Create** & activate a venv:
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Run** app.py:
   ``` python3 app.py ```

In a seperate terminal...

4. **Run** the following command:
   ```
   curl -H "Authorization: Bearer SECRET-TOKEN" http://localhost:5000/api/time/city_name
   ```

   
