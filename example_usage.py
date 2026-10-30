# -*- coding: utf-8 -*-
import json
from client import GenParkAccioShopifyOperator

shopify = GenParkAccioShopifyOperator()

# 1. Cart Abandonment Recovery Prediction
cart = shopify.predict_cart_abandonment_recovery(
    cart_value_usd=145.0,
    items_count=3,
    dwell_time_minutes=12.0,
    customer_past_orders=2
)
print(f"Cart Recovery: P(Recover)={cart['baseline_recovery_probability_pct']}% | Discount: {cart['offered_discount_pct']}% | Expected Rev: ${cart['expected_recovered_revenue_usd']}")
print(f"  Strategy: {cart['recommended_strategy']}")

# 2. Stochastic Inventory Reorder Point (ROP)
rop = shopify.calculate_inventory_reorder_point_and_rop(
    daily_sales_rate=35.0,
    supplier_lead_time_days=10.0,
    lead_time_std_dev=2.5,
    demand_std_dev=6.0,
    service_level_z=1.645
)
print()
print(f"Inventory ROP: Reorder Point = {rop['reorder_point_units']} units (LeadTime Demand: {rop['lead_time_demand_units']}, Safety Stock: {rop['safety_stock_units']})")

# 3. Dynamic Product Bundling Economics
bundle_prods = [
    {"name": "Ultra Hydrating Serum", "price": 48.0, "cogs": 9.50},
    {"name": "Barrier Recovery Cream", "price": 42.0, "cogs": 8.00},
    {"name": "Enzyme Cleanser", "price": 28.0, "cogs": 5.20}
]
bundle = shopify.optimize_dynamic_tier_bundling(bundle_prods, target_bundle_discount_pct=15.0)
print()
print(f"Bundle: {', '.join(bundle['products_in_bundle'])}")
print(f"  Individual Total: ${bundle['total_individual_price_usd']} -> Bundle Price: ${bundle['bundle_price_usd']} (Margin: {bundle['bundle_gross_margin_pct']}%, AOV Lift: +{bundle['expected_aov_lift_pct']}%)")
