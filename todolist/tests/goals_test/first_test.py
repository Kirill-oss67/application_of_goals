def test_root_category(client):
    response = client.get('http://127.0.0.1/boards')
    assert response.status_code == 200
