# Tutorial para configurar e iniciar el servidor de la base de datos relacional y vectorial en Linux y PostgreSQL 

El siguiente es un instructivo de cómo crear por primera vez la base de datos del proyecto ``llms_kgs``, e iniciar su servidor por consola, usando Linux y el software PostgreSQL. 

1. Instalar [pgsql](https://www.postgresql.org/) en la máquina local siguiendo el tutorial del sitio web. 

2. Instalar [pgvector](https://github.com/pgvector/pgvector) mediante las instrucciones de la documentación de GitHub.

3.  Crear el directorio ``/usr/local/pgsql/data`` donde se alojará el *cluster* de bases de datos relacionales y brindarle los permisos a un usuario ``postgres``:  
```bash
sudo su
adduser postgres
mkdir -p /usr/local/pgsql/data
chown postgres /usr/local/pgsql/data
``` 

4. Iniciar sesión con el usuario ``postgres``:  
```bash
  sudo su  ⏎
  su - postgres 
```

5. Iniciar el *cluster*: 
```bash
  /usr/local/pgsql/bin/initdb -D /usr/local/pgsql/data 
```

Este paso crea por defecto una base de datos ``postgres`` en la cual se puede crear el esquema de bases de datos del proyecto ``schema.sql``.      

Cada vez que se desee iniciar el servidor de la base de datos es necesario repetir el paso 2 y ejecutar:
```bash
  /usr/local/pgsql/bin/pg\_ctl -D /usr/local/pgsql/data -l logfile start 
```
