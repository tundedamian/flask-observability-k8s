# app.py
from flask import Flask, request, jsonify
import time
import random
import logging

# Prometheus exporter
from prometheus_flask_exporter import PrometheusMetrics

# OpenTelemetry tracing
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# Choose an exporter — here we use Jaeger exporter (to Jaeger agent/collector)
from opentelemetry.exporter.jaeger.thrift import JaegerExporter

# Basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("flask-otel")

# Flask app
app = Flask(__name__)

# Prometheus metrics (exposes /metrics)
metrics = PrometheusMetrics(app)

# Setup OpenTelemetry TracerProvider with a resource identifying the service
resource = Resource(attributes={
    "service.name": "flask-otel-app",
    "service.version": "0.1.0"
})
tracer_provider = TracerProvider(resource=resource)
trace.set_tracer_provider(tracer_provider)

# Configure Jaeger exporter: default expects agent on host:6831 (udp) or collector endpoint.
jaeger_exporter = JaegerExporter(
    # If you run the Jaeger all-in-one as a k8s service named "jaeger",
    # collector_endpoint="http://jaeger-collector:14268/api/traces" is an option.
    # We'll use agent (UDP) default host/port so no args are necessary when agent is on localhost/kube node.
)

span_processor = BatchSpanProcessor(jaeger_exporter)
tracer_provider.add_span_processor(span_processor)

# Instrument Flask app automatically
FlaskInstrumentor().instrument_app(app)

tracer = trace.get_tracer(__name__)

@app.route("/")
def index():
    with tracer.start_as_current_span("index-handler"):
        # simulate a small amount of work
        time.sleep(random.uniform(0.01, 0.1))
        return """
        <h2>Flask App with Prometheus metrics & OpenTelemetry traces</h2>
        <p>Try <a href="/hello">/hello</a> or <a href="/error">/error</a>.</p>
        """

@app.route("/hello")
def hello():
    with tracer.start_as_current_span("hello-handler"):
        name = request.args.get("name", "DevOps")
        # custom attributes for traces
        trace.get_current_span().set_attribute("app.username", name)
        return jsonify(message=f"Hello, {name}!")

@app.route("/work")
def work():
    # an endpoint that does a bit of work / simulates latency
    with tracer.start_as_current_span("work-handler"):
        delay = random.uniform(0.1, 0.5)
        time.sleep(delay)
        return jsonify(status="done", delay=round(delay, 3))

@app.route("/error")
def error():
    with tracer.start_as_current_span("error-handler"):
        # simulate an error to generate an error span
        try:
            raise ValueError("simulated error for tracing")
        except Exception as e:
            # set span status / record exception
            span = trace.get_current_span()
            span.record_exception(e)
            logger.exception("Simulated error occurred")
            return jsonify(error=str(e)), 500

if __name__ == "__main__":
    # Expose app on port 5000 (Flask default). Prometheus exporter exposes /metrics.
    app.run(host="0.0.0.0", port=5000)

