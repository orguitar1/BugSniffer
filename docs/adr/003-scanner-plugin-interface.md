# ADR 003: Use an Abstract Base Class and Registry for Scanner Discovery

## Status

Accepted

## Context

BugSniffer needs to support multiple security scanners without the orchestration layer needing to know about each scanner's specific implementation. As new scanners are added, the system should accommodate them with minimal changes to existing code.

## Alternatives Considered

**Direct instantiation in scan_service** — The simplest approach. The scan service would import and instantiate each scanner directly. However, this means the service must import every scanner, and adding a new scanner requires modifying the service layer — violating separation of concerns.

**Configuration-based discovery** — Scanners would be declared in a configuration file and loaded dynamically at runtime. This is more flexible and allows enabling or disabling scanners without code changes, but introduces more complexity than the current scale of the project warrants.

## Decision

Define a BaseScanner abstract base class that specifies the interface: a name class attribute and an abstract scan() method that accepts a repository path and returns a list of Finding objects. All scanners inherit from BaseScanner and implement this interface. A separate registry module provides a get_scanners() function that returns the list of active scanner instances. The orchestration service depends only on the registry and the base interface, never on individual scanner implementations.

## Consequences

Adding a new scanner requires only creating a new file in the scanners/ directory and adding one line to the registry — nothing in the API or services layer changes. The interface enforces a consistent contract across all scanners. The registry is currently a hardcoded list, which is appropriate for the current number of scanners. If the scanner count grows significantly, the registry can move to configuration-based discovery without changing the scanner interface or the orchestration layer.
