#ifndef HAWK_MATRIX_H
#define HAWK_MATRIX_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

/*
 * 🦅 Hawk Matrix Runtime
 * Структура матрицы: плоский массив размером rows * cols
 * Индекс элемента (r, c) вычисляется как: r * cols + c
 */
typedef struct {
    int rows;
    int cols;
    double *data;
} Matrix;

/* Создание новой матрицы, заполненной нулями */
static inline Matrix* matrix_new(int rows, int cols) {
    Matrix *m = (Matrix*)malloc(sizeof(Matrix));
    if (!m) {
        fprintf(stderr, "Hawk Error: Не удалось выделить память под Matrix!\n");
        exit(1);
    }
    m->rows = rows;
    m->cols = cols;
    m->data = (double*)calloc((size_t)rows * cols, sizeof(double));
    if (!m->data) {
        fprintf(stderr, "Hawk Error: Не удалось выделить память под данные матрицы!\n");
        free(m);
        exit(1);
    }
    return m;
}

/* Создание матрицы из существующего массива значений */
static inline Matrix* matrix_from_array(int rows, int cols, double *raw_data) {
    Matrix *m = matrix_new(rows, cols);
    for (int i = 0; i < rows * cols; i++) {
        m->data[i] = raw_data[i];
    }
    return m;
}

/* Освобождение памяти */
static inline void matrix_free(Matrix *m) {
    if (m) {
        if (m->data) {
            free(m->data);
        }
        free(m);
    }
}

/* Получение элемента (r, c) */
static inline double matrix_get(Matrix *m, int r, int c) {
    if (r < 0 || r >= m->rows || c < 0 || c >= m->cols) {
        fprintf(stderr, "Hawk Error: Индекс матрицы [%d, %d] вне диапазона %dx%d!\n",
                r, c, m->rows, m->cols);
        exit(1);
    }
    return m->data[r * m->cols + c];
}

/* Установка элемента (r, c) */
static inline void matrix_set(Matrix *m, int r, int c, double val) {
    if (r < 0 || r >= m->rows || c < 0 || c >= m->cols) {
        fprintf(stderr, "Hawk Error: Индекс матрицы [%d, %d] вне диапазона %dx%d!\n",
                r, c, m->rows, m->cols);
        exit(1);
    }
    m->data[r * m->cols + c] = val;
}

/* Транспонирование матрицы: (r, c) -> (c, r) */
static inline Matrix* matrix_transpose(Matrix *m) {
    Matrix *t = matrix_new(m->cols, m->rows);
    for (int r = 0; r < m->rows; r++) {
        for (int c = 0; c < m->cols; c++) {
            t->data[c * t->cols + r] = m->data[r * m->cols + c];
        }
    }
    return t;
}

/* Матричное умножение: A (RxK) * B (KxC) -> Result (RxC) */
static inline Matrix* matrix_mult(Matrix *a, Matrix *b) {
    if (a->cols != b->rows) {
        fprintf(stderr, "Hawk Error: Нельзя умножить матрицы размеров %dx%d и %dx%d!\n",
                a->rows, a->cols, b->rows, b->cols);
        exit(1);
    }
    Matrix *res = matrix_new(a->rows, b->cols);
    for (int r = 0; r < a->rows; r++) {
        for (int c = 0; c < b->cols; c++) {
            double sum = 0.0;
            for (int k = 0; k < a->cols; k++) {
                sum += a->data[r * a->cols + k] * b->data[k * b->cols + c];
            }
            res->data[r * res->cols + c] = sum;
        }
    }
    return res;
}

/* Сложение матриц */
static inline Matrix* matrix_add(Matrix *a, Matrix *b) {
    if (a->rows != b->rows || a->cols != b->cols) {
        fprintf(stderr, "Hawk Error: Размеры матриц для сложения не совпадают!\n");
        exit(1);
    }
    Matrix *res = matrix_new(a->rows, a->cols);
    for (int i = 0; i < a->rows * a->cols; i++) {
        res->data[i] = a->data[i] + b->data[i];
    }
    return res;
}

