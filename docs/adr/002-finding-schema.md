# ADR 002: Use a Single Normalized Finding Schema Across All Scanners

## Status

Accepted

## Context

BugSniffer runs multiple security scanners, each with its own native output format. The API layer, future AI agents, and any persistence layer all need a consistent data contract to work with scan results without coupling to individual scanner implementations.

## Alternatives Considered

**Pass raw scanner output directly** — The simplest approach. Each scanner's native JSON would be forwarded to the API consumer as-is. However, this couples every API consumer to each scanner's specific schema, making it impossible to add or swap scanners without breaking clients.

**Per-scanner response models with a union type at the API layer** — More faithful to each scanner's native output, preserving all tool-specific fields. However, this multiplies complexity as scanners are added, forces API consumers to handle multiple shapes, and makes aggregation and comparison across scanners difficult.

## Decision

Use a single Pydantic Finding model with fields: id, title, description, severity (SeverityLevel enum with low/medium/high/critical values), file, line, scanner, and confidence. Each scanner is responsible for mapping its native output to this schema. The scanner field preserves the source of each finding, allowing consumers to distinguish results by origin when needed.

## Consequences

Every scanner must implement a mapping layer that translates its native output into Finding objects. The schema is a contract — adding or modifying fields requires updating all scanners to remain consistent. The SeverityLevel enum and confidence float normalize results across scanners, but at the cost of some per-scanner nuance being lost in translation. The critical severity level exists in the enum but is not currently produced by any scanner. As more scanners are added, the mapping layer ensures the rest of the system remains insulated from scanner-specific details.
