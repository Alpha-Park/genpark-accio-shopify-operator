# -*- coding: utf-8 -*-
"""
GenPark Accio Shopify Operator Client
Zero-dependency cart abandonment recovery probability predictor, inventory reorder point (ROP) solver,
and multi-product tier bundling revenue optimizer.
"""

import math
from typing import Dict, List, Any, Optional

class GenParkAccioShopifyOperator:
    """
    Optimizes Shopify operations: models cart abandonment recovery curves,
    calculates stochastic reorder points (ROP), and maximizes bundle gross margin.
    """

    def predict_cart_abandonment_recovery(
        self,
        cart_value_usd: float,
        items_count: int,
        dwell_time_minutes: float,
        customer_past_orders: int = 0
    ) -> Dict[str, Any]:
        """
        Predicts recovery conversion probability using calibrated logistic regression:
        z = -0.5 - 0.4*ln(cart) + 0.2*items - 0.15*dwell + 0.5*past_orders
        """
        if cart_value_usd <= 0:
            raise ValueError("Cart value must be positive.")

        # Logit equation
        z = (
            -0.2
            - 0.35 * math.log(max(1.0, cart_value_usd / 50.0))
            + 0.15 * min(5, items_count)
            - 0.10 * min(30.0, dwell_time_minutes) / 10.0
            + 0.60 * min(4, customer_past_orders)
        )

        recovery_prob = 1.0 / (1.0 + math.exp(-z))
        recovery_prob_pct = round(recovery_prob * 100.0, 2)

        # Incentive intervention strategy
        if recovery_prob >= 0.55:
            strategy = "ORGANIC_NUDGE (Send subtle reminder email without discount)"
            offered_discount_pct = 0.0
        elif recovery_prob >= 0.30:
            strategy = "MODERATE_INCENTIVE (Offer 10% limited-time checkout discount)"
            offered_discount_pct = 10.0
        else:
            strategy = "AGGRESSIVE_RECOVERY (Offer 15% discount + free expedited shipping)"
            offered_discount_pct = 15.0

        expected_recovered_revenue = round(cart_value_usd * (1.0 - offered_discount_pct / 100.0) * recovery_prob, 2)

        return {
            "cart_value_usd": cart_value_usd,
            "items_count": items_count,
            "dwell_time_minutes": dwell_time_minutes,
            "customer_past_orders": customer_past_orders,
            "baseline_recovery_probability_pct": recovery_prob_pct,
            "recommended_strategy": strategy,
            "offered_discount_pct": offered_discount_pct,
            "expected_recovered_revenue_usd": expected_recovered_revenue
        }

    def calculate_inventory_reorder_point_and_rop(
        self,
        daily_sales_rate: float,
        supplier_lead_time_days: float,
        lead_time_std_dev: float = 2.0,
        demand_std_dev: float = 5.0,
        service_level_z: float = 1.645
    ) -> Dict[str, Any]:
        """
        Calculates stochastic Reorder Point (ROP) with demand and lead time uncertainty:
        ROP = (d * L) + Z * sqrt(L * sigma_d^2 + d^2 * sigma_L^2)
        """
        if daily_sales_rate <= 0 or supplier_lead_time_days <= 0:
            raise ValueError("Sales rate and lead time must be strictly positive.")

        # Expected demand during lead time
        expected_demand = daily_sales_rate * supplier_lead_time_days

        # Combined standard deviation: sqrt(L * sigma_d^2 + d^2 * sigma_L^2)
        combined_var = (
            supplier_lead_time_days * (demand_std_dev ** 2)
            + (daily_sales_rate ** 2) * (lead_time_std_dev ** 2)
        )
        safety_stock = service_level_z * math.sqrt(combined_var)

        rop = round(expected_demand + safety_stock, 1)

        return {
            "daily_sales_rate": daily_sales_rate,
            "supplier_lead_time_days": supplier_lead_time_days,
            "lead_time_demand_units": round(expected_demand, 1),
            "safety_stock_units": round(safety_stock, 1),
            "reorder_point_units": rop,
            "service_level_target_pct": 95.0 if abs(service_level_z - 1.645) < 0.05 else (99.0 if service_level_z > 2.0 else 90.0)
        }

    def optimize_dynamic_tier_bundling(
        self,
        products: List[Dict[str, Any]],
        target_bundle_discount_pct: float = 15.0
    ) -> Dict[str, Any]:
        """
        Evaluates cross-product bundle economics: computes combined price, gross margin, and expected AOV lift.
        """
        if len(products) < 2:
            raise ValueError("Need at least 2 products to construct a bundle.")

        total_individual_price = sum(p.get("price", 0.0) for p in products)
        total_cogs = sum(p.get("cogs", p.get("price", 0.0) * 0.3) for p in products)

        discount_multiplier = 1.0 - (target_bundle_discount_pct / 100.0)
        bundle_price = round(total_individual_price * discount_multiplier, 2)
        bundle_gross_profit = round(bundle_price - total_cogs, 2)
        bundle_margin_pct = round(100.0 * bundle_gross_profit / bundle_price, 2)

        # Baseline AOV heuristic (highest single product price)
        baseline_aov = max(p.get("price", 0.0) for p in products)
        aov_lift_pct = round(100.0 * (bundle_price - baseline_aov) / max(1e-9, baseline_aov), 1)

        return {
            "products_in_bundle": [p.get("name", "Product") for p in products],
            "total_individual_price_usd": round(total_individual_price, 2),
            "bundle_discount_pct": target_bundle_discount_pct,
            "bundle_price_usd": bundle_price,
            "total_cogs_usd": round(total_cogs, 2),
            "bundle_gross_profit_usd": bundle_gross_profit,
            "bundle_gross_margin_pct": bundle_margin_pct,
            "expected_aov_lift_pct": aov_lift_pct,
            "bundle_feasibility": "PROFITABLE_BUNDLE" if bundle_margin_pct >= 55.0 else "MARGIN_DILUTIVE_WARNING"
        }
