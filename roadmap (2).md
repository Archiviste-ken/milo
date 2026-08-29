# 🧠 MILO — Agentic Engineering Roadmap

> **MILO** is a production-oriented learning project for understanding how LLM agents are engineered: LLM reasoning, tools, memory, planning, execution, verification, recovery, evaluation, observability, security, and production hardening.
>
> **Current status:** ~40% of the full roadmap  
> **Primary language:** Python  
> **Current LLM:** Groq  
> **Design principle:** Build core primitives ourselves before introducing heavyweight agent frameworks.

---

## 🎯 Project Goal

Build MILO from a simple LLM + tools loop into a **small but production-minded agent runtime**.

Target architecture:

```text
👤 User
   ↓
🎯 Goal
   ↓
🧠 Planner
   ↓
📋 Structured Plan
   ↓
🔍 Plan Validation
   ↓
⚙️ Executor
   ↓
🛠️ Tool
   ↓
👀 Observation
   ↓
🔍 Verification
   ↓
┌──────────────────────┐
│ Success?             │
│  ├─ Yes → next step  │
│  └─ No  → recovery   │
└──────────────────────┘
   ↓
🔄 Re-plan when needed
   ↓
🧪 Evaluate / Trace
   ↓
💬 Final Answer
```

---

# 📊 Overall Progress

| Area | Status | Progress | Priority |
|---|---|---:|---|
| Project structure | ✅ Done | 100% | — |
| Groq LLM client | ✅ Done | 100% | — |
| System prompts | ✅ Done | 100% | — |
| Agent runtime | 🟡 In progress | 75% | High |
| Agent state | ✅ Done | 100% | — |
| Tool calling | ✅ Done | 100% | — |
| Tool registry | ✅ Done | 100% | — |
| Structured tool results | ✅ Done | 100% | — |
| Calculator tool | ✅ Done | 100% | — |
| Persistent memory | ✅ Done | 90% | Medium |
| Remember memory | ✅ Done | 100% | — |
| Recall memory | ✅ Done | 100% | — |
| Basic verification | ✅ Done | 100% | — |
| Plan representation | ✅ Done | 100% | — |
| Plan validation | ✅ Done | 100% | — |
| LLM-based planning | 🟡 Working | 85% | High |
| Plan execution | 🟡 Current | 40% | Critical |
| Recovery | 🔴 Not started | 15% | Critical |
| Re-planning | 🔴 Not started | 0% | Critical |
| Context management | 🔴 Not started | 0% | High |
| Advanced memory | 🔴 Not started | 0% | Medium |
| Evaluation harness | 🔴 Not started | 0% | Critical |
| Observability | 🟡 Basic logs | 10% | High |
| Security / permissions | 🔴 Not started | 0% | Critical |
| Sandboxed tools | 🔴 Not started | 0% | High |
| Production hardening | 🔴 Not started | 0% | High |
| Deployment | 🔴 Not started | 0% | Medium |

---

# 🏗️ Phase 0 — Foundation

**Status: ✅ Complete**

### Built

- Python virtual environment
- Application package
- Agent package
- LLM package
- Tools package
- Memory package
- Tests directory
- Clean project-level imports

### Core lesson

> Keep responsibilities separated so individual components can change without rewriting the entire agent.

---

# 🧠 Phase 1 — LLM Layer

**Status: ✅ Complete**

## Files

```text
app/
└── llm/
    └── groq_client.py
```

### Built

- Groq client
- LLM request boundary
- Message handling
- Tool definitions passed to the model

### Architecture

```text
🎮 Agent
   ↓
📡 GroqClient
   ↓
🧠 Groq
   ↓
📡 Response
   ↓
🎮 Agent
```

---

# 📜 Phase 2 — Prompt System

**Status: ✅ Complete**

## File

```text
app/prompts.py
```

### Built

- MILO identity
- Tool usage instructions
- Tool argument rules
- Reliability instructions
- Failure-handling guidance

### Principle

```text
📜 Prompt = Guidance
🐍 Runtime = Enforcement
```

The prompt is not a security boundary.

---

# 🎮 Phase 3 — Agent Runtime

**Status: 🟡 In Progress**

## Files

```text
app/
└── agent/
    ├── runner.py
    └── state.py
```

### Built

- Agent class
- User input handling
- LLM interaction loop
- Iteration limit
- Tool-call processing
- Conversation state
- Observations
- Verification records

### Current loop

```text
👤 User
   ↓
🎮 Runner
   ↓
🧠 LLM
   ↓
🤔 Tool required?
   ├── No → 💬 Answer
   └── Yes
         ↓
      🛠️ Tool
         ↓
      📦 Result
         ↓
      🔍 Verify
         ↓
      🧠 LLM
```

