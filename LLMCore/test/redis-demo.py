import redis
import time

def test_redis_connection():
    try:
        # 连接到 Redis 服务器，假设 Redis 运行在地址 http://redis:6379
        r = redis.Redis(host='redis', port=6379)

        # 1. 测试连接
        if r.ping():
            print("连接到 Redis 成功！")
        else:
            print("连接到 Redis 失败！")
            return

        # 2. 字符串操作：SET 和 GET
        r.set('test_key', 'Hello Redis!')
        value = r.get('test_key')
        print(f"字符串测试：设置 test_key = 'Hello Redis!'，读取结果：{value.decode('utf-8')}")

        # 3. 哈希操作：HSET 和 HGET
        r.hset('test_hash', 'field1', 'value1')
        r.hset('test_hash', 'field2', 'value2')
        field1_value = r.hget('test_hash', 'field1').decode('utf-8')
        field2_value = r.hget('test_hash', 'field2').decode('utf-8')
        print(f"哈希测试：设置 field1 = {field1_value}，field2 = {field2_value}")

        # 4. 列表操作：LPUSH 和 LRANGE
        r.lpush('test_list', 'item1', 'item2', 'item3')
        list_items = r.lrange('test_list', 0, -1)
        print(f"列表测试：插入 item1, item2, item3，读取结果：{[item.decode('utf-8') for item in list_items]}")

        # 5. 集合操作：SADD 和 SMEMBERS
        r.sadd('test_set', 'member1', 'member2', 'member3')
        set_members = r.smembers('test_set')
        print(f"集合测试：插入 member1, member2, member3，读取结果：{[member.decode('utf-8') for member in set_members]}")

        # 6. 有序集合操作：ZADD 和 ZRANGE
        r.zadd('test_zset', {'member1': 1, 'member2': 2, 'member3': 3})
        zset_members = r.zrange('test_zset', 0, -1, withscores=True)
        print(f"有序集合测试：插入 member1 (1), member2 (2), member3 (3)，读取结果：{zset_members}")

        # 7. 发布/订阅机制：PUBLISH 和 SUBSCRIBE
        def message_handler(message):
            print(f"接收到的消息：{message['data'].decode('utf-8')}")

        # 启动订阅者（需要在后台监听）
        pubsub = r.pubsub()
        pubsub.subscribe('test_channel')

        # 发布消息
        r.publish('test_channel', 'Hello, this is a test message!')

        # 订阅者处理消息
        time.sleep(1)  # 等待消息到达
        for message in pubsub.listen():
            if message['type'] == 'message':
                message_handler(message)
                break  # 处理完一次消息后退出

    except Exception as e:
        print(f"Redis 测试失败，错误信息: {e}")


if __name__ == '__main__':
    test_redis_connection()
