DO
$$
BEGIN
   IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'ckan_user') THEN
      CREATE ROLE ckan_user WITH LOGIN PASSWORD 'CKANUserPassword!321';
   END IF;
END
$$;

DO
$$
BEGIN
   IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'readonly_user') THEN
      CREATE ROLE readonly_user WITH LOGIN PASSWORD 'ReadOnlyPassword!321';
   END IF;
END
$$;

DO
$$
BEGIN
   IF NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'ckan_db') THEN
      CREATE DATABASE ckan_db WITH OWNER ckan_user;
   END IF;
END
$$;

DO
$$
BEGIN
   IF NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'datastore_db') THEN
      CREATE DATABASE datastore_db WITH OWNER readonly_user;
   END IF;
END
$$;

-- Grant privileges after ensuring the databases exist
GRANT ALL PRIVILEGES ON DATABASE ckan_db TO ckan_user;
GRANT ALL PRIVILEGES ON DATABASE datastore_db TO readonly_user;


