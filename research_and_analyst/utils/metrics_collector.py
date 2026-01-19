"""
Metrics Collector for AI QA Testing Framework

Tracks and exports metrics for:
- AI quality (precision, recall, F1, BLEU, ROUGE)
- LLM performance (latency, token usage, cost)
- System health (error rates, throughput)

Integrates with Prometheus for monitoring and Grafana for visualization.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field, asdict
from datetime import datetime
import json
from pathlib import Path
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CollectorRegistry
from research_and_analyst.logger import GLOBAL_LOGGER as log

logger = log.bind(module="MetricsCollector")


@dataclass
class AIQualityMetrics:
    """AI-specific quality metrics for LLM testing."""

    # Classification metrics
    precision: float = 0.0
    recall: float = 0.0
    f1_score: float = 0.0
    accuracy: float = 0.0

    # Text generation metrics
    bleu_score: float = 0.0
    rouge_1: float = 0.0
    rouge_2: float = 0.0
    rouge_l: float = 0.0

    # AI-specific metrics
    hallucination_rate: float = 0.0
    citation_accuracy: float = 0.0
    schema_compliance_rate: float = 0.0
    semantic_similarity: float = 0.0

    # Metadata
    test_name: str = ""
    provider: str = ""
    model: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict:
        """Convert metrics to dictionary."""
        return asdict(self)

    def to_json(self) -> str:
        """Convert metrics to JSON string."""
        return json.dumps(self.to_dict(), indent=2)


@dataclass
class PerformanceMetrics:
    """LLM performance and cost metrics."""

    # Latency metrics (milliseconds)
    llm_latency_ms: float = 0.0
    workflow_latency_ms: float = 0.0
    total_latency_ms: float = 0.0

    # Token usage
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0

    # Cost metrics (USD)
    cost_per_request: float = 0.0
    cost_per_1k_tokens: float = 0.0

    # Throughput
    requests_per_minute: float = 0.0
    tokens_per_minute: float = 0.0

    # Metadata
    provider: str = ""
    model: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class SystemHealthMetrics:
    """System-level health and reliability metrics."""

    # Error rates
    error_rate: float = 0.0
    timeout_rate: float = 0.0
    retry_rate: float = 0.0

    # Success metrics
    success_rate: float = 0.0
    test_pass_rate: float = 0.0

    # Resource usage
    cpu_usage_percent: float = 0.0
    memory_usage_mb: float = 0.0

    # Test execution
    total_tests: int = 0
    passed_tests: int = 0
    failed_tests: int = 0
    skipped_tests: int = 0

    # Metadata
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict:
        return asdict(self)


class MetricsCollector:
    """
    Central metrics collection and export system.

    Features:
    - Collect AI quality, performance, and system metrics
    - Export to Prometheus format
    - Save historical metrics to JSON
    - Generate reports for Grafana dashboards
    """

    def __init__(self, storage_path: str = "metrics_data"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(exist_ok=True)

        # In-memory metrics storage
        self.ai_quality_metrics: List[AIQualityMetrics] = []
        self.performance_metrics: List[PerformanceMetrics] = []
        self.system_health_metrics: List[SystemHealthMetrics] = []

        # Prometheus registry
        self.registry = CollectorRegistry()

        # Prometheus metrics - AI Quality
        self.prom_precision = Gauge(
            'ai_quality_precision',
            'Precision score for AI predictions',
            ['test_name', 'provider', 'model'],
            registry=self.registry
        )
        self.prom_recall = Gauge(
            'ai_quality_recall',
            'Recall score for AI predictions',
            ['test_name', 'provider', 'model'],
            registry=self.registry
        )
        self.prom_f1_score = Gauge(
            'ai_quality_f1_score',
            'F1 score for AI predictions',
            ['test_name', 'provider', 'model'],
            registry=self.registry
        )
        self.prom_bleu_score = Gauge(
            'ai_quality_bleu_score',
            'BLEU score for text generation',
            ['test_name', 'provider', 'model'],
            registry=self.registry
        )
        self.prom_hallucination_rate = Gauge(
            'ai_quality_hallucination_rate',
            'Rate of hallucinated/fabricated information',
            ['test_name', 'provider', 'model'],
            registry=self.registry
        )
        self.prom_citation_accuracy = Gauge(
            'ai_quality_citation_accuracy',
            'Accuracy of citations and sources',
            ['test_name', 'provider', 'model'],
            registry=self.registry
        )

        # Prometheus metrics - Performance
        self.prom_llm_latency = Histogram(
            'llm_latency_seconds',
            'LLM API call latency',
            ['provider', 'model'],
            registry=self.registry
        )
        self.prom_total_tokens = Counter(
            'llm_tokens_total',
            'Total tokens consumed',
            ['provider', 'model', 'token_type'],
            registry=self.registry
        )
        self.prom_cost = Counter(
            'llm_cost_usd_total',
            'Total cost in USD',
            ['provider', 'model'],
            registry=self.registry
        )

        # Prometheus metrics - System Health
        self.prom_error_rate = Gauge(
            'system_error_rate',
            'Error rate percentage',
            registry=self.registry
        )
        self.prom_test_pass_rate = Gauge(
            'test_pass_rate',
            'Test pass rate percentage',
            registry=self.registry
        )
        self.prom_tests_total = Counter(
            'tests_total',
            'Total number of tests run',
            ['status'],
            registry=self.registry
        )

        logger.info("MetricsCollector initialized", storage_path=str(self.storage_path))

    def record_ai_quality(self, metrics: AIQualityMetrics):
        """Record AI quality metrics."""
        self.ai_quality_metrics.append(metrics)

        # Update Prometheus metrics
        labels = {
            'test_name': metrics.test_name,
            'provider': metrics.provider,
            'model': metrics.model
        }
        self.prom_precision.labels(**labels).set(metrics.precision)
        self.prom_recall.labels(**labels).set(metrics.recall)
        self.prom_f1_score.labels(**labels).set(metrics.f1_score)
        self.prom_bleu_score.labels(**labels).set(metrics.bleu_score)
        self.prom_hallucination_rate.labels(**labels).set(metrics.hallucination_rate)
        self.prom_citation_accuracy.labels(**labels).set(metrics.citation_accuracy)

        logger.info("AI quality metrics recorded",
                   test=metrics.test_name,
                   f1=f"{metrics.f1_score:.3f}",
                   bleu=f"{metrics.bleu_score:.3f}")

    def record_performance(self, metrics: PerformanceMetrics):
        """Record performance metrics."""
        self.performance_metrics.append(metrics)

        # Update Prometheus metrics
        self.prom_llm_latency.labels(
            provider=metrics.provider,
            model=metrics.model
        ).observe(metrics.llm_latency_ms / 1000.0)  # Convert to seconds

        self.prom_total_tokens.labels(
            provider=metrics.provider,
            model=metrics.model,
            token_type='prompt'
        ).inc(metrics.prompt_tokens)

        self.prom_total_tokens.labels(
            provider=metrics.provider,
            model=metrics.model,
            token_type='completion'
        ).inc(metrics.completion_tokens)

        self.prom_cost.labels(
            provider=metrics.provider,
            model=metrics.model
        ).inc(metrics.cost_per_request)

        logger.info("Performance metrics recorded",
                   provider=metrics.provider,
                   latency_ms=metrics.llm_latency_ms,
                   tokens=metrics.total_tokens,
                   cost=f"${metrics.cost_per_request:.4f}")

    def record_system_health(self, metrics: SystemHealthMetrics):
        """Record system health metrics."""
        self.system_health_metrics.append(metrics)

        # Update Prometheus metrics
        self.prom_error_rate.set(metrics.error_rate)
        self.prom_test_pass_rate.set(metrics.test_pass_rate)

        self.prom_tests_total.labels(status='passed').inc(metrics.passed_tests)
        self.prom_tests_total.labels(status='failed').inc(metrics.failed_tests)
        self.prom_tests_total.labels(status='skipped').inc(metrics.skipped_tests)

        logger.info("System health metrics recorded",
                   pass_rate=f"{metrics.test_pass_rate:.1f}%",
                   error_rate=f"{metrics.error_rate:.1f}%")

    def export_prometheus(self) -> bytes:
        """Export metrics in Prometheus format."""
        return generate_latest(self.registry)

    def save_metrics_snapshot(self, filename: Optional[str] = None):
        """Save current metrics to JSON file."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"metrics_snapshot_{timestamp}.json"

        filepath = self.storage_path / filename

        snapshot = {
            "timestamp": datetime.now().isoformat(),
            "ai_quality_metrics": [m.to_dict() for m in self.ai_quality_metrics],
            "performance_metrics": [m.to_dict() for m in self.performance_metrics],
            "system_health_metrics": [m.to_dict() for m in self.system_health_metrics],
            "summary": self.get_summary()
        }

        with open(filepath, 'w') as f:
            json.dump(snapshot, f, indent=2)

        logger.info("Metrics snapshot saved", filepath=str(filepath))
        return filepath

    def get_summary(self) -> Dict:
        """Get summary statistics across all metrics."""
        if not self.ai_quality_metrics:
            return {"status": "no_metrics_collected"}

        # Calculate averages for AI quality
        avg_precision = sum(m.precision for m in self.ai_quality_metrics) / len(self.ai_quality_metrics)
        avg_recall = sum(m.recall for m in self.ai_quality_metrics) / len(self.ai_quality_metrics)
        avg_f1 = sum(m.f1_score for m in self.ai_quality_metrics) / len(self.ai_quality_metrics)
        avg_bleu = sum(m.bleu_score for m in self.ai_quality_metrics) / len(self.ai_quality_metrics)
        avg_hallucination = sum(m.hallucination_rate for m in self.ai_quality_metrics) / len(self.ai_quality_metrics)
        avg_citation_accuracy = sum(m.citation_accuracy for m in self.ai_quality_metrics) / len(self.ai_quality_metrics)

        # Calculate averages for performance
        if self.performance_metrics:
            avg_latency = sum(m.llm_latency_ms for m in self.performance_metrics) / len(self.performance_metrics)
            total_tokens = sum(m.total_tokens for m in self.performance_metrics)
            total_cost = sum(m.cost_per_request for m in self.performance_metrics)
        else:
            avg_latency = 0
            total_tokens = 0
            total_cost = 0

        # System health summary
        if self.system_health_metrics:
            latest_health = self.system_health_metrics[-1]
            test_pass_rate = latest_health.test_pass_rate
            error_rate = latest_health.error_rate
        else:
            test_pass_rate = 0
            error_rate = 0

        return {
            "ai_quality": {
                "precision": round(avg_precision, 3),
                "recall": round(avg_recall, 3),
                "f1_score": round(avg_f1, 3),
                "bleu_score": round(avg_bleu, 3),
                "hallucination_rate": round(avg_hallucination, 3),
                "citation_accuracy": round(avg_citation_accuracy, 3)
            },
            "performance": {
                "avg_latency_ms": round(avg_latency, 2),
                "total_tokens": total_tokens,
                "total_cost_usd": round(total_cost, 4)
            },
            "system_health": {
                "test_pass_rate": round(test_pass_rate, 2),
                "error_rate": round(error_rate, 2)
            },
            "metrics_count": {
                "ai_quality": len(self.ai_quality_metrics),
                "performance": len(self.performance_metrics),
                "system_health": len(self.system_health_metrics)
            }
        }

    def print_summary(self):
        """Print formatted summary to console."""
        summary = self.get_summary()

        print("\n" + "="*60)
        print("AI QA TESTING METRICS SUMMARY")
        print("="*60)

        print("\n📊 AI QUALITY METRICS:")
        for key, value in summary["ai_quality"].items():
            print(f"   {key.replace('_', ' ').title()}: {value}")

        print("\n⚡ PERFORMANCE METRICS:")
        for key, value in summary["performance"].items():
            print(f"   {key.replace('_', ' ').title()}: {value}")

        print("\n🏥 SYSTEM HEALTH:")
        for key, value in summary["system_health"].items():
            print(f"   {key.replace('_', ' ').title()}: {value}%")

        print("\n📈 METRICS COLLECTED:")
        for key, value in summary["metrics_count"].items():
            print(f"   {key.replace('_', ' ').title()}: {value}")

        print("\n" + "="*60 + "\n")


# Global metrics collector instance
_global_collector: Optional[MetricsCollector] = None

def get_metrics_collector() -> MetricsCollector:
    """Get or create global metrics collector instance."""
    global _global_collector
    if _global_collector is None:
        _global_collector = MetricsCollector()
    return _global_collector
