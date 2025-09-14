from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import asyncio
from typing import List, Dict
from core.stream_manager import StreamManager

app = FastAPI(title="Unilog Dashboard")

# Mount static folder for CSS/JS if needed
app.mount("/static", StaticFiles(directory="dashboard/static"), name="static")

# In-memory store for logs (for demo; replace with DB for production)
logs: List[Dict] = []

# Stream manager instance (can push logs here)
stream_manager = StreamManager()


@app.get("/")
async def get_dashboard():
    """Return dashboard HTML."""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Unilog Dashboard</title>
        <style>
            body { font-family: Arial, sans-serif; padding: 20px; }
            table { border-collapse: collapse; width: 100%; }
            th, td { border: 1px solid #ddd; padding: 8px; }
            th { background-color: #f2f2f2; }
            tr:nth-child(even) { background-color: #f9f9f9; }
        </style>
    </head>
    <body>
        <h1>Unilog Dashboard</h1>
        <input id="search" placeholder="Search logs..." oninput="filterLogs()" />
        <table id="logTable">
            <thead>
                <tr>
                    <th>Timestamp</th>
                    <th>Level</th>
                    <th>Message</th>
                    <th>Details</th>
                </tr>
            </thead>
            <tbody id="logBody"></tbody>
        </table>

        <script>
            const ws = new WebSocket("ws://localhost:8000/ws");
            const logBody = document.getElementById("logBody");
            const searchInput = document.getElementById("search");

            ws.onmessage = function(event) {
                const log = JSON.parse(event.data);
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${log.timestamp}</td>
                    <td>${log.level}</td>
                    <td>${log.message}</td>
                    <td><pre>${JSON.stringify(log, null, 2)}</pre></td>
                `;
                logBody.prepend(row);
                filterLogs();
            };

            function filterLogs() {
                const filter = searchInput.value.toLowerCase();
                Array.from(logBody.rows).forEach(row => {
                    row.style.display = Array.from(row.cells)
                        .some(cell => cell.innerText.toLowerCase().includes(filter)) ? "" : "none";
                });
            }
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        if not logs:
            await asyncio.sleep(0.5)
            continue
        while logs:
            log_entry = logs.pop(0)
            await websocket.send_json(log_entry)
        await asyncio.sleep(0.1)


def push_log(log_entry: Dict):
    logs.append(log_entry)
