# cython: boundscheck=False, wraparound=False, initializedcheck=False, cdivision=True
cimport cython

import numpy as np
cimport numpy as np
from scipy.sparse import csr_matrix

from sisl._indices cimport _index_sorted
from sisl._sparse import fold_csr_matrix_nc

__all__ = ['_phase_nc_csr_c64', '_phase_nc_csr_c128',
           '_phase_nc_array_c64', '_phase_nc_array_c128']

# The fused data-types forces the data input to be of "correct" values.
ctypedef fused numeric_complex:
    float
    double
    float complex
    double complex


def _phase_nc_csr_c64(np.ndarray[np.int32_t, ndim=1, mode='c'] PTR,
                      np.ndarray[np.int32_t, ndim=1, mode='c'] NCOL,
                      np.ndarray[np.int32_t, ndim=1, mode='c'] COL,
                      numeric_complex[:, ::1] D,
                      np.ndarray[np.complex64_t, ndim=1, mode='c'] PHASES, const int p_opt):

    # Convert to memory views
    cdef int[::1] ptr = PTR
    cdef int[::1] ncol = NCOL
    cdef int[::1] col = COL
    cdef float complex[::1] phases = PHASES
    cdef Py_ssize_t nr = ncol.shape[0]

    # Now create the folded sparse elements
    V_PTR, V_NCOL, V_COL = fold_csr_matrix_nc(PTR, NCOL, COL)
    cdef int[::1] v_ptr = V_PTR
    cdef int[::1] v_ncol = V_NCOL
    cdef int[::1] v_col = V_COL

    cdef np.ndarray[np.complex64_t, ndim=1, mode='c'] V = np.zeros([v_col.shape[0]], dtype=np.complex64)
    cdef float complex[::1] v = V
    cdef float complex ph, v12
    cdef Py_ssize_t r, rr, ind, s_idx
    cdef int c

    if p_opt == 0:
        for r in range(nr):
            rr = r * 2
            for ind in range(ptr[r], ptr[r] + ncol[r]):
                c = (col[ind] % nr) * 2
                ph = phases[ind]
                s_idx = _index_sorted(v_col[v_ptr[rr]:v_ptr[rr] + v_ncol[rr]], c)

                v[v_ptr[rr] + s_idx] = v[v_ptr[rr] + s_idx] + <float complex> (ph * D[ind, 0])
                v12 = <float complex> (D[ind, 2] + 1j * D[ind, 3])
                v[v_ptr[rr] + s_idx+1] = v[v_ptr[rr] + s_idx+1] + ph * v12
                v[v_ptr[rr+1] + s_idx] = v[v_ptr[rr+1] + s_idx] + ph * v12.conjugate()
                v[v_ptr[rr+1] + s_idx+1] = v[v_ptr[rr+1] + s_idx+1] + <float complex> (ph * D[ind, 1])

    else:
        for r in range(nr):
            rr = r * 2
            for ind in range(ptr[r], ptr[r] + ncol[r]):
                c = (col[ind] % nr) * 2
                ph = phases[col[ind] / nr]
                s_idx = _index_sorted(v_col[v_ptr[rr]:v_ptr[rr] + v_ncol[rr]], c)

                v[v_ptr[rr] + s_idx] = v[v_ptr[rr] + s_idx] + <float complex> (ph * D[ind, 0])
                v12 = <float complex> (D[ind, 2] + 1j * D[ind, 3])
                v[v_ptr[rr] + s_idx+1] = v[v_ptr[rr] + s_idx+1] + ph * v12
                v[v_ptr[rr+1] + s_idx] = v[v_ptr[rr+1] + s_idx] + ph * v12.conjugate()
                v[v_ptr[rr+1] + s_idx+1] = v[v_ptr[rr+1] + s_idx+1] + <float complex> (ph * D[ind, 1])

    return csr_matrix((V, V_COL, V_PTR), shape=(nr * 2, nr * 2))


