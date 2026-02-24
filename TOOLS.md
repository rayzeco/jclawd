---
summary: "Environment & operational conventions"
---

# TOOLS.md

## Environment & Operational Conventions

### General Philosophy
Tools and environments should:
- Enable automation
- Support repeatable delivery
- Be enterprise-ready and scalable
- Align with AI-driven workflows

### Common Technical Context (High-Level)
- Docker-based deployments and VPS environments
- AI tooling integrations (OpenAI, Claude, agent frameworks)
- Data platforms: SQL Server, Postgres, semantic layer tooling
- Modernization stacks involving legacy enterprise systems

### Repo & Code Conventions (Guiding Principles)
- Prefer modular, reusable components
- Design for multi-client reuse where possible
- Use clear separation: raw data, business logic, semantic layer
- Favor declarative models over embedded procedural logic

### Identity & Defaults
- Git / author identity typically aligned to JC / Rayze context
- Default organizational identity: Rayze
- Default strategic lens: enterprise AI consulting & platformization

### Security & Secrets Guidance
- Avoid storing secrets in plain-text MD files
- Assume enterprise-grade security expectations
- Prefer environment variables and secure vaults for keys

### Operational Defaults
- Design solutions assuming multi-tenant enterprise usage
- Favor cloud + containerized architectures
- Build with auditability and governance in mind