### Remaining

- Plan-driven execution
- Better state transitions
- Explicit execution lifecycle
- Recovery
- Re-planning
- Cancellation / timeout handling

---

# 📦 Phase 4 — Agent State

**Status: ✅ Complete**

## File

```text
app/agent/state.py
```

### State currently tracks

| Field | Purpose |
|---|---|
| `messages` | Conversation / tool messages |
| `iteration` | Current runtime iteration |
| `tool_calls` | Tools requested/executed |
| `observations` | Tool outputs |
| `verifications` | Verification results |
| `errors` | Runtime errors |
| `plan` | Current plan representation |
| `current_step` | Current plan step |
| `status` | Runtime lifecycle status |

### Future state

- Goal
- Plan version
- Current action
- Retry count
- Token budget
- Observation budget
- Timing
- Tool permissions
- Recovery decisions
- Final outcome

---

# 🛠️ Phase 5 — Tool System

**Status: ✅ Complete**

## Files

```text
app/
└── tools/
    ├── registry.py
    ├── tool_result.py
    ├── calculator.py
    └── memory_tools.py
```

### Current tools

| Tool | Purpose | Status |
|---|---|---|
| `calculate` | Mathematical calculations | ✅ |
| `remember_memory` | Store durable information | ✅ |
| `recall_memory` | Retrieve stored information | ✅ |

### Architecture

```text
🧠 LLM
   ↓
📋 TOOL_DEFINITIONS
   ↓
🎮 Runner
   ↓
📋 Tool Registry
   ↓
🛠️ Python Function
   ↓
📦 ToolResult
```

---

# 📦 Phase 6 — Structured Tool Results

**Status: ✅ Complete**

## File

```text
app/tools/tool_result.py
```

### Standard contract

```python
ToolResult(
    success=True,
    data={...},
    error=None,
)
```

or:

```python
ToolResult(
    success=False,
    data=None,
    error="...",
)
```

### Principle

```text
🛠️ Tool
   ↓
📦 ToolResult
├── ✅ success
├── 📦 data
└── ❌ error
```

---

# 💾 Phase 7 — Persistent Memory

**Status: ✅ Mostly Complete**

## Files

```text
app/
└── memory/
    └── store.py

data/
└── memory.json
```

and:

```text
app/tools/memory_tools.py
```

### Remember

```text
👤 User
   ↓
📝 remember_memory
   ↓
💾 MemoryStore
   ↓
📄 memory.json
```

### Recall

```text
👤 User
   ↓
🔎 recall_memory
   ↓
💾 MemoryStore
   ↓
📄 memory.json
   ↓
📦 Matching memories
   ↓
🧠 LLM
```

### Key distinction

```text
📝 Remember = WRITE
🔎 Recall = READ
```

### Future improvements

- Deduplication
- Memory relevance scoring
- Metadata
- Confidence
- Semantic search
- Memory consolidation
- Forgetting / expiration
- Conflict resolution

> JSON storage is intentionally retained for learning. Do not replace it with a vector database just for the sake of using one.

---

# 🔍 Phase 8 — Verification

**Status: ✅ Basic Version Complete**

## File

```text
app/agent/verifier.py
```

### Current behavior

```text
🛠️ Tool
   ↓
📦 ToolResult
   ↓
🔍 verify_tool_result()
   ↓
✅ Valid
or
❌ Failed
```

### Current checks

- Tool failure
- Missing data
- Successful result

### Future

Make verification task-aware and evidence-based.

```text
⚙️ Action
   ↓
👀 Observation
   ↓
🔍 Independent verification
   ↓
📊 Evidence
```

---

# 📋 Phase 9 — Plan Representation

**Status: ✅ Complete**

## File

```text
app/agent/plan.py
```

### Current model

```python
Plan(
    goal="...",
    steps=[
        PlanStep(
            action="calculate",
            arguments={
                "expression": "25 * 8"
            }
        )
    ]
)
```

### Concept

```text
📋 Plan
├── 🎯 Goal
└── 🪜 Steps
```

---

# 🛡️ Phase 10 — Plan Validation

**Status: ✅ Complete**

## File

```text
app/agent/plan_validator.py
```

### Current policy

Only explicitly allowed actions can appear:

```text
calculate
remember_memory
recall_memory
```

### Architecture

```text
🧠 LLM
   ↓
📋 Proposed Plan
   ↓
🔍 Validator
   ├── ✅ Allowed
   └── ❌ Reject
```

