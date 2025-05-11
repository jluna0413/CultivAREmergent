# CultivAR Developer Documentation

## Collection Page Implementation

The Collection page (Strains page) allows users to manage their cannabis strain database. This document explains the implementation details of the strain management functionality.

### Database Models

The strain management functionality uses the following database models:

1. **Strain**: Represents a cannabis strain with properties like name, genetics, description, etc.
   - Located in `app/models/base_models.py`
   - Key fields: id, name, breeder_id, indica, sativa, autoflower, description, seed_count, cycle_time, url, short_description

2. **Breeder**: Represents a seed breeder or bank.
   - Located in `app/models/base_models.py`
   - Key fields: id, name

### Handlers

The business logic for strain management is implemented in the following handler modules:

1. **strain_handlers.py**: Contains functions for managing strains.
   - `get_strain(strain_id)`: Get a strain by ID.
   - `get_in_stock_strains()`: Get all strains with seed_count > 0.
   - `get_out_of_stock_strains()`: Get all strains with seed_count = 0.
   - `add_strain(data)`: Add a new strain to the database.
   - `update_strain(strain_id, data)`: Update an existing strain.
   - `delete_strain(strain_id)`: Delete a strain from the database.

2. **breeder_handlers.py**: Contains functions for managing breeders.
   - `get_breeders()`: Get all breeders.
   - `add_breeder(data)`: Add a new breeder to the database.
   - `update_breeder(breeder_id, data)`: Update an existing breeder.
   - `delete_breeder(breeder_id)`: Delete a breeder from the database.

### API Routes

The API routes for strain management are defined in `app/routes/routes.py`:

1. **Strain API Routes**:
   - `GET /strains/<int:strain_id>`: Get a strain by ID.
   - `GET /strains/in-stock`: Get all in-stock strains.
   - `GET /strains/out-of-stock`: Get all out-of-stock strains.
   - `POST /strains`: Add a new strain.
   - `PUT /strains/<int:strain_id>`: Update a strain.
   - `DELETE /strains/<int:strain_id>`: Delete a strain.

2. **Breeder API Routes**:
   - `GET /breeders`: Get all breeders.
   - `POST /breeders`: Add a new breeder.
   - `PUT /breeders/<int:breeder_id>`: Update a breeder.
   - `DELETE /breeders/<int:breeder_id>`: Delete a breeder.

### Frontend Implementation

The frontend for the Collection page is implemented in the following files:

1. **strains.html**: The main template for the Collection page.
   - Located in `app/web/templates/views/strains.html`
   - Contains the HTML structure for the page, including the strain cards, filters, and modals.

2. **JavaScript**: The JavaScript code for the Collection page is embedded in the strains.html template.
   - Handles form submission for adding, editing, and deleting strains and breeders.
   - Implements filtering and searching functionality.
   - Manages the UI for the genetics slider and view modes.

### Configuration Loading

The application uses a configuration system to load data from the database into memory for faster access:

1. **Config Class**: Defined in `app/config/config.py`
   - Contains static properties for storing application data, including Strains and Breeders.

2. **load_config_from_db()**: Defined in `app/config/load_config.py`
   - Loads data from the database into the Config class.
   - Called during application startup and after any changes to the database.

### Implementation Notes

1. **Modal Handling**: The application uses Bootstrap 5 modals for the add/edit forms.
   - The "Add Strain" modal can be opened from the main page.
   - The "Add Breeder" modal can be opened from within the "Add Strain" modal.
   - When a breeder is added, the "Add Breeder" modal is closed and the "Add Strain" modal is reopened with the new breeder selected.

2. **Form Validation**: Basic form validation is implemented in JavaScript.
   - The strain name is required.
   - The Indica/Sativa percentages must add up to 100%.

3. **Database Updates**: After any changes to the database (adding, updating, or deleting strains or breeders), the Config is reloaded to ensure the UI displays the latest data.

4. **Error Handling**: All API calls include error handling to display appropriate messages to the user.

### Future Improvements

1. **Pagination**: Implement pagination for the strain list to improve performance with large collections.
2. **Image Upload**: Add the ability to upload and display strain images.
3. **Strain Tags**: Implement a tagging system for strains to allow for more advanced filtering.
4. **Strain Reviews**: Add the ability for users to rate and review strains.
5. **Strain Lineage**: Implement a visual representation of strain genetics and lineage.
