def get_customer_metrics(*, data, from_, to, min_total_spend=None):
    customers = {}

    for order in data:
        order_date = order["orderDate"]

        # Inclusive date filter
        if order_date < from_ or order_date > to:
            continue

        customer_id = order["customerId"]

        order_amount = sum(
            item["quantity"] * item["unitPrice"]
            for item in order["lineItems"]
        )

        if customer_id not in customers:
            customers[customer_id] = {
                "customerId": customer_id,
                "orderCount": 0,
                "totalSpend": 0,
            }

        customers[customer_id]["orderCount"] += 1
        customers[customer_id]["totalSpend"] += order_amount

    results = []

    for customer in customers.values():
        customer["avgOrderValue"] = (
            customer["totalSpend"] / customer["orderCount"]
        )

        if (
            min_total_spend is None
            or customer["totalSpend"] >= min_total_spend
        ):
            results.append(customer)

    results.sort(key=lambda x: x["customerId"])

    return {"results": results}
