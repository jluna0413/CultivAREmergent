# SeedFinder API Integration

This document provides setup instructions, API usage examples, and troubleshooting guidance for integrating SeedFinder cannabis strain and breeder data into CultivAR.

**Note:** The external SeedFinder API uses "strain" terminology in its method names and data structures (e.g., `searchStrain`, `strainInfo`), which we preserve to match the external API contract. Within CultivAR, these correspond to "cultivar" concepts.

## Table of Contents
- [Setup and Configuration](#setup-and-configuration)
- [API Key Acquisition](#api-key-acquisition)
- [Testing the Integration](#testing-the-integration)
- [Available API Methods](#available-api-methods)
- [Usage Examples](#usage-examples)
- [Rate Limits and Best Practices](#rate-limits-and-best-practices)
- [Error Handling](#error-handling)
- [Troubleshooting](#troubleshooting)
- [Future Enhancements](#future-enhancements)

## Setup and Configuration

### Prerequisites
- Python 3.9+
- pip
- CultivAR installation

### Installation steps:
1. **Install the package** (already in requirements.txt): `pip install seedfinder==0.2.1`
2. **Obtain API key** from seedfinder.eu
3. **Configure environment variables**

### Configuration details:
The integration supports two ways to configure the API key:
- `SEEDFINDER_API_KEY` in .env files (recommended for consistency with project naming)
- `SF_API_KEY` environment variable (SeedFinder's default)

**Example .env entry:**
```
SEEDFINDER_API_KEY=your-api-key-here
```

**Note:** The API works with limited functionality without an API key for testing purposes.

## API Key Acquisition

### Step-by-step guide:
1. Visit https://en.seedfinder.eu/
2. Create an account or log in
3. Navigate to API section: https://en.seedfinder.eu/api/
4. Generate API key
5. Copy key to .env file

### Security note
Keep API key confidential, don't commit to version control

### Rate limits
Check the SeedFinder website for current free tier limits and paid options.

## Testing the Integration

### Running the test script:
```bash
python scripts/test_seedfinder_api.py
```

### Expected output:
- API key configuration status
- Client initialization results  
- Search, breeder info, and cultivar info method tests
- Rate limit handling validation
- Error handling verification

### Interpreting results:
- ✅ Success indicators: API calls return data successfully
- ❌ Common failure reasons: Missing API key, rate limits, network issues
- Verify API connectivity by checking that methods return expected data

## Available API Methods

**Note:** These are external SeedFinder API methods that use "strain" terminology in their names and parameters.

| Method | Parameters | Returns | Use Case |
|--------|------------|---------|----------|
| `searchStrain(strain, exact=False)` | strain name (string), exact match flag (boolean) | List of matching strains with IDs and basic info | Finding strains by name for import |
| `breederInfo(breeder_id, show_strains=True)` | breeder ID (string), include strains flag (boolean) | Breeder details including country, website, strain list | Populating breeder database with detailed information |
| `strainInfo(strain_id, breeder_id, lang='en', show_parents=False, show_hybrids=False, ...)` | strain ID, breeder ID, language, various flags | Comprehensive strain data including genetics, flowering time, cannabinoid content, lineage | Importing complete strain profiles with lineage data |
| `parents(strain_id, breeder_id, generations=1)` | strain ID, breeder ID, number of generations | Parent strain information for lineage tracking | Building genetic lineage trees |
| `hybrids(strain_id, breeder_id, generations=1)` | strain ID, breeder ID, number of generations | Hybrid offspring information | Discovering related strains |

## Usage Examples

**Note:** These examples show external SeedFinder API calls that use "strain" terminology, which maps to cultivar concepts in CultivAR.

### Example 1: Search for a strain
```python
from seedfinder import SeedFinder
from app.config.config import Config

# Initialize client
client = SeedFinder(api_key=Config.SEEDFINDER_API_KEY)

# Search for strains (external API method)
results = client.searchStrain("Blue Dream", exact=False)
print(f"Found {len(results)} strains matching 'Blue Dream'")

# Extract identifiers for subsequent API calls
if results:
    first_strain = results[0] if isinstance(results, list) else results
    if isinstance(first_strain, dict):
        # Get strain and breeder identifiers (not display names) for API calls
        strain_id = first_strain.get('id') or first_strain.get('strain_id') or first_strain.get('sid')
        breeder_id = (first_strain.get('breeder_id') or 
                     first_strain.get('breeder') or 
                     first_strain.get('bid'))
        print(f"Strain ID: {strain_id}")
        print(f"Breeder ID: {breeder_id}")
```

### Example 2: Get breeder information
```python
# Get breeder details using breeder identifier/slug, not display name (external API method)
breeder_data = client.breederInfo("dna-genetics", show_strains=True)  # Use breeder slug/ID
print(f"Breeder: {breeder_data.get('name')}")
print(f"Country: {breeder_data.get('country')}")
```

### Example 3: Get detailed strain info with lineage
```python
# First search for strain to get proper identifiers, then call strainInfo with identifiers
search_results = client.searchStrain("OG Kush", exact=False)
if search_results:
    first_strain = search_results[0] if isinstance(search_results, list) else search_results
    if isinstance(first_strain, dict):
        # Extract proper identifiers (not display names) for the API call
        strain_id = first_strain.get('id') or first_strain.get('strain_id') or first_strain.get('sid')
        breeder_id = (first_strain.get('breeder_id') or 
                     first_strain.get('breeder') or 
                     first_strain.get('bid'))
        
        # Call strainInfo with canonical identifiers (slugs), not display names
        strain_data = client.strainInfo(
            strain_id=strain_id,      # Strain identifier (not name)
            breeder_id=breeder_id,    # Breeder identifier (not name)  
            show_parents=True, 
            show_hybrids=True
        )
        print(f"Strain: {strain_data.get('name')}")
        print(f"Genetics: {strain_data.get('genetics')}")
        print(f"Parents: {len(strain_data.get('parents', []))}")

# Note: strain_id and breeder_id are identifiers (typically slugs), not display names
```

### Example 4: Error handling pattern
```python
try:
    results = client.searchStrain("OG Kush", exact=False)  # External API call
    # Process results
    if results:
        first_strain = results[0] if isinstance(results, list) else results
        if isinstance(first_strain, dict):
            # Use proper identifiers for strainInfo call
            strain_id = first_strain.get('id') or first_strain.get('strain_id')
            breeder_id = first_strain.get('breeder_id') or first_strain.get('breeder')
            
            if strain_id and breeder_id:
                strain_data = client.strainInfo(
                    strain_id=strain_id,      # Use identifiers, not names
                    breeder_id=breeder_id,    # Use identifiers, not names
                    show_parents=True,
                    show_hybrids=True
                )
except requests.exceptions.Timeout as e:
    print(f"API request timed out: {e}")
except requests.exceptions.HTTPError as e:
    if e.response.status_code == 429:  # Rate limit
        print(f"Rate limit exceeded: {e}")
    else:
        print(f"HTTP error: {e}")
except requests.exceptions.RequestException as e:
    print(f"Network request failed: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Rate Limits and Best Practices

### Rate limit information:
- Free tier: Check SeedFinder website for current limits
- Paid tier: Available on the website for higher limits

### Best practices:
- **Implement caching** to reduce API calls
- **Use exponential backoff** for retries when rate limited
- **Batch operations** when possible to minimize requests
- **Cache frequently accessed data** locally (recommend 1-hour TTL for strain data, 24-hour TTL for breeder data)
- **Respect rate limits** to avoid IP bans

### Caching strategy:
- Use Redis or in-memory cache for performance
- Cache 1-hour TTL for strain data (frequently updated)
- Cache 24-hour TTL for breeder data (less frequently updated)

## Error Handling

### Common errors and solutions:

**ImportError: Module 'seedfinder' not found**
- Solution: Install package with `pip install seedfinder==0.2.1`

**HTTP 401 Unauthorized: Invalid API key**
- Solution: Check .env configuration and verify your API key

**HTTP 404 Not Found: Invalid strain/breeder ID**
- Solution: Verify strain/breeder names and IDs format

**HTTP 429 Too Many Requests: Rate limit exceeded**
- Solution: Implement exponential backoff and caching

**Network errors: Connection issues**
- Solution: Check internet connectivity and SeedFinder API status

**Timeout errors: Slow response**
- Solution: Increase timeout settings and verify network connection

### Error handling pattern:
```python
import time
import requests

def make_api_call_with_retry(client, method, *args, max_retries=3):
    for attempt in range(max_retries):
        try:
            return method(*args)
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:  # Rate limited
                wait_time = (2 ** attempt) + 1  # Exponential backoff
                print(f"Rate limited, waiting {wait_time}s...")
                time.sleep(wait_time)
                continue
            else:
                raise
        except requests.exceptions.RequestException:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)
```

## Troubleshooting

### Problem: "Module 'seedfinder' not found"
- Solution: Install package, verify requirements.txt contains `seedfinder==0.2.1`

### Problem: "API key not configured"
- Solution: Check .env file, verify `Config.SEEDFINDER_API_KEY` loads correctly

### Problem: "Rate limit exceeded"
- Solution: Implement caching layer, reduce request frequency, use exponential backoff

### Problem: "No results returned"
- Solution: Verify strain/breeder names format, try different search terms

### Problem: "Timeout errors"
- Solution: Check network connectivity, increase timeout settings, verify SeedFinder API status

### Debugging tips:
- Enable debug logging to see API request details
- Use test script (`python scripts/test_seedfinder_api.py`) to validate connectivity
- Check SeedFinder API status page for service availability

## Future Enhancements

### Planned features:
- **Data mapping service** (Phase SF-003): Transform API strain data to CultivAR cultivar models
- **Service layer with caching** (Phase SF-004): Efficient data access patterns
- **Bulk import scripts** (Phase SF-007): Mass data import capabilities  
- **UI integration** (Phase SF-008): User interface for data management

### Extension points:
- Custom data transformations for specific use cases
- Additional API endpoints as SeedFinder adds new features
- Integration with other cannabis strain databases
- Advanced lineage tracking and genetic analysis

## References

- [SeedFinder Python package documentation](https://seedfinder-python.readthedocs.io/)
- [SeedFinder API documentation](https://en.seedfinder.eu/api/)
- [PyPI package page](https://pypi.org/project/seedfinder/)
- [CultivAR project roadmap](Roadmap.md)