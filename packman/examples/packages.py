# flake8: NOQA
from user_definitions import *

PACKAGES = {
    "logstash": {
        "name": "logstash",
        "version": "1.3.2",
        "source_urls": [
            "https://download.elasticsearch.org/logstash/logstash/logstash-1.3.2-flatjar.jar",
        ],
        "depends": [
            'openjdk-7-jdk'
        ],
        "package_path": "{0}/logstash/".format(PACKAGES_PATH),
        "sources_path": "{0}/logstash".format(SOURCES_PATH),
        "src_package_type": "dir",
        "dst_package_type": "deb",
        "bootstrap_script": "{0}/logstash-bootstrap.sh".format(SCRIPTS_PATH),
        "bootstrap_template": "logstash-bootstrap.template",
        "config_templates": {
            "__template_file_init": {
                "template": "{0}/logstash/init/logstash.conf.template".format(CONFIGS_PATH),
                "output_file": "logstash.conf",
                "config_dir": "config/init",
                "dst_dir": "/etc/init",
            },
            "__params_init": {
                "jar": "logstash.jar",
                "log_file": "/var/log/logstash.out",
                "conf_path": "/etc/logstash.conf",
                "run_dir": "/opt/logstash",
                "user": "root",
            },
            "__template_file_conf": {
                "template": "{0}/logstash/conf/logstash.conf.template".format(CONFIGS_PATH),
                "output_file": "logstash.conf",
                "config_dir": "config/conf",
                "dst_dir": "/etc",
            },
            "__params_conf": {
                "events_queue": "cloudify-events",
                "logs_queue": "cloudify-logs",
                "test_tcp_port": "9999",
                "events_index": "cloudify_events",
            }
        }
    },
    "elasticsearch": {
        "name": "elasticsearch",
        "version": "1.0.1",
        "source_urls": [
            "https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-1.0.1.tar.gz",
        ],
        "depends": [
            'openjdk-7-jdk'
        ],
        "package_path": "{0}/elasticsearch/".format(PACKAGES_PATH),
        "sources_path": "{0}/elasticsearch".format(SOURCES_PATH),
        "src_package_type": "dir",
        "dst_package_type": "deb",
        "bootstrap_script": "{0}/elasticsearch-bootstrap.sh".format(SCRIPTS_PATH),
        "bootstrap_template": "elasticsearch-bootstrap.template",
        "config_templates": {
            "__template_file_init": {
                "template": "{0}/elasticsearch/init/elasticsearch.conf.template".format(CONFIGS_PATH),
                "output_file": "elasticsearch.conf",
                "config_dir": "config/init",
                "dst_dir": "/etc/init",
            },
            "__params_init": {
                "run_dir": "/opt/elasticsearch",
                "user": "root",
            },
            "__template_file_conf": {
                "template": "{0}/elasticsearch/init/elasticsearch.conf.template".format(CONFIGS_PATH),
                "output_file": "elasticsearch.conf",
                "config_dir": "config/conf",
                "dst_dir": "/etc/init",
            },
            "__params_conf": {
            }
        }
    },
    "kibana3": {
        "name": "kibana3",
        "version": "3.0.0milestone4",
        "source_urls": [
            "https://download.elasticsearch.org/kibana/kibana/kibana-3.0.0milestone4.tar.gz",
        ],
        "depends": [
            'openjdk-7-jdk',
            'logstash',
            'elasticsearch'
        ],
        "package_path": "{0}/kibana3/".format(PACKAGES_PATH),
        "sources_path": "{0}/kibana3".format(SOURCES_PATH),
        "src_package_type": "dir",
        "dst_package_type": "deb",
        "bootstrap_script": "{0}/kibana-bootstrap.sh".format(SCRIPTS_PATH),
        "bootstrap_template": "kibana-bootstrap.template",
    },
	 "trio": {
        "name": "trio",
     		"version": "1",
     	 	"package_path": "{0}/trio/".format(PACKAGES_PATH),
      	"sources_path": "{0}/trio".format(SOURCES_PATH),
      	"src_package_type": "dir",
      	"dst_package_type": "deb",
      	"reqs": [
            {
                "url": "https://github.com/nir0s/packman-example/archive/develop.tar.gz",
                "components": ['kibana3'],
            },
        ]
    },
}
