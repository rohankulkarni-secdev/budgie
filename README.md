# budgie

A budget and settling-in companion for international students — track your expenses, see where your money's going, and find country-specific guidance for visas, university steps, and local rules, all in one place.

## Features

- **Logs** — log expenses by category (Food, Rent, Transport, Entertainment, Groceries, Other), with support for all currencies (live conversion using exchangeRate API)
- **Savings system** - Keep track of monthly savings and/or losses.
- **Budget System** - Set budget for user.
  
  ----------- YET TO BE WORKED ON -----------------
- **Dashboard** — monthly spending, category breakdowns, high-spend days, and expense trends
- **Insights** — see which categories are eating your budget and what to consider cutting
- **Help!** — pick a country and get a list of relevant rules, from university requirements to visa documents to local norms

## Tech stack

- **Backend:** Flask (Python)
- **Database:** SQLite3
- **Templates:** Jinja2
- **Frontend:** vanilla HTML/CSS/JS (no framework)

## Getting started

Clone the repo:
```bash
git clone https://github.com/yourusername/budgie.git
cd budgie
```

Create and activate a virtual environment:
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Run the app:
```bash
python app.py
```

Then open `http://localhost:5000` in your browser.



This is currently a personal/portfolio project.

## License

MIT — feel free to fork and adapt for your own use.
