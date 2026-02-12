import sys
import os
import django
from django.conf import settings

# Setup Django environment
sys.path.append('d:/Projects/Protego')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_safety_system.settings')
django.setup()

from safety.services import MultiModalRiskFusionService

def test_fusion_logic():
    service = MultiModalRiskFusionService()
    
    print("Testing Fusion Logic...")

    # Case 1: Low inputs -> Should be low risk
    r1 = service._fuse_risk_scores(0.1, 0.1, 0.1)
    print(f"Low Inputs (0.1, 0.1, 0.1) -> {r1:.2f} [Expected < 0.4]")
    assert r1 < 0.4

    # Case 2: Moderate inputs -> Should be moderate
    r2 = service._fuse_risk_scores(0.5, 0.5, 0.5)
    print(f"Moderate Inputs (0.5, 0.5, 0.5) -> {r2:.2f} [Expected ~0.5]")

    # Case 3: High Audio ONLY (Scream) -> Should be HIGH (Critical Change)
    r3 = service._fuse_risk_scores(0.1, 0.9, 0.1)
    print(f"High Audio ONLY (0.1, 0.9, 0.1) -> {r3:.2f} [Expected >= 0.8 due to max logic]")
    assert r3 >= 0.8

    # Case 4: High Motion ONLY (Crash) -> Should be HIGH
    r4 = service._fuse_risk_scores(0.9, 0.1, 0.1)
    print(f"High Motion ONLY (0.9, 0.1, 0.1) -> {r4:.2f} [Expected >= 0.8 due to max logic]")
    assert r4 >= 0.8
    
    print("\nALL CHECKS PASSED!")

if __name__ == "__main__":
    test_fusion_logic()
