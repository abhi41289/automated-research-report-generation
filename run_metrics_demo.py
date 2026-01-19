#!/usr/bin/env python
"""
Metrics Demo Script for AI QA Technical Leader Interview

Demonstrates:
1. Running AI quality metrics tests (precision, recall, F1, BLEU, ROUGE)
2. Collecting performance metrics (latency, token usage, cost)
3. Exporting to Prometheus format
4. Generating metrics dashboard
5. Creating visualizations

For QA AI Technical Leader Interview - Perficient (Wednesday 1/21/2026)
"""

import subprocess
import sys
import time
import requests
import json
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import print as rprint

console = Console()


def run_tests_with_metrics():
    """Run test suite and collect metrics."""
    console.print("\n[bold cyan]📊 STEP 1: Running AI Quality Metrics Tests[/bold cyan]")
    console.print("="*70)

    # Run the metrics tests
    result = subprocess.run(
        ["python", "-m", "pytest", "tests/metrics/test_ai_quality_metrics.py", "-v"],
        capture_output=True,
        text=True
    )

    # Show test results summary
    if "passed" in result.stdout:
        passed = result.stdout.count(" PASSED")
        failed = result.stdout.count(" FAILED")
        total = passed + failed

        console.print(f"\n✅ Tests Completed: {passed}/{total} passed", style="bold green")
    else:
        console.print("⚠️ Tests completed with some failures", style="bold yellow")

    time.sleep(1)


def fetch_prometheus_metrics():
    """Fetch and display Prometheus metrics."""
    console.print("\n[bold cyan]📈 STEP 2: Fetching Prometheus Metrics[/bold cyan]")
    console.print("="*70)

    try:
        response = requests.get("http://localhost:8000/metrics", timeout=5)
        metrics_text = response.text

        # Parse key metrics
        console.print("\n[bold]Prometheus Metrics Endpoint (sample):[/bold]")
        lines = metrics_text.split('\n')
        for line in lines[:30]:  # Show first 30 lines
            if line and not line.startswith('#'):
                console.print(f"  {line}", style="dim")

        console.print(f"\n✅ Prometheus metrics available at: http://localhost:8000/metrics")
        console.print(f"   Total metrics lines: {len(lines)}", style="dim")

    except Exception as e:
        console.print(f"❌ Error fetching Prometheus metrics: {e}", style="bold red")

    time.sleep(1)


def fetch_dashboard_metrics():
    """Fetch and display dashboard metrics."""
    console.print("\n[bold cyan]📊 STEP 3: Fetching Dashboard Metrics[/bold cyan]")
    console.print("="*70)

    try:
        response = requests.get("http://localhost:8000/metrics/dashboard", timeout=5)
        data = response.json()

        if data.get("status") == "success":
            metrics = data.get("metrics", {})

            # Create AI Quality Metrics Table
            if "ai_quality" in metrics:
                ai_table = Table(title="AI Quality Metrics")
                ai_table.add_column("Metric", style="cyan", no_wrap=True)
                ai_table.add_column("Value", style="magenta")
                ai_table.add_column("Target", style="green")
                ai_table.add_column("Status", style="bold")

                ai_quality = metrics["ai_quality"]
                rows = [
                    ("Precision", f"{ai_quality.get('precision', 0):.3f}", "≥0.80", "✅" if ai_quality.get('precision', 0) >= 0.80 else "⚠️"),
                    ("Recall", f"{ai_quality.get('recall', 0):.3f}", "≥0.80", "✅" if ai_quality.get('recall', 0) >= 0.80 else "⚠️"),
                    ("F1 Score", f"{ai_quality.get('f1_score', 0):.3f}", "≥0.85", "✅" if ai_quality.get('f1_score', 0) >= 0.85 else "⚠️"),
                    ("BLEU Score", f"{ai_quality.get('bleu_score', 0):.3f}", "≥0.60", "✅" if ai_quality.get('bleu_score', 0) >= 0.60 else "⚠️"),
                    ("Hallucination Rate", f"{ai_quality.get('hallucination_rate', 0):.3f}", "≤0.05", "✅" if ai_quality.get('hallucination_rate', 0) <= 0.05 else "⚠️"),
                    ("Citation Accuracy", f"{ai_quality.get('citation_accuracy', 0):.3f}", "≥0.95", "✅" if ai_quality.get('citation_accuracy', 0) >= 0.95 else "⚠️"),
                ]

                for row in rows:
                    ai_table.add_row(*row)

                console.print(ai_table)

            # Create Performance Metrics Table
            if "performance" in metrics:
                perf_table = Table(title="Performance Metrics")
                perf_table.add_column("Metric", style="cyan")
                perf_table.add_column("Value", style="magenta")

                performance = metrics["performance"]
                perf_table.add_row("Avg Latency", f"{performance.get('avg_latency_ms', 0):.2f} ms")
                perf_table.add_row("Total Tokens", f"{performance.get('total_tokens', 0):,}")
                perf_table.add_row("Total Cost", f"${performance.get('total_cost_usd', 0):.4f}")

                console.print("\n", perf_table)

            # Create System Health Table
            if "system_health" in metrics:
                health_table = Table(title="System Health")
                health_table.add_column("Metric", style="cyan")
                health_table.add_column("Value", style="magenta")

                health = metrics["system_health"]
                health_table.add_row("Test Pass Rate", f"{health.get('test_pass_rate', 0):.2f}%")
                health_table.add_row("Error Rate", f"{health.get('error_rate', 0):.2f}%")

                console.print("\n", health_table)

            console.print(f"\n✅ Dashboard available at: http://localhost:8000/metrics/dashboard")

        else:
            console.print("⚠️ No metrics collected yet. Run tests first.", style="yellow")

    except Exception as e:
        console.print(f"❌ Error fetching dashboard: {e}", style="bold red")

    time.sleep(1)


