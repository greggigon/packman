packman
=======

[![Build Status](https://travis-ci.org/cloudify-cosmo/packman.svg?branch=develop)](https://travis-ci.org/cloudify-cosmo/packman)

[![Gitter chat](https://badges.gitter.im/cloudify-cosmo/packman.png)](https://gitter.im/cloudify-cosmo/packman)

packman creates packages.

You can write a dict containing your package's configuration and packman will retrieve the resources and create a package accordingly.

The project was initally invented to create Cloudify (http://getcloudify.org/) packages and is now progressing towards being a simple open-source solution to creating different types of packages.

### Documentation
[packman documentation](https://packman.readthedocs.org/en/latest/)

### Installation
see [packman requirements](http://packman.readthedocs.org/en/latest/installation.html#pre-requirements) before installing packman
```shell
 pip install packman
 # or, for dev:
 pip install https://github.com/cloudify-cosmo/cloudify-packager/archive/develop.tar.gz
```

### Usage Examples

```shell
 # `pkm get` retrieves component sources
 pkm get --components my_component --components_file /my_components_file.py
 # `pkm pack` packages sources, scripts and configs.
 pkm pack -c my_component,my_other_component
 # `pkm make` ... does both one after the other
 pkm make -x excluded_component
```

### Additional Information
- [packman's cli](http://packman.readthedocs.org/en/latest/pkm.html)
- [Quick Start](http://packman.readthedocs.org/en/latest/quick_start.html)
- [Components Configuration](http://packman.readthedocs.org/en/latest/component_config.html)
- [Alternative Implementations](http://packman.readthedocs.org/en/latest/alternative_methods.html)
- [Template Handling](http://packman.readthedocs.org/en/latest/template_handling.html)
- [packman API](http://packman.readthedocs.org/en/latest/api.html)

### Vagrant
A vagrantfile is provided to load machines:

- a packman host (which, by default, is prepared for packaging components)
- a tester host (which, by default, is a clean machine to test the package installation on)
- CentOS and other distribs are being added...

##### Automated Vagrant Testing Environment
In future versions, an automated process of retrieval, packaging and installation will be implemented to check the entire process.
