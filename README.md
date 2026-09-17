# budgie

A budget and settling-in companion for international students — track your expenses, see where your money's going, and find country-specific guidance for visas, university steps, and local rules, all in one place.

## Features

- **Logs** — log expenses by category (Food, Rent, Transport, Entertainment, Groceries, Other), with support for EUR and INR
  ----------- YET TO BE WORKED ON -----------------
- **Dashboard** — a monthly overview of your spending and balance
- **Insights** — see which categories are eating your budget and what to consider cutting
- **Help!** — pick a country and get a list of relevant rules, from university requirements to visa documents to local norms
- Soft, warm interface designed to feel like a companion rather than a spreadsheet

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

## Project structure

```
budgie/
├── app.py                 # Flask routes and app logic
├── requirements.txt
├── budget.db               # SQLite database (created on first run, gitignored)
├── templates/
│   ├── home.html            # animated wheel navigation
│   ├── expenses.html        # log + view expenses (Logs)
│   ├── dashboard.html
│   ├── insights.html
│   └── help.html
└── static/
    └── (css/js assets, if split out from templates)
```

## Roadmap

- [x] Homepage with animated navigation wheel
- [x] Log expenses by category
- [x] Delete logged expenses
- [ ] Dashboard with monthly totals and balance
- [ ] Insights with spending breakdowns and suggestions
- [ ] Help! page with country-specific rules and resources
- [ ] live currency conversion
- [ ] Login authentication and region selection to retrieve region specific data (APIs)

## Contributing

This is currently a personal/portfolio project and not yet open for external contributions, but suggestions and issues are welcome.

## License

MIT — feel free to fork and adapt for your own use.
