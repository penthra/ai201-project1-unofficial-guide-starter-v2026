# Live logging preflight — November 14, 2026

Service: https://campus-life-rag.onrender.com
These observations precede deployment of the new logger and are **not** the
requested ten-run cost sample or server JSON log evidence. No private Render
logs were accessible through the public endpoint.

- Initial parking-permit request: curl timed out after 55.021 seconds with no
  response bytes. Cold-start status and server outcome are unknown; do not
  classify this as a measured warm response.
- Non-string request `{"question":123}`: HTTP 400. Response header `Rndr-Id`:
  `9f6ba583-233f-4263`; response Date: `Sat, 14 Nov 2026 20:08:50 GMT`.
  No `X-Request-ID` application header. Body:

```json
{"error":"Send JSON with a question in it, like {\"question\": \"is the housing lottery random?\"}"}
```

- Retried question `When can students purchase a parking permit?`: HTTP 200.
  Response header `Rndr-Id`: `b63b19d1-9799-4ddf`; response Date:
  `Sat, 14 Nov 2026 20:09:21 GMT`. No `X-Request-ID` application header. Body:

```json
{"answer":"Student permits for the west lots go on sale in August (admin_parking_permits.txt).","best_distance":0.4196,"corpus":"campus_life","question":"When can students purchase a parking permit?","refused":false,"sources":["admin_library_holds.txt","admin_parking_permits.txt","advising_registration.txt","study_library_hours.txt","transit_shuttle.txt"],"threshold":0.6}
```

Current repository `serve.py` had no request logging before the local change.
The above response headers alone cannot prove whether private platform logs
exist. The new application JSON logs require redeployment and verification
in the service's Render Logs page.
