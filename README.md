# FakeCSV

FakeCSV is a web application for generating fake CSV datasets based on custom schemas.
http://chazzy.pythonanywhere.com/

## Features

- Create and manage schemas for CSV files
- Define columns with specific data types and ranges
- Generate fake datasets based on the defined schemas
- Download generated datasets in CSV format
- The files(static for admin and media) are stored on **AWS S3**.
- Errors tracking by **sentry.io**.

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
- Path: `/create-schema/`
- Edit an existing schema to modify its name, columns, or column properties.
- Path: `/edit-schema/<int:pk>/`
- Delete a schema and all associated datasets.
- Path: `/delete-schema/<int:pk>/`

### Manage Columns

- Delete a column from a schema.
- Path: `/delete-column/<int:pk>/`

### View Schema Details

- View detailed information about a schema, including its columns and generated datasets.
- Path: `/detail-schema/<int:pk>/`

### Generate Datasets

- Download generated datasets
- Path: `/download_data_set/<int:pk>/`
### View Schema List

- View a list of all created schemas.
- Path: `/list/`

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.