### Critical principle

> The LLM proposes capabilities; Python defines capabilities.

---

# 🧠 Phase 11 — LLM-Based Planning

**Status: 🟡 Working**

## File

```text
app/agent/planner.py
```

### Current flow

```text
👤 User
   ↓
📋 Planner
   ↓
🧠 Groq
   ↓
JSON
   ↓
📦 Plan
   ↓
🔍 Validation
```

### Current capabilities

- Calculation planning
- Memory-write planning
- Memory-recall planning
- Structured JSON output
- Plan validation

### Current limitation

The planner generates the plan, but the runtime still needs to make the plan the authoritative execution source.

---

# ⚙️ Phase 12 — Plan Executor

**Status: 🟡 Current Phase**

## File

```text
app/agent/executor.py
```

### Goal

Execute the validated plan directly.

Target:

```text
🧠 Planner
   ↓
📋 Plan
   ↓
🔍 Validate
   ↓
⚙️ Executor
   ↓
🛠️ Tool
```

### Critical architectural change

Current:

```text
📋 Plan
   ↓
🤷 Plan generated
   ↓
🧠 LLM decides tools again
```

Target:

```text
📋 Plan
   ↓
🔍 Validate
   ↓
⚙️ Execute exact step
```

This makes planning authoritative.

---

# 🔄 Phase 13 — Recovery

**Status: 🔴 Not Started**

Teach MILO that:

```text
❌ Tool failure
```

does not automatically mean:

```text
🔄 Retry
```

### Recovery model

```text
❌ Failure
   ↓
🤔 Is recovery possible?
   ├── No → report failure
   └── Yes
         ↓
      🔄 Retry / alternate action
```

### Must handle

- Retry safety
- Idempotency
- Retry limits
- Error types
- Timeouts
- Side effects
- Duplicate operations

---

# 🧠 Phase 14 — Re-Planning

**Status: 🔴 Not Started**

When reality differs from the original plan:

```text
📋 Original Plan
       ↓
⚙️ Execute
       ↓
👀 Observation
       ↓
❌ Unexpected result
       ↓
🧠 Re-plan
       ↓
📋 New Plan
```

Target:

```text
PLAN
 ↓
ACT
 ↓
OBSERVE
 ↓
VERIFY
 ↓
ADAPT
 ↓
RE-PLAN
```

---

# 🧠 Phase 15 — Context Management

**Status: 🔴 Not Started**

Long-running agents cannot keep every message forever.

Build:

- Conversation trimming
- Context summarization
- Relevant-memory retrieval
- Token budgeting
- Observation compression
- Important-event preservation

Target:

```text
💬 Conversation
      +
💾 Relevant Memory
      +
📌 Important State
      ↓
🧠 Context Builder
      ↓
LLM
```

---

# 💾 Phase 16 — Advanced Memory

**Status: 🔴 Not Started**

Move beyond basic JSON storage after the fundamentals are understood.

Potential architecture:

```text
💾 Memory
├── Episodic
│   └── What happened
├── Semantic
│   └── Stable facts
└── Procedural
    └── Useful procedures
```

Potential improvements:

- Semantic retrieval
- Relevance ranking
- Deduplication
- Memory consolidation
- Importance scoring
- Temporal metadata
- Explicit forgetting
- Memory conflict resolution

---

# 🧪 Phase 17 — Evaluation Harness

**Status: 🔴 Not Started**

Create repeatable tasks:

| Test | What it checks |
|---|---|
| Simple calculation | Tool selection |
| Memory write | Remember behavior |
| Memory recall | Retrieval |
| Multi-step task | Planning |
| Tool failure | Error handling |
| Invalid plan | Validation |
| Unnecessary memory | Memory discipline |
| Multiple tools | Execution ordering |
| Repeated task | Stability |
| Max iterations | Runtime safety |

Target:

```text
🧪 Tasks
   ↓
🤖 MILO
   ↓
📊 Evaluation
├── Success rate
├── Tool accuracy
├── Planning accuracy
├── Recovery rate
├── Latency
└── Token usage
```

---

# 📊 Phase 18 — Observability

**Status: 🟡 Basic Logs**

Current:

```text
🔧 Tool
📦 Result
🔍 Verification
```

Target:

```text
📍 Trace
├── Request
├── Planning latency
├── LLM call
├── Tokens
├── Tool call
├── Tool latency
├── Observation
├── Verification
├── Retry
├── Re-plan
└── Final answer
```

Eventually learn:

- Structured logging
- Trace IDs
- OpenTelemetry
- Metrics
- Prometheus
- GenAI spans
- Error aggregation
- Cost tracking

