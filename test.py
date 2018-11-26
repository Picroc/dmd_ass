from utils import __data_provider as provider

tmp = provider.get_customers()

for customer in tmp:
    print(tmp.pop())

tmp = provider.get_locations()
for adr in tmp:
    print(tmp.pop())
