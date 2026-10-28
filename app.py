"""Gestor de tareas CLI con Factory Method, Observer y Strategy."""
from dataclasses import dataclass
from datetime import date
from abc import ABC, abstractmethod
import argparse
import json
from pathlib import Path

@dataclass
class Tarea:
    id: int
    titulo: str
    prioridad: str = 'media'
    completada: bool = False

class FabricaTareas:
    """Factory Method: centraliza validacion y creacion de tareas."""
    @staticmethod
    def crear(identificador: int, titulo: str, prioridad: str = 'media') -> Tarea:
        if not titulo.strip():
            raise ValueError('El titulo no puede estar vacio')
        if prioridad not in ('alta', 'media', 'baja'):
            raise ValueError('Prioridad invalida')
        return Tarea(identificador, titulo.strip(), prioridad)

class Observador(ABC):
    @abstractmethod
    def actualizar(self, evento: str, tarea: Tarea): ...

class NotificadorConsola(Observador):
    def actualizar(self, evento: str, tarea: Tarea):
        print(f'[Evento] {evento}: #{tarea.id} {tarea.titulo}')

class EstrategiaOrden(ABC):
    @abstractmethod
    def ordenar(self, tareas: list[Tarea]) -> list[Tarea]: ...

class OrdenPorId(EstrategiaOrden):
    def ordenar(self, tareas):
        return sorted(tareas, key=lambda t: t.id)

class OrdenPorPrioridad(EstrategiaOrden):
    def ordenar(self, tareas):
        peso = {'alta': 0, 'media': 1, 'baja': 2}
        return sorted(tareas, key=lambda t: (peso[t.prioridad], t.id))

class GestorTareas:
    def __init__(self, ruta: Path):
        self.ruta = ruta
        self.observadores: list[Observador] = []
        self.tareas = [Tarea(**t) for t in json.loads(ruta.read_text(encoding='utf-8'))] if ruta.exists() else []

    def suscribir(self, observador: Observador):
        self.observadores.append(observador)

    def _emitir(self, evento, tarea):
        for observador in self.observadores:
            observador.actualizar(evento, tarea)

    def _guardar(self):
        from dataclasses import asdict
        self.ruta.parent.mkdir(parents=True, exist_ok=True)
        self.ruta.write_text(json.dumps([asdict(t) for t in self.tareas], ensure_ascii=False, indent=2), encoding='utf-8')

    def agregar(self, titulo, prioridad='media'):
        siguiente = max((t.id for t in self.tareas), default=0) + 1
        tarea = FabricaTareas.crear(siguiente, titulo, prioridad)
        self.tareas.append(tarea)
        self._guardar()
        self._emitir('creada', tarea)
        return tarea

    def completar(self, identificador):
        tarea = next((t for t in self.tareas if t.id == identificador), None)
        if tarea is None:
            raise ValueError('Tarea no encontrada')
        tarea.completada = True
        self._guardar()
        self._emitir('completada', tarea)

    def listar(self, estrategia: EstrategiaOrden):
        return estrategia.ordenar(self.tareas)

def main():
    parser = argparse.ArgumentParser(description='Gestor de tareas')
    parser.add_argument('--archivo', default='tareas.json')
    sub = parser.add_subparsers(dest='accion', required=True)
    alta = sub.add_parser('agregar')
    alta.add_argument('titulo')
    alta.add_argument('--prioridad', choices=['alta', 'media', 'baja'], default='media')
    completar = sub.add_parser('completar')
    completar.add_argument('id', type=int)
    listar = sub.add_parser('listar')
    listar.add_argument('--orden', choices=['id', 'prioridad'], default='id')
    args = parser.parse_args()
    gestor = GestorTareas(Path(args.archivo))
    gestor.suscribir(NotificadorConsola())
    try:
        if args.accion == 'agregar':
            gestor.agregar(args.titulo, args.prioridad)
        elif args.accion == 'completar':
            gestor.completar(args.id)
        else:
            estrategia = OrdenPorPrioridad() if args.orden == 'prioridad' else OrdenPorId()
            for t in gestor.listar(estrategia):
                print(f'{t.id:>3} | {t.prioridad:<5} | {"OK" if t.completada else "Pendiente":<9} | {t.titulo}')
    except ValueError as exc:
        parser.error(str(exc))

if __name__ == '__main__':
    main()
