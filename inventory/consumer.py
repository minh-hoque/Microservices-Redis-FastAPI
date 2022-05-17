import time

from main import Product, redis

key = "order_completed"
group = "inventory-group"

try:
    redis.xgroup_create(key, group)
except:
    print("Group already exists!")


while True:
    try:
        results = redis.xreadgroup(group, key, {key: ">"}, None)

        if results:
            for result in results:
                obj_dict = result[1][0][1]
                try:
                    product = Product.get(obj_dict["product_id"])
                    print(product)
                    product.quantity = product.quantity - int(obj_dict["quantity"])  # type: ignore
                    product.save()
                except:
                    redis.xadd("refund_order", obj_dict, "*")

    except Exception as e:
        print(str(e))
    time.sleep(1)
