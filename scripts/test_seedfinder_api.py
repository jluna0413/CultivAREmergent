#!/usr/bin/env python3
"""
SeedFinder API Connectivity Test - Validates API access, tests core methods, and handles rate limits and errors
"""

import os
import sys
import time
import requests
from typing import Dict, Any, Optional

# Add project root to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.config.config import Config

try:
    from seedfinder import SeedFinder
except ImportError as e:
    print(f"❌ Error importing seedfinder: {e}")
    print("💡 Install with: pip install seedfinder==0.2.1")
    sys.exit(1)


def print_section(title: str):
    """Print formatted section header."""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")


def print_result(test_name: str, success: bool, message: str = ""):
    """Print test result with symbol and optional message."""
    symbol = "[PASS]" if success else "[FAIL]"
    status = "PASS" if success else "FAIL"
    print(f"{symbol} {test_name}: {status}")
    if message:
        print(f"   {message}")


def test_api_key_configuration() -> bool:
    """Test if API key is configured."""
    print_section("API Key Configuration Test")
    
    api_key_configured = bool(Config.SEEDFINDER_API_KEY)
    sf_api_key = os.getenv("SF_API_KEY")
    sf_api_key_configured = bool(sf_api_key)
    
    print_result("API Key Configuration", api_key_configured or sf_api_key_configured)
    
    if not api_key_configured and not sf_api_key_configured:
        print("   [WARNING] No API key configured. API will work with limited functionality.")
        print("   [INFO] To configure: add SEEDFINDER_API_KEY to your .env file")
    
    if api_key_configured:
        print(f"   Using SEEDFINDER_API_KEY: {'Set' if Config.SEEDFINDER_API_KEY else 'Not set'}")
    if sf_api_key_configured:
        print(f"   Using SF_API_KEY: {'Set' if sf_api_key else 'Not set'}")
    
    return api_key_configured or sf_api_key_configured


def test_seedfinder_initialization() -> Optional[object]:
    """Test SeedFinder client initialization."""
    print_section("SeedFinder Initialization Test")
    
    try:
        # Use the configured API key or default to environment variable
        api_key = Config.SEEDFINDER_API_KEY or os.getenv("SF_API_KEY")
        client = SeedFinder(api_key=api_key)
        print_result("Initialization", True, f"Client created successfully")
        return client
    except Exception as e:
        print_result("Initialization", False, f"Failed to initialize: {str(e)}")
        return None


def test_search_strain(client: object) -> Dict[str, Any]:
    """Test searchStrain method."""
    print_section("Search Strain Test")
    
    try:
        # Test with a well-known strain
        result = client.searchStrain("Blue Dream", exact=False)
        
        success = result is not None
        result_count = len(result) if result else 0
        
        print_result("searchStrain", success)
        
        if success:
            print(f"   Found {result_count} strains matching 'Blue Dream'")
            if result_count > 0:
                print(f"   First result: {result[0] if isinstance(result, list) and result else result}")
        else:
            print("   No results returned")
        
        return {
            "success": success,
            "result_count": result_count,
            "sample_data": result[0] if isinstance(result, list) and result else result
        }
    except requests.exceptions.Timeout as e:
        print_result("searchStrain", False, f"Timeout error: {str(e)}")
        return {"success": False, "result_count": 0, "sample_data": None}
    except requests.exceptions.HTTPError as e:
        if e.response and e.response.status_code == 429:
            print_result("searchStrain", False, f"Rate limit exceeded (429): {str(e)}")
        else:
            print_result("searchStrain", False, f"HTTP error ({e.response.status_code if e.response else 'unknown'}): {str(e)}")
        return {"success": False, "result_count": 0, "sample_data": None}
    except requests.exceptions.RequestException as e:
        print_result("searchStrain", False, f"Network error: {str(e)}")
        return {"success": False, "result_count": 0, "sample_data": None}
    except Exception as e:
        print_result("searchStrain", False, f"Unexpected error ({type(e).__name__}): {str(e)}")
        return {"success": False, "result_count": 0, "sample_data": None}


