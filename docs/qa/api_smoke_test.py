import json
import urllib.request
import urllib.error

BASE_URL = "http://localhost:8000"

tests = [
    ("GET", "/", None, [200]),
    ("GET", "/health", None, [200]),
    ("GET", "/books/", None, [200]),
    ("GET", "/users/", None, [200]),
    ("GET", "/loans/", None, [200]),
    ("GET", "/reservations/", None, [200]),
    ("GET", "/fines/", None, [200]),
    ("GET", "/notifications/", None, [200]),

    # Error validation tests
    ("POST", "/books/", {}, [400, 422]),
    ("POST", "/users/", {}, [400, 422]),
    ("POST", "/loans/", {}, [400, 422]),
    ("POST", "/reservations/", {}, [400, 422]),
    ("POST", "/fines/", {}, [400, 422]),
    ("POST", "/notifications/", {}, [400, 422]),

    # Non-existent resource tests
    ("GET", "/books/999999", None, [404, 422]),
    ("GET", "/users/999999", None, [404, 422]),
    ("GET", "/loans/999999", None, [404, 422]),
    ("GET", "/reservations/999999", None, [404, 422]),
    ("GET", "/fines/999999", None, [404, 422]),
    ("GET", "/notifications/999999", None, [404, 422]),
]

results = []

for method, path, body, expected in tests:
    url = BASE_URL + path
    data = None
    headers = {}

    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"

    req = urllib.request.Request(url, data=data, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            status = response.status
            response_body = response.read().decode("utf-8", errors="ignore")[:120]
    except urllib.error.HTTPError as e:
        status = e.code
        response_body = e.read().decode("utf-8", errors="ignore")[:120]
    except Exception as e:
        status = "ERROR"
        response_body = str(e)

    passed = status in expected
    results.append((method, path, status, expected, "PASS" if passed else "FAIL"))

print("\n=== API SMOKE TEST RESULTS ===")
for method, path, status, expected, result in results:
    print(f"{result:4} | {method:6} | {path:35} | status={status} | expected={expected}")

total = len(results)
passed = sum(1 for item in results if item[-1] == "PASS")

print(f"\nSummary: {passed}/{total} tests passed")

if passed != total:
    raise SystemExit(1)