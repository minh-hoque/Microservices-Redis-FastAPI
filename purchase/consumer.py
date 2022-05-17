import time

from main import Order, redis

key = "refund_order"
group = "payment-group"

try:
    redis.xgroup_create(key, group)
except:
    print("Group already exists!")


while True:
    try:
        results = redis.xreadgroup(group, key, {key: ">"}, None)
        print(results)
        if results:
            for result in results:
                obj_dict = result[1][0][1]
                order = Order.get(obj_dict["pk"])
                print("HERE: ", order)
                order.status = "refunded"
                order.save()

    except Exception as e:
        print(str(e))
    time.sleep(1)
