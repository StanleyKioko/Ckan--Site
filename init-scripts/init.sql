CREATE ROLE ckan_user WITH LOGIN PASSWORD 'CKANUserPassword!321';
CREATE DATABASE ckan_db WITH OWNER ckan_user;
GRANT ALL PRIVILEGES ON DATABASE ckan_db TO ckan_user;

CREATE ROLE readonly_user WITH LOGIN PASSWORD 'ReadOnlyPassword!321';
CREATE DATABASE datastore_db WITH OWNER readonly_user;
GRANT ALL PRIVILEGES ON DATABASE datastore_db TO readonly_user;
