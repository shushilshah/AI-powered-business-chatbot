import pandas as pd
import random
import numpy as np
from faker import Faker

fake = Faker()
random.seed(42)
np.random.seed(42)

# Generate Customers
num_customers = 1000
customer_ids = [fake.uuid4()[:8] for _ in range(num_customers)]
customer_data = pd.DataFrame({
    "customer_id": customer_ids,
    "name": [fake.name() for _ in range(num_customers)],
    "email": [fake.email() for _ in range(num_customers)],
    "location": [fake.city() for _ in range(num_customers)],
    "signup_date": [fake.date_between(start_date="-2y", end_date="today") for _ in range(num_customers)]
})

# Generate Orders
num_orders = 5000
prices = np.random.randint(10, 500, num_orders)
cost_prices = [round(price * random.uniform(0.6, 0.9), 2) for price in prices]
categories = ["Electronics", "Clothing",
              "Home & Kitchen", "Sports", "Books", "Beauty", "Toys"]
order_data = pd.DataFrame({
    "order_id": [fake.uuid4()[:8] for _ in range(num_orders)],
    "customer_id": [random.choice(customer_ids) for _ in range(num_orders)],
    "product": [fake.word().capitalize() for _ in range(num_orders)],
    "category": [random.choice(categories) for _ in range(num_orders)],
    "quantity": np.random.randint(1, 5, num_orders),
    "cost_price": cost_prices,
    "selling_price": np.random.randint(10, 500, num_orders),
    "order_date": [fake.date_between(start_date="-1y", end_date="today") for _ in range(num_orders)]
})

# Generate Support Tickets
num_tickets = 1000
issue_types = ["Billing", "Shipping Delay",
               "Product Issue", "Return Request", "General Inquiry"]
ticket_status = ["Open", "In Progress", "Resolved", "Closed"]
created_dates = [fake.date_between(
    start_date="-6m", end_date="today") for _ in range(num_tickets)]
resolved_dates = [
    fake.date_between(start_date=created,
                      end_date="today") if random.random() > 0.3 else None
    for created in created_dates
]
support_data = pd.DataFrame({
    "ticket_id": [fake.uuid4()[:8] for _ in range(num_tickets)],
    "customer_id": [random.choice(customer_ids) for _ in range(num_tickets)],
    "issue_type": [random.choice(issue_types) for _ in range(num_tickets)],
    "status": [random.choice(ticket_status) for _ in range(num_tickets)],
    "created_at": created_dates,
    "resolved_at": resolved_dates
})

# Generate Product Reviews
num_reviews = 3000
review_data = pd.DataFrame({
    "review_id": [fake.uuid4()[:8] for _ in range(num_reviews)],
    "customer_id": [random.choice(customer_ids) for _ in range(num_reviews)],
    "product": [random.choice(order_data["product"].tolist()) for _ in range(num_reviews)],
    "rating": np.random.randint(1, 6, num_reviews),
    "review_text": [fake.sentence() for _ in range(num_reviews)],
    "review_date": [fake.date_between(start_date="-1y", end_date="today") for _ in range(num_reviews)]
})

# Save as JSON for MongoDB
customer_data.to_csv("src/data/customers.csv", index=False)
order_data.to_csv("src/data/orders.csv", index=False)
support_data.to_csv("src/data/support_tickets.csv", index=False)
review_data.to_csv("src/data/reviews.csv", index=False)

print("Datasets generated successfully!")


# from faker import Faker
# import random
# import pandas as pd

# fake = Faker()

# # Sample product and country pools
# products = [
#     {"id": "P001", "name": "Laptop", "category": "Electronics", "price": 1200},
#     {"id": "P002", "name": "Smartphone", "category": "Electronics", "price": 800},
#     {"id": "P003", "name": "Desk Chair", "category": "Furniture", "price": 150},
#     {"id": "P004", "name": "Coffee Machine",
#         "category": "Appliances", "price": 90},
#     {"id": "P005", "name": "Headphones", "category": "Electronics", "price": 200},
#     {"id": "P006", "name": "Office Desk", "category": "Furniture", "price": 300}
# ]

# countries = ['USA', 'UK', 'Germany', 'Canada',
#              'India', 'Australia', 'Nepal', 'Japan', 'France']


# def generate_sales_data(n=500):
#     data = []

#     for i in range(n):
#         product = random.choice(products)
#         client_id = fake.uuid4()
#         client_name = fake.name()
#         country = random.choice(countries)
#         quantity = random.randint(1, 20)
#         unit_price = product["price"]
#         discount = round(random.uniform(0, 0.2), 2)  # Up to 20% discount
#         cost_price = unit_price * random.uniform(0.6, 0.9)
#         revenue = round(quantity * unit_price * (1 - discount), 2)
#         cost = round(quantity * cost_price, 2)
#         profit = round(revenue - cost, 2)
#         date = fake.date_between(start_date='-1y', end_date='today')

#         data.append({
#             "Transaction ID": fake.uuid4(),
#             "Date": date,
#             "Client ID": client_id,
#             "Client Name": client_name,
#             "Country": country,
#             "Product ID": product["id"],
#             "Product Name": product["name"],
#             "Category": product["category"],
#             "Quantity": quantity,
#             "Unit Price": unit_price,
#             "Discount": discount,
#             "Total Revenue": revenue,
#             "Total Cost": cost,
#             "Profit": profit
#         })

#     return pd.DataFrame(data)


# # Generate dataset
# df = generate_sales_data(1000)
# df.to_csv("src/data/sales_data.csv", index=False)
# print(df.head())