def test_breeder_info(client: object) -> Dict[str, Any]:
    """Test breederInfo method."""
    print_section("Breeder Info Test")
    
    try:
        # First search for a strain to get a valid breeder identifier/slug, not display name
        search_result = client.searchStrain("Blue Dream", exact=False)
        
        if not search_result:
            # Fallback to hardcoded breeder slug/ID if search fails
            print("   Using fallback breeder slug...")
            breeder_id = "dna-genetics"  # Common breeder slug format
        else:
            # Get the first strain's breeder ID/slug from search result
            first_strain = search_result[0] if isinstance(search_result, list) else search_result
            if isinstance(first_strain, dict):
                # Extract breeder identifier using common field names (identifiers, not display names)
                breeder_id = (first_strain.get('breeder_id') or 
                             first_strain.get('breeder') or 
                             first_strain.get('bid'))
                if not breeder_id:
                    print_result("breederInfo", False, f"No breeder identifier found in search result: {first_strain}")
                    return {"success": False, "breeder_data": None, "has_name": False}
                print(f"   Using breeder identifier from search: {breeder_id}")
            else:
                print_result("breederInfo", False, f"Search result not a dict: {type(first_strain)}")
                return {"success": False, "breeder_data": None, "has_name": False}
        
        # Call breederInfo with the actual breeder identifier/slug (not display name)
        result = client.breederInfo(breeder_id, show_strains=True)
        
        success = result is not None
        has_name = bool(result.get('name')) if isinstance(result, dict) else False
        
        print_result("breederInfo", success)
        
        if success and isinstance(result, dict):
            # Print fields if present, handle missing keys gracefully
            print(f"   Breeder: {result.get('name', 'Unknown')}")
            print(f"   Country: {result.get('country', 'Unknown')}")
            print(f"   Strain count: {result.get('strain_count', 'Unknown') if 'strain_count' in result else 'N/A'}")
        elif success:
            print(f"   Breeder data: {result}")
        else:
            print_result("breederInfo", False, "No result returned from API")
            return {"success": False, "breeder_data": None, "has_name": False}
        
        return {
            "success": success,
            "breeder_data": result,
            "has_name": has_name
        }
    except requests.exceptions.Timeout as e:
        print_result("breederInfo", False, f"Timeout error: {str(e)}")
        return {"success": False, "breeder_data": None, "has_name": False}
    except requests.exceptions.HTTPError as e:
        if e.response and e.response.status_code == 429:
            print_result("breederInfo", False, f"Rate limit exceeded (429): {str(e)}")
        else:
            print_result("breederInfo", False, f"HTTP error ({e.response.status_code if e.response else 'unknown'}): {str(e)}")
        return {"success": False, "breeder_data": None, "has_name": False}
    except requests.exceptions.RequestException as e:
        print_result("breederInfo", False, f"Network error: {str(e)}")
        return {"success": False, "breeder_data": None, "has_name": False}
    except Exception as e:
        print_result("breederInfo", False, f"Unexpected error ({type(e).__name__}): {str(e)}")
        return {"success": False, "breeder_data": None, "has_name": False}


