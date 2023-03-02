from sqlalchemy import create_engine, text


db_username = "e7bgl9wjqwg5pbn4g5sm"
db_password = "pscale_pw_KZvcOOcnwh3dHQB8v2gNbrhnqjlNcqvKx4lp6arhzNb"
db_host = "ap-southeast.connect.psdb.cloud"
db_name = "clinic"
ssl_ca = "/etc/ssl/cert.pem"

db_connection_string = f"mysql+pymysql://{db_username}:{db_password}@{db_host}/"

engine = create_engine(db_connection_string, connect_args={
  "ssl": {"ssl_ca": ssl_ca}})
                      
with engine.connect() as conn:
  result = conn.execute(text("select * from patients"))
  print(result.all())