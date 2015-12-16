
## Getting Started with Custom Web Applications Using Girder

### Get girder
```sh
git clone git://github.com/girder/girder.git
cd girder
```

### Copy the local Girder config to girder
(see [girder.local.cfg](girder.local.cfg))
```sh
cp "$PATH_TO_LOCAL_GIRDER_CONFIG" ./girder/conf/girder.local.cfg
```

### Perform the invocation ritual
```sh
pip install -r requirements.txt -r requirements-dev.txt

# if you have plugins you want to use...
for plugin in $PLUGINS_YOU_PLAN_TO_ENABLE ; do
    for requirement in requirements.txt requirements-dev.txt ; do
        if [ -f "plugins/$plugin/$requirement" ] ; then
            pip install -r "plugins/$plugin/$requirement"
        fi
    done
done

npm install
./node_modules/grunt-cli/bin/grunt
```

### Girder, engaged!
```sh
python -m girder
```
(Don't switch to your browser quite yet).

Girder uses a mongodb server for its persistence layer.  Also: for our purposes,
we'll need to run girder behind a proxy web server (in this case, nginx).  For
the demo, these services will run on docker containers, but can also run on
their own just fine.

### Run mongo container
```sh
docker run -p 27017:27017 mongo
```

### Run nginx container
(see provided [nginx.conf](nginx.conf))
```sh
docker run --net=host -p 8080:8080                          \
    -v "$ABSOLUTE_PATH_TO_NGINX_CONF:/etc/nginx/nginx.conf" \
    -v "$ABSOLUTE_PATH_TO_YOUR_WEB_ROOT:/web" nginx
```

[http://localhost:8080](http://localhost:8080) should give you the index page
for your chosen web root, and
[http://localhost:8080/girder](http://localhost:8080/girder) should give you the
main girder web application.  If so, congrats!  Go nuts and hack up the frontend
of your dreams!  Check out the [External Web Clients](http://girder.readthedocs.org/en/latest/external-web-clients.html#using-girder-javascript-utilities-and-views)
page in the Girder documentation for tips on getting started.

