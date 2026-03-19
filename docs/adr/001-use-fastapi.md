# ADR 001: Use FastAPI as the Backend Framework

## Status

Accepted

## Context

BugSniffer needed a Python web framework for a focused API that integrates with Python-native security tools. The backend serves a REST API for submitting scan requests and returning structured findings. Main candidates were FastAPI, Django REST Framework, and Flask.

## Alternatives Considered

**Django REST Framework** — Mature and battle-tested, but heavyweight for this use case. It brings an ORM, admin interface, and authentication system that BugSniffer doesn't need. The additional complexity and boilerplate would slow down early development without providing meaningful value.

**Flask** — Lightweight and flexible, but lacks built-in request/response validation, has no native async support, and requires manual wiring for schema definitions and API documentation.

## Decision

Use FastAPI as the backend framework. FastAPI provides native Pydantic integration, which gives declarative request and response validation with minimal boilerplate. OpenAPI documentation is generated automatically from the route definitions and Pydantic models. Async support is built in, which will be valuable when scan processing moves to background jobs. The framework is lightweight enough to stay out of the way while providing strong defaults for an API-first application.

## Consequences

Pydantic is a first-class dependency throughout the system — all request, response, and domain models use it. Database integration, authentication, and background job processing will each require explicit library choices when those features are added, since FastAPI does not provide them out of the box. The team must evaluate and select these dependencies individually as the project grows.