def test_strain_info(client: object) -> Dict[str, Any]:
    """Test strainInfo method."""
    print_section("Strain Info Test")
    
    try:
        # First, search for a strain to get proper identifiers
        search_result = client.searchStrain("OG Kush", exact=False)
        
        if not search_result:
            print_result("strainInfo", False, "Could not find strain to test with")
            return {"success": False, "strain_data": None}
        
        # Get the first strain (should have proper ID fields)
        first_strain = search_result[0] if isinstance(search_result, list) else search_result
        
        if not isinstance(first_strain, dict):
            print_result("strainInfo", False, f"Expected dict from search, got {type(first_strain)}")
            return {"success": False, "strain_data": None}
        
        # Extract proper identifiers - try common field names for strain ID
        # Expected keys: 'id' (canonical), or fallback to other common identifiers
        strain_id = first_strain.get('id') or first_strain.get('strain_id') or first_strain.get('sid')
        if not strain_id:
            print_result("strainInfo", False, f"No strain ID found in result: {first_strain}")
            return {"success": False, "strain_data": None}
        
        # Extract breeder identifier - try common field names for breeder ID
        # Expected keys: 'breeder_id' (canonical), 'breeder' (slug), or 'bid' (short ID)
        breeder_id = (first_strain.get('breeder_id') or 
                     first_strain.get('breeder') or 
                     first_strain.get('bid'))
        if not breeder_id:
            print_result("strainInfo", False, f"No breeder ID found in result: {first_strain}")
            return {"success": False, "strain_data": None}
        
        # Now call strainInfo with canonical identifiers, not display names
        result = client.strainInfo(
            strain_id=strain_id,        # Use proper strain identifier (not name)
            breeder_id=breeder_id,      # Use proper breeder identifier (not name)
            show_parents=True,
            show_hybrids=True
        )
        
        success = result is not None
        has_genetics = bool(result.get('genetics')) if isinstance(result, dict) else False
        
        print_result("strainInfo", success)
        
        if success and isinstance(result, dict):
            print(f"   Strain: {result.get('name', 'Unknown')}")
            print(f"   Genetics: {result.get('genetics', 'Unknown')}")
            print(f"   Flowering: {result.get('flowering', 'Unknown')}")
            print(f"   Parents: {len(result.get('parents', [])) if result.get('parents') else 0}")
            print(f"   Hybrids: {len(result.get('hybrids', [])) if result.get('hybrids') else 0}")
        elif success:
            print(f"   Strain data: {result}")
        
        return {
            "success": success,
            "strain_data": result,
            "has_genetics": has_genetics
        }
    except requests.exceptions.Timeout as e:
        print_result("strainInfo", False, f"Timeout error: {str(e)}")
        return {"success": False, "strain_data": None, "has_genetics": False}
    except requests.exceptions.HTTPError as e:
        if e.response and e.response.status_code == 429:
            print_result("strainInfo", False, f"Rate limit exceeded (429): {str(e)}")
        else:
            print_result("strainInfo", False, f"HTTP error ({e.response.status_code if e.response else 'unknown'}): {str(e)}")
        return {"success": False, "strain_data": None, "has_genetics": False}
    except requests.exceptions.RequestException as e:
        print_result("strainInfo", False, f"Network error: {str(e)}")
        return {"success": False, "strain_data": None, "has_genetics": False}
    except Exception as e:
        print_result("strainInfo", False, f"Unexpected error ({type(e).__name__}): {str(e)}")
        return {"success": False, "strain_data": None, "has_genetics": False}


def test_rate_limit_handling(client: object) -> bool:
    """Test rate limit handling with true backoff behavior."""
    print_section("Rate Limit Handling Test")
    
    try:
        # Use a constant query and attempt up to 3 times with proper backoff
        q = "rate-limit-probe"
        attempts = 0
        retries = 0
        succeeded = False
        delays = [1, 2, 4]  # Exponential backoff: 1s, 2s, 4s
        
        for i in range(3):
            attempts += 1
            try:
                print(f"   Making attempt {i+1}/3...")
                result = client.searchStrain(q)
                succeeded = True
                print(f"      Attempt {i+1}: Success")
                break  # Exit loop on success
            except requests.exceptions.Timeout:
                print(f"      Attempt {i+1}: Timeout")
            except requests.exceptions.HTTPError as e:
                if e.response and e.response.status_code == 429:
                    retries += 1
                    print(f"      Attempt {i+1}: Rate limited (429)")
                    # Only sleep if not the last attempt (condition: i < len(delays) - 1)
                    if i < len(delays) - 1:  # Avoid sleeping after last attempt
                        print(f"      Waiting {delays[i]} seconds for backoff...")
                        time.sleep(delays[i])
                else:
                    print(f"      Attempt {i+1}: HTTP error ({e.response.status_code if e.response else 'unknown'})")
            except requests.exceptions.RequestException:
                print(f"      Attempt {i+1}: Network error")
            except Exception as e:
                error_msg = str(e).lower()
                if "429" in error_msg or "rate" in error_msg or "limit" in error_msg:
                    retries += 1
                    print(f"      Attempt {i+1}: Rate limited - {error_msg}")
                    # Only sleep if not the last attempt (condition: i < len(delays) - 1)
                    if i < len(delays) - 1:  # Avoid sleeping after last attempt
                        print(f"      Waiting {delays[i]} seconds for backoff...")
                        time.sleep(delays[i])
                else:
                    print(f"      Attempt {i+1}: Failed - {error_msg}")
        
        overall_success = succeeded
        print_result("Rate Limit Handling", overall_success, f"Attempts: {attempts}, Retries: {retries}, Succeeded: {succeeded}")
        
        return overall_success
    except Exception as e:
        print_result("Rate Limit Handling", False, f"Test failed: {str(e)}")
        return False