---

# 🔐 Phase 19 — Security & Permissions

**Status: 🔴 Not Started**

Before powerful tools are added:

```text
🧠 LLM
   ↓
🛡️ Policy
   ↓
🔐 Permission Check
   ↓
⚙️ Tool
```

Potential controls:

- Tool allowlists
- Argument validation
- Resource limits
- Timeouts
- Confirmation gates
- Rate limits
- Secret isolation
- Audit logs

---

# 🏖️ Phase 20 — Sandbox

**Status: 🔴 Not Started**

Only after the core runtime is stable.

Potential capabilities:

```text
📁 File access
💻 Command execution
🧪 Test execution
🐙 Git operations
```

Target:

```text
🧠 Agent
   ↓
🛡️ Policy
   ↓
🏖️ Sandbox
   ↓
⚙️ Execution
```

Potential protections:

- Path jail
- Command restrictions
- Working-directory restriction
- CPU limits
- Memory limits
- Timeouts
- Network restrictions
- Process isolation

---

# 🛠️ Phase 21 — Real Engineering Tools

**Status: 🔴 Not Started**

Add tools deliberately.

| Tool | Value | Risk |
|---|---|---|
| Calculator | Learning primitive | 🟢 Low |
| Memory | Agent state | 🟢 Low |
| File reader | Context | 🟡 Medium |
| Code search | Coding agents | 🟡 Medium |
| Test runner | Verification | 🟡 Medium |
| Git read operations | Repo reasoning | 🟡 Medium |
| Git write operations | Agent actions | 🟠 Higher |
| Shell | General execution | 🔴 High |
| Browser actions | External side effects | 🔴 High |

---

# 🤖 Phase 22 — Coding-Agent Capabilities

**Status: 🔴 Future**

Once the core runtime is stable:

```text
👤 "Fix this bug."
       ↓
🧠 Understand
       ↓
🔎 Search code
       ↓
📋 Plan
       ↓
📝 Edit
       ↓
🧪 Run tests
       ↓
🔍 Verify
       ↓
🔄 Fix if needed
       ↓
📊 Report
```

---

# 🌐 Phase 23 — MCP / External Tool Protocols

**Status: 🔴 Future**

Learn:

- Tool schemas
- Tool discovery
- JSON-RPC
- MCP
- Registry
- Governance
- Permissions
- Transport boundaries

Target:

```text
🧠 MILO
   ↓
📋 Tool Registry
   ↓
🌐 External Tool Server
   ↓
🛠️ Capability
```

Build the primitive concepts yourself before hiding them behind a framework.

---

# 🧪 Phase 24 — Red-Team & Safety Evaluation

**Status: 🔴 Future**

Test MILO against:

- Prompt injection
- Tool manipulation
- Invalid arguments
- Malicious tool outputs
- Excessive tool calls
- Context poisoning
- Memory poisoning
- Unsafe action requests
- Plan injection
- Resource exhaustion

Target:

```text
🧪 Attack
   ↓
🤖 MILO
   ↓
🛡️ Safety Gate
   ↓
📊 Result
```

---

# 🚀 Phase 25 — Production Hardening

**Status: 🔴 Future**

### Reliability

- Timeouts
- Retries
- Circuit breakers
- Graceful failure
- Cancellation
- Idempotency

### Security

- Secrets management
- Permissions
- Sandboxing
- Input validation
- Output validation

### Performance

- Token budgets
- Caching
- Safe parallel tool execution
- Latency tracking

### Engineering

- Unit tests
- Integration tests
- Evaluation suite
- Structured logs
- Tracing
- Metrics
- Configuration management

---

# 🌐 Phase 26 — Deployment

**Status: 🔴 Future**

Target:

```text
                👤 User
                   ↓
              🌐 API / UI
                   ↓
              🎮 MILO
                   ↓
        ┌──────────┼──────────┐
        ↓          ↓          ↓
      🧠 LLM     💾 DB      🛠️ Tools
                   ↓
               📊 Telemetry
```

Learn:

- API authentication
- Rate limiting
- Persistent database
- Secrets
- Containers
- Health checks
- Logging
- Monitoring
- Graceful shutdown

---

# 🏆 Final Target Architecture

