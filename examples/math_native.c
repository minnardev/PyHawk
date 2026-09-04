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
    printf("%s ", "=== 🦅 Математика Hawk на лету ===");
    printf("\n");
    double r = 5.0;
    double S = (pi * pow(r, 2.0));
    printf("%s ", "Радиус:");
    printf("%g ", (double)(r));
    printf("\n");
    printf("%s ", "Площадь круга S = pi r^2:");
    printf("%g ", (double)(S));
    printf("\n");
    double val = f(10.0);
    printf("%s ", "f(x) = 2x + 1 при x=10:");
    printf("%g ", (double)(val));
    printf("\n");
    if ((r == 5.0)) {
        printf("%s ", "Условие (r = 5) сработало: r равно пяти!");
        printf("\n");
    }
    if (((1.0 < r) && (r < 10.0))) {
        printf("%s ", "r находится строго между 1 и 10!");
        printf("\n");
    }
    double count = 3.0;
    printf("%s ", "Обратный отсчёт:");
    printf("\n");
    while ((count > 0.0)) {
        printf("%g ", (double)(count));
        printf("\n");
        count = (count - 1.0);
    }
    printf("%s ", "Полетели! 🦅");
    printf("\n");
    return 0;
}