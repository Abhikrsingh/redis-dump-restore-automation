import redis
import json
import datetime
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
config_file = os.path.join(script_dir, "cre_json", "restore.json")

with open(config_file, 'r') as f:
    config_data = json.load(f)

def restore_database(instance, db, input_file):
    start_time = datetime.datetime.now()
    print(f"Restoration for database {db} on instance {instance['host']} started at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")

    client = redis.StrictRedis(
        host=instance['host'],
        port=instance['port'],
        db=db,
        password=instance['password']
    )

    try:
        with open(input_file, 'r') as f:
            dump_data = json.load(f)

        print(f"Restoring keys from {input_file} to database {db}...")

        restored_count = 0
        for key, data in dump_data.items():
            try:
                binary_value = bytes.fromhex(data['value']) 
                ttl = data['ttl']
                if ttl == -1:
                    ttl = 0  
                
                client.restore(key, ttl * 1000, binary_value, replace=True)
                restored_count += 1
                print(f"Restored key: {key} with TTL: {ttl}")
            except Exception as e:
                print(f"Error restoring key {key}: {e}")

        print(f"Total keys restored for database {db}: {restored_count}")

    except FileNotFoundError:
        print(f"File {input_file} not found. Skipping database {db}.")

    end_time = datetime.datetime.now()
    print(f"Restoration for database {db} completed at: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total duration for database {db}: {end_time - start_time}")
    print("---------------------------------------------------")

def restore_for_all_instances():
    for instance in config_data['instances']:
        for db in instance['databases']:
            input_file = os.path.join(instance['dump_path'], f"{instance['file_prefix']}{db}.json")
            restore_database(instance, db, input_file)

if __name__ == "__main__":
    restore_for_all_instances()
