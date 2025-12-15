import pygame
import numpy as np

def make_surface(size, color):
    """
    size, color로 surface를 생성합니다.
    """
    surf = pygame.Surface(size)
    surf.fill(color)
    return surf

def load_obj(filename: str):
    """
    .obj 파일 읽어 정점과 모서리 리스트를 반환합니다.
    정점: np.array, shape (N,3)
    모서리: tuple 리스트(int, int)
    """
    vertices = []
    faces = []

    with open(filename, 'r') as f:
        for line in f:
            if line.startswith('v '):
                parts = line.strip().split()[1:]
                vertices.append([float(p) for p in parts])
            elif line.startswith('f '):
                parts = line.strip().split()[1:]
                # f 1 2 3  → 0-indexed
                face = [int(p.split('/')[0])-1 for p in parts]
                faces.append(face)

    vertices = np.array(vertices, dtype=float)

    edges = set()
    for face in faces:
        for i in range(len(face)):
            a = face[i]
            b = face[(i+1)%len(face)]
            edges.add(tuple(sorted((a,b))))
    edges = list(edges)

    return vertices, edges
