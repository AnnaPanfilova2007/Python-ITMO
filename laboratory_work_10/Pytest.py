import unittest
import math
from unittest.mock import patch, MagicMock
import concurrent.futures
import numba

# Импортируем функции из вашего модуля
from main import integrate, integrate_async, integrate_process, integrate_async_nogil


class TestIntegrateFunctions(unittest.TestCase):

    def setUp(self):
        """тестовые данные"""
        self.sin_func = math.sin
        self.linear_func = lambda x: x
        self.constant_func = lambda x: 2.0
        self.a = 0.0
        self.b = 1.0
        self.n_iter = 1000
        self.n_jobs = 3

    # Тесты для функции integrate

    def test_integrate_sin_positive_range(self):
        """Тест интегрирования sin на положительном диапазоне"""
        result = integrate(self.sin_func, 0, math.pi / 2, n_iter=5000)
        expected = 1.0
        self.assertAlmostEqual(result, expected, delta=0.01)

    def test_integrate_sin_negative_range(self):
        """Тест интегрирования sin на отрицательном диапазоне"""
        result = integrate(self.sin_func, -math.pi / 2, math.pi / 2, n_iter=5000)
        expected = 0.0  # ∫_{-π/2}^{π/2} sin(x) dx = 0
        self.assertAlmostEqual(result, expected, delta=0.001)

    def test_integrate_linear_function(self):
        """Тест интегрирования линейной функции"""
        result = integrate(self.linear_func, 0, 1, n_iter=5000)
        expected = 0.5  # ∫₀¹ x dx = 0.5
        self.assertAlmostEqual(result, expected, delta=0.001)

    def test_integrate_constant_function(self):
        """Тест интегрирования константной функции"""
        result = integrate(self.constant_func, 0, 5, n_iter=5000)
        expected = 10.0  # ∫₀⁵ 2 dx = 10
        self.assertAlmostEqual(result, expected, delta=0.001)

    def test_integrate_zero_range(self):
        """Тест интегрирования на нулевом диапазоне"""
        result = integrate(self.sin_func, 0, 0, n_iter=5000)
        self.assertEqual(result, 0.0)

    def test_integrate_negative_n_iter_raises_error(self):
        """Тест что n_iter <= 0 вызывает ошибку"""
        with self.assertRaises(ValueError):
            integrate(self.sin_func, 0, 1, n_iter=0)

    def test_integrate_single_iteration(self):
        """Тест с минимальным количеством итераций"""
        result = integrate(self.constant_func, 0, 1, n_iter=1)
        expected = 2.0  # f(0) * 1 = 2 * 1 = 2
        self.assertAlmostEqual(result, expected, delta=0.001)

    # Тесты для функции integrate_async

    def test_integrate_async_basic(self):
        """Базовый тест"""
        result = integrate_async(self.sin_func, 0, math.pi / 2,
                                 n_iter=5000, n_jobs=2)
        expected = 1.0
        self.assertAlmostEqual(result, expected, delta=0.01)

    def test_integrate_async_different_n_jobs(self):
        """Тест с разным количеством потоков"""
        for n_jobs in [1, 2, 4]:
            with self.subTest(n_jobs=n_jobs):
                result = integrate_async(self.linear_func, 0, 1,
                                         n_iter=5000, n_jobs=n_jobs)
                expected = 0.5
                self.assertAlmostEqual(result, expected, delta=0.001)

    def test_integrate_async_consistency(self):
        """Тест согласованности с последовательной версией"""
        async_result = integrate_async(self.sin_func, 0, math.pi / 2,
                                       n_iter=5000, n_jobs=3)
        sync_result = integrate(self.sin_func, 0, math.pi / 2, n_iter=5000)
        self.assertAlmostEqual(async_result, sync_result, delta=0.001)

    def test_integrate_async_mock_executor(self):
        """Тест с моком ThreadPoolExecutor"""
        with patch('concurrent.futures.ThreadPoolExecutor') as mock_executor:
            mock_future = MagicMock()
            mock_future.result.return_value = 0.5

            mock_executor_instance = MagicMock()
            mock_executor_instance.submit.return_value = mock_future
            mock_executor.return_value.__enter__.return_value = mock_executor_instance

            # Имитируем as_completed
            with patch('concurrent.futures.as_completed', return_value=[mock_future]):
                result = integrate_async(self.linear_func, 0, 1,
                                         n_iter=100, n_jobs=1)
                self.assertAlmostEqual(result, 0.5, delta=0.001)

    # Тесты для функции integrate_process

    def test_integrate_process_basic(self):
        """Базовый тест для многопроцессной версии"""
        result = integrate_process(self.sin_func, 0, math.pi / 2,
                                   n_iter=5000, n_jobs=2)
        expected = 1.0
        self.assertAlmostEqual(result, expected, delta=0.01)


    def test_integrate_process_reverse_bounds(self):
        """Тест с обратными границами интегрирования"""
        result = integrate_process(self.linear_func, 1, 0, n_iter=5000, n_jobs=2)
        expected = -0.5  # ∫₁⁰ x dx = -0.5
        self.assertAlmostEqual(result, expected, delta=0.001)

    # Тесты для функции integrate_async_nogil

    def test_integrate_async_nogil_basic(self):
        """Базовый тест для NOGIL версии"""
        # Мокаем декоратор numba.jit чтобы избежать компиляции во время тестов
        with patch('numba.jit') as mock_jit:
            mock_jit.return_value = integrate  # Возвращаем оригинальную функцию

            result = integrate_async_nogil(self.sin_func, 0, math.pi / 2,
                                           n_iter=5000, n_jobs=2)
            expected = 1.0
            self.assertAlmostEqual(result, expected, delta=0.01)

    def test_integrate_async_nogil_mock_integrate(self):
        """Тест с моком внутренней функции integrate"""
        mock_integrate = MagicMock()
        mock_integrate.return_value = 0.25

        with patch('main.integrate', mock_integrate):
            with patch('numba.jit') as mock_jit:
                mock_jit.return_value = mock_integrate

                result = integrate_async_nogil(self.linear_func, 0, 1,
                                               n_iter=100, n_jobs=2)
                mock_integrate.assert_called()

    def test_integrate_async_nogil_jit_decorator(self):
        """Тест что функция использует декоратор numba.jit"""
        # Проверяем что numba.jit вызывается с правильными аргументами
        with patch('numba.jit') as mock_jit:
            mock_jit.return_value = integrate

            # Вызываем функцию
            integrate_async_nogil(self.sin_func, 0, 1, n_iter=100)

            # Проверяем что jit был вызван с правильными параметрами
            mock_jit.assert_called_once()
            call_args = mock_jit.call_args

            # Проверяем что передан nogil=True
            self.assertIn('nogil', call_args[1])
            self.assertTrue(call_args[1]['nogil'])

    # Компаративные тесты

    def test_all_methods_consistency(self):
        """Тест согласованности между всеми методами"""
        for func in [self.linear_func, self.sin_func]:
            with self.subTest(func=func.__name__ if hasattr(func, '__name__') else 'lambda'):
                sync_result = integrate(func, 0, 1, n_iter=5000)

                async_result = integrate_async(func, 0, 1, n_iter=5000, n_jobs=2)
                self.assertAlmostEqual(async_result, sync_result, delta=0.001)

                process_result = integrate_process(func, 0, 1, n_iter=5000, n_jobs=2)
                self.assertAlmostEqual(process_result, sync_result, delta=0.001)

                # Тестируем NOGIL версию с моком
                with patch('numba.jit') as mock_jit:
                    mock_jit.return_value = integrate
                    nogil_result = integrate_async_nogil(func, 0, 1, n_iter=5000, n_jobs=2)
                    self.assertAlmostEqual(nogil_result, sync_result, delta=0.001)

    def test_performance_characteristics(self):
        """Тест что функции не падают при разных параметрах"""
        test_cases = [
            (self.sin_func, -math.pi, math.pi, 10000, 1),
            (self.linear_func, 0, 100, 100000, 4),
            (self.constant_func, -10, 10, 1000, 8),
        ]

        for func, a, b, n_iter, n_jobs in test_cases:
            with self.subTest(f"func={func}, a={a}, b={b}"):
                # Просто проверяем что функции выполняются без ошибок
                try:
                    result1 = integrate(func, a, b, n_iter=n_iter)
                    result2 = integrate_async(func, a, b, n_iter=n_iter, n_jobs=n_jobs)
                    result3 = integrate_process(func, a, b, n_iter=n_iter, n_jobs=n_jobs)

                    with patch('numba.jit') as mock_jit:
                        mock_jit.return_value = integrate
                        result4 = integrate_async_nogil(func, a, b, n_iter=n_iter, n_jobs=n_jobs)

                    # Все результаты должны быть числами
                    self.assertIsInstance(result1, (int, float))
                    self.assertIsInstance(result2, (int, float))
                    self.assertIsInstance(result3, (int, float))
                    self.assertIsInstance(result4, (int, float))

                except Exception as e:
                    self.fail(f"Функция упала с ошибкой: {e}")

    # Тесты граничных случаев

    def test_very_small_range(self):
        """Тест очень маленького диапазона"""
        result = integrate(self.sin_func, 0, 0.0001, n_iter=100)
        self.assertIsInstance(result, float)

    def test_very_large_range(self):
        """Тест очень большого диапазона"""
        result = integrate(self.sin_func, 0, 1000, n_iter=1000)
        self.assertIsInstance(result, float)

    def test_very_large_n_iter(self):
        """Тест с очень большим количеством итераций"""
        result = integrate(self.linear_func, 0, 1, n_iter=1000000)
        self.assertAlmostEqual(result, 0.5, delta=0.0001)

    def test_negative_values(self):
        """Тест с отрицательными значениями функции"""
        result = integrate(lambda x: -x, 0, 1, n_iter=5000)
        expected = -0.5
        self.assertAlmostEqual(result, expected, delta=0.001)


if __name__ == '__main__':
    unittest.main(verbosity=2)