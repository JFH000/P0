# Robot Language Parser

Este proyecto es un analizador sintáctico (parser) para un lenguaje de programación diseñado para controlar un robot en un mundo bidimensional. El objetivo del parser es verificar la sintaxis de los programas escritos en este lenguaje, asegurando que sean válidos antes de su ejecución.

## 📜 Descripción

El robot puede moverse en una matriz \( n \times n \) y ejecutar acciones como mover, girar, colocar y recoger objetos (fichas y globos). El parser se encarga de validar la estructura del programa, asegurando que:

- Las variables estén correctamente declaradas antes de su uso.
- Los procedimientos sean definidos antes de ser llamados.
- Los comandos y estructuras de control tengan la sintaxis adecuada.
- Se permita la recursión en los procedimientos.

## 🚀 Características

- Implementación en **Python**.
- Validación de **variables y procedimientos**.
- Soporte para **estructuras de control** como condicionales y bucles.
- Reconocimiento de comandos básicos como **movimiento y manipulación de objetos**.

## 📌 Comandos Básicos Soportados

El parser reconoce los siguientes comandos del lenguaje del robot:

- `M` → Moverse hacia adelante.
- `R` → Girar a la derecha.
- `C` → Dejar una ficha.
- `B` → Colocar un globo.
- `c` → Recoger una ficha.
- `b` → Recoger un globo.
- `P` → Reventar un globo.
- `J(n)` → Saltar `n` pasos (sin aterrizar en obstáculos).
- `G(x,y)` → Ir a la posición `(x,y)`.
- 
