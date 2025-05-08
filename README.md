
1.**limpie dos veces 50mil:**
```bash
awk -F ' \\| ' '{
    rut = sprintf("%010s", $1);
    nombre = sprintf("%-50s", substr($2, 1, 50));
    edad = sprintf("%02d", $3);
    direccion = sprintf("%-100s", substr($4, 1, 100));
    print rut "|" nombre "|" edad "|" direccion;
}' millones50 > limpio.txt


```

2.**crear la bdd en un contenedor de docker, asi lo hice**
```bash
docker run --name tarea_bdd -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=tarea_bdd -p 5432:5432 -d postgres

```

**dps ese supuesto limpio lo copie en el contenedor donde esta la bdd**
```bash
docker cp ruta_del_limpio.txt nombre_contendor:/tmp/limpio.txt

```
**dps hay que ingresar al cotenedor y aplicar este comando para limpiarlos real**
```bash
sort -t'|' -k1,1 -u /tmp/limpio.txt > /tmp/limpio_sin_duplicados.txt

```
**dps ingresar a la bdd e insertar los datos limpios en las tablas personas1 y 2:**
```bash

COPY personas1(rut, nombre, edad, direccion)
FROM '/tmp/limpio.txt'
WITH (FORMAT csv, DELIMITER '|');

COPY personas2(rut, nombre, edad, direccion)
FROM '/tmp/limpio.txt'
WITH (FORMAT csv, DELIMITER '|');
```
**LISTO AMBAS DEBERIAN TENER 49750490 ALGO ASI**