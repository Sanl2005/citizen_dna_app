import requests
import json

try:
    response = requests.get('http://127.0.0.1:8000/schemes/')
    
    if response.status_code != 200:
        print(f"Error: Status {response.status_code}")
        print(response.text)
    else:
        schemes = response.json()
        
        print(f"\n✓ Found {len(schemes)} schemes\n")
        print("First scheme raw data:")
        print(json.dumps(schemes[0], indent=2))
        print("\n" + "="*60 + "\n")
        
        print("Categories for all schemes:")
        print("-" * 60)
        
        for scheme in schemes:
            cat = scheme.get('category', 'MISSING')
            print(f"• {scheme['scheme_name']}: {cat}")
    
except Exception as e:
    import traceback
    print(f"Error: {e}")
    traceback.print_exc()
