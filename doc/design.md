# Design

## Users etc.

### Authentication

* Only staff and teachers using LTI from A+ (check [Django LTI Login](https://github.com/Aalto-LeTech/django-lti-login))
* local users for debugging (there should be no need in production)

## Authorization

* Groups and permissions
* At least two levels for the groups. E.g. School and research group.
	* Depth should probably not be limited (aka. group can be member of a group)
* Groups have administrators that can edit members
* Use similar permission system as in A+ and django rest framework
	* Check `permissions.py` and `views.py` in [a-plus/authorization](https://github.com/Aalto-LeTech/a-plus/tree/master/authorization)

## Serice roles and purposes

### Course management

* Interface to see all registered courses under your control (check authorization)
* Can edit location where the course will be pulled (git).
* Can be automatically populated from local filesystem (check course update monitoring)
* Select where course updates are uploaded (staging vs. production environments)

### Course update monitoring

* Trigger hook path. Will be called from the version control system (or anywhere else)
* Will schedule a build task for the course (celery)
* Only one task should be scheduled at a time (if one is running, one will stay in the queue)
* Directory tree watcher. If there is change in the files in a tree it will trigger a build with chagned course directory as a source. Will be used for local development with containers.

### Course building

* Given course path it will build the course using containers.
* Build process should be modular.
	* In start we will check that if there is `build.sh`, then we will use current sphinx, pyyaml container to build it by running `./build.sh`
	* In the future, we will check if the repo contains course configuration with list of container and executable pairs (will be another class)
	* Dopcker interfaces should be modular (support for local containers and kubernetes)
	* Check docker [compile script](https://github.com/apluslms/course-templates/blob/rst/docker-compile.sh)
* Builders will get the course in one path and generate output to another
	* To support current environment we will start by copying read-only stuff to working directory
* validate that all serviced used in the course exist
	* if course uses service `my-unique-service`, then there needs to be service with that name in the system

### Course uploading

* Modular system for different backend services
	* e.g. mooc-grader plugin that knows what files are required from the course repo to configure mooc-grader
	* multiple instances of the same plugin (multiple different mooc graders)
* Modular system for uploaders
	* e.g. local path, scp, blockstorage etc.
	* For now local path is good as we can mount network volumes that will do the sharing of data
* Process needs to handle nontlinear workflow
	* example workflow for mooc-grader
		* collect files
		* use uploader to copy files
		* use web API to inform service about the new files
	* example workflow for API service
		* collect files
		* use web API to make changes to the service
	* example workflow for A+
		* collect files
		* upload static files to mooc-grader (heh. this will move some day in the future) (use uploader from above)
		* create aplus.json
		* provide link to aplus.json that can be configured to A+
		* cal webhook to trigger course update on A+ (not yet supported in A+)

### Environment management

* List of configured services (e.g. mooc-graders) in installed environment
* configuration stored in yaml file could be enough
* commandline interface to add services

## General notes about the design

* As many processes are done asyncronously locally or in kubernetes cloud, we need to deliver as good as possible status information to the web UI
* Look into using websockets to push updates to the client instead of polling
	* Of course, service can start by polling or manually updating a view
* We need to design a good method to automatically give web API access to grader (and other services) for godfather (in other words, share secrets between two machines)

## Notes about Django stuff

* Use Django version 2 (notice that some features used in our other services might differ)
* Use conf utilities from [raphendyr-django-essentials](https://github.com/raphendyr/raphendyr-django-essentials). For examples: [a-plus](https://github.com/Aalto-LeTech/a-plus/blob/master/aplus/settings.py#L351), [mooc-grader](https://github.com/Aalto-LeTech/mooc-grader/blob/master/grader/settings.py#L231) and [mooc-jutut](https://github.com/Aalto-LeTech/mooc-jutut/blob/master/jutut/settings.py#L370)
* For django-lti-login and celery configuration, check examples from [mooc-jutut](https://github.com/Aalto-LeTech/mooc-jutut/)
* use jinja2 for the templates. Check configuration from [mooc-jutut](https://github.com/Aalto-LeTech/mooc-jutut/blob/master/jutut/settings.py#L117) (template backend with name `Jinja2-templates-jinja`)
	* note: there is also need for django tamplates as django admin uses those
	* relevant django apps: `django_jinja`, `django_jinja.contrib._humanize` (if needed), `bootstrapform_jinja` (handy for rendering bootstrap styled forms)
* If we need web API for gotfather (e.g. for javascript): [Django Rest Framework](http://www.django-rest-framework.org/)
	* And swagger of course ([this](https://github.com/marcgibbons/django-rest-swagger) might be useful)
