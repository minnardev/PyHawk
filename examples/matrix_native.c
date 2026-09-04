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

/* --- Точка входа программы --- */
int main(int argc, char **argv) {
    printf("%s ", "=== 🦅 Демонстрация матриц в Hawk ===");
    printf("\n");
    Matrix *A = matrix_from_array(2, 2, (double[]){1.0, 2.0, 3.0, 4.0});
    printf("%s ", "Матрица A:");
    printf("\n");
    printf("\n"); matrix_print(A);
    printf("\n");
    Matrix *B = matrix_from_array(2, 2, (double[]){2.0, 0.0, 1.0, 2.0});
    printf("%s ", "Матрица B:");
    printf("\n");
    printf("\n"); matrix_print(B);
    printf("\n");
    Matrix *C = matrix_mult(A, B);
    printf("%s ", "Матричное произведение A * B:");
    printf("\n");
    printf("\n"); matrix_print(C);
    printf("\n");
    Matrix *At = matrix_transpose(A);
    printf("%s ", "Транспонированная A':");
    printf("\n");
    printf("\n"); matrix_print(At);
    printf("\n");
    printf("%s ", "Определитель det(A):");
    printf("%g ", (double)(matrix_det(A)));
    printf("\n");
    Matrix *scaled = matrix_scale(A, 10.0);
    printf("%s ", "A * 10:");
    printf("\n");
    printf("\n"); matrix_print(scaled);
    printf("\n");
    return 0;
}