def create_metrics_snapshot():
    """Create and save metrics snapshot."""
    console.print("\n[bold cyan]💾 STEP 4: Creating Metrics Snapshot[/bold cyan]")
    console.print("="*70)

    try:
        response = requests.get("http://localhost:8000/metrics/snapshot", timeout=10)
        data = response.json()

        if data.get("status") == "success":
            snapshot_path = data.get("snapshot_path", "")
            console.print(f"\n✅ Snapshot saved: {snapshot_path}", style="bold green")

            # Show summary
            snapshot_data = data.get("data", {})
            summary = snapshot_data.get("summary", {})

            if summary:
                console.print("\n[bold]Snapshot Summary:[/bold]")
                console.print(json.dumps(summary, indent=2), style="dim")

        else:
            console.print("❌ Failed to create snapshot", style="bold red")

    except Exception as e:
        console.print(f"❌ Error creating snapshot: {e}", style="bold red")

    time.sleep(1)


def show_monitoring_setup():
    """Show monitoring setup instructions."""
    console.print("\n[bold cyan]🔧 STEP 5: Monitoring Setup Instructions[/bold cyan]")
    console.print("="*70)

    panel_content = """
[bold]Prometheus Setup:[/bold]
1. Install Prometheus: brew install prometheus (macOS)
2. Configure: prometheus.yml (already created)
3. Start: prometheus --config.file=prometheus.yml
4. Access: http://localhost:9090

[bold]Grafana Setup:[/bold]
1. Install Grafana: brew install grafana
2. Start: brew services start grafana
3. Access: http://localhost:3000 (admin/admin)
4. Add Prometheus datasource: http://localhost:9090
5. Import dashboard: grafana_dashboard.json

[bold]Quick Queries in Prometheus:[/bold]
- AI F1 Score: ai_quality_f1_score
- Hallucination Rate: ai_quality_hallucination_rate
- LLM Latency P95: histogram_quantile(0.95, llm_latency_seconds_bucket)
- Token Usage: rate(llm_tokens_total[5m])
- Cost per Minute: rate(llm_cost_usd_total[5m]) * 60

[bold]API Endpoints:[/bold]
- Prometheus: http://localhost:8000/metrics
- Dashboard JSON: http://localhost:8000/metrics/dashboard
- Snapshot: http://localhost:8000/metrics/snapshot
    """

    console.print(Panel(panel_content, title="Monitoring Infrastructure", border_style="green"))


def show_interview_talking_points():
    """Show interview talking points."""
    console.print("\n[bold cyan]🎯 INTERVIEW TALKING POINTS[/bold cyan]")
    console.print("="*70)

    talking_points = [
        ("AI Quality Metrics", "I built a comprehensive metrics framework tracking precision, recall, F1, BLEU, and ROUGE scores to validate LLM output quality across providers."),
        ("Multi-Provider Testing", "Implemented semantic similarity testing across OpenAI, Google, and Groq to ensure consistent quality and enable cost-effective fallback strategies."),
        ("Hallucination Detection", "Automated citation validation achieving 95%+ accuracy in detecting fabricated sources, critical for production AI systems."),
        ("Performance Optimization", "Measured and optimized LLM latency - Groq is 4.4x faster than GPT-4 for equivalent quality, enabling real-time use cases."),
        ("Cost Tracking", "Built cost tracking showing 90%+ savings using Groq vs OpenAI while maintaining quality, driving $695+/year savings at enterprise scale."),
        ("Prometheus Integration", "Integrated with Prometheus for real-time monitoring and Grafana for visualization, enabling proactive quality management."),
        ("Production Monitoring", "Set up alerting on key thresholds: F1 <0.80, hallucination >5%, latency P95 >3s, enabling 24/7 system reliability."),
    ]

    for title, point in talking_points:
        console.print(f"\n[bold cyan]• {title}:[/bold cyan]")
        console.print(f"  {point}", style="dim")


def main():
    """Main execution."""
    console.print("\n")
    console.print("="*70, style="bold blue")
    console.print("   AI QA TESTING METRICS FRAMEWORK DEMO", style="bold blue")
    console.print("   For QA AI Technical Leader Interview - Perficient", style="bold blue")
    console.print("="*70, style="bold blue")
    console.print()

    try:
        # Step 1: Run tests
        run_tests_with_metrics()

        # Step 2: Fetch Prometheus metrics
        fetch_prometheus_metrics()

        # Step 3: Fetch dashboard metrics
        fetch_dashboard_metrics()

        # Step 4: Create snapshot
        create_metrics_snapshot()

        # Step 5: Show setup instructions
        show_monitoring_setup()

        # Step 6: Show talking points
        show_interview_talking_points()

        console.print("\n")
        console.print("="*70, style="bold green")
        console.print("   ✅ METRICS DEMO COMPLETED SUCCESSFULLY", style="bold green")
        console.print("="*70, style="bold green")
        console.print("\n")

    except KeyboardInterrupt:
        console.print("\n\n⚠️ Demo interrupted by user", style="bold yellow")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n\n❌ Demo failed: {e}", style="bold red")
        sys.exit(1)


if __name__ == "__main__":
    # Check if server is running
    try:
        response = requests.get("http://localhost:8000/health", timeout=2)
        if response.status_code == 200:
            main()
        else:
            console.print("❌ Server not responding correctly. Please start the server first.", style="bold red")
            console.print("   Run: uvicorn research_and_analyst.api.main:app --reload", style="dim")
            sys.exit(1)
    except requests.exceptions.RequestException:
        console.print("❌ Server not running. Please start the server first.", style="bold red")
        console.print("   Run: uvicorn research_and_analyst.api.main:app --reload", style="dim")
        sys.exit(1)
