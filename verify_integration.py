
import os
import django
import sys
from datetime import datetime

# Setup Django environment
sys.path.append('/Users/deepika/Documents/PROJECTS/AI-Safety-System-for-Women-Students')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_safety_system.settings')
django.setup()

from django.contrib.auth.models import User
from routing.services import RoutePredictionService
from routing.models import Route

def verify_route_prediction():
    print("Starting Route Prediction Verification...")
    
    # 1. Ensure a test user exists
    user, created = User.objects.get_or_create(username='test_user')
    if created:
        print("Created test user.")
    
    # 2. Define test coordinates (Chicago)
    # Origin: Near UIC
    origin_lat = 41.8640
    origin_lng = -87.7068
    # Dest: Near Loop
    dest_lat = 41.7829
    dest_lng = -87.6043
    
    service = RoutePredictionService()
    
    try:
        print("Calling predict_safe_route...")
        result = service.predict_safe_route(
            origin_lat=origin_lat,
            origin_lng=origin_lng,
            destination_lat=dest_lat,
            destination_lng=dest_lng,
            route_type='safest',
            user=user,
            time_of_day=datetime.now().time(),
            day_of_week=datetime.now().weekday()
        )
        
        route = result['route']
        print(f"Success! Route ID: {route.id}")
        print(f"Total Distance: {route.total_distance:.2f} km")
        print(f"Est Duration: {route.estimated_duration:.2f} mins")
        print(f"Risk Score: {route.overall_risk_score:.4f}")
        
        # Check segments
        segment_count = route.segments.count()
        print(f"Generated {segment_count} segments.")
        
        if segment_count == 0:
            print("ERROR: No segments generated!")
            exit(1)
            
        print("Verification PASSED.")
        
    except Exception as e:
        print(f"Verification FAILED with error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)

if __name__ == "__main__":
    verify_route_prediction()
