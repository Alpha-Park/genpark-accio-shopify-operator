# -*- coding: utf-8 -*-
"""
GenPark Accio Shopify Operator FastMCP Server
"""

import json
from typing import Dict, List, Any, Optional
from mcp.server.fastmcp import FastMCP
from client import GenParkAccioShopifyOperator

mcp = FastMCP("genpark-accio-shopify-operator")
shopify = GenParkAccioShopifyOperator()

@mcp.tool()
def predict_cart_abandonment_recovery(
    cart_value_usd: float,
    items_count: int,
    dwell_time_minutes: float,
    customer_past_orders: int = 0
) -> str:
    """
    Predicts recovery conversion probability using calibrated logistic regression.
    """
    res = shopify.predict_cart_abandonment_recovery(cart_value_usd, items_count, dwell_time_minutes, customer_past_orders)
    return json.dumps(res, indent=2)

@mcp.tool()
def calculate_inventory_reorder_point_and_rop(
    daily_sales_rate: float,
    supplier_lead_time_days: float,
    lead_time_std_dev: float = 2.0,
    demand_std_dev: float = 5.0,
    service_level_z: float = 1.645
) -> str:
    """
    Calculates stochastic Reorder Point (ROP) with demand and lead time uncertainty.
    """
    res = shopify.calculate_inventory_reorder_point_and_rop(daily_sales_rate, supplier_lead_time_days, lead_time_std_dev, demand_std_dev, service_level_z)
    return json.dumps(res, indent=2)

@mcp.tool()
def optimize_dynamic_tier_bundling(
    products_json: str,
    target_bundle_discount_pct: float = 15.0
) -> str:
    """
    Evaluates cross-product bundle economics: computes combined price, gross margin, and expected AOV lift.
    """
    prods = json.loads(products_json)
    res = shopify.optimize_dynamic_tier_bundling(prods, target_bundle_discount_pct)
    return json.dumps(res, indent=2)

def main():
    print("Testing Shopify Operator:")
    print(predict_cart_abandonment_recovery(120.0, 3, 8.5, 2))

if __name__ == "__main__":
    main()
