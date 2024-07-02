# Odds Arbitrage Matches Finding

This project is designed to scrape data from the web and process it for further analysis to evaluate the presence of eventual games on which doing the arbitrage. The project includes a Python script (`scraping.py`) and a Jupyter notebook (`scraping.ipynb`) that demonstrate the scraping process and subsequent data handling.

## Files

- `draws.txt`: Contains, for each sport in oddsportal.com website, if the sport admits draws or not.
- `scraping.ipynb`: Jupyter notebook demonstrating the scraping process.
- `scraping.py`: Python script for scraping data.

## Requirements

To run this project, you'll need the following packages:

- `requests`
- `beautifulsoup4`
- `pandas`
- `numpy`
- `jupyter`

You can install the required packages using `pip`:

```bash
pip install requests beautifulsoup4 pandas numpy jupyter
```

## Usage

### Running the Python Script

You can run the `scraping.py` script using Python:

```bash
python scraping.py
```

This script will perform the web scraping and display eventual abritrable games.

### Using the Jupyter Notebook

To explore the scraping process and data analysis interactively, you can use the Jupyter notebook `scraping.ipynb`:

```bash
jupyter notebook scraping.ipynb
```

This will open the notebook in your web browser, where you can run the cells and see the outputs step by step.

## Project Structure

- `draws.txt`: Draws possibility in sport (T = sport admits draw, F otherwise).
- `scraping.ipynb`: Jupyter notebook with scraping and data analysis.
- `scraping.py`: Python script for scraping.

## Contributing

If you would like to contribute to this project, please fork the repository and submit a pull request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
