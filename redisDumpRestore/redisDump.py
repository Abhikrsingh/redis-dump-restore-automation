import redis
import json
import datetime
import os

def dump_keys(host, port, password, db, pattern, limit, output_file):
    start_time = datetime.datetime.now()
    print(f"Dump for database {db} started at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")

    client = redis.StrictRedis(host=host, port=port, db=db, password=password)

    cursor = 0
    count = 0
    dump_data = {}

    print(f"Fetching keys matching pattern: {pattern or '*'}")

    while True:
        cursor, keys = client.scan(cursor, match=pattern, count=1000)

        for key in keys:
            try:
                key_str = key.decode('utf-8')
                ttl = client.ttl(key)
                value = client.dump(key)
                if value is not None:
                    dump_data[key_str] = {
                        'value': value.hex(),
                        'ttl': ttl
                    }
                    count += 1
            except Exception as e:
                print(f"Error processing key {key}: {e}")

            if limit is not None and count >= limit:
                print(f"Reached limit of {limit} keys.")
                cursor = 0
                break

        if cursor == 0 or (limit is not None and count >= limit):
            break

    print(f"Total keys processed: {count}")

    end_time = datetime.datetime.now()
    print(f"Dump for database {db} instance {host} completed at: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total duration: {end_time - start_time}")

    with open(output_file, 'w') as f:
        json.dump(dump_data, f, indent=2)

    print(f"Dump saved to {output_file}")
    print("--------------------------------------")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_file = os.path.join(script_dir, "cre_json", "details.json")

    # Load configuration
    with open(config_file, 'r') as file:
        config = json.load(file)

    current_date = datetime.datetime.now().strftime("%Y-%m-%d")

    for instance in config["instances"]:
        host = instance["host"]
        port = instance["port"]
        password = instance["password"]
        dbs = instance["databases"]
        file_prefix = instance["file_prefix"]
        dump_path = instance["dump_path"]
        pattern = instance.get("pattern", None)  # Default to None (all keys)
        limit = instance.get("limit", None)  # Default to None (no limit)

        # Append the current date to the dump path
        dated_dump_path = os.path.join(dump_path, current_date)
        if not os.path.exists(dated_dump_path):
            os.makedirs(dated_dump_path)

        for db in dbs:
            output_file = os.path.join(dated_dump_path, f"{file_prefix}{db}.json")
            dump_keys(host, port, password, db, pattern, limit, output_file)