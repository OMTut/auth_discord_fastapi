# Httpx
<p>httpx is a modern, async-capable HTTP client library for Python. It's
essentially the next-generation replacement for the popular requests 
library</p>

### Async support
- supports both sync and async http reqs
- allows non-blocking http calls

Similar methods: get, post, put, delete etc

```
import httpx

async def fetch_data():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.example.com/data")
        return response.json()
```