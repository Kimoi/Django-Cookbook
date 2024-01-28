from recipes.models import Product, Recipe


Product(name="Kiwi").save()
Product(name="Lychee").save()
Product(name="Peach").save()

Recipe(name="Fruit Salad").save()
Recipe(name="Fruit Pizza").save()
Recipe(name="Fruits With Fruits").save()

print("all done")
quit()
