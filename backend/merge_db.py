import sqlite3
import os

def get_table_names(cursor):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    return [table[0] for table in cursor.fetchall()]

def merge_user_data():
    # 連接到數據庫
    conn_local = sqlite3.connect('db.sqlite3.local')
    conn_current = sqlite3.connect('db.sqlite3')
    
    try:
        # 獲取本地數據庫中的用戶數據
        cursor_local = conn_local.cursor()
        cursor_current = conn_current.cursor()
        
        # 獲取實際的表名
        local_tables = get_table_names(cursor_local)
        current_tables = get_table_names(cursor_current)
        
        print("Available tables in local database:", local_tables)
        print("Available tables in current database:", current_tables)
        
        # 合併用戶相關的表
        user_tables = [
            'users_user',
            'users_usereducation',
            'users_workexperience',  # 修改了表名
            'users_userproject',
            'users_userskill'
        ]
        
        for table in user_tables:
            if table not in local_tables or table not in current_tables:
                print(f"Skipping table {table} as it doesn't exist in both databases")
                continue
                
            print(f"Merging table: {table}")
            
            # 獲取本地數據
            cursor_local.execute(f"SELECT * FROM {table}")
            local_data = cursor_local.fetchall()
            
            # 獲取列名
            cursor_local.execute(f"PRAGMA table_info({table});")
            columns = cursor_local.fetchall()
            column_count = len(columns)
            
            # 插入或更新數據
            placeholders = ','.join(['?' for _ in range(column_count)])
            for row in local_data:
                try:
                    cursor_current.execute(f"INSERT OR REPLACE INTO {table} VALUES ({placeholders})", row)
                except Exception as e:
                    print(f"Error inserting row in {table}: {e}")
                    continue
        
        # 提交更改
        conn_current.commit()
        print("User data merge completed successfully!")
        
    except Exception as e:
        print(f"Error during merge: {e}")
        
    finally:
        conn_local.close()
        conn_current.close()

if __name__ == '__main__':
    merge_user_data() 