```text
                         👤 USER
                            │
                            ▼
                      🎯 GOAL / TASK
                            │
                            ▼
                     🧠 PLANNER LLM
                            │
                            ▼
                     📋 STRUCTURED PLAN
                            │
                            ▼
                      🔍 PLAN VALIDATOR
                            │
                            ▼
                       🎮 RUNTIME
                            │
              ┌─────────────┴─────────────┐
              │                           │
              ▼                           ▼
          💾 MEMORY                   🛡️ POLICY
                                          │
                                          ▼
                                     ⚙️ EXECUTOR
                                          │
                                    ┌─────┴─────┐
                                    ▼           ▼
                                 🛠️ TOOL    🏖️ SANDBOX
                                    │
                                    ▼
                                 📦 RESULT
                                    │
                                    ▼
                                 👀 OBSERVE
                                    │
                                    ▼
                                 🔍 VERIFY
                                    │
                                 ┌──┴───┐
                                 ▼      ▼
                                ✅      ❌
                                │       │
                                │    🔄 RECOVER
                                │       │
                                │    🧠 RE-PLAN
                                │       │
                                └──┬────┘
                                   ▼
                              🧪 EVALUATE
                                   │
                                   ▼
                              📊 OBSERVE
                                   │
                                   ▼
                               💬 ANSWER
```

---

# 🗺️ Recommended Build Order From Here

Follow this sequence:

```text
1.  ⚙️ Plan Executor              ← NOW
        ↓
2.  🔍 Stronger verification
        ↓
3.  🔄 Recovery
        ↓
4.  🧠 Re-planning
        ↓
5.  🧠 Context management
        ↓
6.  💾 Better memory
        ↓
7.  🧪 Evaluation harness
        ↓
8.  📊 Observability
        ↓
9.  🛡️ Permissions
        ↓
10. 🏖️ Sandbox
        ↓
11. 🛠️ Coding tools
        ↓
12. 🌐 MCP
        ↓
13. 🧪 Red-team evaluation
        ↓
14. 🚀 Production hardening
        ↓
15. 🌐 Deployment
```

---

# ❌ Things We Should NOT Do Yet

- ❌ LangGraph before understanding the runtime
- ❌ 20+ tools before the core loop is reliable
- ❌ Vector DB just because it sounds advanced
- ❌ Multi-agent systems before single-agent reliability
- ❌ Autonomous shell access before sandboxing
- ❌ Browser automation before permission controls
- ❌ Fine-tuning before evaluation
- ❌ Distributed infrastructure before the local architecture is correct

> **Goal: understanding, not technology collecting.**

---

# 🧠 What MILO Is Teaching You

| Concept | MILO component |
|---|---|
| LLM API integration | `groq_client.py` |
| Prompt engineering | `prompts.py` |
| Agent loops | `runner.py` |
| State management | `state.py` |
| Tool calling | `registry.py` |
| Tool contracts | `tool_result.py` |
| Tool implementation | `calculator.py` |
| Persistent memory | `store.py` |
| Memory tools | `memory_tools.py` |
| Planning | `planner.py` |
| Structured plans | `plan.py` |
| Guardrails | `plan_validator.py` |
| Verification | `verifier.py` |
| Execution | `executor.py` |
| Recovery | Future |
| Re-planning | Future |
| Evaluation | Future |
| Observability | Future |
| Security | Future |
| Sandboxing | Future |
| Coding agents | Future |
| MCP | Future |
| Production engineering | Future |

---

# 🏁 Definition of Done

MILO is a strong agentic-engineering capstone when it can:

- [ ] Accept a user goal
- [ ] Decide whether planning is necessary
- [ ] Generate a structured plan
- [ ] Validate the plan
- [ ] Execute approved steps
- [ ] Track state
- [ ] Use tools
- [ ] Persist and retrieve memory
- [ ] Observe tool results
- [ ] Independently verify important outcomes
- [ ] Detect failures
- [ ] Recover safely when possible
- [ ] Re-plan when necessary
- [ ] Manage context
- [ ] Evaluate itself on repeatable tasks
- [ ] Produce useful traces and metrics
- [ ] Enforce tool permissions
- [ ] Sandbox risky execution
- [ ] Resist common prompt/tool attacks
- [ ] Handle timeouts and retries
- [ ] Run reliably as a service

---

# 📈 Current Milestone

```text
MILO
████████████░░░░░░░░░░░░░░░░  ~40%

✅ Foundation
✅ LLM
✅ Prompting
✅ Tools
✅ Memory
✅ Tool contracts
✅ Verification
✅ Structured planning

🚧 NOW
⚙️ Plan execution

🔜 NEXT
🔄 Recovery
🧠 Re-planning
🧪 Evaluation
📊 Observability
🛡️ Security
🏖️ Sandboxing
🚀 Production hardening
```

> **Core philosophy:** Build the smallest working primitive, understand it, test it, then make it production-grade. Don't hide important concepts behind frameworks.
