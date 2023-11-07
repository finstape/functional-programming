from functools import reduce

orders = [
    {"order_id": 1, "customer_id": 101, "amount": 150.0},
    {"order_id": 2, "customer_id": 102, "amount": 200.0},
    {"order_id": 3, "customer_id": 101, "amount": 75.0},
    {"order_id": 4, "customer_id": 103, "amount": 100.0},
    {"order_id": 5, "customer_id": 101, "amount": 50.0},
    {"order_id": 6, "customer_id": 104, "amount": 175.0},
    {"order_id": 7, "customer_id": 105, "amount": 225.0},
    {"order_id": 8, "customer_id": 103, "amount": 80.0},
    {"order_id": 9, "customer_id": 106, "amount": 95.0},
    {"order_id": 10, "customer_id": 101, "amount": 55.0},
    {"order_id": 11, "customer_id": 102, "amount": 155.0},
    {"order_id": 12, "customer_id": 104, "amount": 105.0},
    {"order_id": 13, "customer_id": 103, "amount": 65.0},
    {"order_id": 14, "customer_id": 107, "amount": 115.0},
    {"order_id": 15, "customer_id": 101, "amount": 45.0},
    {"order_id": 16, "customer_id": 106, "amount": 185.0},
    {"order_id": 17, "customer_id": 102, "amount": 205.0},
    {"order_id": 18, "customer_id": 105, "amount": 125.0},
    {"order_id": 19, "customer_id": 104, "amount": 145.0},
    {"order_id": 20, "customer_id": 108, "amount": 90.0}
]

if __name__ == "__main__":

    """ Filtering orders """
    id = int(input("Write customer_id: "))
    orders_by_id = list(filter(lambda order: order["customer_id"] == id, orders))

    print(f"\nOrders by customer_id {id}: ")
    for order in orders_by_id:
        print(f"order_id: {order['order_id']}, amount: {order['amount']}")

    """ Calculating the amount of orders """
    total_amount = reduce(lambda cnt, order: cnt + order["amount"], orders_by_id, 0)
    print(f"\nTotal amount by customer_id {id}: {total_amount}")

    """ Calculating the average amount of orders """
    print(f"\nThe average amount of orders by cutstomer_id {id}: {total_amount / len(orders_by_id)}")
