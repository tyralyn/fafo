# https://xkcd.com/287/
#
# Given a fixed menu of items and prices and an amount of money in
# your wallet, get all possible combos of menu items totaling
# your budget exactly.

'''
MENU_LIST = list(zip(MENU_DICT.keys(), MENU_DICT.values())
MENU_LIST = [
	("Fruit" , 2.15),
	("Fries" , 2.75),
	("Salad" , 3.35),
	("Wings" , 3.55),
	("Mozzarella Sticks", 4.20),
	("Sampler Plate", 5.80)
]
ITEMS_AND_PRICES = list(zip(*MENU_LIST))
ITEMS = list(ITEMS_AND_PRICES[0])
PRICES = list(ITEMS_AND_PRICES[1])
'''

MENU_DICT = {
	"Fruit" : 2.15,
	"Fries" : 2.75,
	"Salad" : 3.35,
	"Wings" : 3.55,
	"Mozzarella Sticks": 4.20,
	"Sampler Plate": 5.80
}
# ITEMS = list(MENU_DICT.keys())
# PRICES = list(MENU_DICT.values())

def possible_orders(order, change, menu):
	# if no money leftover, yay we have made a perfect order, return it
	if change == 0:
		return order

	# if there's nothing in the menu, it means we've eliminated all possible orders
	if not menu:
		return None

	# if your remaining money can't buy anything, put your most recent item back
	# and try to buy something else
	cheapest = min(menu.items(), key=lambda k: k[1])
	if change < cheapest[1]:
		most_recent = order.pop()
		new_menu = menu.copy()
		new_menu.pop(most_recent)

		return possible_orders(order, change + MENU_DICT[most_recent], new_menu)

	# if your remaining money can buy something, buy it and try to buy something else
	affordable_menu = { k:v for k,v in menu.items() if v <= change}
	costliest = max(affordable_menu.items(), key=lambda k: k[1])
	return possible_orders(order + [costliest[0]], change - costliest[1], affordable_menu)


# print(possible_orders([], 4.55, MENU_DICT))