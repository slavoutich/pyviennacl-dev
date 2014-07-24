#!/usr/bin/env python

import logging, math, os, random
import numpy as np
import pyviennacl as p

logger = logging.getLogger('pyviennacl')
default_context = p.backend.Context()


def diff(a, b):
    ret = 0

    # Convert NumPy types to ViennaCL types (they're much more convenient!)
    if isinstance(a, np.ndarray):
        if a.ndim == 1:
            a = p.Vector(a, dtype = a.dtype)
        elif a.ndim == 2:
            if isinstance(b, p.MagicMethods):
                a = p.Matrix(a, dtype = a.dtype, layout = b.layout)
            else:
                a = p.Matrix(a, dtype = a.dtype)
        else:
            raise TypeError("Something went wrong")

    if isinstance(b, np.ndarray):
        if b.ndim == 1:
            b = p.Vector(b)
        elif b.ndim == 2:
            if isinstance(a, p.MagicMethods):
                b = p.Matrix(b, dtype = b.dtype, layout = a.layout)
            else:
                b = p.Matrix(b, dtype = b.dtype)
        else:
            raise TypeError("Something went wrong")

    # The MagicMethods class guarantees that we have some useful facilities
    #   (and both Node and Leaf are derived from MagicMethods)
    if isinstance(a, p.MagicMethods) and isinstance(b, p.MagicMethods):
        if a.result_container_type is p.Matrix and b.result_container_type is p.Matrix and a.layout != b.layout:
            # We want to make sure that a and b have the same layout
            # So construct a temporary matrix, and assign b to it
            temp = p.Matrix(b.shape, dtype = b.dtype, layout = a.layout)
            p.Assign(temp, b.result).execute()
            b = temp
        d = p.ElementFabs(a - b)
        cpu_d = d.as_ndarray()
        if len(d.shape) == 1:
            # vector
            for i in range(d.shape[0]):
                act = math.fabs(cpu_d[i])
                if act > ret:
                    ret = act
        elif len(d.shape) == 2:
            # matrix
            for i in range(d.shape[0]):
                for j in range(d.shape[1]): 
                    act = math.fabs(cpu_d[i, j])
                    if act > ret:
                        ret = act
        else:
            raise TypeError("Something went wrong..")
        return ret
    else:
        # We don't have either ndarrays or ViennaCL types so assume plain scalar
        if isinstance(a, p.MagicMethods):
            if issubclass(a.result_container_type, p.ScalarBase):
                a = a.value
        if isinstance(b, p.MagicMethods):
            if issubclass(b.result_container_type, p.ScalarBase):
                b = b.value
        return np.fabs(a - b) / max(np.fabs(a), np.fabs(b))


def get_host_scalar(dtype):
    return p.HostScalar(random.random(), dtype=dtype)


def get_device_scalar(dtype):
    return p.Scalar(random.random(), dtype=dtype)


def get_vector(size, dtype, context=default_context):
    numpy_A = np.random.rand(size)
    numpy_A = np.asarray(numpy_A, dtype=dtype)
    vcl_A = p.Vector(numpy_A, context=context)
    return numpy_A, vcl_A


def get_vector_range(size, dtype, context=default_context):
    numpy_A, vcl_A = get_vector(size, dtype, context)

    big_A = np.ones((size*4,), dtype=dtype)

    vcl_big_range_A = p.Vector(big_A, context=context)
    vcl_big_range_A[size:2*size] = vcl_A
    vcl_range_A = vcl_big_range_A[size:2*size]

    return numpy_A, vcl_range_A


def get_vector_slice(size, dtype, context=default_context):
    numpy_A, vcl_A = get_vector(size, dtype, context)

    big_A = np.ones((size*4,), dtype=dtype)

    vcl_big_slice_A = p.Vector(big_A, context=context)
    vcl_big_slice_A[size:-size:2] = vcl_A
    vcl_slice_A = vcl_big_slice_A[size:-size:2]

    return numpy_A, vcl_slice_A


def get_numpy_upper_matrix(size1, size2, order, dtype):
    numpy_A = np.random.rand(size1, size2)
    numpy_A = np.asarray(numpy_A, dtype=dtype, order=order)
    for i in range(size1):
        for j in range(size2):
            if j < i:
                numpy_A[i, j] = 0
    return numpy_A


def get_numpy_unit_upper_matrix(size1, size2, order, dtype):
    numpy_A = get_numpy_upper_matrix(size1, size2, order=order, dtype=dtype)
    for i in range(size1):
        for j in range(size2):
            if i == j:
                numpy_A[i, j] = 1.0
    return numpy_A


def get_numpy_lower_matrix(size1, size2, order, dtype):
    return get_numpy_upper_matrix(size2, size1, order, dtype).T


def get_numpy_unit_lower_matrix(size1, size2, order, dtype):
    return get_numpy_unit_upper_matrix(size2, size1, order, dtype).T


numpy_matrix_forms = {
    'upper': get_numpy_upper_matrix,
    'lower': get_numpy_lower_matrix,
    'unit_upper': get_numpy_unit_upper_matrix,
    'unit_lower': get_numpy_unit_lower_matrix
}


def get_matrix(size1, size2, layout, dtype,
               form=None, context=default_context):
    if form is None:
        numpy_A = np.random.rand(size1,size2)
        numpy_A = np.asarray(numpy_A, order=layout, dtype=dtype)
    else:
        numpy_A = numpy_matrix_forms[form](size1, size2, layout, dtype)

    vcl_A = p.Matrix(numpy_A, layout=layout, context=context)
    return numpy_A, vcl_A


def get_matrix_range(size1, size2, layout, dtype,
                     form=None, context=default_context):
    numpy_A, vcl_A = get_matrix(size1, size2, layout, dtype, form, context)

    big_A = np.ones((size1 * 4, size2 * 4), order=layout, dtype=dtype)

    vcl_big_range_A = p.Matrix(big_A, layout=layout, context=context)
    vcl_big_range_A[size1:2*size1, size2:2*size2] = vcl_A
    vcl_range_A = vcl_big_range_A[size1:2*size1, size2:2*size2]

    return numpy_A, vcl_range_A


def get_matrix_slice(size1, size2, layout, dtype,
                     form=None, context=default_context):
    numpy_A, vcl_A = get_matrix(size1, size2, layout, dtype, form, context)

    big_A = np.ones((size1 * 4, size2 * 4), order=layout, dtype=dtype)

    vcl_big_slice_A = p.Matrix(big_A, layout=layout, context=context)
    vcl_big_slice_A[size1:-size1:2, size2::3] = vcl_A
    vcl_slice_A = vcl_big_slice_A[size1:-size1:2, size2::3]

    return numpy_A, vcl_slice_A
