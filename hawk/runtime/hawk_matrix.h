#ifndef HAWK_MATRIX_H
#define HAWK_MATRIX_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <math.h>

/*
 * Hawk Matrix Runtime
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
        fprintf(stderr, "Hawk Error: Failed to allocate memory for Matrix!\n");
        exit(1);
    }
    m->rows = rows;
    m->cols = cols;
    m->data = (double*)calloc((size_t)rows * cols, sizeof(double));
    if (!m->data) {
        fprintf(stderr, "Hawk Error: Failed to allocate memory for Matrix data!\n");
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
        fprintf(stderr, "Hawk Error: Matrix index [%d, %d] out of bounds for %dx%d!\n",
                r, c, m->rows, m->cols);
        exit(1);
    }
    return m->data[r * m->cols + c];
}

/* Установка элемента (r, c) */
static inline void matrix_set(Matrix *m, int r, int c, double val) {
    if (r < 0 || r >= m->rows || c < 0 || c >= m->cols) {
        fprintf(stderr, "Hawk Error: Matrix index [%d, %d] out of bounds for %dx%d!\n",
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
        fprintf(stderr, "Hawk Error: Cannot multiply matrices of dimensions %dx%d and %dx%d!\n",
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
        fprintf(stderr, "Hawk Error: Matrix dimensions do not match for addition!\n");
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
        fprintf(stderr, "Hawk Error: Matrix dimensions do not match for subtraction!\n");
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
        fprintf(stderr, "Hawk Error: Determinant is only defined for square matrices!\n");
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

/* ==============================================================================
 * Math, String & Value Helpers
 * ============================================================================== */

/* Python-style modulo for doubles */
static inline double hawk_mod(double a, double b) {
    if (b == 0.0) {
        fprintf(stderr, "Hawk Error: Division or modulo by zero!\n");
        exit(1);
    }
    double m = fmod(a, b);
    if ((m < 0.0 && b > 0.0) || (m > 0.0 && b < 0.0)) {
        m += b;
    }
    return m;
}

static inline bool hawk_str_eq(const char *s1, const char *s2) {
    if (s1 == s2) return true;
    if (!s1 || !s2) return false;
    return strcmp(s1, s2) == 0;
}

static inline const char* hawk_str_concat(const char *s1, const char *s2) {
    if (!s1) s1 = "";
    if (!s2) s2 = "";
    size_t len = strlen(s1) + strlen(s2) + 1;
    char *res = (char*)malloc(len);
    if (!res) return "";
    snprintf(res, len, "%s%s", s1, s2);
    return res;
}

static inline const char* hawk_num_to_str(double n) {
    char *buf = (char*)malloc(64);
    if (!buf) return "";
    if (n == (long)n) {
        snprintf(buf, 64, "%ld", (long)n);
    } else {
        snprintf(buf, 64, "%g", n);
    }
    return buf;
}

static inline const char* hawk_bool_to_str(bool b) {
    return b ? "true" : "false";
}

/* ==============================================================================
 * HawkVal Dynamic Value System
 * ============================================================================== */

typedef enum {
    HAWK_VAL_NUM,
    HAWK_VAL_STR,
    HAWK_VAL_BOOL,
    HAWK_VAL_MATRIX
} HawkValType;

typedef struct {
    HawkValType type;
    double num;
    char *str;
    bool boolean;
    Matrix *mat;
} HawkVal;

static inline HawkVal hawk_val_num(double n) {
    HawkVal v;
    memset(&v, 0, sizeof(HawkVal));
    v.type = HAWK_VAL_NUM;
    v.num = n;
    return v;
}

static inline HawkVal hawk_val_str(const char *s) {
    HawkVal v;
    memset(&v, 0, sizeof(HawkVal));
    v.type = HAWK_VAL_STR;
    v.str = s ? strdup(s) : strdup("");
    return v;
}

static inline HawkVal hawk_val_bool(bool b) {
    HawkVal v;
    memset(&v, 0, sizeof(HawkVal));
    v.type = HAWK_VAL_BOOL;
    v.boolean = b;
    return v;
}

static inline HawkVal hawk_val_matrix(Matrix *m) {
    HawkVal v;
    memset(&v, 0, sizeof(HawkVal));
    v.type = HAWK_VAL_MATRIX;
    v.mat = m;
    return v;
}

static inline double hawk_val_to_num(HawkVal v) {
    if (v.type == HAWK_VAL_NUM) return v.num;
    if (v.type == HAWK_VAL_STR && v.str) {
        char *endptr = NULL;
        return strtod(v.str, &endptr);
    }
    if (v.type == HAWK_VAL_BOOL) return v.boolean ? 1.0 : 0.0;
    return 0.0;
}

static inline const char* hawk_val_to_str(HawkVal v) {
    if (v.type == HAWK_VAL_STR && v.str) return v.str;
    if (v.type == HAWK_VAL_NUM) {
        return hawk_num_to_str(v.num);
    }
    if (v.type == HAWK_VAL_BOOL) return v.boolean ? "true" : "false";
    return "";
}

static inline bool hawk_val_to_bool(HawkVal v) {
    if (v.type == HAWK_VAL_BOOL) return v.boolean;
    if (v.type == HAWK_VAL_NUM) return v.num != 0.0;
    if (v.type == HAWK_VAL_STR && v.str) return strlen(v.str) > 0;
    return false;
}

static inline HawkVal hawk_val_add(HawkVal a, HawkVal b) {
    if (a.type == HAWK_VAL_MATRIX && b.type == HAWK_VAL_MATRIX) {
        return hawk_val_matrix(matrix_add(a.mat, b.mat));
    }
    if (a.type == HAWK_VAL_STR || b.type == HAWK_VAL_STR) {
        const char *sa = hawk_val_to_str(a);
        const char *sb = hawk_val_to_str(b);
        return hawk_val_str(hawk_str_concat(sa, sb));
    }
    return hawk_val_num(hawk_val_to_num(a) + hawk_val_to_num(b));
}

static inline HawkVal hawk_val_sub(HawkVal a, HawkVal b) {
    if (a.type == HAWK_VAL_MATRIX && b.type == HAWK_VAL_MATRIX) {
        return hawk_val_matrix(matrix_sub(a.mat, b.mat));
    }
    return hawk_val_num(hawk_val_to_num(a) - hawk_val_to_num(b));
}

static inline HawkVal hawk_val_mult(HawkVal a, HawkVal b) {
    if (a.type == HAWK_VAL_MATRIX && b.type == HAWK_VAL_MATRIX) {
        return hawk_val_matrix(matrix_mult(a.mat, b.mat));
    }
    if (a.type == HAWK_VAL_MATRIX) {
        return hawk_val_matrix(matrix_scale(a.mat, hawk_val_to_num(b)));
    }
    if (b.type == HAWK_VAL_MATRIX) {
        return hawk_val_matrix(matrix_scale(b.mat, hawk_val_to_num(a)));
    }
    return hawk_val_num(hawk_val_to_num(a) * hawk_val_to_num(b));
}

static inline HawkVal hawk_val_div(HawkVal a, HawkVal b) {
    double denom = hawk_val_to_num(b);
    if (denom == 0.0) {
        fprintf(stderr, "Hawk Error: Division by zero!\n");
        exit(1);
    }
    return hawk_val_num(hawk_val_to_num(a) / denom);
}

static inline HawkVal hawk_val_mod(HawkVal a, HawkVal b) {
    double denom = hawk_val_to_num(b);
    return hawk_val_num(hawk_mod(hawk_val_to_num(a), denom));
}

static inline HawkVal hawk_val_pow(HawkVal a, HawkVal b) {
    return hawk_val_num(pow(hawk_val_to_num(a), hawk_val_to_num(b)));
}

static inline bool hawk_val_eq(HawkVal a, HawkVal b) {
    if (a.type == HAWK_VAL_STR && b.type == HAWK_VAL_STR) {
        return (a.str && b.str) ? (strcmp(a.str, b.str) == 0) : (a.str == b.str);
    }
    if (a.type == HAWK_VAL_BOOL && b.type == HAWK_VAL_BOOL) {
        return a.boolean == b.boolean;
    }
    return hawk_val_to_num(a) == hawk_val_to_num(b);
}

static inline bool hawk_val_eq_str(HawkVal a, const char *s) {
    if (a.type == HAWK_VAL_STR && a.str && s) {
        return strcmp(a.str, s) == 0;
    }
    return false;
}

static inline bool hawk_val_eq_num(HawkVal a, double n) {
    return hawk_val_to_num(a) == n;
}

static inline bool hawk_val_eq_bool(HawkVal a, bool b) {
    return hawk_val_to_bool(a) == b;
}

static inline void hawk_val_print(HawkVal v) {
    if (v.type == HAWK_VAL_NUM) {
        if (v.num == (long)v.num) {
            printf("%ld ", (long)v.num);
        } else {
            printf("%g ", v.num);
        }
    } else if (v.type == HAWK_VAL_STR) {
        printf("%s ", v.str ? v.str : "");
    } else if (v.type == HAWK_VAL_BOOL) {
        printf("%s ", v.boolean ? "true" : "false");
    } else if (v.type == HAWK_VAL_MATRIX) {
        printf("\n");
        matrix_print(v.mat);
    }
}

/* Ввод данных пользователем с авто-определением числа/строки (как в интерпретаторе Hawk) */
static inline HawkVal hawk_input(const char *prompt) {
    if (prompt && strlen(prompt) > 0) {
        printf("%s", prompt);
        fflush(stdout);
    }
    char buffer[4096];
    if (fgets(buffer, sizeof(buffer), stdin)) {
        size_t len = strlen(buffer);
        while (len > 0 && (buffer[len - 1] == '\n' || buffer[len - 1] == '\r')) {
            buffer[--len] = '\0';
        }
        // Проверяем, является ли ввод числом
        char *start = buffer;
        while (*start == ' ' || *start == '\t') start++;
        if (*start != '\0') {
            char *endptr = NULL;
            double d = strtod(start, &endptr);
            if (endptr != start) {
                while (*endptr == ' ' || *endptr == '\t') endptr++;
                if (*endptr == '\0') {
                    return hawk_val_num(d);
                }
            }
        }
        return hawk_val_str(buffer);
    }
    return hawk_val_str("");
}

/* Ввод строки пользователем (консольный prompt) */
static inline char* hawk_input_str(const char *prompt) {
    if (prompt && strlen(prompt) > 0) {
        printf("%s", prompt);
        fflush(stdout);
    }
    char buffer[4096];
    if (fgets(buffer, sizeof(buffer), stdin)) {
        size_t len = strlen(buffer);
        while (len > 0 && (buffer[len - 1] == '\n' || buffer[len - 1] == '\r')) {
            buffer[--len] = '\0';
        }
        return strdup(buffer);
    }
    return strdup("");
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

/* ============================================================
 * Cross-Platform OS, System & Audio Functions
 * ============================================================ */

/* Выполнить системную команду, вернуть код возврата */
static inline double hawk_system(const char *cmd) {
    if (!cmd) return 0.0;
    return (double)system(cmd);
}

/* Определить текущую ОС */
static inline const char* hawk_os_name(void) {
#if defined(_WIN32) || defined(_WIN64)
    return "windows";
#elif defined(__APPLE__)
    return "macos";
#else
    return "linux";
#endif
}

/* Звуковой сигнал (beep) */
static inline void hawk_beep(void) {
#if defined(_WIN32) || defined(_WIN64)
    /* Windows: системный сигнал через MessageBeep (без winmm) */
    printf("\a");
    fflush(stdout);
#else
    printf("\a");
    fflush(stdout);
#endif
}

/* Воспроизвести аудиофайл (в фоне, не блокируя выполнение) */
static inline void hawk_play_sound(const char *path) {
    if (!path || strlen(path) == 0) return;

    char cmd[4096];

#if defined(__APPLE__)
    /* macOS: afplay в фоне */
    snprintf(cmd, sizeof(cmd), "afplay \"%s\" &", path);
    system(cmd);
#elif defined(_WIN32) || defined(_WIN64)
    /* Windows: PowerShell SoundPlayer без блокировки */
    snprintf(cmd, sizeof(cmd),
        "powershell -NoProfile -Command \""
        "(New-Object Media.SoundPlayer '%s').PlaySync()\" &",
        path);
    system(cmd);
#else
    /* Linux: paplay -> aplay -> play (sox) */
    snprintf(cmd, sizeof(cmd),
        "(paplay \"%s\" 2>/dev/null || aplay \"%s\" 2>/dev/null || play \"%s\" 2>/dev/null) &",
        path, path, path);
    system(cmd);
#endif
}

#endif /* HAWK_MATRIX_H */

