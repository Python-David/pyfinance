
# PyFinance CLI

PyFinance is a command-line interface (CLI) application for managing personal finances, including expenses and investments.

## Features

- Register and login functionality for users.
- Add, list, and import expenses and investments from CSV files.
- Generate plots for expenses by category.

## Installation

To install PyFinance, you will need Python 3.8 or later. Clone the repository and install the dependencies:

```bash
git clone https://github.com/yourusername/pyfinance.git
cd pyfinance
pip install -r requirements.txt
```

## Configuration

PyFinance uses environment variables for configuration. Create a `.env` file in the root directory of the project with the following content:

```dotenv
DATABASE_URL=postgresql://pyfinance_user:pyfinance_pass@localhost:5431/pyfinance_db
POSTGRES_USER=pyfinance_user
POSTGRES_PASSWORD=pyfinance_pass
POSTGRES_DB=pyfinance_db
```

You can modify the values to match your database settings. The application will use these values to connect to the PostgreSQL database.

## Usage

### Setting Up the Database

Start the PostgreSQL database using Docker Compose:

```bash
docker-compose up -d
```

### User Commands

- Register a new user:

  ```bash
  pyfinance register --name <name> --email <email> --password <password>
  ```

- Login as an existing user:

  ```bash
  pyfinance login --email <email> --password <password>
  ```

### Expense Commands

- Add a new expense:

  ```bash
  pyfinance add-expense --category <category> --amount <amount> --date <YYYY-MM-DD> [--description <description>]
  ```

- List expenses:

  ```bash
  pyfinance list-expenses [--year <year>] [--month <month>] [--day <day>] [--show-csv]
  ```

- Add expenses from a CSV file:

  ```bash
  pyfinance add-expenses-from-csv --file-path <path/to/csv>
  ```

### Investment Commands

- Add a new investment:

  ```bash
  pyfinance add-investment --type <type> --amount <amount> --date <YYYY-MM-DD> [--description <description>]
  ```

- List investments:

  ```bash
  pyfinance list-investments [--year <year>] [--month <month>] [--day <day>] [--show-csv]
  ```

- Add investments from a CSV file:

  ```bash
  pyfinance add-investments-from-csv --file-path <path/to/csv>
  ```

### Plot Commands

- Generate and save a plot of expenses by category:

  ```bash
  pyfinance show [--year <year>] [--month <month>] [--day <day>]
  ```

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue.

## License

This project is licensed under the [MIT License](LICENSE).
