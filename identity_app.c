/* 🦅 Сгенерировано компилятором Hawk v0.1 */
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <math.h>
#include "/Users/mark/Documents/PythonPROGRAMM/HAWK/hawk/runtime/hawk_matrix.h"

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif
#define pi M_PI
#define e 2.71828182845904523536

/* --- Прототипы пользовательских функций --- */
double f(double x);

/* --- Реализации пользовательских функций --- */
double f(double x) {
    return ((2.0 * x) + 1.0);
    return 0.0;
}

/* --- Точка входа программы --- */
int main(int argc, char **argv) {
    double r = 5.0;
    double S = (pi * pow(r, 2.0));
    printf("%s ", "Area:");
    printf("%g ", (double)(S));
    printf("\n");
    Matrix *m = matrix_from_array(2, 2, (double[]){1.0, 2.0, 3.0, 4.0});
    Matrix *mt = matrix_transpose(m);
    printf("%s ", "m' =");
    printf("\n");
    printf("\n"); matrix_print(mt);
    printf("\n");
    printf("%s ", "det =");
    printf("%g ", (double)(matrix_det(m)));
    printf("\n");
    if (((1.0 < r) && (r < 10.0))) {
        printf("%s ", "r in range");
        printf("\n");
    }
    printf("%s ", "f(3) =");
    printf("%g ", (double)(f(3.0)));
    printf("\n");
    return 0;
}