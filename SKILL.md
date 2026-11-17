---
description: Autonomous Shopify Operator. Handles store setup, product listing, and cross-border marketing automation.
license: MIT
metadata:
  last_deployed: "2026-04-25"
  version: "1.0.0"
  source: "https://www.accio.com/"
---

# Accio Shopify Operator

This skill enables AI agents to act as a full-service e-commerce manager. It specializes in automating the technical and creative tasks required to launch and scale a Shopify store globally.

## MCP runtime requirements

The standard-library-only policy applies to direct `client.py` use. Running `mcp_server.py` requires Python 3.10+ and the official `mcp` SDK (`mcp>=1.0.0,<2`) from `requirements.txt`. Install it into your chosen environment from the repository checkout:

```bash
python -m pip install -r requirements.txt
```

Configure the MCP client with that environment's absolute Python executable path and the absolute path to `mcp_server.py`. The client launches a local STDIO process; a GitHub URL is not a remote MCP endpoint.

## Instructions
1. **Store Setup:** Automate the configuration of Shopify settings based on user business goals.
2. **Product Orchestration:** Generate high-converting product descriptions, images (using external tools), and metadata from raw ideas or source links.
3. **Marketing Automation:** Draft and schedule email marketing campaigns and social media posts tailored for international markets.
4. **Inventory & Sync:** Monitor stock levels and suggest replenishment or trend-based listing adjustments.

## Examples
- "Set up a Shopify store for eco-friendly yoga mats and list the top 5 trending products in this niche."
- "Create an email marketing campaign for my Shopify store targeting the European market for the upcoming summer season."
