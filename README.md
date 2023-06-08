# FakeCSV

FakeCSV is a web application for generating fake CSV datasets based on custom schemas.

## Features

- Create and manage schemas for CSV files
- Define columns with specific data types and ranges
- Generate fake datasets based on the defined schemas
- Download generated datasets in CSV format

## Installation

1. Clone the repository:

   
   git clone <repository_url>

2. Install the required dependencies:
    pip install -r requirements.txt

3. Configure the database settings in the `settings.py` file.

4. Apply the database migrations:

5. Start the development server:

6. Access the application in your browser at `http://localhost:8000`.

## Usage

### Create and Manage Schemas

- Create a new schema by providing a name and defining the columns with their respective data types and ranges.
- Edit an existing schema to modify its name, columns, or column properties.
- Delete a schema and all associated datasets.

### Generate Datasets

- Generate a dataset for a schema by specifying the number of rows. The dataset will be processed and available for download.
- Download a generated dataset in CSV format.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.