/* Вычитание матриц */
static inline Matrix* matrix_sub(Matrix *a, Matrix *b) {
    if (a->rows != b->rows || a->cols != b->cols) {
        fprintf(stderr, "Hawk Error: Размеры матриц для вычитания не совпадают!\n");
        exit(1);
    }
    Matrix *res = matrix_new(a->rows, a->cols);
    for (int i = 0; i < a->rows * a->cols; i++) {
        res->data[i] = a->data[i] - b->data[i];
    }
    return res;
}

/* Умножение матрицы на скаляр */
static inline Matrix* matrix_scale(Matrix *m, double s) {
    Matrix *res = matrix_new(m->rows, m->cols);
    for (int i = 0; i < m->rows * m->cols; i++) {
        res->data[i] = m->data[i] * s;
    }
    return res;
}

/* Определитель квадратной матрицы (det) */
static inline double matrix_det(Matrix *m) {
    if (m->rows != m->cols) {
        fprintf(stderr, "Hawk Error: Определитель существует только для квадратных матриц!\n");
        exit(1);
    }
    int n = m->rows;
    if (n == 1) {
        return m->data[0];
    }
    if (n == 2) {
        return m->data[0] * m->data[3] - m->data[1] * m->data[2];
    }
    if (n == 3) {
        double a = m->data[0], b = m->data[1], c = m->data[2];
        double d = m->data[3], e = m->data[4], f = m->data[5];
        double g = m->data[6], h = m->data[7], i = m->data[8];
        return a*(e*i - f*h) - b*(d*i - f*g) + c*(d*h - e*g);
    }

    // Для n > 3: метод Гаусса с частичным выбором ведущего элемента
    double *temp = (double*)malloc(sizeof(double) * n * n);
    for (int i = 0; i < n * n; i++) temp[i] = m->data[i];

    double det = 1.0;
    for (int col = 0; col < n; col++) {
        int pivot = col;
        for (int row = col + 1; row < n; row++) {
            if (fabs(temp[row * n + col]) > fabs(temp[pivot * n + col])) {
                pivot = row;
            }
        }
        if (fabs(temp[pivot * n + col]) < 1e-12) {
            free(temp);
            return 0.0;
        }
        if (pivot != col) {
            for (int k = 0; k < n; k++) {
                double t = temp[col * n + k];
                temp[col * n + k] = temp[pivot * n + k];
                temp[pivot * n + k] = t;
            }
            det = -det;
        }
        det *= temp[col * n + col];
        for (int row = col + 1; row < n; row++) {
            double factor = temp[row * n + col] / temp[col * n + col];
            for (int k = col; k < n; k++) {
                temp[row * n + k] -= factor * temp[col * n + k];
            }
        }
    }
    free(temp);
    return det;
}

/* Красивая печать матрицы */
static inline void matrix_print(Matrix *m) {
    printf("[");
    for (int r = 0; r < m->rows; r++) {
        if (r > 0) printf(" ");
        for (int c = 0; c < m->cols; c++) {
            double val = m->data[r * m->cols + c];
            if (val == (long)val) {
                printf("%ld", (long)val);
            } else {
                printf("%.4g", val);
            }
            if (c + 1 < m->cols) printf(", ");
        }
        if (r + 1 < m->rows) {
            printf(" ;\n");
        }
    }
    printf("]\n");
}

/* Ввод строки пользователем (консольный prompt) */
static inline char* hawk_input_str(const char *prompt) {
    if (prompt && strlen(prompt) > 0) {
        printf("%s", prompt);
        fflush(stdout);
    }
    static char buffer[1024];
    if (fgets(buffer, sizeof(buffer), stdin)) {
        size_t len = strlen(buffer);
        if (len > 0 && (buffer[len - 1] == '\n' || buffer[len - 1] == '\r')) {
            buffer[len - 1] = '\0';
        }
    } else {
        buffer[0] = '\0';
    }
    return buffer;
}

/* Ввод числа пользователем */
static inline double hawk_input_num(const char *prompt) {
    if (prompt && strlen(prompt) > 0) {
        printf("%s", prompt);
        fflush(stdout);
    }
    double val = 0.0;
    if (scanf("%lf", &val) != 1) {
        val = 0.0;
    }
    return val;
}

#endif /* HAWK_MATRIX_H */

