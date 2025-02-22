import redis
import pandas as pd


def get_objects_from_csv(filepath):
    df = pd.read_csv(filepath)

    time = df.iloc[:, 0].to_json(orient='split')
    ch_1 = df.iloc[:, 1].to_json(orient='split')
    ch_2 = df.iloc[:, 2].to_json(orient='split')
    ch_3 = df.iloc[:, 3].to_json(orient='split')
    ch_4 = df.iloc[:, 4].to_json(orient='split')

    return time, ch_1, ch_2, ch_3, ch_4


def set_redis_db_connection():
    # Connect to Redis
    #redis_host = "127.0.0.1"
    redis_host = "sbnd-db01.fnal.gov"
    redis_port = 6379  # Default Redis port
    redis_password = "B4730D6D9606E3EB37048EB017D4C69EFB56243CCC408E3BEC3BFDEEDF792876"

    print("=== Initializing ...")

    # Create a Redis client instance
    redis_client = redis.StrictRedis(
        host=redis_host,
        port=redis_port,
        password=redis_password,
        decode_responses=True  # Decode responses to UTF-8
    )

    print("=== Connecting ...")

    # Test the connection
    try:
        redis_client.ping()
        print("Connected to Redis!")
    except redis.ConnectionError as e:
        print(f"Error connecting to Redis: {e}")

    print("=== CLIENT KEYS:")
    # Get list of keys
    keys_list = redis_client.keys("*")  # "*" means all keys, you can use pattern matching here

    # Sort the keys alphabetically
    keys_list.sort()

    # Print the sorted list of keys
    print("Sorted list of keys:")
    for key in keys_list:
        print(key)

    return redis_client


def send_to_redis_db(redis_client, time, ch_1, ch_2, ch_3, ch_4):
    print("=== Add the binary data to redis ...")
    # Add the binary data to Redis as a string
    redis_client.set('tpc_fc:osc:time', time)
    redis_client.set('tpc_fc:osc:ch_1', ch_1)
    redis_client.set('tpc_fc:osc:ch_2', ch_2)
    redis_client.set('tpc_fc:osc:ch_3', ch_3)
    redis_client.set('tpc_fc:osc:ch_4', ch_4)


def get_from_redis_db(redis_client):
    time = redis_client.get('tpc_fc:osc:time')
    ch_1 = redis_client.get('tpc_fc:osc:ch_1')
    ch_2 = redis_client.get('tpc_fc:osc:ch_2')
    ch_3 = redis_client.get('tpc_fc:osc:ch_3')
    ch_4 = redis_client.get('tpc_fc:osc:ch_4')

    print("Time\n", time)
    print("Channel 1\n", ch_1)
    print("Channel 2\n", ch_2)
    print("Channel 3\n", ch_3)
    print("Channel 4\n", ch_4)

    return time, ch_1, ch_2, ch_3, ch_4


if __name__ == "__main__":
    filepath = "FC_mini_osc/triggered_data/oscilloscope_data_1718742368-7585113_ALL.csv"

    time, ch1, ch2, ch3, ch4 = get_objects_from_csv(filepath)
    redis_client = set_redis_db_connection()
    #send_to_redis_db(redis_client, ch1, ch2, ch3, ch4)
    get_from_redis_db(redis_client)
