import unittest
import sys
import os
import httpx

# Ensure project root is on sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.main import app
from backend.database import SessionLocal, Base, engine
from backend.analytics import seed_demo

class TestRoadSafeAPI(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        Base.metadata.create_all(bind=engine)
        db = SessionLocal()
        seed_demo(db)
        db.close()
        self.transport = httpx.ASGITransport(app=app)
        self.client = httpx.AsyncClient(transport=self.transport, base_url="http://testserver")

    async def asyncTearDown(self):
        await self.client.aclose()

    async def test_health(self):
        r = await self.client.get('/health')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()['status'], 'healthy')

    async def test_meta(self):
        r = await self.client.get('/api/v1/meta')
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertEqual(data['team_id'], 'Team_015')
        self.assertIn('six_core_answers', data)

    async def test_summary_stats(self):
        r = await self.client.get('/api/v1/accidents/stats/summary')
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertGreater(data['total_accidents'], 50)
        self.assertGreater(data['fatalities'], 500)
        self.assertGreater(data['critical_blackspots'], 5)

    async def test_hotspots_where_question(self):
        """Question 1: Where are accidents most likely to occur?"""
        r = await self.client.get('/api/v1/accidents/analytics/hotspots')
        self.assertEqual(r.status_code, 200)
        hotspots = r.json()
        self.assertGreater(len(hotspots), 50)
        self.assertGreaterEqual(hotspots[0]['risk_score'], hotspots[-1]['risk_score'])
        self.assertTrue('drivers' in hotspots[0])
        self.assertGreater(len(hotspots[0]['drivers']), 0)

    async def test_risk_scoring_why_question(self):
        """Question 2: Why are accidents occurring there? Explainable AI."""
        r = await self.client.get('/api/v1/accidents/analytics/risk?latitude=28.7365&longitude=77.1643&operating_speed=110&speed_limit=70&weather=Rain&road_condition=Wet&time_of_day=Night')
        self.assertEqual(r.status_code, 200)
        res = r.json()
        self.assertGreaterEqual(res['risk_score'], 70)
        self.assertEqual(res['risk_band'], 'Critical')
        self.assertIn('drivers', res)
        for d in res['drivers']:
            self.assertIn('actionable_insight', d)

    async def test_causes_distribution(self):
        """Question 2: MoRTH Cause of Accident Breakdown"""
        r = await self.client.get('/api/v1/accidents/analytics/causes')
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertIn('national_causes', data)
        top = next((c for c in data['national_causes'] if c['cause'] == 'Overspeeding'), None)
        self.assertIsNotNone(top)
        self.assertGreater(top['share_crashes_pct'], 60)

    async def test_vulnerability_who_question(self):
        """Question 3: Who/what is most vulnerable?"""
        r = await self.client.get('/api/v1/accidents/analytics/vulnerability')
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertIn('modes', data)
        self.assertGreater(data['vru_share_total'], 60.0)

    async def test_temporal_when_question(self):
        """Question 4: When is the risk highest?"""
        r = await self.client.get('/api/v1/accidents/analytics/temporal')
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertIn('hourly_distribution', data)
        self.assertEqual(len(data['hourly_distribution']), 24)

    async def test_prediction_forecasting(self):
        """Question 4: Prediction / Future Risk Forecasting"""
        r = await self.client.get('/api/v1/accidents/analytics/prediction?horizon_days=90')
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertIn('forecast_trajectory', data)
        self.assertGreater(len(data['forecast_trajectory']), 3)

    async def test_interventions_catalog_what_first(self):
        """Question 5: What intervention should be implemented first?"""
        r = await self.client.get('/api/v1/accidents/analytics/interventions')
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertIn('interventions', data)
        self.assertGreaterEqual(len(data['interventions']), 3)

    async def test_counterfactual_simulation_impact(self):
        """Question 6: Can we predict whether the intervention will reduce accidents?"""
        payload = {
            "baseline_risk": 84.0,
            "baseline_fatalities_annual": 32,
            "baseline_crashes_annual": 48,
            "selected_interventions": [
                "speed_cameras",
                "pedestrian_infrastructure",
                "high_mast_lighting"
            ]
        }
        r = await self.client.post('/api/v1/accidents/analytics/simulate', json=payload)
        self.assertEqual(r.status_code, 200)
        res = r.json()
        self.assertLess(res['simulated_risk'], res['baseline_risk'])
        self.assertGreater(res['risk_reduction_pct'], 40.0)
        self.assertGreater(res['lives_saved_annual'], 10)
        self.assertGreater(res['crashes_prevented_annual'], 15)

    async def test_route_risk(self):
        """Safe Route evaluation"""
        r = await self.client.get('/api/v1/accidents/analytics/route-risk?origin=Delhi&destination=Agra')
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertIn('Yamuna Expressway', data['corridor_name'])
        self.assertGreater(data['risk_score'], 50)

    async def test_trauma_centers_golden_hour(self):
        """Emergency trauma centers"""
        r = await self.client.get('/api/v1/accidents/analytics/trauma-centers?latitude=28.7365&longitude=77.1643')
        self.assertEqual(r.status_code, 200)
        centers = r.json()
        self.assertGreater(len(centers), 5)
        self.assertIn('distance_km', centers[0])

    async def test_crud_accident(self):
        """CRUD verification"""
        new_inc = {
            "location": "NH-48 Test Corridor Km 45",
            "latitude": 28.4500,
            "longitude": 77.0200,
            "state": "Haryana",
            "district": "Gurugram",
            "accident_type": "collision",
            "severity": "severe",
            "casualties": 3,
            "injuries": 2,
            "fatalities": 1,
            "weather_condition": "Clear",
            "road_condition": "Dry",
            "time_of_day": "Morning",
            "speed_limit": 80,
            "observed_speed": 98,
            "contributing_factors": "Speeding test"
        }
        r = await self.client.post('/api/v1/accidents/', json=new_inc)
        self.assertEqual(r.status_code, 201)
        created = r.json()
        inc_id = created['id']
        self.assertGreater(created['risk_score'], 0)

        # Get
        r2 = await self.client.get(f'/api/v1/accidents/{inc_id}')
        self.assertEqual(r2.status_code, 200)

        # Delete
        r3 = await self.client.delete(f'/api/v1/accidents/{inc_id}')
        self.assertEqual(r3.status_code, 204)

    async def test_all_states_pan_india(self):
        """Verify all 36 States and Union Territories analytics"""
        r = await self.client.get('/api/v1/accidents/analytics/states')
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertIn('total_entities', data)
        self.assertEqual(data['total_entities'], 36)
        self.assertEqual(len(data['states']), 36)
        self.assertGreater(data['national_crashes_2023'], 400000)
        self.assertGreater(data['national_fatalities_2023'], 150000)

    async def test_state_dossier_detailed(self):
        """Verify deep-dive dossier for individual states (e.g. Tamil Nadu, Uttar Pradesh, Delhi)"""
        for state in ["Tamil Nadu", "Uttar Pradesh", "Delhi"]:
            r = await self.client.get(f'/api/v1/accidents/analytics/states/{state}')
            self.assertEqual(r.status_code, 200)
            dossier = r.json()
            self.assertEqual(dossier['state'], state)
            self.assertIn('history', dossier)
            self.assertIn('blackspots', dossier)
            self.assertIn('recommendations', dossier)
            self.assertGreater(len(dossier['history']), 3)

    async def test_historical_50yr_trends(self):
        """Verify MoRTH 50-year longitudinal road accident & motorization trends (1970-2019)"""
        r = await self.client.get('/api/v1/accidents/analytics/historical-50yr')
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertIn('records', data)
        self.assertGreater(len(data['records']), 25)
        self.assertEqual(data['records'][0]['year'], 1970)
        self.assertEqual(data['records'][-1]['year'], 2019)
        self.assertIn('key_takeaways', data)

    async def test_junction_control_million_plus_cities(self):
        """Verify intersection traffic control analysis across 50 million-plus cities"""
        r = await self.client.get('/api/v1/accidents/analytics/junction-control')
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertIn('cities', data)
        self.assertGreaterEqual(len(data['cities']), 45)
        self.assertIn('national_summary', data)
        self.assertIn('engineering_implication', data)

        # City specific filter
        r_delhi = await self.client.get('/api/v1/accidents/analytics/junction-control?city=Delhi')
        self.assertEqual(r_delhi.status_code, 200)
        d_data = r_delhi.json()
        self.assertIn('city_data', d_data)
        self.assertEqual(d_data['city_data']['city'], 'Delhi')

    async def test_police_blackspots_registry(self):
        """Verify official police station blackspots registry (2016-2018 records)"""
        r = await self.client.get('/api/v1/accidents/analytics/police-blackspots')
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertIn('spots', data)
        self.assertGreater(len(data['spots']), 50)
        self.assertIn('total_matched', data)

        # State filter
        r_kerala = await self.client.get('/api/v1/accidents/analytics/police-blackspots?state=Kerala')
        self.assertEqual(r_kerala.status_code, 200)
        k_data = r_kerala.json()
        self.assertGreater(len(k_data['spots']), 0)
        self.assertEqual(k_data['spots'][0]['state'], 'Kerala')

    async def test_highways_network_color_coded(self):
        """Verify color-coded Indian highway risk network (Green, Yellow, Orange, Red)"""
        r = await self.client.get('/api/v1/accidents/analytics/highways')
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertIn('highways', data)
        self.assertGreaterEqual(len(data['highways']), 20)
        self.assertIn('color_legend', data)
        
        # Verify all 4 required colors exist
        colors = set(h['color'] for h in data['highways'])
        self.assertTrue({'green', 'yellow', 'orange', 'red'}.issubset(colors))

        # Test extreme filter (Red)
        r_red = await self.client.get('/api/v1/accidents/analytics/highways?risk_level=extreme')
        self.assertEqual(r_red.status_code, 200)
        red_highways = r_red.json()['highways']
        self.assertTrue(all(h['color'] == 'red' for h in red_highways))

        # Test safe filter (Green)
        r_green = await self.client.get('/api/v1/accidents/analytics/highways?risk_level=none')
        self.assertEqual(r_green.status_code, 200)
        green_highways = r_green.json()['highways']
        self.assertTrue(all(h['color'] == 'green' for h in green_highways))

    async def test_blackspots_severity_distribution(self):
        """Verify Blackspot Severity has realistic distribution across Critical, High, and Moderate regions"""
        r = await self.client.get('/api/v1/accidents/analytics/hotspots')
        self.assertEqual(r.status_code, 200)
        hotspots = r.json()
        
        crit = [h for h in hotspots if h['risk_score'] >= 80]
        high = [h for h in hotspots if 60 <= h['risk_score'] < 80]
        mod = [h for h in hotspots if h['risk_score'] < 60]

        # Verify all three severity bands have substantial representation across India
        self.assertGreaterEqual(len(crit), 30, "Critical blackspots should be >= 30")
        self.assertGreaterEqual(len(high), 30, "High severity accident zones should be >= 30")
        self.assertGreaterEqual(len(mod), 20, "Moderate severity accident zones should be >= 20")

        # Verify bands match scores
        for h in crit:
            self.assertEqual(h['risk_band'], 'Critical')
        for h in high:
            self.assertEqual(h['risk_band'], 'High')
        for h in mod:
            self.assertEqual(h['risk_band'], 'Moderate')

if __name__ == '__main__':
    unittest.main()