def _phase_nc_csr_c128(np.ndarray[np.int32_t, ndim=1, mode='c'] PTR,
                       np.ndarray[np.int32_t, ndim=1, mode='c'] NCOL,
                       np.ndarray[np.int32_t, ndim=1, mode='c'] COL,
                       numeric_complex[:, ::1] D,
                       np.ndarray[np.complex128_t, ndim=1, mode='c'] PHASES, const int p_opt):

    # Convert to memory views
    cdef int[::1] ptr = PTR
    cdef int[::1] ncol = NCOL
    cdef int[::1] col = COL
    cdef double complex[::1] phases = PHASES
    cdef Py_ssize_t nr = ncol.shape[0]

    # Now create the folded sparse elements
    V_PTR, V_NCOL, V_COL = fold_csr_matrix_nc(PTR, NCOL, COL)
    cdef int[::1] v_ptr = V_PTR
    cdef int[::1] v_ncol = V_NCOL
    cdef int[::1] v_col = V_COL

    cdef np.ndarray[np.complex128_t, ndim=1, mode='c'] V = np.zeros([v_col.shape[0]], dtype=np.complex128)
    cdef double complex[::1] v = V
    cdef double complex ph, v12
    cdef Py_ssize_t r, rr, ind, s_idx
    cdef int c

    if p_opt == 0:
        for r in range(nr):
            rr = r * 2
            for ind in range(ptr[r], ptr[r] + ncol[r]):
                c = (col[ind] % nr) * 2
                ph = phases[ind]
                s_idx = _index_sorted(v_col[v_ptr[rr]:v_ptr[rr] + v_ncol[rr]], c)

                v[v_ptr[rr] + s_idx] = v[v_ptr[rr] + s_idx] + <double complex> (ph * D[ind, 0])
                v12 = <double complex> (D[ind, 2] + 1j * D[ind, 3])
                v[v_ptr[rr] + s_idx+1] = v[v_ptr[rr] + s_idx+1] + ph * v12
                v[v_ptr[rr+1] + s_idx] = v[v_ptr[rr+1] + s_idx] + ph * v12.conjugate()
                v[v_ptr[rr+1] + s_idx+1] = v[v_ptr[rr+1] + s_idx+1] + <double complex> (ph * D[ind, 1])

    else:
        for r in range(nr):
            rr = r * 2
            for ind in range(ptr[r], ptr[r] + ncol[r]):
                c = (col[ind] % nr) * 2
                ph = phases[col[ind] / nr]
                s_idx = _index_sorted(v_col[v_ptr[rr]:v_ptr[rr] + v_ncol[rr]], c)

                v[v_ptr[rr] + s_idx] = v[v_ptr[rr] + s_idx] + <double complex> (ph * D[ind, 0])
                v12 = <double complex> (D[ind, 2] + 1j * D[ind, 3])
                v[v_ptr[rr] + s_idx+1] = v[v_ptr[rr] + s_idx+1] + ph * v12
                v[v_ptr[rr+1] + s_idx] = v[v_ptr[rr+1] + s_idx] + ph * v12.conjugate()
                v[v_ptr[rr+1] + s_idx+1] = v[v_ptr[rr+1] + s_idx+1] + <double complex> (ph * D[ind, 1])

    return csr_matrix((V, V_COL, V_PTR), shape=(nr * 2, nr * 2))


