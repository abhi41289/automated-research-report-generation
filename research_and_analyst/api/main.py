from fastapi import FastAPI, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import os
from research_and_analyst.api.routes import report_routes
from datetime import datetime
from research_and_analyst.utils.metrics_collector import get_metrics_collector
import json

app = FastAPI(title="Autonomous Report Generator UI")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="research_and_analyst/api/templates")
app.templates = templates  # so templates accessible inside router

# 🔹 ADD THIS FUNCTION
def basename_filter(path: str):
    return os.path.basename(path)

# 🔹 REGISTER FILTER
templates.env.filters["basename"] = basename_filter

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

#health check have been added
@app.get("/health")
async def health_check():
    """Health check endpoint for container orchestration"""
    return {
        "status": "healthy",
        "service": "research-report-generation",
        "timestamp": datetime.now().isoformat()
    }

# Prometheus metrics endpoint
@app.get("/metrics")
async def prometheus_metrics():
    """
    Prometheus-compatible metrics endpoint.

    Exposes:
    - AI quality metrics (precision, recall, F1, BLEU, hallucination rate)
    - Performance metrics (latency, token usage, cost)
    - System health metrics (error rate, test pass rate)

    Usage: Configure Prometheus to scrape this endpoint
    """
    collector = get_metrics_collector()
    metrics_data = collector.export_prometheus()
    return Response(content=metrics_data, media_type="text/plain")

# Metrics dashboard endpoint
@app.get("/metrics/dashboard")
async def metrics_dashboard():
    """
    JSON metrics dashboard for AI QA testing.

    Returns aggregated metrics for Grafana or custom dashboards.
    """
    collector = get_metrics_collector()
    summary = collector.get_summary()
    return {
        "status": "success",
        "timestamp": datetime.now().isoformat(),
        "metrics": summary
    }

# Metrics snapshot endpoint
@app.get("/metrics/snapshot")
async def metrics_snapshot():
    """
    Save and return current metrics snapshot.

    Useful for historical tracking and analysis.
    """
    collector = get_metrics_collector()
    snapshot_path = collector.save_metrics_snapshot()

    # Read the snapshot file
    with open(snapshot_path, 'r') as f:
        snapshot_data = json.load(f)

    return {
        "status": "success",
        "snapshot_path": str(snapshot_path),
        "data": snapshot_data
    }

# Register Routes
app.include_router(report_routes.router)
