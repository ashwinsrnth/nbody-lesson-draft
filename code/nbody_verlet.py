# -*- coding: utf-8 -*-
"""
Created on Sat May 16 12:19:34 2015
@author: Ian Hawke, Ashwin Srinath
"""

import numpy

def dqdt(r, v, m):
    """
    Compute the derivatives of velocity and position.

    Parameters
    ----------

    r : list of float
        Positions (3 N)
    v : list of float
        Velocities (3 N)
    m : list of float
        Masses (N)

    Returns
    -------

    drdt : list of float
        Derivative of positions (3 N)
    dvdt : list of float
        Derivative of velocities (3 N)
    """

    N = len(m)
    drdt = numpy.zeros_like(r)
    dvdt = numpy.zeros_like(v)
    dr = numpy.zeros((3,))
    for i in range(N):
        for k in range(3):
            drdt[i][k] = v[i][k]
        for j in range(i):
            for k in range(3):
                dr[k] = r[i][k] - r[j][k]
            mag = (dr[0]**2 + dr[1]**2 + dr[2]**2)**(-1.5)
            for k in range(3):
                dvdt[i][k] -= mag * m[j] * dr[k]
                dvdt[j][k] += mag * m[i] * dr[k]
    return drdt, dvdt

def advance_verlet(bodies, dt, n):
    """
    Step forward using a velocity-Verlet integrator.
    """

    r = numpy.array(bodies[0])
    v = numpy.array(bodies[1])
    m = numpy.array(bodies[2])
    for step in range(n):
        drdt, dvdt = dqdt(r, v, m)
        r += dt * v + 0.5 * dt**2 * dvdt
        vstar = v + 0.5 * dt * dvdt
        drdt, dvdt = dqdt(r, vstar, m)
        v = vstar + 0.5 * dt * dvdt

    bodies[0] = list(r)
    bodies[1] = list(v)
    bodies[2] = list(m)
