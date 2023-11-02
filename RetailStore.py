from Toolbox import create_tool
from GroceryBag import create_grocery

# Constants
GST = 0.14

# Tax Calculation Function
def calculate_tax(cost, is_taxable):
    return cost * GST if is_taxable else 0.0

# The Customer Class
class Customer:
    def __init__(self, name, cash, retail_store):
        self.name = name
        self.cash = cash
        self.shopping_cart = {"tools": [], "groceries": []}
        self.retail_store = retail_store
    
    def add_to_cart(self, item, item_type):
        self.shopping_cart[item_type].append(item)
    
    def checkout(self):
        total_cost = sum(item.get_cost() + calculate_tax(item.get_cost(), item_type == "tools")
                         for item_type, items in self.shopping_cart.items() 
                         for item in items)
        
        if total_cost <= self.cash:
            self.cash -= total_cost
            self.retail_store.record_purchase(self, total_cost)
            print(f"\n{self.name}'s Purchase:")
            for item_type, items in self.shopping_cart.items():
                for item in items:
                    item.display()
            print(f"\nTotal Cost: ${total_cost:.2f}\n")
            self.shopping_cart = {"tools": [], "groceries": []}
        else:
            print(f"{self.name} doesn't have enough cash for this purchase.\n")

# The Retail Store Class
class RetailStore:
    def __init__(self):
        self.customers = []
        self.total_revenue = 0.0
        self.tool_revenue = 0.0
        self.grocery_revenue = 0.0
    
    def record_purchase(self, customer, amount):
        self.total_revenue += amount
        for tool in customer.shopping_cart['tools']:
            self.tool_revenue += tool.get_cost() + calculate_tax(tool.get_cost(), True)
        for grocery in customer.shopping_cart['groceries']:
            self.grocery_revenue += grocery.get_cost()
    
    def display_statistics(self):
        num_customers = len(self.customers)
        avg_spending = self.total_revenue / num_customers if num_customers > 0 else 0.0
        tool_percentage = (self.tool_revenue / self.total_revenue) * 100 if self.total_revenue > 0 else 0
        grocery_percentage = 100 - tool_percentage
        
        print("\nRetail Store Statistics:")
        print(f"Average Customer Spending: ${avg_spending:.2f}")
        print(f"Total Revenue: ${self.total_revenue:.2f}")
        print(f"Tool Revenue Percentage: {tool_percentage:.2f}%")
        print(f"Grocery Revenue Percentage: {grocery_percentage:.2f}%")

# Test Program
if __name__ == "__main__":
    store = RetailStore()
    # Create customers
    betty = Customer("betty", 100, store)
    mike = Customer("mike", 150, store)
    harvey = Customer("harvey", 200, store)
    
    store.customers.extend([betty, mike, harvey])

    # Betty's shopping experience
    betty_tool = create_tool()
    betty.add_to_cart(betty_tool, "tools")
    betty_grocery = create_grocery()
    betty.add_to_cart(betty_grocery, "groceries")
    betty.checkout()
    
    # Mike's shopping experience
    mike_tool = create_tool()
    mike.add_to_cart(mike_tool, "tools")
    mike_grocery = create_grocery()
    mike.add_to_cart(mike_grocery, "groceries")
    mike.checkout()

    # Harvey's shopping experience
    harvey_tool = create_tool()
    harvey.add_to_cart(harvey_tool, "tools")
    harvey_grocery = create_grocery()
    harvey.add_to_cart(harvey_grocery, "groceries")
    harvey.checkout()

    # Display store statistics
    store.display_statistics()