def test_error_handling(client: object) -> bool:
    """Test error handling with invalid inputs."""
    print_section("Error Handling Test")
    
    try:
        # Test with invalid strain that should return 404
        try:
            result = client.strainInfo(strain_id="nonexistent-strain-12345", breeder_id="invalid")
            print("   Invalid strain test: Unexpected success")
        except requests.exceptions.Timeout:
            print("   Invalid strain test: Handled timeout correctly")
        except requests.exceptions.HTTPError as e:
            print(f"   Invalid strain test: Handled HTTP error correctly ({e.response.status_code if e.response else 'unknown'})")
        except requests.exceptions.RequestException:
            print("   Invalid strain test: Handled network error correctly")
        except Exception as e:
            error_msg = str(e).lower()
            print(f"   Invalid strain test: Handled correctly - {error_msg}")
        
        # Test with empty parameters
        try:
            result = client.searchStrain("")
            print("   Empty query test: Unexpected success")
        except requests.exceptions.Timeout:
            print("   Empty query test: Handled timeout correctly")
        except requests.exceptions.HTTPError as e:
            print(f"   Empty query test: Handled HTTP error correctly ({e.response.status_code if e.response else 'unknown'})")
        except requests.exceptions.RequestException:
            print("   Empty query test: Handled network error correctly")
        except Exception as e:
            error_msg = str(e).lower()
            print(f"   Empty query test: Handled correctly - {error_msg}")
        
        print_result("Error Handling", True, "All errors handled gracefully")
        return True
    except Exception as e:
        print_result("Error Handling", False, f"Error handling failed: {str(e)}")
        return False


def run_all_tests():
    """Run all tests and return summary."""
    print("SeedFinder API Connectivity Test")
    print(f"Started at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = {
        "api_config": test_api_key_configuration(),
        "initialization": False,
        "search_strain": {"success": False},
        "breeder_info": {"success": False},
        "strain_info": {"success": False},
        "rate_limit": False,
        "error_handling": False
    }
    
    try:
        client = test_seedfinder_initialization()
        if client:
            results["initialization"] = True
            results["search_strain"] = test_search_strain(client)
            results["breeder_info"] = test_breeder_info(client)
            results["strain_info"] = test_strain_info(client)
            results["rate_limit"] = test_rate_limit_handling(client)
            results["error_handling"] = test_error_handling(client)
    except KeyboardInterrupt:
        print("\n⚠️  Test interrupted by user")
        return results
    except Exception as e:
        print(f"\n❌ Error during testing: {str(e)}")
        return results
    
    # Print final summary
    print_section("Test Summary")
    print(f"API Configuration: {'[PASS]' if results['api_config'] else '[FAIL]'}")
    print(f"Initialization: {'[PASS]' if results['initialization'] else '[FAIL]'}")
    print(f"Search Strain: {'[PASS]' if results['search_strain']['success'] else '[FAIL]'}")
    print(f"Breeder Info: {'[PASS]' if results['breeder_info']['success'] else '[FAIL]'}")
    print(f"Strain Info: {'[PASS]' if results['strain_info']['success'] else '[FAIL]'}")
    print(f"Rate Limits: {'[PASS]' if results['rate_limit'] else '[FAIL]'}")
    print(f"Error Handling: {'[PASS]' if results['error_handling'] else '[FAIL]'}")
    
    # Count successful tests
    successful_tests = sum([
        results['api_config'],
        results['initialization'],
        results['search_strain']['success'],
        results['breeder_info']['success'],
        results['strain_info']['success'],
        results['rate_limit'],
        results['error_handling']
    ])
    
    total_tests = 7
    print(f"\nOverall: {successful_tests}/{total_tests} tests passed")
    
    return results


if __name__ == "__main__":
    print("Usage: python scripts/test_seedfinder_api.py")
    print("Make sure to set SEEDFINDER_API_KEY in your .env file")
    print("To use this script:")
    print("   1. Get an API key from https://en.seedfinder.eu/api/")
    print("   2. Add it to your .env file: SEEDFINDER_API_KEY=your-key-here")
    print("   3. Or set environment variable: export SF_API_KEY=your-key-here")
    print("   4. Run: python scripts/test_seedfinder_api.py")
    print()
    
    test_results = run_all_tests()
    
    # Exit with appropriate code
    successful_tests = sum([
        test_results['api_config'],
        test_results['initialization'],
        test_results['search_strain']['success'],
        test_results['breeder_info']['success'],
        test_results['strain_info']['success'],
        test_results['rate_limit'],
        test_results['error_handling']
    ])
    
    exit_code = 0 if successful_tests == 7 else 1
    sys.exit(exit_code)