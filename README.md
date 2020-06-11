# Server code for imputation.io

## Running locally 

To use gunicorn and serve on port :5000

```
bin/run_local.sh
```

To run using flask debug dev server

```
python -m app
```

## Testing

Use 

```
tox
```

There are pytest submodule in

```
app.test
```

## Deployment to Google Apps Engine

Use scipt

```
bin/gcloud_deploy.sh
```

This will

Steps:
1. Run test suite with tox
2. If tests ok:
    + Delete all but the last 5 version numbers
    + Deploy the app to google apps engine


