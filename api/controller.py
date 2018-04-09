import subprocess

def get_current_state(user_id, engine):
	"""
	returns data and models visible to user
	"""
	data_query = """ SELECT * from data """
    data_files = pd.read_sql_query(text(data_query), engine)

    model_query = """ SELECT * from models """
    model_files = pd.read_sql_query(text(model_query), engine)

    return data.to_json(orient="records")


def launch_job(model_id, data_id, user_id,conn):
	"""
	core computation that launch_box() calls in the API
	"""
    job_id = model_id + data_id + user_id 

    add_job = """ INSERT INTO jobs VALUES (%s, %s,%s, %s, false)"""

    cur = conn.cursor()
    cur.execute(add_job, (job_id,
                          model_id,
                          data_id,
                          logfile))

    #get model url from model_id
    model_path = "assets/models/model1.py"

    #get data url from data_id
    data_path = "assets/data/data1.csv"    

    subprocess.call("python3 {} {} {}".format(model_path,data_path, job_id), shell=True)

    update_job = """ UPDATE jobs SET completed = true WHERE id = %s"""
    cur.execute(update_job, (job_id))
    #get logfile and user_id from job and send along to API 