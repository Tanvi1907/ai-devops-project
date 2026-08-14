import pytest
from app import app

# This creates a test client - a fake browser to test our app without running the real server
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# Test 1: Check if home route works
def test_home_route(client):
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == "AI DevOps project is running!"

# Test 2: Check if health route works
def test_health_route(client):
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == "healthy"

# Test 3: Check if greet route works with a name
def test_greet_route(client):
    response = client.get('/greet/Tanvi')
    assert response.status_code == 200
    data = response.get_json()
    assert "Tanvi" in data['message']

# Test 4: Check if 404 error handler works
def test_404_route(client):
    response = client.get('/randompage')
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == "This route does not exist"

# Test 5: Check if analyze-error route rejects empty request
def test_analyze_error_empty(client):
    response = client.post('/analyze-error', json={})
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data