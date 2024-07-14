# Setting up Database Proxy

1. Install the Cloud SQL Admin Proxy using the following
<https://medium.com/google-cloud/connecting-dbeaver-to-cloud-sql-3f672ece836b>
<https://cloud.google.com/sql/docs/mysql/connect-auth-proxy>

2. Save the ./cloud-sql-proxy executable to your working directory
- 

2. Run the CLOUD SQL Admin Proxy 

```sh
$ ./cloud-sql-proxy --port 3306 dear-ocean-dev:us-central1:dca-dev-sandbox
```

3. Use the test app to make sure the connection works.

```
$ python src/app.py test_db
```