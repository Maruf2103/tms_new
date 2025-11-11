import urllib.request

def check(url, term):
    try:
        with urllib.request.urlopen(url, timeout=5) as r:
            body = r.read().decode('utf-8', errors='ignore')
            found = term in body
            count = body.count(term)
            print(f"{url} -> found={found}, count={count}")
    except Exception as e:
        print(f"{url} -> error: {e}")

if __name__ == '__main__':
    check('http://127.0.0.1:8000/dashboard/', 'My Recent Bookings')
    check('http://127.0.0.1:8000/bus-schedule/', 'My Recent Bookings')
    check('http://127.0.0.1:8000/view-schedules/', 'My Recent Bookings')
