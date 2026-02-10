
import os
import django
from django.conf import settings

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_safety_system.settings')
django.setup()

from django.test import RequestFactory
from django.contrib.auth.models import User
from safety.views import CheckMotionView, AnalyzeAudioView
from safety.models import SensorEvent, AudioEvent, EmergencyAlert

def verify_endpoints():
    print("Verifying endpoints...")
    
    # Get the user that API will use (DefaultUserAuthentication uses first user)
    user = User.objects.first()
    if not user:
        user = User.objects.create(username='testuser', email='test@example.com')
        user.set_password('password')
        user.save()
    
    print(f"Test user: {user.username} (ID: {user.id})")

    factory = RequestFactory()

    # --- Test 1: Check Motion (High Anomaly) ---
    print("\nTest 1: Check Motion (High Anomaly)")
    data_high = {
        "accelerometer": {"x": 40.0, "y": 0.0, "z": 0.0}, # Max accel -> norm 1.0 (weighted 0.7)
        "gyroscope": {"x": 10.0, "y": 0.0, "z": 0.0}      # Max gyro -> norm 1.0 (weighted 0.3)
    } # Should result in score 1.0 > 0.6
    
    request = factory.post('/api/safety/check_motion/', data_high, content_type='application/json')
    request.user = user
    view = CheckMotionView.as_view()
    response = view(request)
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.data}")
    
    if response.status_code == 200 and response.data['anomaly_detected']:
        print("PASS: High anomaly detected.")
    else:
        print("FAIL: High anomaly not detected or error.")

    # --- Test 2: Check Motion (Low Anomaly) ---
    print("\nTest 2: Check Motion (Low Anomaly)")
    data_low = {
        "accelerometer": {"x": 0.0, "y": 9.8, "z": 0.0}, # Normal gravity -> Low score
        "gyroscope": {"x": 0.0, "y": 0.0, "z": 0.0}
    }
    
    request = factory.post('/api/safety/check_motion/', data_low, content_type='application/json')
    request.user = user
    view = CheckMotionView.as_view()
    response = view(request)
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.data}")

    if response.status_code == 200 and not response.data['anomaly_detected']:
         print("PASS: Low anomaly strictly ignored.")
    else:
         print("FAIL: Low anomaly detected or error.")


    # --- Test 3: Analyze Audio (Distress) ---
    print("\nTest 3: Analyze Audio (Distress)")
    # Using dummy logic: if MFCC[0] > 1.0 -> score 0.8
    data_audio_distress = {
        "audio_mfcc": [2.0, 0.5, 0.1], 
        "location": {"lat": 12.34, "lon": 56.78}
    }
    
    request = factory.post('/api/safety/analyze_audio/', data_audio_distress, content_type='application/json')
    request.user = user
    view = AnalyzeAudioView.as_view()
    response = view(request)
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.data}")
    
    if response.status_code == 200 and response.data['emergency_triggered']:
        print("PASS: Distress detected.")
        # Verify DB
        event = AudioEvent.objects.filter(user=user).last()
        alert = None
        if event:
            alert = EmergencyAlert.objects.filter(audio_event=event).first()
        
        if event and alert:
             print("PASS: Database records created (AudioEvent + EmergencyAlert).")
        else:
             print("FAIL: Database records missing.")
    else:
        print("FAIL: Distress not detected or error.")

    # --- Test 4: Analyze Audio (Normal) ---
    print("\nTest 4: Analyze Audio (Normal)")
    data_audio_normal = {
        "audio_mfcc": [0.1, 0.1, 0.1], 
        "location": {"lat": 12.34, "lon": 56.78}
    }
    
    request = factory.post('/api/safety/analyze_audio/', data_audio_normal, content_type='application/json')
    request.user = user
    view = AnalyzeAudioView.as_view()
    response = view(request)
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.data}")
    
    if response.status_code == 200 and not response.data['emergency_triggered']:
        print("PASS: Normal audio ignored.")
    else:
        print("FAIL: Normal audio triggered emergency or error.")

if __name__ == "__main__":
    try:
        verify_endpoints()
    except Exception as e:
        print(f"An error occurred: {e}")