def _phase_nc_array_c64(np.ndarray[np.int32_t, ndim=1, mode='c'] PTR,
                        np.ndarray[np.int32_t, ndim=1, mode='c'] NCOL,
                        np.ndarray[np.int32_t, ndim=1, mode='c'] COL,
                        numeric_complex[:, ::1] D,
                        np.ndarray[np.complex64_t, ndim=1, mode='c'] PHASES, const int p_opt):

    # Convert to memory views
    cdef int[::1] ptr = PTR
    cdef int[::1] ncol = NCOL
    cdef int[::1] col = COL
    cdef float complex[::1] phases = PHASES

    cdef Py_ssize_t nr = ncol.shape[0]
    cdef np.ndarray[np.complex64_t, ndim=2, mode='c'] V = np.zeros([nr * 2, nr * 2], dtype=np.complex64)
    cdef float complex[:, ::1] v = V
    cdef float complex ph, v12
    cdef Py_ssize_t r, rr, ind, c

    if p_opt == 0:
        for r in range(nr):
            rr = r * 2
            for ind in range(ptr[r], ptr[r] + ncol[r]):
                c = (col[ind] % nr) * 2
                ph = phases[ind]
                v[rr, c] = v[rr, c] + <float complex> (ph * D[ind, 0])
                v12 = <float complex> (D[ind, 2] + 1j * D[ind, 3])
                v[rr, c+1] = v[rr, c+1] + ph * v12
                v[rr+1, c] = v[rr+1, c] + ph * v12.conjugate()
                v[rr+1, c+1] = v[rr+1, c+1] + <float complex> (ph * D[ind, 1])

    else:
        for r in range(nr):
            rr = r * 2
            for ind in range(ptr[r], ptr[r] + ncol[r]):
                c = (col[ind] % nr) * 2
                ph = phases[col[ind] / nr]
                v[rr, c] = v[rr, c] + <float complex> (ph * D[ind, 0])
                v12 = <float complex> (D[ind, 2] + 1j * D[ind, 3])
                v[rr, c+1] = v[rr, c+1] + ph * v12
                v[rr+1, c] = v[rr+1, c] + ph * v12.conjugate()
                v[rr+1, c+1] = v[rr+1, c+1] + <float complex> (ph * D[ind, 1])

    return V


def _phase_nc_array_c128(np.ndarray[np.int32_t, ndim=1, mode='c'] PTR,
                         np.ndarray[np.int32_t, ndim=1, mode='c'] NCOL,
                         np.ndarray[np.int32_t, ndim=1, mode='c'] COL,
                         numeric_complex[:, ::1] D,
                         np.ndarray[np.complex128_t, ndim=1, mode='c'] PHASES, const int p_opt):

    # Convert to memory views
    cdef int[::1] ptr = PTR
    cdef int[::1] ncol = NCOL
    cdef int[::1] col = COL
    cdef double complex[::1] phases = PHASES
    cdef Py_ssize_t nr = ncol.shape[0]

    cdef np.ndarray[np.complex128_t, ndim=2, mode='c'] V = np.zeros([nr * 2, nr * 2], dtype=np.complex128)
    cdef double complex[:, ::1] v = V
    cdef double complex ph, v12
    cdef Py_ssize_t r, rr, ind, c

    if p_opt == 0:
        for r in range(nr):
            rr = r * 2
            for ind in range(ptr[r], ptr[r] + ncol[r]):
                c = (col[ind] % nr) * 2
                ph = phases[ind]
                v[rr, c] = v[rr, c] + <double complex> (ph * D[ind, 0])
                v12 = <double complex> (D[ind, 2] + 1j * D[ind, 3])
                v[rr, c+1] = v[rr, c+1] + ph * v12
                v[rr+1, c] = v[rr+1, c] + ph * v12.conjugate()
                v[rr+1, c+1] = v[rr+1, c+1] + <double complex> (ph * D[ind, 1])

    else:
        for r in range(nr):
            rr = r * 2
            for ind in range(ptr[r], ptr[r] + ncol[r]):
                c = (col[ind] % nr) * 2
                ph = phases[col[ind] / nr]
                v[rr, c] = v[rr, c] + <double complex> (ph * D[ind, 0])
                v12 = <double complex> (D[ind, 2] + 1j * D[ind, 3])
                v[rr, c+1] = v[rr, c+1] + ph * v12
                v[rr+1, c] = v[rr+1, c] + ph * v12.conjugate()
                v[rr+1, c+1] = v[rr+1, c+1] + <double complex> (ph * D[ind, 1])

    return V
