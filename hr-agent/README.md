# HR Agent + MCP Server

An HR assistant that answers employee questions about **policies, benefits,
and FAQs**. It's split into two pieces:

- **`hr_mcp_server.py`** — an MCP (Model Context Protocol) server that
  exposes HR knowledge as tools (`get_policy`, `get_benefit`, `search_faq`,
  `search_hr_knowledge`, etc.). Data lives in `hr_data.py` as simple
  in-memory Python dicts — swap that for a real database, HRIS API
  (BambooHR, Workday), or document store later without touching the server.
- **`hr_agent.py`** — a CLI agent that connects to the MCP server, gives
  Claude access to its tools, and runs the standard tool-use loop to answer
  employee questions grounded in that data (rather than letting the model
  guess at policy specifics).

```
hr-agent-mcp/
├── hr_data.py         # mock HR data (policies, benefits, FAQs)
├── hr_mcp_server.py    # MCP server exposing that data as tools
├── hr_agent.py          # CLI agent (Claude + MCP tool-use loop)
├── test_server.py       # smoke test for the MCP server (no API key needed)
├── requirements.txt
└── README.md
```

## Setup

```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Try the MCP server on its own (no API key needed)

```bash
python test_server.py
```

This spins up the server, lists its tools, and calls a few of them directly
so you can confirm everything's wired up correctly.

## Run the agent

Set your Anthropic API key:

```bash
export ANTHROPIC_API_KEY=sk-ant-...
```

Then either ask a one-off question:

```bash
python hr_agent.py "How much PTO do I get after 3 years?"
```

or chat interactively:

```bash
python hr_agent.py
```

```
HR Agent ready. Ask a question (or type 'exit').

You: Do we get a 401k match?
HR Agent: Yes — the company matches 100% of the first 3% you contribute
and 50% of the next 2%, for a max match of 4%, vesting immediately.
```

## Available MCP tools

| Tool | Purpose |
|---|---|
| `list_policies` | List all policy titles |
| `get_policy(policy_name)` | Full text of one policy |
| `list_benefits` | List all benefit names |
| `get_benefit(benefit_name)` | Details of one benefit |
| `search_faq(query)` | Keyword search over FAQs |
| `search_hr_knowledge(query)` | Keyword search across policies, benefits, and FAQs |

## Using this MCP server with Claude Desktop instead

You can also point Claude Desktop directly at `hr_mcp_server.py` instead of
(or in addition to) using `hr_agent.py`. Add this to your Claude Desktop
`claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "hr-agent": {
      "command": "/absolute/path/to/venv/bin/python",
      "args": ["/absolute/path/to/hr-agent-mcp/hr_mcp_server.py"]
    }
  }
}
```

Restart Claude Desktop and the HR tools will show up in the tool picker.

## Extending this to real data

Everything the server does routes through `POLICIES`, `BENEFITS`, and
`FAQS` in `hr_data.py`. To connect real data:

- **Database**: replace the dict lookups in `hr_mcp_server.py` with query
  calls (e.g. SQLAlchemy) inside each `@mcp.tool()` function.
- **HRIS API** (BambooHR/Workday/etc.): call their REST API inside each
  tool function instead of reading from the dicts.
- **Documents/wiki**: add a tool that does retrieval (embeddings + vector
  search, or simple keyword search like `search_hr_knowledge` already
  does) over your policy documents.

The agent (`hr_agent.py`) doesn't need any changes — it just calls
whatever tools the server advertises.

## Notes / production considerations

- This is a starting point, not a production HR system: it has no
  authentication, no audit logging, and no handling of sensitive personal
  data (pay disputes, medical/leave specifics, harassment complaints —
  the system prompt tells the agent to redirect those to a human).
- `hr_agent.py` uses model `claude-sonnet-4-6`; change `MODEL` at the top
  of the file if you want a different one.
